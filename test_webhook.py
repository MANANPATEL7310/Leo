import requests


user_message = "Can you tell me about black holes in 3-4 lines"

request_message = {"message": user_message}

url = "http://localhost:5678/webhook-test/89680d33-ba8a-47d5-a69a-5e6897b3a56d"

response = requests.post(url, json=request_message)

print(response.status_code)

print(response.json()[0]["output"])