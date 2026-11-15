from kgnav.llm.gemini import GeminiProvider


def test_schema_conversion_normalizes_types_and_drops_unsupported_keys():
    schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "limit": {"type": "integer", "default": 10},
            "name": {"type": ["string", "null"]},
        },
        "required": ["name"],
    }
    assert GeminiProvider._gemini_schema(schema) == {
        "type": "OBJECT",
        "properties": {
            "limit": {"type": "INTEGER"},
            "name": {"type": "STRING"},
        },
        "required": ["name"],
    }


def test_legacy_tool_history_translates_to_gemini_parts():
    provider = object.__new__(GeminiProvider)
    provider._tool_names = {}
    messages = [
        {"role": "user", "content": "Find the auth module."},
        {"role": "assistant", "content": [
            {"type": "text", "text": "I will search."},
            {"type": "tool_use", "id": "tool-1", "name": "find_nodes", "input": {"name": "auth"}},
        ]},
        {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": "tool-1", "content": "{\\\"nodes\\\": []}", "is_error": False}
        ]},
    ]
    converted = provider._convert_messages(messages)
    assert converted[0]["role"] == "user"
    assert converted[1]["role"] == "model"
    assert converted[1]["parts"][1]["functionCall"] == {"name": "find_nodes", "args": {"name": "auth"}}
    assert converted[2]["parts"][0]["functionResponse"]["name"] == "find_nodes"

import asyncio
import httpx


def test_gemini_response_parses_text_and_tool_calls():
    async def scenario():
        def handler(request):
            assert request.url.path.endswith("/gemini-test:generateContent")
            payload = __import__("json").loads(request.content)
            assert payload["systemInstruction"]["parts"][0]["text"] == "system rules"
            assert payload["tools"][0]["functionDeclarations"][0]["name"] == "lookup"
            return httpx.Response(200, json={"candidates": [{"content": {"parts": [
                {"text": "Searching now."},
                {"functionCall": {"name": "lookup", "args": {"term": "auth"}}, "thoughtSignature": "sig-1"},
            ]}}]})

        provider = GeminiProvider(api_key="test-key")
        await provider._client.aclose()
        provider._client = httpx.AsyncClient(transport=httpx.MockTransport(handler), headers={"x-goog-api-key": "test-key"})
        try:
            response = await provider.create(
                model="gemini-test", max_tokens=100, system="system rules",
                messages=[{"role": "user", "content": "find auth"}],
                tools=[{"name": "lookup", "description": "lookup", "input_schema": {"type": "object", "properties": {"term": {"type": "string"}}}}],
            )
            assert response.content[0].text == "Searching now."
            assert response.content[1].name == "lookup"
            assert response.content[1].thought_signature == "sig-1"
        finally:
            await provider.close()

    asyncio.run(scenario())


def test_tool_call_round_trip_preserves_gemini_thought_signature():
    provider = object.__new__(GeminiProvider)
    provider._tool_names = {"call-1": "lookup"}
    from kgnav.llm.base import ToolUseBlock
    messages = [
        {"role": "assistant", "content": [ToolUseBlock(id="call-1", name="lookup", input={"term": "auth"}, thought_signature="sig-1")]},
        {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "call-1", "content": "found", "is_error": False}]},
    ]
    converted = provider._convert_messages(messages)
    assert converted[0]["parts"][0]["thoughtSignature"] == "sig-1"
    assert converted[1]["parts"][0]["functionResponse"]["name"] == "lookup"


# ---------------------------------------------------------------- resilience tests (no network, no real httpx needed)
import json as _json

from kgnav.llm.gemini import QuotaExhaustedError


class FakeResp:
    def __init__(self, status, body=None, headers=None, text=None):
        self.status_code, self._body, self.headers = status, body, headers or {}
        self.text = text if text is not None else _json.dumps(body if body is not None else {})

    @property
    def is_error(self):
        return self.status_code >= 400

    def json(self):
        if self._body is None:
            raise ValueError("no json")
        return self._body


class FakeClient:
    def __init__(self, responses):
        self.responses, self.calls, self.payloads = list(responses), 0, []

    async def post(self, url, json=None):
        self.calls += 1
        self.payloads.append(json)
        return self.responses.pop(0)

    async def aclose(self):
        pass


def ok_body(parts, finish="STOP"):
    return FakeResp(200, {"candidates": [{"content": {"parts": parts}, "finishReason": finish}]})


def make(responses, **kw):
    # Keep retry tests independent of a developer .env pacing setting.
    kw.setdefault("min_interval_s", 0)
    p = GeminiProvider(api_key="k", **kw)
    p._client = FakeClient(responses)
    p.sleeps = []
    p._jitter = lambda d: d

    async def fake_sleep(s):
        p.sleeps.append(s)

    p._sleep = fake_sleep
    return p


def call(p, tools=None):
    return asyncio.run(p.create(model="m", max_tokens=10, system="s", messages=[{"role": "user", "content": "hi"}], tools=tools))


def test_429_retry_honours_server_retry_delay():
    err = FakeResp(429, {"error": {"message": "slow down", "details": [{"@type": "type.googleapis.com/google.rpc.RetryInfo", "retryDelay": "7s"}]}})
    p = make([err, ok_body([{"text": "done"}])])
    r = call(p)
    assert r.content[0].text == "done" and p._client.calls == 2 and p.sleeps == [8.0]


def test_daily_quota_fails_fast_without_retrying():
    err = FakeResp(429, {"error": {"message": "Quota exceeded ... GenerateRequestsPerDayPerProjectPerModel-FreeTier"}})
    p = make([err, ok_body([{"text": "never"}])])
    raised = False
    try:
        call(p)
    except QuotaExhaustedError:
        raised = True
    assert raised and p._client.calls == 1 and p.sleeps == []


def test_5xx_gives_up_after_max_retries_with_exponential_backoff():
    p = make([FakeResp(503, {"error": {"message": "overloaded"}})] * 3, max_retries=2)
    raised = False
    try:
        call(p)
    except RuntimeError as e:
        raised = "503" in str(e)
    assert raised and p._client.calls == 3 and p.sleeps == [2.0, 4.0]


def test_finish_reason_is_surfaced():
    p = make([ok_body([{"text": "partial"}], finish="MAX_TOKENS")])
    assert call(p).stop_reason == "MAX_TOKENS"


def test_malformed_function_call_is_retried_once():
    p = make([ok_body([], finish="MALFORMED_FUNCTION_CALL"), ok_body([{"functionCall": {"name": "x", "args": {}}}])])
    r = call(p)
    assert r.content[0].name == "x" and p._client.calls == 2


def test_thought_parts_are_not_returned_as_text():
    p = make([ok_body([{"text": "internal reasoning", "thought": True}, {"text": "answer"}])])
    assert [b.text for b in call(p).content] == ["answer"]


def test_no_arg_tool_omits_empty_parameters_and_optional_is_flattened():
    tools = [
        {"name": "get_schema", "description": "d", "input_schema": {"type": "object", "properties": {}}},
        {"name": "t", "description": "d", "input_schema": {"type": "object", "properties": {
            "p": {"anyOf": [{"type": "object"}, {"type": "null"}], "title": "P"}, "n": {"type": "integer", "default": 3}}}},
    ]
    p = make([ok_body([{"text": "x"}])])
    call(p, tools)
    decls = p._client.payloads[0]["tools"][0]["functionDeclarations"]
    assert "parameters" not in decls[0]
    props = decls[1]["parameters"]["properties"]
    assert props["p"]["type"] == "OBJECT" and "anyOf" not in props["p"] and props["n"] == {"type": "INTEGER"}


def test_pacing_waits_between_requests():
    p = make([ok_body([{"text": "a"}]), ok_body([{"text": "b"}])], min_interval_s=5.0)
    call(p)
    call(p)
    assert len(p.sleeps) == 1 and 0 < p.sleeps[0] <= 5.0


def test_persistent_503_raises_llm_unavailable_so_agent_can_fall_back():
    from kgnav.llm.base import LLMUnavailableError
    p = make([FakeResp(503, {"error": {"message": "high demand"}})] * 2, max_retries=1)
    raised = False
    try:
        call(p)
    except LLMUnavailableError:
        raised = True
    assert raised and p._client.calls == 2


def test_default_backoff_is_jittered_within_25_percent():
    p = make([FakeResp(503, {"error": {"message": "x"}}), ok_body([{"text": "ok"}])])
    del p._jitter  # use the real jitter
    p._jitter = GeminiProvider(api_key="k")._jitter
    call(p)
    assert 2.0 <= p.sleeps[0] <= 2.5
