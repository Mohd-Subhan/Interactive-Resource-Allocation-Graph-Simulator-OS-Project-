import networkx as nx

class ResourceManager:
    def __init__(self):
        self.allocation_graph = nx.DiGraph()
        self.resources = set()
        self.processes = set()

    def allocate(self, process, resource):
        self.processes.add(process)
        self.resources.add(resource)
        self.allocation_graph.add_node(process)
        self.allocation_graph.add_node(resource)

        holders = [p for p, r in self.allocation_graph.edges() if r == resource]
        if holders and holders[0] != process:
            if not self.allocation_graph.has_edge(resource, process):
                self.allocation_graph.add_edge(resource, process, type='request')
            return f"{process} requested {resource} (held by {holders[0]})"

        if self.allocation_graph.has_edge(resource, process):
            self.allocation_graph.remove_edge(resource, process)

        self.allocation_graph.add_edge(process, resource, type='allocation')
        return f"Allocated {resource} to {process}"

    def release(self, process, resource):
        if self.allocation_graph.has_edge(process, resource):
            self.allocation_graph.remove_edge(process, resource)
            for p in list(self.allocation_graph.successors(resource)):
                self.allocation_graph.remove_edge(resource, p)
                self.allocate(p, resource)
            if self.allocation_graph.degree(process) == 0:
                self.allocation_graph.remove_node(process)
            if self.allocation_graph.degree(resource) == 0:
                self.allocation_graph.remove_node(resource)
            return f"Released {resource} from {process}"
        return f"No allocation of {resource} to {process} exists"

    def detect_deadlock(self):
        try:
            cycles = list(nx.simple_cycles(self.allocation_graph))
            deadlock_cycles = []

            for cycle in cycles:
                has_allocation = False
                has_request = False
                cycle_edges = []

                for i in range(len(cycle)):
                    u = cycle[i]
                    v = cycle[(i + 1) % len(cycle)]
                    if self.allocation_graph.has_edge(u, v):
                        edge_type = self.allocation_graph[u][v]['type']
                        cycle_edges.append((u, v))
                        if edge_type == 'allocation':
                            has_allocation = True
                        elif edge_type == 'request':
                            has_request = True

                if has_allocation and has_request:
                    deadlock_cycles.append(cycle_edges)

            if deadlock_cycles:
                return True, f"Deadlock Detected! Cycle: {repr(deadlock_cycles[0])}"
            return False, "No Deadlock Detected"
        except Exception as e:
            return False, f"Error in deadlock detection: {str(e)}"

    def clear_all(self):
        self.allocation_graph.clear()
        self.processes.clear()
        self.resources.clear()
        return "All allocations and requests have been cleared"
