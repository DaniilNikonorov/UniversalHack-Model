import requests

# Define the URL of your Flask app
app_url = 'http://127.0.0.1:5001'  # Assuming your Flask app is running locally on port 5000

# Define the user ID for which you want recommendations
user_id = 50

# Create a JSON payload with the user ID
payload = {'user_id': user_id, 'device_id': 352398080550058, 'items_id': [104821, 107726, 100671]}

# Send a POST request to the /predict_user endpoint
response = requests.post(f'{app_url}/predict_user', json=payload)

# Check if the request was successful
if response.status_code == 200:
    recommendations = response.json()
    print(recommendations)
else:
    print(f'Error: {response.status_code} - {response.text}')
