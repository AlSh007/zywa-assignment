import requests

# Replace 'your_identifier' with the actual phone number or card ID you want to query
identifier = "0545576586"

# Make a GET request to the /get_card_status endpoint
response = requests.get(f'http://127.0.0.1:5000/get_card_status?identifier={identifier}')

# Print the response
print(response.json())
