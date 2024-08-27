
import requests
url = "http://20.244.56.144/test/auth"
data = {
    "companyName": "GITAM",
    "clientID": "b979b511-6d71-45cc-91c8-a587cdb5f115",
    "clientSecret": "FzmRzoWAIbGyuBwJ",
    "ownerName": "Kalidindi Sree Harsha Varma",
    "ownerEmail": "skalidindi@gitam.in",
    "rollNo": "HU21CSEN0300339"
}

response = requests.post(url, json=data)
print(response.json())
