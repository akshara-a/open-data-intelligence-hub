import requests

URL = "https://proglangpredictor.streamlit.app/"

try:
    response = requests.get(URL, timeout=30)

    print("Status Code:", response.status_code)

except Exception as e:
    print("Error:", e)