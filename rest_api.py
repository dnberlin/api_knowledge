import requests
import json
import urllib.parse

URL = "https://owner-api.teslamotors.com"
ACCESS_TOKEN = ""

def main():
    # Get OAuth2 token
    PAYLOAD = {'password': '',
    'email': '',
    'client_secret': '',
    'client_id': '',
    'grant_type': 'password'}
    HEADERS = {'content-type': 'application/json'}
    data = post_request("/oauth/token", HEADERS, PAYLOAD)
    print_json(data)
    write_file(data, filename="oauth2.json")
    ACCESS_TOKEN = data["access_token"]
    
    # Make diagostic call
    HEADERS = {'content-type': 'application/json',
    'authorization': ACCESS_TOKEN}
    data = request_get('/api/1/diagnostics', HEADERS)
    print_json(data)
    
    # Vehicle ID
    HEADERS = {'content-type': 'application/json',
    'authorization': ACCESS_TOKEN}
    data = request_get('/api/1/vehicles', HEADERS)
    print_json(data)
    VEHICLE_ID = data["response"][0]["id"]
    
    #
    HEADERS = {'content-type': 'application/json',
    'authorization': ACCESS_TOKEN}
    request_url = '/api/1/vehicles/' + VEHICLE_ID
    data = request_get(request_url, HEADERS)
    print_json(data)
    
def get_request(location, header, parameter = {}):
    request_url = URL + location
    r = requests.get(url = request_url, params = parameter, headers=header)
    print(debug_request_content(r))
    if (r.status_code == requests.codes.ok):   
        print(debug_answer_content(r)) 
        # Extract data in json format
        data = json.loads(r.text)
        # data = r.json()
    else:
        r.raise_for_status()
    return data
    
def get_request_endpoint():
    # https://www.geeksforgeeks.org/get-post-requests-using-python/
    data = load_file("out.json")
    for element in data["results"][0]["address_components"]:
        API_ENDPOINT = F"https://xyz.com/volunteer/{element['long_name']}/badge/{element['short_name']}"
        print(API_ENDPOINT)
        #r=requests.get(API_ENDPOINT)
        #print(r.text)
    
def post_request(location, header, data = {}):
    request_url = URL + location
    r = requests.post(url = request_url, data = data, headers=header)
    print(debug_request_content(r))
    if (r.status_code == requests.codes.ok):   
        print(debug_answer_content(r)) 
        # Extract data in json format
        data = json.loads(r.text)
        # data = r.json()
    else:
        r.raise_for_status()
    return data
    
def load_file(filename="in.json"):
    # Load json-data from file
    with open(filename, 'r') as text_file_input:
        data = text_file_input.read()
    # Load content as json object
    json_obj = json.loads(data)
    return json_obj

def write_file(data, filename="out.json"):
    # Write json-data to file
    with open(filename, 'w') as test_file_output:
        json.dump(data, test_file_output, sort_keys=True, indent=4)
        print(F"File {filename} written")

def print_json(data):
    print(json.dumps(data, sort_keys=True, indent=4))

def debug_request_content(r):
    return F"""
Quering the following request:
Request: {r.url}
Encoding: {r.encoding}
Status code: {r.status_code}
"""

def debug_answer_content(r):
    headers = ""
    for key,value in r.headers.items():
        headers += F"{key}: {value} \n"
    return F"""
Headers:
{headers}
"""

if __name__ == "__main__":
    main()
