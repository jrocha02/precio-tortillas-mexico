#!/usr/bin/env python3
"""Build-time data prep for the Precio de las tortillas en México site.

Reads the dbt marts (local ``publish/*.parquet`` if present, else the public
GitHub Release parquet) with DuckDB, runs the same queries that the old Evidence
pages used, and writes small JSON files into ``web/src/lib/data/`` that the
static site consumes. Also derives one lat/long centroid per city from the
municipio GeoJSON so the homepage map can draw OpenStreetMap markers.

Run from anywhere:
    BUILT_AT=$(date -u +%FT%TZ) python web/scripts/prepare-data.py
"""

from __future__ import annotations

import datetime as dt
import json
import os
from pathlib import Path

import duckdb

SCRIPT_DIR = Path(__file__).resolve().parent
WEB_DIR = SCRIPT_DIR.parent
REPO_ROOT = WEB_DIR.parent
PUBLISH_DIR = REPO_ROOT / "publish"
GEOJSON_PATH = REPO_ROOT / "data" / "geo" / "mexico_municipios.geojson"
OUT_DIR = WEB_DIR / "src" / "lib" / "data"

RELEASE_BASE = "https://github.com/jrocha02/precio-tortillas-mexico/releases/latest/download"
MARTS = ["mart_price_inflation", "dim_city", "mart_channel_gap"]


def resolve_source(mart: str) -> str:
    """Local parquet if the CI export produced it, otherwise the release URL."""
    local = PUBLISH_DIR / f"{mart}.parquet"
    if local.exists():
        return str(local)
    return f"{RELEASE_BASE}/{mart}.parquet"


def json_default(value):
    if isinstance(value, (dt.date, dt.datetime)):
        return value.isoformat()
    raise TypeError(f"Not JSON serializable: {type(value)}")


def rows(con: duckdb.DuckDBPyConnection, sql: str) -> list[dict]:
    cur = con.execute(sql)
    cols = [c[0] for c in cur.description]
    out = []
    for rec in cur.fetchall():
        row = {}
        for col, val in zip(cols, rec):
            if isinstance(val, (dt.date, dt.datetime)):
                # month-truncated dates -> "YYYY-MM-DD"
                row[col] = val.isoformat()[:10]
            else:
                row[col] = val
        out.append(row)
    return out


def write(name: str, payload) -> None:
    path = OUT_DIR / name
    path.write_text(json.dumps(payload, default=json_default, ensure_ascii=False))
    print(f"  wrote {path.relative_to(REPO_ROOT)} ({path.stat().st_size:,} bytes)")


# --------------------------------------------------------------------------- #
# City centroids from the municipio GeoJSON (build-time only, never shipped).
# --------------------------------------------------------------------------- #
def _iter_points(geom: dict):
    t = geom.get("type")
    coords = geom.get("coordinates")
    if t == "Polygon":
        for ring in coords:
            yield from ring
    elif t == "MultiPolygon":
        for poly in coords:
            for ring in poly:
                yield from ring


def centroids_by_cvegeo(wanted: set[str]) -> dict[str, tuple[float, float]]:
    if not GEOJSON_PATH.exists():
        print(f"  WARNING: {GEOJSON_PATH} missing; map markers will be empty")
        return {}
    data = json.loads(GEOJSON_PATH.read_text())
    result: dict[str, tuple[float, float]] = {}
    for feat in data.get("features", []):
        cve = str(feat.get("properties", {}).get("CVEGEO", ""))
        if cve not in wanted:
            continue
        sx = sy = n = 0.0
        for x, y in _iter_points(feat["geometry"]):
            sx += x
            sy += y
            n += 1
        if n:
            result[cve] = (round(sy / n, 5), round(sx / n, 5))  # (lat, lng)
    return result


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(":memory:")
    con.execute("INSTALL httpfs; LOAD httpfs;")

    for mart in MARTS:
        src = resolve_source(mart)
        con.execute(f"CREATE VIEW {mart} AS SELECT * FROM read_parquet('{src}')")
        print(f"source: {mart} <- {src}")

    # ---- meta ----------------------------------------------------------- #
    latest_mes = con.execute(
        "SELECT max(mes) FROM mart_price_inflation"
    ).fetchone()[0]
    built_at = os.environ.get("BUILT_AT") or (
        dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    )
    write("meta.json", {
        "built_at": built_at,
        "latest_mes": latest_mes.isoformat()[:10] if latest_mes else None,
    })

    # ---- index ---------------------------------------------------------- #
    precio_nacional_mensual = rows(con, """
        SELECT mes, canal, AVG(precio_mensual) AS precio
        FROM mart_price_inflation
        WHERE ciudad_canonical IS NOT NULL
        GROUP BY mes, canal
        ORDER BY mes
    """)
    precio_actual = rows(con, """
        SELECT canal,
               AVG(precio_mensual) AS precio,
               AVG(inflacion_yoy)  AS inflacion_yoy
        FROM mart_price_inflation
        WHERE mes = (SELECT MAX(mes) FROM mart_price_inflation)
          AND ciudad_canonical IS NOT NULL
        GROUP BY canal
    """)
    municipio_prices = rows(con, """
        SELECT c.inegi_municipio_code AS cvegeo,
               c.ciudad_canonical,
               c.estado_canonical,
               AVG(i.precio_mensual) AS precio
        FROM mart_price_inflation i
        JOIN dim_city c USING (city_id)
        WHERE i.mes = (SELECT MAX(mes) FROM mart_price_inflation)
          AND i.canal = 'tortillerias'
          AND c.inegi_municipio_code IS NOT NULL
        GROUP BY 1, 2, 3
    """)
    cents = centroids_by_cvegeo({r["cvegeo"] for r in municipio_prices})
    city_points = []
    for r in municipio_prices:
        c = cents.get(r["cvegeo"])
        if not c:
            continue
        city_points.append({
            "ciudad_canonical": r["ciudad_canonical"],
            "estado_canonical": r["estado_canonical"],
            "lat": c[0],
            "lng": c[1],
            "precio": r["precio"],
        })
    write("index.json", {
        "precio_nacional_mensual": precio_nacional_mensual,
        "precio_actual": precio_actual,
        "city_points": city_points,
    })

    # ---- inflacion ------------------------------------------------------ #
    yoy = rows(con, """
        WITH monthly AS (
            SELECT mes, canal, AVG(inflacion_yoy) AS yoy_raw
            FROM mart_price_inflation
            WHERE inflacion_yoy IS NOT NULL
            GROUP BY mes, canal
        )
        SELECT mes, canal,
               AVG(yoy_raw) OVER (
                   PARTITION BY canal ORDER BY mes
                   ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
               ) AS inflacion_yoy_nacional
        FROM monthly
        ORDER BY mes
    """)
    top_inflation = rows(con, """
        WITH peak_per_city AS (
            SELECT ciudad_canonical, estado_canonical, canal, mes,
                   precio_mensual, inflacion_yoy,
                   ROW_NUMBER() OVER (
                       PARTITION BY ciudad_canonical, canal
                       ORDER BY inflacion_yoy DESC
                   ) AS rn
            FROM mart_price_inflation
            WHERE inflacion_yoy IS NOT NULL
              AND ciudad_canonical IS NOT NULL
        )
        SELECT ciudad_canonical, estado_canonical, mes, canal,
               precio_mensual, inflacion_yoy
        FROM peak_per_city
        WHERE rn = 1
        ORDER BY canal, inflacion_yoy DESC
    """)
    write("inflacion.json", {"yoy": yoy, "top_inflation": top_inflation})

    # ---- ciudades ------------------------------------------------------- #
    cities_list = [r["value"] for r in rows(con, """
        SELECT DISTINCT ciudad_canonical AS value
        FROM mart_price_inflation
        WHERE ciudad_canonical IS NOT NULL
        ORDER BY ciudad_canonical
    """)]
    city_series = rows(con, """
        SELECT mes, ciudad_canonical, canal, precio_mensual
        FROM mart_price_inflation
        WHERE ciudad_canonical IS NOT NULL
        ORDER BY mes, ciudad_canonical
    """)
    ranking = rows(con, """
        SELECT ciudad_canonical, estado_canonical, region, canal,
               precio_mensual, inflacion_yoy
        FROM mart_price_inflation
        WHERE mes = (SELECT MAX(mes) FROM mart_price_inflation)
          AND ciudad_canonical IS NOT NULL
        ORDER BY precio_mensual DESC
    """)
    write("ciudades.json", {
        "cities_list": cities_list,
        "city_series": city_series,
        "ranking": ranking,
    })

    # ---- canales -------------------------------------------------------- #
    channel_trend = rows(con, """
        SELECT mes,
               AVG(precio_tortilleria) AS precio_tortilleria,
               AVG(precio_autoservicio) AS precio_autoservicio,
               AVG(gap_relativo)        AS gap_promedio
        FROM mart_channel_gap
        WHERE precio_tortilleria IS NOT NULL
          AND precio_autoservicio IS NOT NULL
        GROUP BY mes
        ORDER BY mes
    """)
    gap_over_time = rows(con, """
        SELECT mes, AVG(gap_relativo) AS gap_promedio
        FROM mart_channel_gap
        WHERE gap_relativo IS NOT NULL
        GROUP BY mes
        ORDER BY mes
    """)
    current_gap_by_city = rows(con, """
        SELECT ciudad_canonical, estado_canonical, region,
               precio_tortilleria, precio_autoservicio,
               gap_absoluto, gap_relativo
        FROM mart_channel_gap
        WHERE mes = (SELECT MAX(mes) FROM mart_channel_gap)
          AND precio_tortilleria IS NOT NULL
          AND precio_autoservicio IS NOT NULL
        ORDER BY gap_relativo DESC
    """)
    write("canales.json", {
        "channel_trend": channel_trend,
        "gap_over_time": gap_over_time,
        "current_gap_by_city": current_gap_by_city,
    })

    print("done.")


if __name__ == "__main__":
    main()
