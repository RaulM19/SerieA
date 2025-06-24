from neo4j import GraphDatabase

URI      = "neo4j+s://ad1c0800.databases.neo4j.io"
USER     = "neo4j"
PASSWORD = "jqXYhbQmS7Fu4lU31K8jbl2Gin8lQ8SXDLepnFjUdtM"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def query_top_transfer_active(tx, limit=10):
    cypher = """
    MATCH (e:Equipo)
    OPTIONAL MATCH (j:Jugador)-[:TRASPASO]->(e)
    WITH e.nombre AS equipo, count(j) AS totalTransfers
    RETURN equipo, totalTransfers
    ORDER BY totalTransfers DESC
    LIMIT $limit
    """
    return list(tx.run(cypher, {"limit": limit}))

if __name__ == "__main__":
    with driver.session() as session:
        results = session.execute_read(query_top_transfer_active, 10)
        print(f"{'Equipo':30s} | Total de traspasos")
        print("-" * 50)
        for r in results:
            print(f"{r['equipo']:30s} | {r['totalTransfers']:5d}")
    driver.close()
