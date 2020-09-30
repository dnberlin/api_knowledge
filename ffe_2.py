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
failed_tests = ["test7, test3", "test1", "..."]

def main():
    # Set to keep track of visited nodes.
    # Driver Code
    for test in test_definitions:
        visited = set()
        dfs(visited, test_definitions, test)

def dfs(visited, graph, node):
    if node not in visited and node != "...":
        print (F"Node is {node}")
        visited.add(node)
        for neighbour in graph[node]["parentTests"]:
            dfs(visited, graph, neighbour)


if __name__ == '__main__':
    main()