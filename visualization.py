import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GraphVisualizer:
    def __init__(self, manager, canvas):
        self.manager = manager
        self.canvas = canvas

    def show_graph(self):
        """ Displays the resource allocation graph on the Tkinter canvas. """
        graph = self.manager.allocation_graph
        fig = plt.Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        ax.clear()

        pos = nx.spring_layout(graph, k=1.5, iterations=100)
        node_colors = ['lightblue' if n in self.manager.processes else 'lightgreen' for n in graph.nodes()]

        nx.draw_networkx_nodes(graph, pos, node_color=node_colors, node_size=1000, ax=ax)
        nx.draw_networkx_labels(graph, pos, font_size=8, font_weight='bold', ax=ax)

        allocation_edges = [(u, v) for u, v, d in graph.edges(data=True) if d['type'] == 'allocation']
        request_edges = [(u, v) for u, v, d in graph.edges(data=True) if d['type'] == 'request']

        has_deadlock, deadlock_msg = self.manager.detect_deadlock()
        cycle_edges = set()
        if has_deadlock and "Cycle:" in deadlock_msg:
            try:
                cycle_str = deadlock_msg.split("Cycle: ")[1].strip("[]")
                cycle_edges = set(eval(cycle_str))
            except Exception:
                cycle_edges = set()

        nx.draw_networkx_edges(graph, pos, edgelist=allocation_edges, edge_color='gray', arrows=True, ax=ax)
        nx.draw_networkx_edges(graph, pos, edgelist=request_edges, edge_color='red', style='dashed', arrows=True, ax=ax)

        ax.set_title("Resource Allocation Graph")
        ax.axis('off')

        # Clear previous content before updating visualization
        for widget in self.canvas.winfo_children():
            widget.destroy()

        canvas_widget = FigureCanvasTkAgg(fig, master=self.canvas)
        canvas_widget.draw()
        canvas_widget.get_tk_widget().pack(fill="both", expand=True)
