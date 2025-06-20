# pip install neo4j networkx python-louvain matplotlib

from neo4j import GraphDatabase
import networkx as nx
import community.community_louvain as community_louvain
import matplotlib.pyplot as plt

# 1. Leer aristas de transferencia con peso
URI      = "neo4j+s://da91fa3e.databases.neo4j.io"
USER     = "neo4j"
PASSWORD = "P9k60EGJi8pb7d2zMlTkmW9aX4e5Zexz7aNy85yBn1A"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def fetch_edges(tx):
    return tx.run("""
    MATCH (e1:Equipo)<-[:TRASPASO]-(j:Jugador)-[:TRASPASO]->(e2:Equipo)
    WHERE e1.nombre < e2.nombre
    RETURN e1.nombre AS source, e2.nombre AS target, count(DISTINCT j) AS weight
    """).data()

with driver.session() as sess:
    edges = sess.read_transaction(fetch_edges)
driver.close()

# 2. Montar grafo NetworkX
G = nx.Graph()
for r in edges:
    G.add_edge(r['source'], r['target'], weight=r['weight'])

# 3. Detectar comunidades (Louvain)
partition = community_louvain.best_partition(G, weight='weight')

# 4. Métrica global de modularidad
modularity = community_louvain.modularity(partition, G, weight='weight')
print(f"Modularidad global: {modularity:.4f}\n")

# 5. Construir dict comunidades → nodos
communities = {}
for node, comm in partition.items():
    communities.setdefault(comm, []).append(node)

# 6. Calcular métricas por comunidad
print("Comunidad | Tamaño | Peso interno |  Peso externo |  Ratio interno")
for comm, nodes in communities.items():
    intra = 0
    inter = 0
    for u, v, data in G.edges(data=True):
        w = data.get('weight',1)
        if partition[u] == comm == partition[v]:
            intra += w
        elif partition[u] == comm or partition[v] == comm:
            inter += w
    size = len(nodes)
    ratio = intra/(intra+inter) if (intra+inter)>0 else 0
    print(f"{comm:9d} | {size:6d} | {intra:12d} | {inter:13d} | {ratio:13.2f}")

print()

# 7. Dibujar con colores según comunidad
pos = nx.spring_layout(G, seed=42)
cmap = plt.get_cmap('tab20')
fig, ax = plt.subplots(figsize=(8,8))
for comm, nodes in communities.items():
    nx.draw_networkx_nodes(
        G, pos,
        nodelist=nodes,
        node_color=[cmap(comm)],
        label=f'Comunidad {comm}',
        node_size=300,
        ax=ax
    )
nx.draw_networkx_edges(G, pos, alpha=0.3, ax=ax)
nx.draw_networkx_labels(G, pos, font_size=8, ax=ax)
ax.axis('off')
ax.legend()
plt.show()
