import requests
import json

URL = ""
HEADERS = {'content-type': 'application/json'}

def main():
    # Get all people
    print("Solution (1):")
    data = get_request("https://swapi.dev/api/people/", HEADERS)
    # (1) Find Obi and extract name and gender
    obi = {}
    for person in data["results"]:
        if person["name"] == "Obi-Wan Kenobi":
            print(F" [*] Person found: He is {person['gender']} and is called {person['name']}")
            # Save his dataset
            obi = person
    # (2) Find residence on Obi's hometown
    print("Solution (2):")
    obi_homeworld_endpoint = obi["homeworld"]
    data = get_request(obi_homeworld_endpoint, HEADERS)
    for resident in data["residents"]:
        print(F" [*] {get_name_gender(resident)[0]} is living on Obi's homeworld")
    # (3) Find all movies Obi was in
    print("Solution (3):")
    obi_films = []
    data = get_request("https://swapi.dev/api/films/", HEADERS)
    for film in data["results"]:
        for character in film["characters"]:
            if character == obi['url']:
                print(F" [*] Obi was part of: {film['title']}")
                obi_films.append(film["url"])
    # (3) Find all movies Obi was in
    print("Solution (4):")
    obi_friends = {}
    for film in obi_films:
        data = get_request(film, HEADERS)
        for character in data["characters"]:
            if character == obi['url']:
                continue;
            elif character not in obi_friends.keys():
                obi_friends[character] = 1
            else:
                obi_friends[character] = obi_friends[character] + 1
    for key, value in {k: v for k, v in sorted(obi_friends.items(), key=lambda item: item[1], reverse = True)}.items():
        print(F" [*] {get_name_gender(key)[0]} played {value} times together with Obi")

        

def get_name_gender(url_endpoint):
    data = get_request(url_endpoint, HEADERS)
    return [data["name"], data["gender"]]

def get_request(location, header, parameter = {}):
    request_url = URL + location
    r = requests.get(url=request_url, params=parameter, headers=header)
    #print(debug_request_content(r))
    if (r.status_code == requests.codes.ok):   
        #print(debug_answer_content(r)) 
        # Extract data in json format
        data = json.loads(r.text)
        # data = r.json()
    else:
        r.raise_for_status()
    return data

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