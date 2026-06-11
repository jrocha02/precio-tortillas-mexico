---
title: Comparar ciudades
---

# Comparar precios entre ciudades

Selecciona hasta varias ciudades para comparar la evolución de su precio promedio mensual.

```sql cities_list
SELECT DISTINCT ciudad_canonical AS value
FROM tortilla.inflation
WHERE ciudad_canonical IS NOT NULL
ORDER BY ciudad_canonical
```

<Dropdown
    name=selected_cities
    data={cities_list}
    value=value
    multiple=true
    defaultValue={['Culiacán', 'Ciudad Juárez', 'Mérida']}
    title="Ciudades"
/>

<Dropdown
    name=selected_canal
    title="Canal"
    defaultValue="tortillerias">
    <DropdownOption value="tortillerias" valueLabel="Tortillerías"/>
    <DropdownOption value="autoservicios" valueLabel="Autoservicios"/>
</Dropdown>

```sql city_trends
SELECT 
    mes,
    ciudad_canonical,
    precio_mensual
FROM tortilla.inflation
WHERE ciudad_canonical IN ${inputs.selected_cities.value}
  AND canal = '${inputs.selected_canal.value}'
ORDER BY mes, ciudad_canonical
```

<LineChart 
    data={city_trends}
    x=mes
    y=precio_mensual
    series=ciudad_canonical
    title="Precio mensual por ciudad"
    yAxisTitle="MXN / kg"
/>

## Ranking actual

```sql ranking
SELECT 
    ciudad_canonical,
    estado_canonical,
    region,
    precio_mensual,
    inflacion_yoy
FROM tortilla.inflation
WHERE mes = (SELECT MAX(mes) FROM tortilla.inflation)
  AND canal = '${inputs.selected_canal.value}'
  AND ciudad_canonical IS NOT NULL
ORDER BY precio_mensual DESC
```

<DataTable data={ranking} rows=15>
    <Column id=ciudad_canonical title="Ciudad"/>
    <Column id=estado_canonical title="Estado"/>
    <Column id=region title="Región"/>
    <Column id=precio_mensual title="Precio (MXN/kg)" fmt="$#,##0.00"/>
    <Column id=inflacion_yoy title="Inflación YoY" fmt=pct1/>
</DataTable>
