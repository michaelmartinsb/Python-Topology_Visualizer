import json

def synchronize_nodes(floor_plan_file, network_structure_file):
    # Load floor plan nodes
    with open(floor_plan_file, 'r') as f:
        floor_plan_data = json.load(f)
    
    floor_plan_nodes = {node['label'] for node in floor_plan_data['nodes']}

    # Load network structure
    with open(network_structure_file, 'r') as f:
        network_structure_data = json.load(f)
    
    network_nodes = set(network_structure_data['nodes'])

    # Synchronize nodes
    new_network_nodes = list(floor_plan_nodes)
    new_network_edges = [
        edge for edge in network_structure_data['edges']
        if edge['source'] in floor_plan_nodes and edge['target'] in floor_plan_nodes
    ]

    # Update network structure
    network_structure_data['nodes'] = new_network_nodes
    network_structure_data['edges'] = new_network_edges

    # Save updated network structure
    with open(network_structure_file, 'w') as f:
        json.dump(network_structure_data, f, indent=4)

# File paths
floor_plan_file = 'floor_plan_nodes.json'
network_structure_file = 'network_structure.json'

# Synchronize nodes
synchronize_nodes(floor_plan_file, network_structure_file)
