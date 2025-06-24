# Serie A Graph Analysis – README

Bienvenido al repositorio **“Serie A”**, un estudio de la liga italiana de fútbol modelado en Neo4j y analizado con Python.  
Aquí encontrarás los datos históricos, el modelo de grafo y un conjunto de consultas listas para ejecutar.

---

## Requisitos

| Herramienta | Versión recomendada |
|-------------|--------------------|
| Python      | ≥ 3.10             |
| Neo4j       | 5.x (Desktop o Aura) |
| pip         | ≥ 21               |

Instalación mínima de dependencias:

```bash
pip install neo4j
```

> Para visualizar grafos instala también  
> `pip install networkx matplotlib python-louvain`.

## Ejecutar las consultas

Cada archivo en `scripts/` es independiente. Por ejemplo, para detectar comunidades:

```bash
python scripts/louvain_community.py
```

Los resultados se imprimen en consola y, si instalaste los paquetes opcionales, se mostrará un gráfico con las comunidades.