import requests

url = "https://data.gharchive.org/2025-01-01-0.json.gz"

response = requests.get(url)

with open("data/2025-01-01-0.json.gz", "wb") as f:
    f.write(response.content)

print("Downloaded successfully!")