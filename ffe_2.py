from collections import defaultdict
import json
import pprint

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
traversed_tests = []
unique_tests = set()
all_connections = []
unique_connections = set()
connection_count = {}

def main():
    
    # (1)
    print("Solution (1):")
    # This is a tree problem, traverse to discover the path for each failed test
    for failed_test in failed_tests:
        visited = set()
        dfs(visited, test_definitions, failed_test)
    # Sort the data
    sorted_test = sort()
    # Print results
    for test, occurence in sorted_test.items():
        print(F"{occurence} test's are dependent on {test}")
    
    # (2)
    print("Solution (2):")
    # Get all connection
    for test in test_definitions:
        visited = set()
        dfs(visited, test_definitions, test)
    # Flatten list
    all_connections_flat = [item for sublist in all_connections for item in sublist]
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
    traversed_tests = []
    for passed_test in test_definitions:
        if passed_test in failed_tests:
            continue
        else:
            visited = set()
            dfs_2(visited, test_definitions, passed_test)
    # Find connection of passed tests
    passed_connections = []
    for unique_passed_test in unique_tests:
        passed_connections.append(test_definitions[unique_passed_test]['dependent_connections'])
    # Flatten list
    passed_connections_flat = [item for sublist in passed_connections for item in sublist]
    # Feed result set with connection that were passed
    for connection in passed_connections_flat:
        if connection in connection_count.keys():
            connection_count[connection] = connection_count[connection] + 1
    # Sort result dict 
    sorted_connections = {k: v for k, v in sorted(connection_count.items(), key=lambda item: item[1])}
    # Print results
    for connection, times_passed in sorted_connections.items():
        print(F"{connection} was successfully passed by {times_passed} test(s)")
    
def sort():
    # Count the occourency of each test for each path
    sorted_test = {}
    for test in traversed_tests:
        if test not in sorted_test:
            sorted_test[test] = 1
        else:
            sorted_test[test] = sorted_test[test] + 1
    # Sort by most occurency        
    return {k: v for k, v in sorted(sorted_test.items(), key=lambda item: item[1], reverse = True)}

def dfs(visited, graph, node):
    # For production mode
    #  if node not in visited:
    # For test purposes
    if node not in visited and node != "...":
        #print (F"Node is {node}")
        traversed_tests.append(node)
        all_connections.append(graph[node]['dependent_connections'])
        visited.add(node)
        for neighbour in graph[node]["parentTests"]:
            dfs(visited, graph, neighbour)

def dfs_2(visited, graph, node):
    # For production mode
    #  if node not in visited:
    # For test purposes
    if node not in visited and node != "...":
        #print (F"Node is {node}")
        unique_tests.add(node)
        visited.add(node)
        for neighbour in graph[node]["parentTests"]:
            dfs_2(visited, graph, neighbour)


if __name__ == '__main__':
    main()