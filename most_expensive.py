from neo4j import GraphDatabase


# Replace with the actual URI, username and password
AURA_CONNECTION_URI = "neo4j+s://da91fa3e.databases.neo4j.io"
AURA_USERNAME = "neo4j"
AURA_PASSWORD = "P9k60EGJi8pb7d2zMlTkmW9aX4e5Zexz7aNy85yBn1A"

# Driver instantiation
driver = GraphDatabase.driver(
    AURA_CONNECTION_URI,
    auth=(AURA_USERNAME, AURA_PASSWORD)
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
