.PHONY: setup up seed test demo eval
setup:
	python3 -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -e ".[dev]"
up:
	docker compose up -d
seed:
	. .venv/bin/activate && python scripts/seed_graph.py
test:
	. .venv/bin/activate && pytest -q
demo:
	. .venv/bin/activate && kgnav ask "If I deprecate the legacy-auth-module, which downstream API routes and frontend components will break?"
eval:
	. .venv/bin/activate && python eval/run_eval.py
