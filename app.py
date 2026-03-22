import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# ---------- SESSION STATE INIT ----------
if "graph" not in st.session_state:
    st.session_state.graph = nx.DiGraph()

# ---------- RESOURCE MANAGER ----------
def allocate(p, r):
    G = st.session_state.graph
    holders = [u for u, v in G.edges() if v == r]

    if holders and holders[0] != p:
        G.add_edge(r, p, type="request")
        return f"{p} requested {r} (held by {holders[0]})"
    else:
        if G.has_edge(r, p):
            G.remove_edge(r, p)

        G.add_edge(p, r, type="allocation")
        return f"Allocated {r} to {p}"


def detect_deadlock():
    G = st.session_state.graph
    cycles = list(nx.simple_cycles(G))

    for cycle in cycles:
        has_alloc = False
        has_req = False

        for i in range(len(cycle)):
            u = cycle[i]
            v = cycle[(i + 1) % len(cycle)]
            if G.has_edge(u, v):
                t = G[u][v]["type"]
                if t == "allocation":
                    has_alloc = True
                if t == "request":
                    has_req = True

        if has_alloc and has_req:
            return True

    return False


# ---------- UI ----------
st.title("Interactive Resource Allocation Graph Simulator")

p = st.text_input("Process")
r = st.text_input("Resource")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Allocate"):
        if p and r:
            msg = allocate(p, r)
            st.success(msg)

with col2:
    if st.button("Check Deadlock"):
        if detect_deadlock():
            st.error("Deadlock Detected!")
        else:
            st.success("No Deadlock")

with col3:
    if st.button("Clear Graph"):
        st.session_state.graph.clear()
        st.warning("Graph Cleared")


# ---------- GRAPH VISUALIZATION ----------
G = st.session_state.graph

fig, ax = plt.subplots(figsize=(6,4))

if len(G.nodes()) > 0:
    pos = nx.spring_layout(G, k=1.5, seed=42)

    alloc_edges = [(u,v) for u,v,d in G.edges(data=True) if d["type"]=="allocation"]
    req_edges = [(u,v) for u,v,d in G.edges(data=True) if d["type"]=="request"]

    nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=2000, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold", ax=ax)

    nx.draw_networkx_edges(G, pos, edgelist=alloc_edges, edge_color="black", arrows=True, ax=ax)
    nx.draw_networkx_edges(G, pos, edgelist=req_edges, edge_color="red", style="dashed", arrows=True, ax=ax)

ax.set_title("Resource Allocation Graph")
ax.axis("off")

st.pyplot(fig)