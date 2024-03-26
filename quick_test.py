import requests

# Define the URL
url = "http://ops.epo.org/3.2/rest-services/classification/cpc/search"

# Define the query parameters
params = {
    "q": "car,light"  # Use comma instead of space
}

# Define the headers (replace 'YOUR_TOKEN' with your actual token)
headers = {
    "Authorization": "Bearer AFHK6reZYbVUXqLXzeJyy5UuU0Q8"
}

# Make the GET request
response = requests.get(url, params=params, headers=headers)

# Print the response
print(response.text)

# # import xml.etree.ElementTree as ET
# # from lxml import etree
# # import pandas as pd
# # import xmltodict
# #
# #
# # import requests
# # code = "B60R"
# #
# # # Replace 'YOUR_API_KEY' with your actual API key
# # api_key = 'J0QNGcRz4kpWByNLMGD5YWsrHM2e'
# #
# # # Define the URL for the API endpoint
# # url = f"http://ops.epo.org/3.2/rest-services/classification/cpc/{code}"
# #
# # # Define the query parameters
# # params = {
# #     "depth": "1"
# # }
# #
# # # Set the headers with the Authorization token
# # headers = {
# #     "Authorization": f"Bearer {api_key}"
# # }
# #
# # # Make the GET request
# # response = requests.get(url, headers=headers, params=params)
# #
# # # Check if the request was successful
# # if response.status_code == 200:
# #     # Print the response content
# #     #print(response.content)
# #     xmlp = ET.XMLParser(encoding="utf-8")
# #     root = ET.fromstring(response.content,parser=xmlp)
# #     for elem in root.iter():
# #         if 'text' in elem.tag:
# #             print(elem.text)
# #
# # else:
# #     print("Error:", response.status_code)
# import requests
#
# bearer_token = 'VkJ6R2RSZUdYVmRaTzdiQ0drRFJTUTlURm1lMUdyOW46dlZaS2FWU2h6OGExdkQ0Yw=='
#
# def get_access_token(bearer_token):
#     base_address = "https://ops.epo.org/3.2/auth/accesstoken"
#
#     # Define headers
#     headers = {
#         "Authorization": f"Basic {bearer_token}",
#         "Accept": "application/x-www-form-urlencoded",
#         "User-Agent": "PostmanRuntime/7.30.0"
#     }
#
#     # Define form data
#     form_data = {
#         "grant_type": "client_credentials"
#     }
#
#     # Send POST request
#     response = requests.post(base_address, headers=headers, data=form_data)
#
#     # Print response headers
#     for header, value in response.headers.items():
#         print(f"{header} = {value}")
#
#     # Parse JSON response content
#     json_content = response.json()
#     return json_content
#
# # Replace 'your_bearer_token' with your actual bearer token
#
#
# # Get access token
# token = get_access_token(bearer_token)
#
# # Print access token
# print("Access token:", token)