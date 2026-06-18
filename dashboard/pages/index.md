---
title: Tortillanomics
---

# 🌽 El precio de la tortilla en México

Desde 2007. Datos del SNIIM, modelados con dbt, actualizados cada semana.

<BigValue 
    data={precio_actual.filter(d => d.canal === 'tortillerias')}
    value=precio
    title="Precio promedio (tortillerías)"
    fmt="$#,##0.00"
/>

<BigValue 
    data={precio_actual.filter(d => d.canal === 'autoservicios')}
    value=precio
    title="Precio promedio (autoservicios)"
    fmt="$#,##0.00"
/>

<BigValue 
    data={precio_actual.filter(d => d.canal === 'tortillerias')}
    value=inflacion_yoy
    title="Inflación 12m (tortillerías)"
    fmt=pct1
/>



```sql precio_nacional_mensual
SELECT
    mes,
    canal,
    AVG(precio_mensual) AS precio
FROM tortilla.inflation
WHERE ciudad_canonical IS NOT NULL
GROUP BY mes, canal
ORDER BY mes
```

<LineChart 
    data={precio_nacional_mensual}
    x=mes
    y=precio
    series=canal
    title="Precio promedio nacional por canal"
    yAxisTitle="MXN / kg"
/>

```sql precio_actual
SELECT 
    canal,
    AVG(precio_mensual) AS precio,
    AVG(inflacion_yoy) AS inflacion_yoy
FROM tortilla.inflation
WHERE mes = (SELECT MAX(mes) FROM tortilla.inflation)
  AND ciudad_canonical IS NOT NULL
GROUP BY canal
```

## Precio por municipio

```sql municipio_prices
SELECT 
    c.inegi_municipio_code AS cvegeo,
    c.ciudad_canonical,
    AVG(i.precio_mensual) AS precio
FROM tortilla.inflation i
JOIN tortilla.city c USING (city_id)
WHERE i.mes = (SELECT MAX(mes) FROM tortilla.inflation)
  AND i.canal = 'tortillerias'
  AND c.inegi_municipio_code IS NOT NULL
GROUP BY 1, 2
```

<AreaMap
    data={municipio_prices}
    areaCol=cvegeo
    geoJsonUrl='/tortillanomics/mexico_municipios.geojson'
    geoId=CVEGEO
    value=precio
    valueFmt="$#,##0.00"
    title="Precio actual de la tortilla por municipio (tortillerías)"
/>
