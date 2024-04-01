import requests

url = "https://graph.imdbapi.dev/v1"

response = requests.get(url)

print(response.json())