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

def main():
    # This is a tree problem, traverse to discover the path for each failed test
    for failed_test in failed_tests:
        visited = set()
        dfs(visited, test_definitions, failed_test)
    # Sort the data
    sorted_test = sort()
    # Print results
    print(sorted_test)

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
        print (F"Node is {node}")
        traversed_tests.append(node)
        visited.add(node)
        for neighbour in graph[node]["parentTests"]:
            dfs(visited, graph, neighbour)


if __name__ == '__main__':
    main()