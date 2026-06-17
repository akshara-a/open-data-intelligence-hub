import gzip
import json
import polars as pl
from pathlib import Path

records = []

for file in Path("data").glob("*.json.gz"):

    date = file.stem.split("-0")[0]

    with gzip.open(file, "rt", encoding="utf-8") as f:

        for line in f:

            obj = json.loads(line)

            if obj["type"] != "PullRequestEvent":
                continue

            try:
                language = (
                    obj["payload"]
                       ["pull_request"]
                       ["base"]
                       ["repo"]
                       ["language"]
                )

                if language is None:
                    continue

                records.append({
                    "date": date,
                    "language": language
                })

            except:
                pass

df = pl.DataFrame(records)

summary = (
    df.group_by(["date", "language"])
      .len()
      .sort(["date", "len"])
)

summary.write_csv("language_trends.csv")

print(summary.head())