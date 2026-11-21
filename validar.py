#!/usr/bin/env python3
"""Valida los datos abiertos de Giros Argentina, tabla de RTP de tragamonedas.

Uso: python3 validar.py
Sale con código 0 si todo está bien y con 1 si hay al menos una falla.
Solo usa la biblioteca estándar.
"""
import csv
import json
import os
import re
import sys
from urllib.parse import urlparse

AQUI = os.path.dirname(os.path.abspath(__file__))

# La única fuente que vale es el sitio oficial del propio estudio.
# Un estudio nuevo se suma acá con su dominio oficial.
SITIO_DEL_ESTUDIO = {
    "BGaming": "bgaming.com",
    "Evoplay": "evoplay.games",
    "Hacksaw Gaming": "hacksawgaming.com",
    "Nolimit City": "nolimitcity.com",
    "PG Soft": "pgsoft.com",
    "Pragmatic Play": "pragmaticplay.com",
    "Push Gaming": "pushgaming.com",
    "Spribe": "spribe.co",
    "Wazdan": "wazdan.com",
    "Yggdrasil Gaming": "yggdrasilgaming.com",
}

ARCHIVOS = {
    "rtp_tragamonedas": {
        "columnas": ["juego", "estudio", "rtp_porcentaje", "rtp_otros_valores", "volatilidad",
                     "apuesta_min_eur", "apuesta_max_eur", "ganancia_maxima_x",
                     "fuente_url", "url_giros"],
        "numericas": ["rtp_porcentaje", "apuesta_min_eur", "apuesta_max_eur", "ganancia_maxima_x"],
        "clave": ["juego", "estudio"],
    },
}
fallas = []


def falla(mensaje):
    fallas.append(mensaje)
    print("FALLA:", mensaje)


def es_sitio_del_estudio(estudio, url):
    dominio = SITIO_DEL_ESTUDIO.get(estudio)
    host = (urlparse(url).hostname or "").lower()
    return bool(dominio) and (host == dominio or host.endswith("." + dominio))


def leer_csv(nombre):
    with open(os.path.join(AQUI, nombre + ".csv"), encoding="utf-8", newline="") as fh:
        lector = csv.reader(fh)
        cabecera = next(lector)
        filas = [dict(zip(cabecera, fila)) for fila in lector]
    return cabecera, filas


def leer_json(nombre):
    with open(os.path.join(AQUI, nombre + ".json"), encoding="utf-8") as fh:
        return json.load(fh)


def normal(valor, numerica):
    """Lleva un valor de CSV o de JSON a una forma comparable."""
    if valor is None or valor == "":
        return None
    if numerica:
        return float(valor)
    return str(valor)


def validar_url(nombre, n, campo, url):
    partes = urlparse(url)
    if partes.scheme != "https" or not partes.hostname:
        falla(f"{nombre} fila {n}: {campo} no es una URL https: {url!r}")


def validar_archivo(nombre, regla):
    cabecera, filas = leer_csv(nombre)
    datos_json = leer_json(nombre)
    if cabecera != regla["columnas"]:
        falla(f"{nombre}: la cabecera no es la esperada: {cabecera}")
        return 0
    if not filas:
        falla(f"{nombre}: no hay filas")

    # CSV y JSON iguales
    if len(filas) != len(datos_json):
        falla(f"{nombre}: el CSV tiene {len(filas)} filas y el JSON {len(datos_json)}")
    for n, (fila_csv, fila_json) in enumerate(zip(filas, datos_json), start=2):
        if list(fila_json.keys()) != regla["columnas"]:
            falla(f"{nombre} fila {n}: las claves del JSON no coinciden con la cabecera")
            continue
        for col in regla["columnas"]:
            es_num = col in regla["numericas"]
            try:
                a, b = normal(fila_csv[col], es_num), normal(fila_json[col], es_num)
            except ValueError:
                falla(f"{nombre} fila {n}: {col} no es un número: {fila_csv[col]!r}")
                continue
            if a != b:
                falla(f"{nombre} fila {n}: {col} difiere entre CSV ({a!r}) y JSON ({b!r})")

    # Filas duplicadas y claves duplicadas
    vistas, claves = set(), set()
    for n, fila in enumerate(filas, start=2):
        entera = tuple(fila[c] for c in regla["columnas"])
        if entera in vistas:
            falla(f"{nombre} fila {n}: fila duplicada")
        vistas.add(entera)
        clave = tuple(fila[c].strip().lower() for c in regla["clave"])
        if clave in claves:
            falla(f"{nombre} fila {n}: clave duplicada {clave}")
        claves.add(clave)

    # Fuente y enlace al sitio
    for n, fila in enumerate(filas, start=2):
        url = fila["fuente_url"].strip()
        if not url:
            falla(f"{nombre} fila {n}: fuente_url vacía")
        else:
            validar_url(nombre, n, "fuente_url", url)
            if not es_sitio_del_estudio(fila["estudio"], url):
                falla(f"{nombre} fila {n}: fuente_url no es del sitio oficial de {fila['estudio']}: {url}")
        giros = fila["url_giros"]
        if not re.fullmatch(r"https://girosargentina\.com/(tragamonedas|juegos)/[a-z0-9-]+/", giros):
            falla(f"{nombre} fila {n}: url_giros con forma inesperada: {giros}")
        for col in regla["columnas"]:
            if fila[col] != fila[col].strip():
                falla(f"{nombre} fila {n}: {col} con espacios al borde")
    return len(filas)


def validar_rtp():
    _, filas = leer_csv("rtp_tragamonedas")
    for n, fila in enumerate(filas, start=2):
        for col in ("juego", "estudio"):
            if not fila[col]:
                falla(f"rtp_tragamonedas fila {n}: {col} vacío")
        try:
            rtp = float(fila["rtp_porcentaje"])
        except ValueError:
            falla(f"rtp_tragamonedas fila {n}: rtp_porcentaje no es un número: {fila['rtp_porcentaje']!r}")
            continue
        if not 80 <= rtp <= 100:
            falla(f"rtp_tragamonedas fila {n}: RTP fuera de 80 a 100: {rtp}")
        if fila["rtp_otros_valores"]:
            for parte in fila["rtp_otros_valores"].split(";"):
                try:
                    otro = float(parte)
                except ValueError:
                    falla(f"rtp_tragamonedas fila {n}: rtp_otros_valores con un valor no numérico: {parte!r}")
                    continue
                if not 80 <= otro <= 100 or otro >= rtp:
                    falla(f"rtp_tragamonedas fila {n}: rtp_otros_valores fuera de rango o no menor que el RTP: {otro}")
        minimo, maximo = fila["apuesta_min_eur"], fila["apuesta_max_eur"]
        if bool(minimo) != bool(maximo):
            falla(f"rtp_tragamonedas fila {n}: apuesta mínima y máxima van juntas")
        elif minimo and not 0 < float(minimo) < float(maximo):
            falla(f"rtp_tragamonedas fila {n}: apuesta mínima y máxima incoherentes")
        tope = fila["ganancia_maxima_x"]
        if tope and (not tope.isdigit() or int(tope) <= 0):
            falla(f"rtp_tragamonedas fila {n}: ganancia_maxima_x no es un entero positivo: {tope!r}")


def validar_descriptor():
    ruta = os.path.join(AQUI, "datapackage.json")
    if not os.path.exists(ruta):
        return
    with open(ruta, encoding="utf-8") as fh:
        paquete = json.load(fh)
    recursos = {r["name"]: r for r in paquete.get("resources", [])}
    for nombre, regla in ARCHIVOS.items():
        recurso = recursos.get(nombre.replace("_", "-"))
        if not recurso:
            falla(f"datapackage.json: falta el recurso {nombre}")
            continue
        campos = [c["name"] for c in recurso["schema"]["fields"]]
        if campos != regla["columnas"]:
            falla(f"datapackage.json: los campos de {nombre} no coinciden con el CSV")
        if recurso.get("path") != nombre + ".csv":
            falla(f"datapackage.json: path inesperado en {nombre}")
    sobran = sorted(set(recursos) - {nombre.replace("_", "-") for nombre in ARCHIVOS})
    if sobran:
        falla(f"datapackage.json: recursos que no están en esta edición: {sobran}")


def main():
    totales = {}
    for nombre, regla in ARCHIVOS.items():
        totales[nombre] = validar_archivo(nombre, regla)
    validar_rtp()
    validar_descriptor()
    for nombre, total in totales.items():
        print(f"{nombre}: {total} filas")
    if fallas:
        print(f"{len(fallas)} fallas")
        return 1
    print("OK, 0 fallas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
