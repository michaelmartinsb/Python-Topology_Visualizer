import sys
import json
import numpy as np
import networkx as nx
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLabel, QSplitter, QInputDialog
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from pyvis.network import Network
from matplotlib.patches import Circle
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from PIL import Image
import tempfile
import os

class NetworkVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize data structures for storing node positions
        self.floor_plan_pos = {}
        self.topology_pos = {}

        # Initialize the user interface
        self.initUI()

        # Flags for various states of the application
        self.isNetworkView = True
        self.dragging_node = None
        self.offset = None
        self.adding_node = False
        self.deleting_node = False
        self.renaming_node = False
        self.dragging_node_topology = None
        self.offset_topology = None

    def initUI(self):
        # Set up the main window
        self.setWindowTitle('Network Visualizer')
        self.setGeometry(100, 100, 1200, 900)

        # Set up the central widget and main layout
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)

        # Set up a splitter to divide the UI vertically
        self.splitter = QSplitter(Qt.Vertical)
        self.layout.addWidget(self.splitter)

        # Set up the canvas widget and layout
        self.canvasWidget = QWidget()
        self.canvasLayout = QVBoxLayout()
        self.canvasWidget.setLayout(self.canvasLayout)
        self.splitter.addWidget(self.canvasWidget)

        # Set up the web view for network visualization
        self.webView = QWebEngineView()
        self.canvasLayout.addWidget(self.webView)

        # Set up the controls widget and layout
        self.controlsWidget = QWidget()
        self.controlsLayout = QHBoxLayout()
        self.controlsWidget.setLayout(self.controlsLayout)
        self.splitter.addWidget(self.controlsWidget)

        # Add buttons for various actions
        self.switchViewButton = QPushButton('Switch View')
        self.switchViewButton.clicked.connect(self.switch_view)
        self.controlsLayout.addWidget(self.switchViewButton)

        self.addNodeButton = QPushButton('Add Node')
        self.addNodeButton.clicked.connect(self.add_node)
        self.controlsLayout.addWidget(self.addNodeButton)

        self.deleteNodeButton = QPushButton('Delete Node')
        self.deleteNodeButton.clicked.connect(self.enable_delete_node)
        self.controlsLayout.addWidget(self.deleteNodeButton)

        self.renameNodeButton = QPushButton('Rename Node')
        self.renameNodeButton.clicked.connect(self.enable_rename_node)
        self.controlsLayout.addWidget(self.renameNodeButton)

        # Label to display node details
        self.nodeDetails = QLabel('Node Details: None')
        self.nodeDetails.setWordWrap(True)
        self.controlsLayout.addWidget(self.nodeDetails)

        # Set initial sizes for the splitter panels
        self.splitter.setSizes([800, 100])

        # Load initial data and draw the network hierarchy
        self.load_data()
        self.draw_network_hierarchy()

    def load_data(self):
        # Check if necessary files exist
        if not os.path.exists('network_structure.json'):
            print("Error: network_structure.json file not found")
            return
        if not os.path.exists('floor_plan_nodes.json'):
            print("Error: floor_plan_nodes.json file not found")
            return

        # Load network structure and floor plan data from JSON files
        with open('network_structure.json', 'r') as file:
            self.network_data = json.load(file)
        with open('floor_plan_nodes.json', 'r') as file:
            self.floor_plan_nodes = json.load(file)

        # Initialize position dictionaries for floor plan and topology
        self.floor_plan_pos = {node['label']: (node['x'], node['y']) for node in self.floor_plan_nodes['nodes']}
        self.topology_pos = {node['label']: self.topology_pos.get(node['label'], [0, 0]) for node in self.network_data['nodes']}
        
        # Update the graph structure
        self.update_graph()

    def update_graph(self):
        # Initialize a directed graph using networkx
        self.G = nx.DiGraph()

        # Add nodes and edges to the graph
        for node in self.network_data['nodes']:
            self.G.add_node(node['label'])
        for edge in self.network_data['edges']:
            self.G.add_edge(edge['source'], edge['target'])

    def draw_network_hierarchy(self):
        # Create a pyvis network visualization
        net = Network(notebook=False, width="100%", height="750px")
        
        # Add nodes and edges to the pyvis network
        for node in self.network_data['nodes']:
            net.add_node(node['label'])
        for edge in self.network_data['edges']:
            net.add_edge(edge['source'], edge['target'])

        # Show node manipulation buttons in the UI
        net.show_buttons(filter_=['nodes'])

        # Enable node manipulation options
        net.set_options("""
        {
            "manipulation": {
                "enabled": true,
                "initiallyActive": true,
                "addNode": true,
                "editNode": true,
                "deleteNode": true,
                "controlNodeStyle": {
                    "shape": "dot",
                    "size": 6,
                    "color": {
                        "background": "#ff0000",
                        "border": "#3c3c3c"
                    },
                    "borderWidth": 2,
                    "borderWidthSelected": 3
                }
            },
            "configure": {
                "enabled": true
            }
        }
        """)

        # Save the network visualization to a temporary HTML file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
        net.save_graph(temp_file.name)
        print(f"Graph saved to {temp_file.name}")
        
        # Load the HTML content into the web view
        with open(temp_file.name, 'r') as file:
            html_content = file.read()
        print(html_content)  # Debug: Print HTML content
        self.webView.setUrl(QUrl.fromLocalFile(temp_file.name))

    def draw_floor_plan(self):
        # Remove the current web view widget
        self.canvasLayout.removeWidget(self.webView)
        self.webView.deleteLater()

        # Create a new canvas for the floor plan
        self.canvas = FigureCanvas(plt.Figure())
        self.canvasLayout.addWidget(self.canvas)

        # Check if the floor plan image file exists
        if not os.path.exists('floor_plan.png'):
            print("Error: floor_plan.png file not found")
            return

        # Load the floor plan image
        self.floor_plan_image = Image.open('floor_plan.png')
        arr = np.array(self.floor_plan_image)

        # Draw the floor plan image on the canvas
        self.ax = self.canvas.figure.add_subplot(111)
        self.ax.clear()
        self.ax.imshow(arr, aspect='auto')

        # Draw nodes on the floor plan
        self.node_patches = []
        self.node_texts = []
        for node in self.floor_plan_nodes['nodes']:
            patch = Circle((node['x'], node['y']), 10, color='red', picker=True)
            self.node_patches.append((patch, node))
            self.ax.add_patch(patch)
            text = self.ax.text(node['x'], node['y'], node['label'], color='black', fontsize=12, picker=True)
            self.node_texts.append(text)

        # Render the canvas
        self.canvas.draw()

        # Disconnect any existing events and set up new event handlers
        self.disconnect_events()
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        self.canvas.mpl_connect('pick_event', self.on_text_click)

    def switch_view(self):
        # Save the current state and reload data
        self.save_data()
        self.load_data()

        # Switch between network view and floor plan view
        if self.isNetworkView:
            self.draw_floor_plan()
        else:
            self.canvasLayout.removeWidget(self.canvas)
            self.canvas.deleteLater()
            self.webView = QWebEngineView()
            self.canvasLayout.addWidget(self.webView)
            self.draw_network_hierarchy()
        self.isNetworkView = not self.isNetworkView

    def add_node(self):
        if self.isNetworkView:
            # Add a new node in the network view
            label = f'Node {len(self.network_data["nodes"]) + 1}'
            self.network_data['nodes'].append({"label": label})
            self.topology_pos[label] = [0, 0]

            # Connect the new node to an existing node
            if self.network_data['nodes']:
                source_node = self.network_data['nodes'][0]['label']
            else:
                source_node = label
            self.network_data['edges'].append({'source': source_node, 'target': label})

            # Update the graph and redraw the network
            self.update_graph()
            self.draw_network_hierarchy()
        else:
            # Add a new node in the floor plan view
            width, height = self.floor_plan_image.size
            x, y = width // 2, height // 2
            label = f'Node {len(self.floor_plan_nodes["nodes"]) + 1}'
            new_node = {"label": label, "x": x, "y": y}
            self.floor_plan_nodes['nodes'].append(new_node)
            self.floor_plan_pos[label] = (x, y)

            # Draw the new node on the floor plan
            patch = Circle((x, y), 10, color='red', picker=True)
            self.node_patches.append((patch, new_node))
            self.ax.add_patch(patch)
            text = self.ax.text(x, y, label, color='black', fontsize=12, picker=True)
            self.node_texts.append(text)
            self.canvas.draw()
        
        # Save the updated data
        self.save_data()

    def enable_delete_node(self):
        # Enable the delete node mode
        self.deleting_node = True

    def enable_rename_node(self):
        # Enable the rename node mode
        self.renaming_node = True

    def on_press(self, event):
        if event.inaxes != self.ax:
            return

        if self.deleting_node:
            self.delete_node(event)
            self.deleting_node = False
            return

        # Check if a node is selected for dragging
        for patch, node in self.node_patches:
            if patch.contains(event)[0]:
                self.dragging_node = patch
                self.offset = (node['x'] - event.xdata, node['y'] - event.ydata)
                return

    def on_motion(self, event):
        if self.dragging_node is None or event.inaxes != self.ax:
            return

        # Update the position of the dragged node
        x, y = event.xdata + self.offset[0], event.ydata + self.offset[1]
        self.dragging_node.center = (x, y)
        for text, (patch, node) in zip(self.node_texts, self.node_patches):
            if self.dragging_node == patch:
                text.set_position((x, y))
                node['x'], node['y'] = x, y
                self.floor_plan_pos[node['label']] = (x, y)
                break
        self.canvas.draw()

    def on_release(self, event):
        if self.dragging_node is None:
            return

        # Finalize the position of the dragged node
        for patch, node in self.node_patches:
            if patch == self.dragging_node:
                node['x'], node['y'] = patch.center
                self.dragging_node = None
                self.offset = None

        # Save the updated data
        self.save_data()

    def delete_node(self, event):
        if not self.isNetworkView:
            # Delete a node from the floor plan
            for i, (patch, node) in enumerate(self.node_patches):
                if patch.contains(event)[0]:
                    patch.remove()
                    self.node_texts[i].remove()
                    del self.node_patches[i]
                    del self.node_texts[i]
                    self.floor_plan_nodes['nodes'].remove(node)
                    self.floor_plan_pos.pop(node['label'], None)
                    self.canvas.draw()
                    self.save_data()
                    return
        else:
            # Delete a node from the network view
            node_id = None
            for n_id, n_pos in self.topology_pos.items():
                if n_pos[0] - 0.05 < event.xdata < n_pos[0] + 0.05 and n_pos[1] - 0.05 < n_pos[1] + 0.05:
                    node_id = n_id
                    break
            if node_id:
                self.network_data['nodes'] = [n for n in self.network_data['nodes'] if n['label'] != node_id]
                self.network_data['edges'] = [edge for edge in self.network_data['edges'] if edge['source'] != node_id and edge['target'] != node_id]
                self.topology_pos.pop(node_id, None)
                self.update_graph()
                self.draw_network_hierarchy()
                self.save_data()

    def save_data(self):
        # Update the positions of nodes in the floor plan
        for node in self.floor_plan_nodes['nodes']:
            if node['label'] in self.floor_plan_pos:
                node['x'], node['y'] = self.floor_plan_pos[node['label']]

        # Save the floor plan nodes to a JSON file
        with open('floor_plan_nodes.json', 'w') as file:
            json.dump(self.floor_plan_nodes, file, indent=4)
        
        # Save the network structure to a JSON file
        with open('network_structure.json', 'w') as file:
            json.dump(self.network_data, file, indent=4)

    def on_text_click(self, event):
        if self.renaming_node and event.artist in self.node_texts:
            index = self.node_texts.index(event.artist)
            node = self.node_patches[index][1]

            # Prompt the user to enter a new label for the node
            new_label, ok = QInputDialog.getText(self, 'Edit Node Label', 'Enter new label:', text=node['label'])
            if ok:
                old_label = node['label']
                node['label'] = new_label
                event.artist.set_text(new_label)
                for fp_node in self.floor_plan_nodes['nodes']:
                    if fp_node['label'] == old_label:
                        fp_node['label'] = new_label
                        break
                self.floor_plan_pos[new_label] = self.floor_plan_pos.pop(old_label)
                self.canvas.draw()
                self.save_data()
            self.renaming_node = False

    def disconnect_events(self):
        # Disconnect existing event handlers
        if hasattr(self, 'cid_pick'):
            self.canvas.mpl_disconnect(self.cid_pick)
        if hasattr(self, 'cid_motion'):
            self.canvas.mpl_disconnect(self.cid_motion)
        if hasattr(self, 'cid_release'):
            self.canvas.mpl_disconnect(self.cid_release)
        self.cid_pick = None
        self.cid_motion = None
        self.cid_release = None

if __name__ == '__main__':
    # Initialize and run the PyQt application
    app = QApplication(sys.argv)
    ex = NetworkVisualizer()
    ex.show()
    sys.exit(app.exec_())
