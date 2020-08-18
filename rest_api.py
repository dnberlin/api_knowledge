import requests
import json

def main():
    data = get_request()
    formatted_output = json.dumps(data, sort_keys=True, indent=4)
    print(formatted_output)

def get_request():
    # Make a GET request
    URL = "https://maps.googleapis.com/maps/api/geocode/json"
    API_KEY = "AIzaSyCS2Gjgnz64Eayf5MASyFOBEqIw6VWUaGA"
    
    # location given here 
    location = "TU Berlin, Straße des 17 Juni, Berlin"

    PARAMS = {'address':location, 'key': API_KEY}

    r = requests.get(url = URL, params = PARAMS)

    # Extract data in json format
    data = r.json()

    return data
    
def post_request():
    pass

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
