from neo4j import GraphDatabase

# Datos de conexión
URI      = "neo4j+s://ad1c0800.databases.neo4j.io"
USER     = "neo4j"
PASSWORD = "jqXYhbQmS7Fu4lU31K8jbl2Gin8lQ8SXDLepnFjUdtM"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def query_top_offensive_spender(tx):
    cypher = """
    MATCH (e:Equipo)<-[:JUEGA_EN]-(j:Jugador)
    WHERE j.posicion IN ['Extremo izquierdo','Extremo derecho','Delantero centro']
    WITH e.nombre AS equipo, sum(toInteger(j.`Valor de mercado Num`)) AS gastoAtaque
    RETURN equipo, gastoAtaque
    ORDER BY gastoAtaque DESC
    LIMIT 1
    """
    return tx.run(cypher).single()

if __name__ == "__main__":
    with driver.session() as session:
        record = session.execute_read(query_top_offensive_spender)
        if record:
            equipo = record["equipo"]
            gasto  = record["gastoAtaque"]
            print(f"Equipo que más gasta en ataque: {equipo} (€{gasto:,})")
        else:
            print("No se encontraron datos de gasto en ataque.")
    driver.close()
