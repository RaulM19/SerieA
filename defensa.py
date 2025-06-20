from neo4j import GraphDatabase

# Datos de conexión
URI      = "neo4j+s://da91fa3e.databases.neo4j.io"
USER     = "neo4j"
PASSWORD = "P9k60EGJi8pb7d2zMlTkmW9aX4e5Zexz7aNy85yBn1A"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def query_top_defensive_spender(tx):
    cypher = """
    MATCH (e:Equipo)<-[:JUEGA_EN]-(j:Jugador)
    WHERE j.posicion IN ['Portero','Defensa central','Lateral izquierdo','Lateral derecho']
    WITH e.nombre AS equipo, sum(toInteger(j.`Valor de mercado Num`)) AS gastoDefensa
    RETURN equipo, gastoDefensa
    ORDER BY gastoDefensa DESC
    LIMIT 1
    """
    return tx.run(cypher).single()

if __name__ == "__main__":
    with driver.session() as session:
        record = session.execute_read(query_top_defensive_spender)
        if record:
            equipo = record["equipo"]
            gasto  = record["gastoDefensa"]
            print(f"Equipo que más gasta en defensa: {equipo} (€{gasto:,})")
        else:
            print("No se encontraron datos de gasto en defensa.")
    driver.close()
