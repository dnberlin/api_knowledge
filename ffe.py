import requests
import json

URL = ""
HEADERS = {'content-type': 'application/json'}

def main():
    # (1) Find Obi and extract name and gender
    print("Solution (1):")
    person = find_person("Obi-Wan Kenobi")
    print(F" [*] Person found: {person['name']} is {person['gender']}.")

    # (2) Find residence on Obi's hometown
    print("Solution (2):")
    residents = find_residents_on_homeworld(person["homeworld"])
    for resident in residents:
        print(F" [*] {resident['name']} is living on {person['name']}'s homeworld")

    # (3) Find all movies Obi was in
    print("Solution (3):")
    person_films = find_films_of_person(person['name'])
    for film in person_films:
        print(F" [*] {person['name']} was part of: {film['title']}")

    # (4) Find people that played together with Obi and sort them by occurrence
    print("Solution (4):")
    obi_friends = {}
    for film in person_films:
        for character in film["characters"]:
            if character == person['url']:
                continue;
            elif character not in obi_friends.keys():
                obi_friends[character] = 1
            else:
                obi_friends[character] = obi_friends[character] + 1
    for key, value in {k: v for k, v in sorted(obi_friends.items(), key=lambda item: item[1], reverse = True)}.items():
        print(F" [*] {get_name_gender(key)[0]} played {value} times together with Obi")

def find_person(name):
    data = get_request("https://swapi.dev/api/people/", HEADERS)
    for person in data["results"]:
        if person["name"] == name:
            print(F"Found {person['name']}.")
            return person
    print(F"{name} not found.")
    return None

def find_residents_on_homeworld(homeworld_url_endpoint):
    residents = []
    data = get_request(homeworld_url_endpoint, HEADERS)
    for person_url_endpoint in data["residents"]:
        data = get_request(person_url_endpoint, HEADERS)
        residents.append(data)
    return residents

def find_films_of_person(person):
    person = find_person(person)
    films = []
    data = get_request("https://swapi.dev/api/films/", HEADERS)
    for film in data["results"]:
        for worker_url_endpoint in film["characters"]:
            if worker_url_endpoint == person['url']:
                films.append(film)
    return films



def get_name_gender(url_endpoint):
    data = get_request(url_endpoint, HEADERS)
    return [data["name"], data["gender"]]


""" API call helper functions:
------------------------------"""

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
