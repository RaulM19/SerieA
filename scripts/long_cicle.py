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

def query_longest_positive_correct(tx):
    # ESTA ES LA SINTAXIS VÁLIDA Y EFICIENTE
    cypher = """
    MATCH p = (e1:Equipo)-[:VS*3..3 {esVictoria: true}]->(e1)

    WHERE size(nodes(p)) = 4 AND size(apoc.coll.toSet(nodes(p))) = 3

    WITH p

    RETURN
    [n IN nodes(p) | n.nombre] AS equipos,
    [rel IN relationships(p) | toInteger(rel.Ganados) - toInteger(rel.Perdidos)] AS diffs,
    length(p) AS pasos;
    """
    return list(tx.run(cypher))

# El código para ejecutarla no cambia
with driver.session() as session:
    # Asegúrate de que estás en una sesión de escritura si necesitas correr el Paso 1
    # session.execute_write(...) 
    for record in session.execute_read(query_longest_positive_correct):
        print(record["equipos"], record["diffs"], record["pasos"])