import matplotlib.pyplot as plt
import networkx as nx
import community
import time

def girvan_newman(graph, k_val, degree_threshold=0):
    """Perform the Girvan-Newman algorithm to find community structure."""
    start_time = time.time()
    
    # Creates a list of nodes below the threshold and removes those nodes from the dataset.
    nodes_to_remove = [node for node, degree in graph.degree() if degree < degree_threshold]
    graph.remove_nodes_from(nodes_to_remove)
    
    while graph.number_of_edges() > 0:
        # Step 1: Find the edge with the highest betweenness centrality
        edge_betweenness = nx.edge_betweenness_centrality(graph, k=k_val)
        max_edge = max(edge_betweenness, key=edge_betweenness.get)
        
        # Step 2: Remove the edge
        graph.remove_edge(*max_edge)

        # Step 3: Check for connected components
        components = list(nx.connected_components(graph))
        if len(components) > 1:
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Time elapsed: {elapsed_time:.6f}")
            return components  # Found communities
    
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Time elapsed: {elapsed_time:.6f}")
    
    return [list(graph.nodes())]  # Return the whole graph as one community


# Create an empty graph
G = nx.Graph()

# Specify the path to your edge list file
file_path = 'facebook_combined.txt'  # Make sure this path is correct

# Read edges from the file
with open(file_path, 'r') as f:
    for line in f:
        # Split the line into two parts (source and target)
        edge = line.strip().split()
        if len(edge) == 2:  # Ensure there are two elements
            G.add_edge(int(edge[0]), int(edge[1]))  # Convert to integers and add the edge

k_value = 5
degree = 30

print("Pre-processed:")
print("Number of nodes:", G.number_of_nodes())
print("Number of edges:", G.number_of_edges())
print(f"k value: {k_value}")
print(f"degree threshold: {degree}")

communities = girvan_newman(G, k_value, degree)

print("\nPost-processed:")
print("Number of nodes:", G.number_of_nodes())
print("Number of edges:", G.number_of_edges())

# this will take a long time to generate.
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G)  # positions for all nodes
nx.draw(G, pos, with_labels=True, node_size=700, node_color='lightblue', font_size=10, font_color='black')
plt.title("Network Visualization")
plt.show()