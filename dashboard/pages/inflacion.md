--- 
title: La historia de la inflación
---

# Comparación de la Inflación a traves de los años

El precio de la tortilla se ha triplicado desde 2010 y últimamente se ha tenido un repunte en los precios de la tortilla.

<Dropdown
    name=selected_canal
    title="Canal"
    defaultValue="tortillerias">
    <DropdownOption value="tortillerias" valueLabel="Tortillerías"/>
    <DropdownOption value="autoservicios" valueLabel="Autoservicios"/>
</Dropdown>

## Inflación anualizada 

```sql yoy_nacional
WITH monthly AS (
    SELECT
        mes,
        canal,
        AVG(inflacion_yoy) AS yoy_raw
    FROM tortilla.inflation
    WHERE inflacion_yoy IS NOT NULL and canal = '${inputs.selected_canal.value}'
    GROUP BY mes, canal
)
SELECT
    mes,
    canal,
    yoy_raw,
    AVG(yoy_raw) OVER (
        PARTITION BY canal
        ORDER BY mes
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS inflacion_yoy_nacional
FROM monthly
ORDER BY mes
```

<LineChart 
    data={yoy_nacional}
    x=mes
    y=inflacion_yoy_nacional
    title="Inflación anualizada (YoY) — promedio nacional"
    yAxisTitle="Cambio anual (%)"
    yFmt=pct1
    yAxisLabels=true
/>

Cada punto representa cuánto más cara estaba la tortilla en ese mes comparado
con doce meses antes. Valores por encima de 0.10 (10%) indican inflación
significativa.


## Top 10: Los peores momentos de inflación

Las 10 ciudades más golpeadas por la inflación 

```sql top_inflation
WITH peak_per_city AS (
    SELECT
        ciudad_canonical,
        estado_canonical,
        canal,
        mes,
        precio_mensual,
        inflacion_yoy,
        ROW_NUMBER() OVER (
            PARTITION BY ciudad_canonical, canal 
            ORDER BY inflacion_yoy DESC
        ) AS rn
    FROM tortilla.inflation
    WHERE inflacion_yoy IS NOT NULL
      AND ciudad_canonical IS NOT NULL
      and canal = '${inputs.selected_canal.value}'
)
SELECT
    ciudad_canonical,
    estado_canonical,
    mes,
    canal,
    precio_mensual,
    inflacion_yoy
FROM peak_per_city
WHERE rn = 1
ORDER BY inflacion_yoy DESC
LIMIT 10

```

<DataTable data={top_inflation} rows=10>
    <Column id=ciudad_canonical title="Ciudad"/>
    <Column id=estado_canonical title="Estado"/>
    <Column id=mes title="Mes" fmt="mmm yyyy"/>
    <Column id=canal title="Canal"/>
    <Column id=precio_mensual title="Precio" fmt="$#,##0.00"/>
    <Column id=inflacion_yoy title="Inflación YoY" fmt=pct1 contentType=colorscale/>
</DataTable>


Para el caso de las tortillerias la mayoría se centran en el año **2017-2018**. En León y Guanajuato una de las posibles causas es el gasolinazo que ocurrió a principios de ese año que aumento el precio de la distribución.

La mayoría de estos picos se agrupan en **2012**, cuando una sequía severa en
el medio oeste estadounidense disparó el precio del maíz, principal insumo
para la tortilla mexicana en el caso del canal de autoservicios. Estados como Jalisco, Nayarit y Zacatecas vieron
aumentos anuales superiores al 50% en algunos meses.
