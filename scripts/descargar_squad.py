# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# import re 

# # 1. CONFIGURACIÓN
# url = 'https://www.transfermarkt.es/inter-mailand/startseite/verein/46/saison_id/2024'
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
# }

# # 2. OBTENER HTML
# try:
#     response = requests.get(url, headers=headers)
#     response.raise_for_status()
# except requests.exceptions.RequestException as e:
#     print(f"Error HTTP: {e}")
#     exit()

# # 3. ANALIZAR HTML
# soup = BeautifulSoup(response.content, 'html.parser')

# # 4. ENCONTRAR Y EXTRAER LA TABLA DE JUGADORES
# player_table = soup.find('table', class_='items')

# if player_table:
#     try:
#         dfs = pd.read_html(str(player_table), header=0)
#         if dfs:
#             df = dfs[0]
#             if '#' in df.columns:
#                 df = df.dropna(subset=['#']) 
#             if 'Valor de mercado' in df.columns:
#                 def limpiar_valor_mercado(valor):
#                     if pd.isna(valor) or valor == '-':
#                         return None
#                     valor_str = str(valor).replace('€', '').strip()
#                     multiplicador = 1
#                     if 'mill.' in valor_str:
#                         multiplicador = 1000000
#                         valor_str = valor_str.replace('mill.', '')
#                     elif 'mil' in valor_str: # Para "mil €"
#                         multiplicador = 1000
#                         valor_str = valor_str.replace('mil', '')
                    
#                     valor_str = valor_str.replace(',', '.').strip() # Reemplazar coma decimal por punto
#                     try:
#                         return float(valor_str) * multiplicador
#                     except ValueError:
#                         return None # Si no se puede convertir, devolver None

#                 df['Valor de mercado Numerico'] = df['Valor de mercado'].apply(limpiar_valor_mercado)
#             # 6. GUARDAR DATOS
#             df.to_csv('datos_inter_milan_2024.csv', index=False, encoding='utf-8-sig')
#             print("Datos descargados y guardados en 'datos_inter_milan_2024.csv'")
#             print("\nPrimeras filas de los datos extraídos:")
#             print(df.head())
#         else:
#             print("Pandas no pudo encontrar/parsear la tabla.")
#     except Exception as e:
#         print(f"Error al procesar la tabla con pandas: {e}")
# else:
#     print("No se encontró la tabla de jugadores. Verifica la clase 'items' o la estructura de la página.")

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time   # para ser buen vecino y no abrumar al servidor

# ---------- 1. CONFIGURACIÓN GENERAL ----------
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )
}

# Diccionario {nombre_para_archivo: url_de_transfermarkt}
equipos = {
    "ssc-napoli" :  "https://www.transfermarkt.es/ssc-neapel/startseite/verein/6195/saison_id/2024",
    "inter" : "https://www.transfermarkt.es/inter-mailand/startseite/verein/46/saison_id/2024",
    "atalanta" : "https://www.transfermarkt.es/atalanta-bergamo/startseite/verein/800/saison_id/2024",
    "juventus" : "https://www.transfermarkt.es/juventus-turin/startseite/verein/506/saison_id/2024",
    "as-roma" : "https://www.transfermarkt.es/as-rom/startseite/verein/12/saison_id/2024",
    "lazio-roma" : "https://www.transfermarkt.es/lazio-rom/startseite/verein/398/saison_id/2024",
    "acf-fiorentina" : "https://www.transfermarkt.es/ac-florenz/startseite/verein/430/saison_id/2024",
    "bologna-fc" : "https://www.transfermarkt.es/fc-bologna/startseite/verein/1025/saison_id/2024",
    "ac-milan" : "https://www.transfermarkt.es/ac-mailand/startseite/verein/5/saison_id/2024",
    "como-1907" : "https://www.transfermarkt.es/como-1907/startseite/verein/1047/saison_id/2024",
    "torino-fc" : "https://www.transfermarkt.es/fc-turin/startseite/verein/416/saison_id/2024",
    "udinese-calcio" : "https://www.transfermarkt.es/udinese-calcio/startseite/verein/410/saison_id/2024",
    "genoa-cfc" : "https://www.transfermarkt.es/genua-cfc/startseite/verein/252/saison_id/2024",
    "cagliari-calcio" : "https://www.transfermarkt.es/cagliari-calcio/startseite/verein/1390/saison_id/2024",
    "hellas-verona" : "https://www.transfermarkt.es/hellas-verona/startseite/verein/276/saison_id/2024",
    "parma-calcio-1913" : "https://www.transfermarkt.es/parma-calcio-1913/startseite/verein/130/saison_id/2024",
    "empoli-fc" : "https://www.transfermarkt.es/fc-empoli/startseite/verein/749/saison_id/2024",
    "us-lecce" : "https://www.transfermarkt.es/us-lecce/startseite/verein/1005/saison_id/2024",
    "venezia-fc" : "https://www.transfermarkt.es/venezia-fc/startseite/verein/607/saison_id/2024",
    "ac-monza" : "https://www.transfermarkt.es/ac-monza/startseite/verein/2919/saison_id/2024"
}

# ---------- 2. FUNCIÓN REUTILIZABLE ----------
def scrape_transfermarkt(url: str) -> pd.DataFrame:
    """Devuelve un DataFrame con la tabla de jugadores y valor numérico."""
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.content, "html.parser")
    table = soup.find("table", class_="items")
    if table is None:
        raise ValueError("No se encontró la tabla con clase 'items'.")

    df = pd.read_html(str(table), header=0)[0]

    # Algunos equipos tienen filas de subtítulos vacías; filtramos las que no tengan dorsal
    if "#" in df.columns:
        df = df.dropna(subset=["#"])

    # Limpieza del valor de mercado
    def limpiar_valor_mercado(valor):
        if pd.isna(valor) or valor == "-":
            return None
        txt = str(valor).replace("€", "").strip()
        mult = 1
        if "mill." in txt:
            mult, txt = 1_000_000, txt.replace("mill.", "")
        elif "mil" in txt:
            mult, txt = 1_000, txt.replace("mil", "")
        txt = txt.replace(",", ".").strip()
        try:
            return float(txt) * mult
        except ValueError:
            return None

    if "Valor de mercado" in df.columns:
        df["Valor de mercado Num"] = df["Valor de mercado"].apply(limpiar_valor_mercado)

    return df

# ---------- 3. ITERAR Y GUARDAR ----------
for nombre_archivo, url in equipos.items():
    try:
        print(f"Descargando datos de {nombre_archivo}…")
        datos = scrape_transfermarkt(url)
        csv_path = f"datos_{nombre_archivo}.csv"
        datos.to_csv(csv_path, index=False, encoding="utf-8-sig")
        print(f"  ✓ Guardado en {csv_path} (filas: {len(datos)})")
    except Exception as e:
        print(f"  ✗ Error con {nombre_archivo}: {e}")

    # Pausa de cortesía: evita bloqueos por scraping agresivo
    time.sleep(3)

print("\nProceso terminado.")
