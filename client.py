import requests

url = 'http://localhost:8081/'  # Updated port
data = {'message': 'Hello from the client!'}

response = requests.post(url, json=data)
print(f"Response from server: {response.text}")
