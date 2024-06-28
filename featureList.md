# Network Visualizer Application - Detailed Feature List

## Overview

The Network Visualizer application is a comprehensive tool designed to help users visualize, manipulate, and interact with network structures and floor plans. Below is a detailed feature list outlining the various functionalities provided by the application.

## Features

### General Features

- **Dual View Modes**: The application offers two primary views:
  - **Network Hierarchy View**: Visualize the network structure with nodes and edges in a hierarchical layout.
  - **Floor Plan View**: Visualize and interact with nodes overlaid on a floor plan image.

### Network Hierarchy View

- **Visualization with pyvis**: Utilizes the pyvis library to render network structures in an interactive and visually appealing manner.
- **Node and Edge Representation**: Nodes and edges are displayed with labels for easy identification.
- **Interactive Controls**: 
  - **Manipulate Nodes**: Add, edit, and delete nodes using an interactive interface.
  - **Edge Management**: Define and modify connections between nodes (edges).
- **Customization Options**: Access and modify various visualization settings using built-in pyvis controls.

### Floor Plan View

- **Floor Plan Integration**: Overlay nodes on a provided floor plan image, enabling spatial representation of network elements.
- **Interactive Node Placement**: 
  - **Drag and Drop**: Click and drag nodes to reposition them on the floor plan.
  - **Node Label Display**: Node labels are displayed for easy identification and can be interactively repositioned.
- **Dynamic Node Addition**: Add new nodes directly onto the floor plan at a specified location.
- **Image Rendering**: High-quality rendering of floor plan images using matplotlib.

### Node Management

- **Add Node**:
  - **Network Hierarchy View**: Automatically positions new nodes and connects them to an existing node.
  - **Floor Plan View**: Adds new nodes at the center of the floor plan image.
- **Delete Node**: 
  - **Network Hierarchy View**: Removes nodes and all associated edges.
  - **Floor Plan View**: Deletes nodes and updates the floor plan layout accordingly.
- **Rename Node**:
  - **Interactive Renaming**: Click on a node label to rename it using a dialog prompt.
  - **Label Updates**: Automatically updates labels in both the network and floor plan views.

### View Management

- **Switch View**: 
  - **Toggle Views**: Easily switch between the network hierarchy and floor plan views with a button click.
  - **State Preservation**: Maintains node positions and states when switching between views.
- **Dynamic Resizing**: Adjusts layout dynamically to fit the window size, ensuring an optimal user experience.

### Data Management

- **Data Loading**: 
  - **Network Structure**: Loads network data from `network_structure.json`.
  - **Floor Plan Nodes**: Loads node positions from `floor_plan_nodes.json`.
- **Data Saving**: 
  - **Auto-Save**: Automatically saves changes to node positions and network structure back to the JSON files.
  - **Manual Save**: Provides functions to manually save the current state of the network and floor plan data.
- **File Existence Check**: Validates the existence of required data files and provides error messages if files are missing.

### Event Handling

- **Mouse Event Handling**: 
  - **Press Events**: Handles mouse press events to select and manipulate nodes.
  - **Motion Events**: Handles mouse movement events for dragging nodes.
  - **Release Events**: Finalizes node positions on mouse release.
- **Pick Events**: Handles clicks on node labels for renaming functionality.
- **Event Disconnection**: Ensures proper cleanup of event handlers to prevent memory leaks and unexpected behavior.

### Debugging and Logging

- **Debug Statements**: 
  - **Print Statements**: Outputs relevant information to the console for debugging purposes.
  - **HTML Content Logging**: Logs the HTML content of the network visualization for inspection.

### User Interface Elements

- **Buttons and Controls**:
  - **Switch View Button**: Toggles between network and floor plan views.
  - **Add Node Button**: Initiates the process of adding a new node.
  - **Delete Node Button**: Activates delete node mode.
  - **Rename Node Button**: Activates rename node mode.
- **Labels**: Displays details about selected nodes and other relevant information.

### Visualization Options

- **Network Options**:
  - **Node Styling**: Configures node appearance including shape, size, and color.
  - **Edge Styling**: Defines edge appearance and behavior.
  - **Interactive Buttons**: Provides interactive controls for node and edge manipulation.

- **Floor Plan Options**:
  - **Image Rendering**: Renders floor plan images with high quality.
  - **Node Overlays**: Places nodes accurately on the floor plan based on predefined coordinates.

## Conclusion

The Network Visualizer application offers a robust set of features for visualizing and interacting with network structures and floor plans. With its dual-view modes, comprehensive node management capabilities, and interactive user interface, the application provides a powerful tool for users to manage and explore network layouts effectively. If you have any questions or need further assistance, please feel free to reach out for support.