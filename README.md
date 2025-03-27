# Interactive Resource Allocation Graph Simulator

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)



A dynamic visualization tool for managing and monitoring resource allocation in operating systems,  This simulator visualizes resource allocation graphs, detects deadlocks, and supports interactive modifications through a user-friendly GUI.

## Project Overview

The **Interactive Resource Allocation Graph Simulator** is designed to enhance understanding of resource management in operating systems by:
- Visualizing processes and resources as a bipartite graph with real-time updates.
- Detecting deadlocks using cycle detection in a directed graph.
- Allowing users to allocate and release resources interactively.

### Authors
- **Ch Shiva Kalyan (34)** - 12307446, K23WA  
- **Abhiram (35)** - 12319957, K23WA  
- **Mohd Subhan** - 12314341, K23WA  
**Submitted to:** Dr. Gurbinder Singh Brar

## Features
- **Graphical Interface**: Processes (light blue) and resources (light green) with allocation (gray) and request (red dashed) edges.
- **Deadlock Detection**: Identifies all deadlock cycles, highlighting affected nodes in red.
- **Interactive Controls**: Allocate/release resources via text inputs with instant graph updates.
- **Status Feedback**: Displays messages in a GUI text area.
- **Error Handling**: Alerts for invalid inputs or actions via dialog boxes.

## Prerequisites
- **Python 3.6+**
- Required libraries:
  - `networkx` - Graph management
  - `matplotlib` - Graph visualization
  - `tkinter` - GUI (usually included with Python)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/chshivakalyan/Interactive-resource-allocation-graph-simulator.git
   cd Interactive-resource-allocation-graph-simulator
2. **Install Dependencies**:
     pip install networkx matplotlib
3. **Usage**
   1.run python gui.py

