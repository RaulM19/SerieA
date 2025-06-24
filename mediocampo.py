from neo4j import GraphDatabase

# Datos de conexión
URI      = "neo4j+s://ad1c0800.databases.neo4j.io"
USER     = "neo4j"
PASSWORD = "jqXYhbQmS7Fu4lU31K8jbl2Gin8lQ8SXDLepnFjUdtM"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def query_top_midfield_spender(tx):
    cypher = """
    MATCH (e:Equipo)<-[:JUEGA_EN]-(j:Jugador)
    WHERE j.posicion IN [
      'Pivote',
      'Mediocentro',
      'Interior izquierdo',
      'Interior derecho',
      'Mediapunta',
      'Mediocentro ofensivo'
    ]
    WITH e.nombre AS equipo, sum(toInteger(j.`Valor de mercado Num`)) AS gastoMediocampo
    RETURN equipo, gastoMediocampo
    ORDER BY gastoMediocampo DESC
    LIMIT 1
    """
    return tx.run(cypher).single()

if __name__ == "__main__":
    with driver.session() as session:
        record = session.execute_read(query_top_midfield_spender)
        if record:
            equipo = record["equipo"]
            gasto  = record["gastoMediocampo"]
            print(f"Equipo que más gasta en mediocampo: {equipo} (€{gasto:,})")
        else:
            print("No se encontraron datos de gasto en mediocampo.")
    driver.close()
