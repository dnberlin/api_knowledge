#!/usr/bin/env python3

test_definitions = {
    "test1": {
    "parentTests": [],
    "dependent_connections": ["conn1", "conn5", "conn6", "..."]},
    "test2": {
    "parentTests": ["test1"],
    "dependent_connections": ["conn3", "conn5", "conn26", "conn32", "..."]},
    "test3": {
    "parentTests": ["test2", "..."],
    "dependent_connections": ["conn1", "conn6", "conn30", "..."]},
    "test4": {
    "parentTests": ["test2", "..."],
    "dependent_connections": ["conn8", "conn9", "conn20", "conn67", "conn2", "..."]},
    "test5": {
    "parentTests": ["test3", "test2", "..."],
    "dependent_connections": ["conn74", "conn98", "conn45", "conn13", "conn4", "..."]},
    "test6": {
    "parentTests": [],
    "dependent_connections": ["conn3", "conn20", "conn2", "conn1", "conn33", "..."]},
    "test7": {
    "parentTests": ["test6", "test4", "..."],
    "dependent_connections": ["conn33", "conn51", "conn6", "conn9", "conn10", "..."]},
    "...": {"..."}
}
# There is a " missing between test7 and test3. Maybe you want to correct the exam.
failed_tests = ["test7", "test3", "test1", "..."]

# Tests
traversed_failed_tests = []
unique_tests = set()

# Connections
#  Lists all found connections while traversing
all_connections = []
unique_connections = set()
connection_count = {}

def main():
    
    # (1)
    print("Solution (1):")
    solution_1()
    
    # (2)
    print("Solution (2):")
    solution_2()

def solution_1():
    # Traverse to discover the path for each failed test
    for failed_test in failed_tests:
        visited_failed = set()
        dfs_failed(visited_failed, test_definitions, failed_test)
    # Sort the data
    sorted_test = sort_by_dependence()
    # Print results
    for test, occurence in sorted_test.items():
        print(F"[*] {occurence} test's are dependent on {test}")

def sort_by_dependence():
    # Count the occourency of each test for each path
    sorted_test = {}
    for test in traversed_failed_tests:
        if test not in sorted_test:
            sorted_test[test] = 1
        else:
            sorted_test[test] = sorted_test[test] + 1
    # Sort by most occurency        
    return {k: v for k, v in sorted(sorted_test.items(), key=lambda item: item[1], reverse = True)}

def solution_2():
    # Get all connection
    for test in test_definitions:
        visited_all = set()
        dfs_all(visited_all, test_definitions, test)
    # Flatten list
    all_connections_flat = flatten_list(all_connections)
    # Clean list and skip dublicants
    for connection in all_connections_flat:
        if connection == '...':
            continue
        else:
            unique_connections.add(connection)
    # initialize unique connection dict
    for connection in unique_connections:
        connection_count[connection] = 0
    # Find passed tests
    for passed_test in test_definitions:
        if passed_test in failed_tests:
            continue
        else:
            visited_passed = set()
            dfs_passed(visited_passed, test_definitions, passed_test)
    # Find connection of passed tests
    passed_connections = []
    for unique_passed_test in unique_tests:
        passed_connections.append(test_definitions[unique_passed_test]['dependent_connections'])
    # Flatten list
    passed_connections_flat = flatten_list(passed_connections)
    # Feed result set with connection that were passed
    for connection in passed_connections_flat:
        if connection in connection_count.keys():
            connection_count[connection] = connection_count[connection] + 1
    # Sort result dict 
    sorted_connections = {k: v for k, v in sorted(connection_count.items(), key=lambda item: item[1])}
    # Print results
    for connection, times_passed in sorted_connections.items():
        print(F"[*] {connection} was successfully passed by {times_passed} test(s)")

"""Traversal helper functions"""

def dfs_all(visited, graph, node):
    if node not in visited and node != "...":
        all_connections.append(graph[node]['dependent_connections'])
        visited.add(node)
        for neighbour in graph[node]["parentTests"]:
            dfs_all(visited, graph, neighbour)

def dfs_failed(visited, graph, node):
    if node not in visited and node != "...":
        #print (F"Node is {node}")
        traversed_failed_tests.append(node)
        visited.add(node)
        for neighbour in graph[node]["parentTests"]:
            dfs_failed(visited, graph, neighbour)

def dfs_passed(visited, graph, node):
    if node not in visited and node != "...":
        #print (F"Node is {node}")
        unique_tests.add(node)
        visited.add(node)
        for neighbour in graph[node]["parentTests"]:
            dfs_passed(visited, graph, neighbour)

"""Other helper functions"""
def flatten_list(nested_list):
    return [item for sublist in nested_list for item in sublist]

if __name__ == '__main__':
    main()