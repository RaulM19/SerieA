from typing import Counter
from matplotlib import pyplot as plt
from neo4j import GraphDatabase

URI      = "neo4j+s://da91fa3e.databases.neo4j.io"
USER     = "neo4j"
PASSWORD = "P9k60EGJi8pb7d2zMlTkmW9aX4e5Zexz7aNy85yBn1A"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def build_most_expensive_433(tx):
    cypher = """
    CALL () {
      MATCH (j:Jugador)-[:JUEGA_EN]->(e:Equipo)
      WHERE j.posicion = 'Portero' 
        AND j.`Valor de mercado Num` IS NOT NULL 
        AND j.`Valor de mercado Num` <> '-'
        AND j.`Valor de mercado Num` <> ''
      WITH j, e ORDER BY toInteger(j.`Valor de mercado Num`) DESC
      LIMIT 1
      RETURN
        j.Jugadores AS nombre,
        j.posicion AS posicion,
        toInteger(j.`Valor de mercado Num`) AS valor,
        e.nombre AS equipo
      
      UNION ALL
      
      MATCH (j:Jugador)-[:JUEGA_EN]->(e:Equipo)
      WHERE j.posicion = 'Defensa central'
        AND j.`Valor de mercado Num` IS NOT NULL 
        AND j.`Valor de mercado Num` <> '-'
        AND j.`Valor de mercado Num` <> ''
      WITH j, e ORDER BY toInteger(j.`Valor de mercado Num`) DESC
      LIMIT 2
      RETURN
        j.Jugadores AS nombre,
        j.posicion AS posicion,
        toInteger(j.`Valor de mercado Num`) AS valor,
        e.nombre AS equipo
      
      UNION ALL
      
      MATCH (j:Jugador)-[:JUEGA_EN]->(e:Equipo)
      WHERE j.posicion = 'Lateral izquierdo'
        AND j.`Valor de mercado Num` IS NOT NULL 
        AND j.`Valor de mercado Num` <> '-'
        AND j.`Valor de mercado Num` <> ''
      WITH j, e ORDER BY toInteger(j.`Valor de mercado Num`) DESC
      LIMIT 1
      RETURN
        j.Jugadores AS nombre,
        j.posicion AS posicion,
        toInteger(j.`Valor de mercado Num`) AS valor,
        e.nombre AS equipo
      
      UNION ALL
      
      MATCH (j:Jugador)-[:JUEGA_EN]->(e:Equipo)
      WHERE j.posicion = 'Lateral derecho'
        AND j.`Valor de mercado Num` IS NOT NULL 
        AND j.`Valor de mercado Num` <> '-'
        AND j.`Valor de mercado Num` <> ''
      WITH j, e ORDER BY toInteger(j.`Valor de mercado Num`) DESC
      LIMIT 1
      RETURN
        j.Jugadores AS nombre,
        j.posicion AS posicion,
        toInteger(j.`Valor de mercado Num`) AS valor,
        e.nombre AS equipo
      
      UNION ALL
      
      MATCH (j:Jugador)-[:JUEGA_EN]->(e:Equipo)
      WHERE j.posicion IN ['Pivote','Mediocentro','Mediapunta','Mediocentro ofensivo']
        AND j.`Valor de mercado Num` IS NOT NULL 
        AND j.`Valor de mercado Num` <> '-'
        AND j.`Valor de mercado Num` <> ''
      WITH j, e ORDER BY toInteger(j.`Valor de mercado Num`) DESC
      LIMIT 1
      RETURN
        j.Jugadores AS nombre,
        j.posicion AS posicion,
        toInteger(j.`Valor de mercado Num`) AS valor,
        e.nombre AS equipo
      
      UNION ALL
      
      MATCH (j:Jugador)-[:JUEGA_EN]->(e:Equipo)
      WHERE j.posicion = 'Interior izquierdo'
        AND j.`Valor de mercado Num` IS NOT NULL 
        AND j.`Valor de mercado Num` <> '-'
        AND j.`Valor de mercado Num` <> ''
      WITH j, e ORDER BY toInteger(j.`Valor de mercado Num`) DESC
      LIMIT 1
      RETURN
        j.Jugadores AS nombre,
        j.posicion AS posicion,
        toInteger(j.`Valor de mercado Num`) AS valor,
        e.nombre AS equipo
      
      UNION ALL
      
      MATCH (j:Jugador)-[:JUEGA_EN]->(e:Equipo)
      WHERE j.posicion = 'Interior derecho'
        AND j.`Valor de mercado Num` IS NOT NULL 
        AND j.`Valor de mercado Num` <> '-'
        AND j.`Valor de mercado Num` <> ''
      WITH j, e ORDER BY toInteger(j.`Valor de mercado Num`) DESC
      LIMIT 1
      RETURN
        j.Jugadores AS nombre,
        j.posicion AS posicion,
        toInteger(j.`Valor de mercado Num`) AS valor,
        e.nombre AS equipo
      
      UNION ALL
      
      MATCH (j:Jugador)-[:JUEGA_EN]->(e:Equipo)
      WHERE j.posicion = 'Extremo izquierdo'
        AND j.`Valor de mercado Num` IS NOT NULL 
        AND j.`Valor de mercado Num` <> '-'
        AND j.`Valor de mercado Num` <> ''
      WITH j, e ORDER BY toInteger(j.`Valor de mercado Num`) DESC
      LIMIT 1
      RETURN
        j.Jugadores AS nombre,
        j.posicion AS posicion,
        toInteger(j.`Valor de mercado Num`) AS valor,
        e.nombre AS equipo
      
      UNION ALL
      
      MATCH (j:Jugador)-[:JUEGA_EN]->(e:Equipo)
      WHERE j.posicion = 'Extremo derecho'
        AND j.`Valor de mercado Num` IS NOT NULL 
        AND j.`Valor de mercado Num` <> '-'
        AND j.`Valor de mercado Num` <> ''
      WITH j, e ORDER BY toInteger(j.`Valor de mercado Num`) DESC
      LIMIT 1
      RETURN
        j.Jugadores AS nombre,
        j.posicion AS posicion,
        toInteger(j.`Valor de mercado Num`) AS valor,
        e.nombre AS equipo
      
      UNION ALL
      
      MATCH (j:Jugador)-[:JUEGA_EN]->(e:Equipo)
      WHERE j.posicion = 'Delantero centro'
        AND j.`Valor de mercado Num` IS NOT NULL 
        AND j.`Valor de mercado Num` <> '-'
        AND j.`Valor de mercado Num` <> ''
      WITH j, e ORDER BY toInteger(j.`Valor de mercado Num`) DESC
      LIMIT 1
      RETURN
        j.Jugadores AS nombre,
        j.posicion AS posicion,
        toInteger(j.`Valor de mercado Num`) AS valor,
        e.nombre AS equipo
    }
    WITH collect({nombre:nombre, posicion:posicion, valor:valor, equipo:equipo}) AS squad
    WITH squad,
         reduce(total = 0, x IN squad | total + x.valor) AS totalValue
    UNWIND squad AS p
    RETURN
      p.nombre   AS jugador,
      p.posicion AS posicion,
      p.valor    AS valor,
      p.equipo   AS equipo,
      totalValue AS valorTotal
    ORDER BY
      CASE p.posicion
        WHEN 'Portero'                        THEN 1
        WHEN 'Lateral izquierdo'             THEN 2
        WHEN 'Lateral derecho'               THEN 3
        WHEN 'Defensa central'               THEN 4
        WHEN 'Pivote'                        THEN 5
        WHEN 'Mediocentro'                   THEN 5
        WHEN 'Mediapunta'                    THEN 5
        WHEN 'Mediocentro ofensivo'          THEN 5
        WHEN 'Interior izquierdo'            THEN 6
        WHEN 'Interior derecho'              THEN 7
        WHEN 'Extremo izquierdo'             THEN 8
        WHEN 'Delantero centro'              THEN 9
        WHEN 'Extremo derecho'               THEN 10
        ELSE 11
      END
    """
    return list(tx.run(cypher))

if __name__ == "__main__":
    with driver.session() as session:
        team = session.execute_read(build_most_expensive_433)
        print(f"{'Jugador':25s} {'Posición':25s} {'Equipo':20s} {'Valor (€)':>12s} {'Total (€)':>12s}")
        print("-"*120)
        for row in team:
            jugador = row['jugador'] or 'N/A'
            posicion = row['posicion'] or 'N/A'
            equipo = row['equipo'] or 'N/A'
            valor = row['valor'] or 0
            valorTotal = row['valorTotal'] or 0
            print(f"{jugador:25s} {posicion:25s} {equipo:20s} "
                  f"{valor:12,} {valorTotal:12,}")
    driver.close()

# Contar cuántos jugadores de cada equipo
teams = [row["equipo"] for row in team]
counts = Counter(teams)
total_players = len(teams)  # debería ser 11

# Calcular porcentaje por equipo
labels = list(counts.keys())
percentages = [counts[t] / total_players * 100 for t in labels]

# Graficar
plt.figure(figsize=(8, 6))
bars = plt.bar(labels, percentages, color='skyblue')
plt.xticks(rotation=45, ha='right')
plt.ylabel('Porcentaje del 11 ideal (%)')
plt.title('Distribución de jugadores por equipo en el 11 ideal más caro')

# Anotar porcentajes encima de cada barra
for bar, pct in zip(bars, percentages):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
             f'{pct:.1f}%', ha='center', va='bottom')

plt.tight_layout()
plt.show()