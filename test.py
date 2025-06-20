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

def query_longest_positive(tx):
    cypher = """
    MATCH p = (e1:Equipo)-[rs:VS*1..19]->(eN)
    WHERE ALL(r IN rs WHERE toInteger(r.Ganados) > toInteger(r.Perdidos))
      AND size(nodes(p)) = size(apoc.coll.toSet(nodes(p)))
    WITH p
    ORDER BY length(p) DESC
    LIMIT 1
    RETURN
      [n IN nodes(p) | n.nombre] AS equipos,
      [r IN relationships(p) | toInteger(r.Ganados) - toInteger(r.Perdidos)] AS diffs,
      length(p) AS pasos;
    """
    return list(tx.run(cypher))

with driver.session() as session:
    for record in session.execute_read(query_longest_positive):
        print(record["equipos"], record["diffs"], record["pasos"])