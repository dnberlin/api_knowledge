import requests
import json

URL = ""
HEADERS = {'content-type': 'application/json'}

def main():
    my_favorite_person = "Obi-Wan Kenobi"
    inquire_person(my_favorite_person)

def inquire_person(my_favorite_person):
    """Answers a bunch of question regarding a person"""
    
    # (1) Find person and extract name and gender
    print("Solution (1):")
    person = find_person(my_favorite_person)
    print(F" [*] Person found: {person['name']} is {person['gender']}.")

    # (2) Find residents on hometown
    print("Solution (2):")
    residents = find_residents_on_homeworld_of_person(my_favorite_person)
    for resident in residents:
        print(F" [*] {resident['name']} is living on {my_favorite_person}'s homeworld")

    # (3) Find all movies person was in
    print("Solution (3):")
    person_films = find_films_of_person(my_favorite_person)
    for film in person_films:
        print(F" [*] {my_favorite_person} was part of: {film['title']}")

    # (4) Find people that played together with person and sort them by occurrence
    print("Solution (4):")
    friends = find_best_friends_of_person(my_favorite_person)
    for name, occurrence in friends.items():
        print(F" [*] {get_name(name)} played {occurrence} times together with {my_favorite_person}")

def find_person(name):
    """Find person"""
    data = get_request("https://swapi.dev/api/people/", HEADERS)
    for person in data["results"]:
        if person["name"] == name:
            return person
    return None

def find_residents_on_homeworld_of_person(name):
    """Find residents on a homeworld"""
    homeworld_url_endpoint = find_person(name)['homeworld']
    residents = []
    data = get_request(homeworld_url_endpoint, HEADERS)
    for person_url_endpoint in data["residents"]:
        data = get_request(person_url_endpoint, HEADERS)
        residents.append(data)
    return residents

def find_films_of_person(name):
    """Find films of a person"""
    person = find_person(name)
    films = []
    data = get_request("https://swapi.dev/api/films/", HEADERS)
    for film in data["results"]:
        for person_url_endpoint in film["characters"]:
            if person_url_endpoint == person['url']:
                films.append(film)
    return films

def find_best_friends_of_person(name):
    """Find people that played together with person and order by occurence"""
    person = find_person(name)
    films = find_films_of_person(name)
    friends = {}
    for film in films:
        for character_url_endpoint in film["characters"]:
            if character_url_endpoint == person['url']:
                continue
            elif character_url_endpoint not in friends.keys():
                friends[character_url_endpoint] = 1
            else:
                friends[character_url_endpoint] = friends[character_url_endpoint] + 1
    return {k: v for k, v in sorted(friends.items(), key=lambda item: item[1], reverse = True)}

def get_name(url_endpoint):
    data = get_request(url_endpoint, HEADERS)
    return data["name"]

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
