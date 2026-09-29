import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

from searchAlgos import hospital_graph, locations, gbfs, a_star

st.set_page_config(
    page_title="Emergency Supply Robot - Informed Search",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 Emergency Supply Robot — GBFS & A*")
st.write(
    "Select an initial node, a goal node, and a search algorithm. "
    "The application highlights the returned solution path."
)

nodes = list(hospital_graph.keys())

start = st.selectbox(
    "Select Initial Node",
    nodes,
    index=nodes.index("Pharmacy"),
)

goal = st.selectbox(
    "Select Goal Node",
    nodes,
    index=nodes.index("Emergency_Ward"),
)

algorithm = st.selectbox(
    "Select Search Algorithm",
    ["GBFS", "A*"],
)

if st.button("Run Search"):
    if start == goal:
        path = [start]
        cost = 0.0
    elif algorithm == "GBFS":
        path, cost = gbfs(start, goal)
    else:
        path, cost = a_star(start, goal)

    if path is None:
        st.error("No path was found between the selected nodes.")
    else:
        st.subheader("Search Result")
        st.write(f"**Algorithm:** {algorithm}")
        st.write(f"**Solution Path:** {' → '.join(path)}")
        st.write(f"**Total Path Cost:** {cost:.2f}")

        G = nx.DiGraph()
        for node, position in locations.items():
            G.add_node(node, pos=position)

        for node, neighbors in hospital_graph.items():
            for neighbor, weight in neighbors.items():
                G.add_edge(node, neighbor, weight=weight)

        pos = locations
        fig, ax = plt.subplots(figsize=(10, 6))

        nx.draw_networkx_nodes(
            G, pos, ax=ax, node_size=1800, node_color="lightblue"
        )
        nx.draw_networkx_labels(
            G, pos, ax=ax, font_size=9, font_weight="bold"
        )

        nx.draw_networkx_edges(
            G,
            pos,
            ax=ax,
            arrows=True,
            arrowsize=18,
            width=1.5,
            edge_color="gray",
            connectionstyle="arc3,rad=0.03",
        )

        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(
            G, pos, edge_labels=edge_labels, ax=ax, font_size=8
        )

        path_edges = list(zip(path, path[1:]))
        if path_edges:
            nx.draw_networkx_edges(
                G,
                pos,
                ax=ax,
                edgelist=path_edges,
                width=4,
                edge_color="red",
                arrows=True,
                arrowsize=22,
                connectionstyle="arc3,rad=0.03",
            )

        nx.draw_networkx_nodes(
            G,
            pos,
            ax=ax,
            nodelist=[start],
            node_size=1900,
            node_color="lightgreen",
        )
        nx.draw_networkx_nodes(
            G,
            pos,
            ax=ax,
            nodelist=[goal],
            node_size=1900,
            node_color="gold",
        )

        ax.set_title(f"{algorithm} Solution Path")
        ax.axis("off")
        st.pyplot(fig)
