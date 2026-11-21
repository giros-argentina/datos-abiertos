# RTP de tragamonedas publicado por los estudios

Una tabla con el RTP que publica cada estudio para 159 tragamonedas y otros juegos de casino. La reunió Giros Argentina (https://girosargentina.com), una guía del juego online legal en Argentina. Edición de noviembre de 2026 (versión 2026.11). Contenido para mayores de 18 años (+18).

## Qué hay en cada archivo

- `rtp_tragamonedas.csv` y `rtp_tragamonedas.json` traen la misma tabla, con 159 filas y 10 columnas. Hay una fila por juego.
- `datapackage.json` describe los campos.
- `validar.py` revisa los archivos.
- `CITATION.cff` y `LICENSE` explican cómo citar y qué se puede hacer.

## Columnas

| Columna | Qué es |
| --- | --- |
| `juego` | Nombre del juego. |
| `estudio` | Estudio que desarrolla el juego. |
| `rtp_porcentaje` | RTP teórico que publica el estudio, en porcentaje. Si publica varias versiones, la más alta. |
| `rtp_otros_valores` | Otros valores de RTP que publica el mismo estudio para el juego, separados por punto y coma. Vacía si publica uno solo. |
| `volatilidad` | Volatilidad como la publica el estudio, en su escala y su idioma. En PG Soft es el valor del catálogo, de 1 a 3. |
| `apuesta_min_eur` | Apuesta mínima en euros según la ficha del estudio. |
| `apuesta_max_eur` | Apuesta máxima en euros según la ficha del estudio. |
| `ganancia_maxima_x` | Ganancia máxima en veces la apuesta según el estudio. |
| `fuente_url` | Ficha, catálogo o sitio oficial del estudio del que sale la fila. |
| `url_giros` | Página de Giros Argentina sobre el juego. |

## Qué cubre esta edición

- 159 filas de 10 estudios: Pragmatic Play (62), PG Soft (38), Nolimit City (21), Evoplay (13), Push Gaming (10), BGaming (6), Hacksaw Gaming (4), Spribe (2), Yggdrasil Gaming (2) y Wazdan (1).
- Las 159 filas tienen RTP y fuente.
- 84 filas tienen volatilidad.
- 77 filas tienen ganancia máxima.
- 19 filas tienen apuesta mínima y máxima.
- 15 filas tienen otros valores de RTP.

## Cómo se reunieron los datos

Cada fila sale solo de la página oficial del estudio. La dirección está en la columna `fuente_url`. No usamos prensa, enciclopedias ni sitios de reseñas.

«sin dato» quiere decir que no hay fuente oficial para ese campo. En esta edición ninguna celda lleva «sin dato». Una celda vacía quiere decir que la fuente no publica ese valor. Los juegos sin fuente oficial quedaron afuera.

## RTP y casinos

El RTP es un promedio teórico de largo plazo. Algunos estudios publican más de una versión para el mismo juego. La ficha de Push Gaming lo avisa así: «RTP's may vary per casino». El valor que usa cada casino está en el menú de reglas del juego.

## Actualización

El ritmo es mensual. Cada edición vuelve a revisar las fuentes.

## Licencia y crédito

Licencia Creative Commons Atribución 4.0 Internacional (CC BY 4.0). Podés copiar, adaptar y publicar los datos si das crédito. El texto legal completo está en `LICENSE`.

Crédito sugerido: «Giros Argentina, girosargentina.com», con enlace a https://girosargentina.com.

## Validación

Con Python 3, corré `python3 validar.py` en esta carpeta. El resultado esperado es «OK, 0 fallas».
