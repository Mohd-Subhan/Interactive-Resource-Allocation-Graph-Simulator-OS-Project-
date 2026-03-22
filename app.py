import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

class ResourceManager:
    def __init__(self):
        self.graph = nx.DiGraph()

    def allocate(self, p, r):
        holders = [u for u,v in self.graph.edges() if v == r]

        if holders and holders[0] != p:
            self.graph.add_edge(r,p,type='request')
            return f"{p} requested {r}"
        else:
            if self.graph.has_edge(r,p):
                self.graph.remove_edge(r,p)

            self.graph.add_edge(p,r,type='allocation')
            return f"Allocated {r} to {p}"

    def detect_deadlock(self):
        try:
            cycles = list(nx.simple_cycles(self.graph))
            return len(cycles)>0
        except:
            return False

manager = ResourceManager()

st.title("Interactive Resource Allocation Graph")

p = st.text_input("Process")
r = st.text_input("Resource")

if st.button("Allocate"):
    msg = manager.allocate(p,r)
    st.success(msg)

if st.button("Check Deadlock"):
    if manager.detect_deadlock():
        st.error("Deadlock Detected")
    else:
        st.success("No Deadlock")

fig, ax = plt.subplots()
pos = nx.spring_layout(manager.graph)

alloc = [(u,v) for u,v,d in manager.graph.edges(data=True) if d['type']=='allocation']
req = [(u,v) for u,v,d in manager.graph.edges(data=True) if d['type']=='request']

nx.draw(manager.graph,pos,ax=ax,node_color="lightblue",node_size=1500)
nx.draw_networkx_edges(manager.graph,pos,edgelist=alloc,ax=ax)
nx.draw_networkx_edges(manager.graph,pos,edgelist=req,style='dashed',edge_color='red',ax=ax)

st.pyplot(fig)