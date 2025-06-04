#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Recorre la plantilla de todos los clubes listados en el dict 'equipos',
y genera un CSV con las filas:
    nombre_equipo, nombre_jugador, fecha_inicio, fecha_fin
Solamente se incluyen las etapas que coincidan con alguno de los clubes del CSV de entrada.
"""

from __future__ import annotations
from typing import List, Dict, Tuple
import csv, re, unicodedata, time
from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --------------------------------------------------------------------------- #
# Diccionario con slug → URL fija de plantilla (kader) temporada 2024/25
# --------------------------------------------------------------------------- #
equipos: dict[str, str] = {
    "ssc-napoli":      "https://www.transfermarkt.es/ssc-neapel/startseite/verein/6195/saison_id/2024",
    "inter":           "https://www.transfermarkt.es/inter-mailand/startseite/verein/46/saison_id/2024",
    "atalanta":        "https://www.transfermarkt.es/atalanta-bergamo/startseite/verein/800/saison_id/2024",
    "juventus":        "https://www.transfermarkt.es/juventus-turin/startseite/verein/506/saison_id/2024",
    "as-roma":         "https://www.transfermarkt.es/as-rom/startseite/verein/12/saison_id/2024",
    "lazio-roma":      "https://www.transfermarkt.es/lazio-rom/startseite/verein/398/saison_id/2024",
    "acf-fiorentina":  "https://www.transfermarkt.es/ac-florenz/startseite/verein/430/saison_id/2024",
    "bologna-fc":      "https://www.transfermarkt.es/fc-bologna/startseite/verein/1025/saison_id/2024",
    "ac-milan":        "https://www.transfermarkt.es/ac-mailand/startseite/verein/5/saison_id/2024",
    "como-1907":       "https://www.transfermarkt.es/como-1907/startseite/verein/1047/saison_id/2024",
    "torino-fc":       "https://www.transfermarkt.es/fc-turin/startseite/verein/416/saison_id/2024",
    "udinese-calcio":  "https://www.transfermarkt.es/udinese-calcio/startseite/verein/410/saison_id/2024",
    "genoa-cfc":       "https://www.transfermarkt.es/genua-cfc/startseite/verein/252/saison_id/2024",
    "cagliari-calcio": "https://www.transfermarkt.es/cagliari-calcio/startseite/verein/1390/saison_id/2024",
    "hellas-verona":   "https://www.transfermarkt.es/hellas-verona/startseite/verein/276/saison_id/2024",
    "parma-calcio-1913":"https://www.transfermarkt.es/parma-calcio-1913/startseite/verein/130/saison_id/2024",
    "empoli-fc":       "https://www.transfermarkt.es/fc-empoli/startseite/verein/749/saison_id/2024",
    "us-lecce":        "https://www.transfermarkt.es/us-lecce/startseite/verein/1005/saison_id/2024",
    "venezia-fc":      "https://www.transfermarkt.es/venezia-fc/startseite/verein/607/saison_id/2024",
    "ac-monza":        "https://www.transfermarkt.es/ac-monza/startseite/verein/2919/saison_id/2024"
}

HEADLESS   = True
CSV_PATH   = "equipos.csv"   # Debe contener: nombre, nombre_original, nombre_web
WAIT_SECS  = 15
OUTPUT_CSV = "resultado_fichajes.csv"

# --------------------------------------------------------------------------- #
# Selenium – abrir navegador
# --------------------------------------------------------------------------- #
def open_browser() -> webdriver.Chrome:
    opts = webdriver.ChromeOptions()
    if HEADLESS:
        opts.add_argument("--headless=new")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1920,1080")
    opts.add_argument("--log-level=3")
    return webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=opts,
    )

# --------------------------------------------------------------------------- #
# Cargar CSV de equipos → extraer mapping(normalizado → nombre_original)
# --------------------------------------------------------------------------- #
def normaliza(txt: str) -> str:
    txt = unicodedata.normalize("NFKD", txt).encode("ascii", "ignore").decode()
    txt = txt.lower()
    txt = re.sub(r"\b(ssc?|ac|as|us|fc|cfc|calcio|roma|1907|1913)\b", "", txt)
    txt = re.sub(r"[^a-z0-9]", " ", txt)
    return re.sub(r"\s+", " ", txt).strip()

def cargar_equipos(path: str = CSV_PATH) -> dict[str, str]:
    """
    Lee 'equipos.csv' con columnas: nombre, nombre_original, nombre_web
    Devuelve:
        mapping: dict donde
            key = normaliza(nombre_original)
            value = nombre_original
    """
    mapa: dict[str, str] = {}
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            nom_orig = row["nombre_original"].strip()
            clave = normaliza(nom_orig)
            mapa[clave] = nom_orig
    return mapa

# --------------------------------------------------------------------------- #
# Patrón para extraer jugadores de la plantilla
# --------------------------------------------------------------------------- #
PAT_PLAYER = re.compile(r'href="(/([\w\-]+)/profil/spieler/(\d+))"')

def plantilla(html: str) -> List[Dict[str, str]]:
    jugadores: List[Dict[str, str]] = []
    for _rel, slug, pid in PAT_PLAYER.findall(html):
        jugadores.append(
            {
                "id": int(pid),
                "slug": slug,
                "name": slug.replace("-", " ").title(),
                "transfers_url": f"https://www.transfermarkt.it/{slug}/transfers/spieler/{pid}",
            }
        )
    return jugadores

# --------------------------------------------------------------------------- #
# Parsear historial de fichajes
# --------------------------------------------------------------------------- #
def parse_transfer_history(html: str) -> List[Dict[str, str]]:
    soup = BeautifulSoup(html, "lxml")
    rows = soup.select(".tm-transfer-history.box .tm-player-transfer-history-grid")
    out: List[Dict[str, str]] = []
    for r in rows:
        season   = r.select_one(".tm-player-transfer-history-grid__season")
        date_el  = r.select_one(".tm-player-transfer-history-grid__date")
        old_club = r.select_one(
            ".tm-player-transfer-history-grid__old-club .tm-player-transfer-history-grid__club-link"
        )
        new_club = r.select_one(
            ".tm-player-transfer-history-grid__new-club .tm-player-transfer-history-grid__club-link"
        )
        if season and date_el and old_club and new_club:
            out.append({
                "season": season.text.strip(),
                "date":   date_el.text.strip(),   # ej. '09/lug/2024'
                "from":   old_club.text.strip(),
                "to":     new_club.text.strip(),
            })
    return out

# --------------------------------------------------------------------------- #
# Convertir fechas italianas a datetime
# --------------------------------------------------------------------------- #
MES_IT = {
    "gen": "01", "feb": "02", "mar": "03", "apr": "04",
    "mag": "05", "giu": "06", "lug": "07", "ago": "08",
    "set": "09", "ott": "10", "nov": "11", "dic": "12",
}

def fecha_it_a_iso(fecha: str) -> datetime:
    d, m, y = fecha.split("/")
    m_num = m if m.isdigit() else MES_IT[m.lower()]
    return datetime.strptime(f"{d}/{m_num}/{y}", "%d/%m/%Y")

# --------------------------------------------------------------------------- #
# Generar intervalos: club, fecha inicio, fecha fin
# --------------------------------------------------------------------------- #
def etapas(hist: List[Dict[str, str]]) -> List[Tuple[str, str, str]]:
    asc = list(reversed(hist))   # antiguo → reciente
    out: List[Tuple[str, str, str]] = []
    for i, mv in enumerate(asc):
        club = mv["to"]
        ini  = fecha_it_a_iso(mv["date"]).strftime("%d/%m/%Y")
        fin  = (
            fecha_it_a_iso(asc[i + 1]["date"]).strftime("%d/%m/%Y")
            if i + 1 < len(asc)
            else "al presente"
        )
        out.append((club, ini, fin))
    return out

# --------------------------------------------------------------------------- #
# MAIN – Generar CSV de fichajes
# --------------------------------------------------------------------------- #
def main() -> None:
    # 1) Cargo el mapping normalizado → nombre_original
    mapping_equipos = cargar_equipos()

    # 2) Abrir navegador
    driver = open_browser()

    # 3) Abrir archivo de salida y escribir encabezado
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as fw:
        writer = csv.writer(fw)
        writer.writerow(["nombre_equipo", "nombre_jugador", "fecha_inicio", "fecha_fin"])

        # 4) Iterar sobre cada club según el dict ‘equipos’
        for slug, squad_url in equipos.items():
            print(f"\nProcesando plantilla de: {slug}")
            driver.get(squad_url)

            # Esperar a que cargue la tabla de plantilla (id="yw1")
            WebDriverWait(driver, WAIT_SECS).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#yw1"))
            )

            # 5) Extraer jugadores de la plantilla
            jugadores = plantilla(driver.page_source)
            for p in jugadores:
                driver.get(p["transfers_url"])

                # Esperar a que cargue el historial de transferencias
                WebDriverWait(driver, WAIT_SECS).until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR,
                         ".tm-transfer-history.box .tm-player-transfer-history-grid")
                    )
                )

                hist = parse_transfer_history(driver.page_source)
                if not hist:
                    continue

                # 6) Revisar cada etapa: si coincide, escribir en CSV
                for club, ini, fin in etapas(hist):
                    norm_club = normaliza(club)
                    if norm_club in mapping_equipos:
                        nombre_equipo = mapping_equipos[norm_club]
                        nombre_jugador = p["name"]
                        writer.writerow([nombre_equipo, nombre_jugador, ini, fin])
                        print(nombre_equipo, nombre_jugador, ini, fin)

                # Pequeña pausa para evitar bloqueos
                time.sleep(0.4)

    driver.quit()
    print(f"\nCSV generado en: {OUTPUT_CSV}")

# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    main()
