import xml.etree.ElementTree as ET
from lxml import etree
import pandas as pd
import xmltodict


import requests
code = "B60R"

# Replace 'YOUR_API_KEY' with your actual API key
api_key = 'J0QNGcRz4kpWByNLMGD5YWsrHM2e'

# Define the URL for the API endpoint
url = f"http://ops.epo.org/3.2/rest-services/classification/cpc/{code}"

# Define the query parameters
params = {
    "depth": "1"
}

# Set the headers with the Authorization token
headers = {
    "Authorization": f"Bearer {api_key}"
}

# Make the GET request
response = requests.get(url, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Print the response content
    #print(response.content)
    xmlp = ET.XMLParser(encoding="utf-8")
    root = ET.fromstring(response.content,parser=xmlp)
    for elem in root.iter():
        if 'text' in elem.tag:
            print(elem.text)

else:
    print("Error:", response.status_code)
