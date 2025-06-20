from neo4j import GraphDatabase

# Configura tus credenciales de conexión
URI      = "neo4j+s://da91fa3e.databases.neo4j.io"
USER     = "neo4j"
PASSWORD = "P9k60EGJi8pb7d2zMlTkmW9aX4e5Zexz7aNy85yBn1A"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def query_top_10_longest_in_italy(tx):
    cypher = """
    MATCH (p:Jugador)-[r:TRASPASO]->(e:Equipo)
    WHERE r.fecha_inicio IS NOT NULL                
    WITH p, r,
      apoc.date.parse(r.fecha_inicio, 'ms', 'dd/MM/yyyy')     AS startMs,
      CASE
        WHEN r.fecha_fin STARTS WITH 'al presente' THEN timestamp()
        WHEN r.fecha_fin = '' THEN timestamp()
        ELSE apoc.date.parse(r.fecha_fin, 'ms', 'dd/MM/yyyy')
      END                                                     AS endMs
    WITH p,
         sum((endMs - startMs) / 1000 / 86400)                AS diasTotal
    RETURN
      p.Jugadores           AS jugador,
      diasTotal          AS diasEnLiga,
      round(diasTotal/365.0, 2) AS anosEnLiga
    ORDER BY diasTotal DESC
    LIMIT 10
    """
    return list(tx.run(cypher))

if __name__ == "__main__":
    with driver.session() as session:
        top10 = session.execute_read(query_top_10_longest_in_italy)
        print(f"{'Jugador':25s} {'Días en Serie A':>15s} {'Años en Serie A':>15s}")
        print("-" * 60)
        for rec in top10:
            print(f"{rec['jugador']:25s} {int(rec['diasEnLiga']):15d} {rec['anosEnLiga']:15.2f}")
    driver.close()
