from neo4j import GraphDatabase

# Datos de conexión
URI      = "neo4j+s://da91fa3e.databases.neo4j.io"
USER     = "neo4j"
PASSWORD = "P9k60EGJi8pb7d2zMlTkmW9aX4e5Zexz7aNy85yBn1A"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def query_top3_value_pct(tx):
    cypher = """
    MATCH (e:Equipo)<-[:JUEGA_EN]-(j:Jugador)
    WHERE j.`Valor de mercado Num` IS NOT NULL
      AND j.`Valor de mercado Num` <> ''
      AND j.`Valor de mercado Num` <> '-'
    WITH e, toInteger(j.`Valor de mercado Num`) AS v
    ORDER BY e.nombre, v DESC
    WITH e.nombre AS equipo, collect(v) AS valores
    WITH
      equipo,
      reduce(total = 0, x IN valores | total + x) AS totalValue,
      CASE
        WHEN size(valores) >= 3
        THEN valores[0] + valores[1] + valores[2]
        ELSE reduce(s = 0, x IN valores | s + x)
      END AS top3Value
    RETURN
      equipo,
      totalValue,
      top3Value,
      round(100.0 * top3Value / totalValue, 2) AS pctTop3
    ORDER BY pctTop3 DESC
    """
    return list(tx.run(cypher))

if __name__ == "__main__":
    with driver.session() as session:
        results = session.execute_read(query_top3_value_pct)
        print(f"{'Equipo':25s} {'Total (€)':>12s} {'Top 3 (€)':>12s} {'% Top 3':>8s}")
        print("-" * 60)
        for r in results:
            equipo     = r["equipo"]
            total      = r["totalValue"]
            top3       = r["top3Value"]
            pct_top3   = r["pctTop3"]
            print(f"{equipo:25s} {total:12,} {top3:12,} {pct_top3:8.2f}%")
    driver.close()
