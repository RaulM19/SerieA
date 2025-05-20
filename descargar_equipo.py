import pandas as pd

equipos = pd.read_csv("equipos.csv")
equipos_lista = [e.strip().lower() for e in equipos["nombre"].tolist()]
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/125.0 Safari/537.36"}

for nombre_web in equipos["nombre_web"]:
    nombre_web = nombre_web.strip()
    url = f"https://www.worldfootball.net/teams/{nombre_web}/11/"
    try:
        tablas = pd.read_html(url, header=0, storage_options=headers)
        df = pd.concat(tablas, ignore_index=True)
        # Filtrar filas donde alguna celda contiene el nombre de algún equipo de equipos_lista
        mask = df.apply(
            lambda row: any(
                any(equipo in str(cell).strip().lower() for equipo in equipos_lista)
                for cell in row
            ),
            axis=1
        )
        df_filtrado = df[mask]
        df_filtrado.to_csv(f"{nombre_web}_h2h.csv", index=False, encoding="utf-8")
        print(f"Descargado: {nombre_web}")
    except Exception as e:
        print(f"Error con {nombre_web}: {e}")