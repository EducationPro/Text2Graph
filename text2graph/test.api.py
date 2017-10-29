import requests
import json

url = 'http://localhost:5000/api/v1.0/text/map/'
payload = {'text': 'Google is an American multinational technology company that specializes in Internet-related services and products. Google was founded in 1998 by Larry Page and Sergey Brin while they were PhD students at Stanford University in California.'}
headers = {'content-type': 'application/json'}

response = requests.get(url, data=payload, headers=headers)

print (response.text)
