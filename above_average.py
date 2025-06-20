from neo4j import GraphDatabase
import matplotlib.pyplot as plt

# Conexión a Neo4j
URI      = "neo4j+s://da91fa3e.databases.neo4j.io"
USER     = "neo4j"
PASSWORD = "P9k60EGJi8pb7d2zMlTkmW9aX4e5Zexz7aNy85yBn1A"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

# Consultas Cypher
query_avg = """
MATCH (e:Equipo)<-[:JUEGA_EN]-(j:Jugador)
WITH e, sum(toInteger(j.`Valor de mercado Num`)) AS valorPlantilla
RETURN avg(valorPlantilla) AS avgValor
"""

query_above = """
CALL {
  MATCH (e:Equipo)<-[:JUEGA_EN]-(j:Jugador)
  WITH e, sum(toInteger(j.`Valor de mercado Num`)) AS valorPlantilla
  RETURN avg(valorPlantilla) AS avgValor
}
MATCH (e:Equipo)<-[:JUEGA_EN]-(j:Jugador)
WITH e.nombre AS equipo, sum(toInteger(j.`Valor de mercado Num`)) AS valorPlantilla, avgValor
WHERE valorPlantilla > avgValor
RETURN equipo, valorPlantilla
ORDER BY valorPlantilla DESC
"""

# Ejecutar consultas
with driver.session() as session:
    avg_valor = session.execute_read(lambda tx: tx.run(query_avg).single()["avgValor"])
    above_records = session.execute_read(lambda tx: tx.run(query_above).data())

driver.close()

# Preparar datos para graficar
equipos = [rec["equipo"] for rec in above_records]
valores = [rec["valorPlantilla"] for rec in above_records]

# Graficar
plt.figure(figsize=(10, 6))
plt.bar(equipos, valores)
plt.axhline(avg_valor, linestyle='--', label=f'Promedio: €{int(avg_valor):,}')
plt.xticks(rotation=45, ha='right')
plt.ylabel('Valor de la plantilla (€)')
plt.title('Equipos con valor de plantilla por encima del promedio')
plt.legend()
plt.tight_layout()
plt.show()