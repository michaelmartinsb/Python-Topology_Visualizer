# Network Visualizer Application

## Overview

The Network Visualizer application is a tool designed to help users visualize and manipulate network structures and floor plans interactively. It supports two main views: a network hierarchy view and a floor plan view. Users can switch between these views, add nodes, delete nodes, and rename nodes using a graphical user interface (GUI).

## Features

- **Network Hierarchy View**: Visualize the network structure with nodes and edges.
- **Floor Plan View**: Visualize and interact with nodes placed on a floor plan.
- **Add Node**: Add a new node to the network or floor plan.
- **Delete Node**: Remove a node from the network or floor plan.
- **Rename Node**: Change the label of a node.
- **Switch View**: Toggle between the network hierarchy view and the floor plan view.

## Prerequisites

Before running the application, ensure that you have the following installed:

- Python 3.6 or higher
- The following Python packages:
  - PyQt5
  - numpy
  - networkx
  - pyvis
  - matplotlib
  - pillow

You can install the necessary packages using pip:

```bash
pip install PyQt5 numpy networkx pyvis matplotlib pillow
```

## Setup

1. Ensure that you have the following files in the same directory as the application script (`main.py`):
   - `network_structure.json`: JSON file containing the network structure data.
   - `floor_plan_nodes.json`: JSON file containing the floor plan nodes data.
   - `floor_plan.png`: Image file of the floor plan.

2. The structure of `network_structure.json` should be as follows:
   ```json
   {
       "nodes": [
           {"label": "Node1"},
           {"label": "Node2"},
           ...
       ],
       "edges": [
           {"source": "Node1", "target": "Node2"},
           ...
       ]
   }
   ```

3. The structure of `floor_plan_nodes.json` should be as follows:
   ```json
   {
       "nodes": [
           {"label": "Node1", "x": 100, "y": 150},
           {"label": "Node2", "x": 200, "y": 250},
           ...
       ]
   }
   ```

## Running the Application

To run the application, execute the following command in your terminal:

```bash
python main.py
```

This will launch the Network Visualizer application window.

## Usage Instructions

### Main Window

The main window consists of two main sections: the visualization area and the controls area.

### Visualization Area

- **Network Hierarchy View**: Displays the network structure using pyvis. Nodes and edges are visualized, and users can manipulate nodes (add, edit, delete).
- **Floor Plan View**: Displays the floor plan image with nodes overlaid. Users can interact with nodes (drag, add, delete, rename).

### Controls Area

- **Switch View**: Toggle between the network hierarchy view and the floor plan view.
- **Add Node**: Add a new node to the current view.
- **Delete Node**: Enable delete node mode. Click on a node in the visualization area to delete it.
- **Rename Node**: Enable rename node mode. Click on a node label in the visualization area to rename it.

### Interacting with Nodes

- **Drag Nodes (Floor Plan View)**: Click and drag a node to move it to a new position.
- **Rename Nodes**: Click on a node label while in rename node mode to change the node's label.
- **Delete Nodes**: Click on a node while in delete node mode to remove it.

### Saving and Loading Data

- **Load Data**: The application automatically loads data from `network_structure.json` and `floor_plan_nodes.json` upon startup.
- **Save Data**: The application automatically saves any changes made to the nodes and their positions back to the JSON files.

## Application Structure

### `NetworkVisualizer` Class

The `NetworkVisualizer` class extends `QMainWindow` and serves as the main application window. It contains methods to initialize the UI, load data, update the graph, draw the network hierarchy and floor plan, and handle various user interactions.

#### Key Methods

- **initUI()**: Initializes the user interface elements.
- **load_data()**: Loads the network structure and floor plan data from JSON files.
- **update_graph()**: Updates the network graph structure.
- **draw_network_hierarchy()**: Draws the network hierarchy using pyvis.
- **draw_floor_plan()**: Draws the floor plan and overlays nodes.
- **switch_view()**: Toggles between the network hierarchy view and the floor plan view.
- **add_node()**: Adds a new node to the current view.
- **enable_delete_node()**: Enables the delete node mode.
- **enable_rename_node()**: Enables the rename node mode.
- **on_press(event)**: Handles mouse press events for node interactions.
- **on_motion(event)**: Handles mouse motion events for dragging nodes.
- **on_release(event)**: Handles mouse release events for finalizing node positions.
- **delete_node(event)**: Deletes a node from the current view.
- **save_data()**: Saves the current state of the network structure and floor plan nodes to JSON files.
- **on_text_click(event)**: Handles node label click events for renaming nodes.
- **disconnect_events()**: Disconnects existing event handlers.

## Conclusion

The Network Visualizer application provides a powerful and interactive way to visualize and manipulate network structures and floor plans. By following the instructions in this README, you should be able to set up, run, and use the application effectively. If you encounter any issues or have any questions, please feel free to reach out for support.