#!/usr/bin/env python3

import concurrent.futures
import requests
import json
import time

URL = ""
HEADERS = {'content-type': 'application/json'}

def main():
    # For prototyping disable HTTPS certificate warnings
    requests.packages.urllib3.disable_warnings()

    """Performance measurement
        non-concurrent version: 188s, 165s, 153s
        IO - Bound problem: use threading
        optimizatized version performance: 30s, 35s, 24s
    """
    start_time = time.time()

    my_favorite_person = "Obi-Wan Kenobi"
    inquire_person(my_favorite_person)

    duration = time.time() - start_time
    print(F"Answered all inquiries in {duration} seconds")

def inquire_person(my_favorite_person):
    """Answers a bunch of question regarding a person"""
    
    # (1) Find person and extract name and gender
    print("Solution (1):")
    person = find_person(my_favorite_person)
    print(F" [*] Person found: {person['name']} is {person['gender']}.")

    # (2) Find residents on hometown
    print("Solution (2):")
    resident_urls = find_residents_on_homeworld_of_person(my_favorite_person)
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        for resident_name in executor.map(get_person_name, resident_urls):
            print(F" [*] {resident_name} is living on {my_favorite_person}'s homeworld")

    # (3) Find all movies person was in
    print("Solution (3):")
    film_urls = find_films_of_person(my_favorite_person)
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        for film_title in executor.map(get_film_title, film_urls):
            print(F" [*] {my_favorite_person} was part of: {film_title}")
    
    # (4) Find people that played together with person and sort them by occurrence
    print("Solution (4):")
    friends = find_best_friends_of_person(my_favorite_person)
    for name, occurrence in friends.items():
        print(F" [*] {name} played {occurrence} time(s) together with {my_favorite_person}")

def find_person(name):
    """Find person
    1 apicall in sequence"""
    data = get_request("https://swapi.dev/api/people/", HEADERS)
    for person in data["results"]:
        if person["name"] == name:
            return person
    return None

def find_residents_on_homeworld_of_person(name):
    """Find residents on a homeworld
    2 apicalls in sequence"""
    homeworld_url = find_person(name)['homeworld']
    resident_urls = []
    data = get_request(homeworld_url, HEADERS)
    for person_url in data["residents"]:
        resident_urls.append(person_url)
    return resident_urls

def find_films_of_person(name):
    """Find films of a person
    1 apicall in sequence"""
    person = find_person(name)
    film_urls = []
    for film_url in person['films']:
        film_urls.append(film_url)
    return film_urls

def find_best_friends_of_person(name):
    """Find people that played together with person and order by occurence
    1 apicalls in sequence, others all concurrent"""
    film_urls = find_films_of_person(name)
    friends = {}
    # Collect all people url that played together with person
    all_character_urls = list(get_film_characters_for_films(film_urls))
    all_character_urls_flat = [item for sublist in all_character_urls for item in sublist]
    # Translate url's into there names
    all_character_names = get_names_of_people(all_character_urls_flat)
    # Count ocurrence
    for character_name in all_character_names:
        if character_name == name:
            continue
        elif character_name not in friends.keys():
            friends[character_name] = 1
        else:
            friends[character_name] = friends[character_name] + 1
    # Sort by highest occurence
    return {k: v for k, v in sorted(friends.items(), key=lambda item: item[1], reverse = True)}

def get_film_characters_for_films(film_urls):
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        return executor.map(get_film_characters, film_urls)

def get_names_of_people(person_urls):
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        return executor.map(get_person_name, person_urls)
    
def get_person_name(person_url):
    data = get_request(person_url, HEADERS)
    return data["name"]

def get_film_title(film_url):
    data = get_request(film_url, HEADERS)
    return data["title"]

def get_film_characters(film_url):
    data = get_request(film_url, HEADERS)
    return data['characters']

""" API call helper functions:
------------------------------"""

def get_request(location, header, parameter = {}):
    request_url = URL + location
    r = requests.get(url=request_url, params=parameter, headers=header, verify=False)
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
