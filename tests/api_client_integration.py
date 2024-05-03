# Integration Test #1
# This test is designed to see if the api created in this project was correctly sent and
# received. If yes, then our project can proceed.

import requests

# Define local URL endpoint
url = 'http://localhost:8000/'

# Make a GET request to the API endpoint
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Extract the JSON data from the response
    data = response.json()
    # Print the message from the response
    print(data['message'])
else:
    # Print an error message if the request was not successful
    print('Failed to retrieve data from the API')
