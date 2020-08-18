import requests
import json
import urllib.parse

URL = ""

def main():
    get_request_endpoint()    
    #data = get_request()
    # Format well
    #formatted_output = json.dumps(data, sort_keys=True, indent=4)
    #print(formatted_output)
    # Write to file
    #write_file(data)

def get_request():
    # Make a GET request
    URL = "https://maps.googleapis.com/maps/api/geocode/json"
    API_KEY = "AIzaSyCS2Gjgnz64Eayf5MASyFOBEqIw6VWUaGA"
    
    # location given here 
    location = "TU Berlin, Straße des 17 Juni, Berlin"

    PARAMS = {'address':location, 'key': API_KEY}

    r = requests.get(url = URL, params = PARAMS)

    # Extract data in json format
    data = json.loads(r.text)
    # data = r.json()

    return data
    
def get_request_endpoint():
    # https://www.geeksforgeeks.org/get-post-requests-using-python/
    data = load_file("out.json")
    for element in data["results"][0]["address_components"]:
        API_ENDPOINT = F"https://xyz.com/volunteer/{element['long_name']}/badge/{element['short_name']}"
        print(API_ENDPOINT)
        #r=requests.get(API_ENDPOINT)
        #print(r.text)
    
def post_request():
    pass

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
        
def parse_json(json_obj):
    

'''# Get-request - Get data
resp = requests.get('https://example.com/tasks/')
if resp.status_code != 200:
	raise ApiError(F'GET /tasks/ {resp.status_code}')
for todo_item in resp.json():
	print(F"{todo_item['id']} {todo_item['summary']}")

# POST-request - Provide data
task = {"summary": "Take out trash", "description": "..."}
resp = requests.post("https://example.com/tasks/", json=task)
if resp.status_code != 201:
	raise ApiError(F'POST /task/ {resp.status_code}')
print(F'Created task. ID :{resp.json()["id"]}')
'''
if __name__ == "__main__":
    main()
