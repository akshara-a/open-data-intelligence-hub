import gzip
import json
import polars as pl

records = []

with gzip.open(
    "data/2025-01-01-0.json.gz",
    "rt",
    encoding="utf-8"
) as f:

    for line in f:
        obj = json.loads(line)

        if obj["type"] != "PullRequestEvent":
            continue

        try:
            records.append({
                "repo_name":
                    obj["repo"]["name"],

                "language":
                    obj["payload"]["pull_request"]
                       ["base"]["repo"]
                       ["language"],

                "created_at":
                    obj["created_at"]
            })

        except KeyError:
            continue

df = pl.DataFrame(records)

print(df.head())

print("\nLanguages:")
print(
    df.group_by("language")
      .len()
      .sort("len", descending=True)
      .head(20)
)