#!/usr/bin/env python3
import os
import requests
import json

# Read the API key from the file
with open('api.key', 'r') as file:
    api_key = file.read().replace('\n', '')

url = 'https://api.openai.com/v1/models'

headers = {
    'Authorization': 'Bearer ' + api_key,
    'Content-Type': 'application/json'
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    print("Available models from OpenAI:")
    for model in response.json()['data']:
        print(model['id'])

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
