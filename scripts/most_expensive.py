from neo4j import GraphDatabase


# Replace with the actual URI, username and password
URI      = "neo4j+s://ad1c0800.databases.neo4j.io"
USER     = "neo4j"
PASSWORD = "jqXYhbQmS7Fu4lU31K8jbl2Gin8lQ8SXDLepnFjUdtM"

# Driver instantiation
driver = GraphDatabase.driver(
    URI,
    auth=(USER, PASSWORD)
)

driver.verify_connectivity()

def query_most_expensive_roster(tx):
    cypher = """
    MATCH (e:Equipo)<-[:JUEGA_EN]-(j:Jugador)
    WITH e.nombre AS equipo, sum(toInteger(j.`Valor de mercado Num`)) AS valorPlantilla
    RETURN equipo, valorPlantilla
    ORDER BY valorPlantilla DESC
    LIMIT 1
    """
    return tx.run(cypher).single()

with driver.session() as session:
    record = session.execute_read(query_most_expensive_roster)
    if record:
        equipo = record["equipo"]
        valor  = record["valorPlantilla"]
        print(f"Equipo con plantilla más cara: {equipo} (Valor total: €{valor:,})")
    else:
        print("No se encontró ningún equipo con plantilla.")
