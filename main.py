import networkx as nx
import plotly.graph_objects as go
import json  # For saving
import random  # For random insights

def build_graph():
    G = nx.Graph()
    
    # Starter concepts (customize or load from file later)
    concepts = [
        "Machine Learning Basics",
        "Supervised Learning",
        "Unsupervised Learning",
        "SVM",
        "Kernel Methods",
        "Dimensionality Reduction",
        "PCA",
        "Neural Networks",
        "Bayesian Inference"
    ]
    G.add_nodes_from(concepts)
    
    # Starter edges
    G.add_edge("Machine Learning Basics", "Supervised Learning", label="includes")
    G.add_edge("Machine Learning Basics", "Unsupervised Learning", label="includes")
    G.add_edge("Supervised Learning", "SVM", label="example")
    G.add_edge("SVM", "Kernel Methods", label="uses")
    G.add_edge("Unsupervised Learning", "Dimensionality Reduction", label="includes")
    G.add_edge("Dimensionality Reduction", "PCA", label="technique")
    G.add_edge("Neural Networks", "Kernel Methods", label="relates to")
    G.add_edge("Bayesian Inference", "Machine Learning Basics", label="foundation for")
    
    # Node descriptions for tooltips/reflections
    nx.set_node_attributes(G, {
        "Kernel Methods": "Higher dim insight: Lifts data for non-linear separation, like elevating studying.",
        "PCA": "Reduces dims while preserving variance – meditate on info loss."
    }, "description")
    
    return G

def add_user_inputs(G):
    while True:
        action = input("Add (n)ode, (e)dge, (s)ave, or (q)uit to plot? ").strip().lower()
        if action == 'q':
            break
        elif action == 'n':
            node = input("Enter new concept: ").strip()
            desc = input("Optional description/insight: ").strip()
            G.add_node(node)
            if desc:
                G.nodes[node]['description'] = desc
        elif action == 'e':
            node1 = input("From concept: ").strip()
            node2 = input("To concept: ").strip()
            label = input("Relationship label: ").strip()
            if node1 in G and node2 in G:
                G.add_edge(node1, node2, label=label)
            else:
                print("Nodes not found—add them first!")
        elif action == 's':
            save_graph(G)
        else:
            print("Invalid—try n, e, s, or q.")

def save_graph(G):
    data = nx.node_link_data(G)
    with open('data/graph.json', 'w') as f:
        json.dump(data, f)
    print("Graph saved to data/graph.json!")

def visualize_3d(G):
    pos = nx.spring_layout(G, dim=3)
    
    # Node positions
    node_x = [pos[node][0] for node in G.nodes()]
    node_y = [pos[node][1] for node in G.nodes()]
    node_z = [pos[node][2] for node in G.nodes()]
    node_labels = list(G.nodes())
    node_tooltips = [G.nodes[node].get('description', node) for node in G.nodes()]
    
    # Color by degree (higher degree = redder)
    node_degrees = [G.degree(node) for node in G.nodes()]
    node_colors = [f'rgb({int(255 * (d / max(node_degrees or [1])))}, 100, 100)' for d in node_degrees]
    
    # Edges
    edge_x, edge_y, edge_z = [], [], []
    for edge in G.edges():
        x0, y0, z0 = pos[edge[0]]
        x1, y1, z1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_z.extend([z0, z1, None])
    
    fig = go.Figure()
    
    # Edges
    fig.add_trace(go.Scatter3d(x=edge_x, y=edge_y, z=edge_z, mode='lines', line=dict(color='gray', width=2), hoverinfo='none'))
    
    # Nodes
    fig.add_trace(go.Scatter3d(
        x=node_x, y=node_y, z=node_z,
        mode='markers+text',
        marker=dict(size=10, color=node_colors, line=dict(width=2, color='darkblue')),
        text=node_labels, textposition='top center',
        hovertext=node_tooltips, hoverinfo='text'
    ))
    
    fig.update_layout(
        title="Interactive 3D DSML Concept Graph",
        scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z', aspectmode='cube'),
        width=800, height=600
    )
    fig.show()
    
    # Random reflection
    if G.edges():
        random_edge = random.choice(list(G.edges(data=True)))
        print(f"Meditation prompt: Reflect on how '{random_edge[0]}' {random_edge[2]['label']} '{random_edge[1]}' in higher dims.")

# Main run
if __name__ == "__main__":
    G = build_graph()
    add_user_inputs(G)
    visualize_3d(G)