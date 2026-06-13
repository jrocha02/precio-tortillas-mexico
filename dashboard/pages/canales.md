---
title: Tortillerías vs autoservicios
---

# 🏪 Tortillerías vs autoservicios

Las tortillerías cobran consistentemente más que los supermercados. Pero antes de leer estos números como "eficiencia del autoservicio", hay un matiz importante.

> **Aviso sobre los datos.** Los autoservicios venden principalmente tortillas industriales (genericas), mientras que las tortillerías venden tortilla fresca de nixtamal. Son productos distintos. La diferencia de precio refleja tanto el tipo de producto como el margen del vendedor — no son directamente comparables.

## Brecha promedio nacional a lo largo del tiempo

```sql channel_trend
SELECT
    mes,
    AVG(precio_tortilleria) AS precio_tortilleria,
    AVG(precio_autoservicio) AS precio_autoservicio,
    AVG(gap_relativo) AS gap_promedio
FROM tortilla.channel_gap
WHERE precio_tortilleria IS NOT NULL
  AND precio_autoservicio IS NOT NULL
GROUP BY mes
ORDER BY mes
```

<LineChart 
    data={channel_trend}
    x=mes
    y={["precio_tortilleria", "precio_autoservicio"]}
    title="Precio promedio nacional por canal"
    yAxisTitle="MXN / kg"
    yFmt="$#,##0.00"
/>

A lo largo de 16 años, la brecha entre tortillerías y autoservicios se ha mantenido relativamente estable — los autoservicios cobran aproximadamente la mitad por kilo.

## Brecha relativa a través del tiempo

```sql gap_over_time
SELECT
    mes,
    AVG(gap_relativo) AS gap_promedio
FROM tortilla.channel_gap
WHERE gap_relativo IS NOT NULL
GROUP BY mes
ORDER BY mes
```

<LineChart 
    data={gap_over_time}
    x=mes
    y=gap_promedio
    title="Diferencia porcentual: ¿cuánto más caro es comprar en tortillería?"
    yAxisTitle="Diferencia relativa"
    yFmt=pct1
/>

Un valor de 1.0 significa que las tortillerías cobran el doble que los autoservicios para esa fecha. La estabilidad de esta línea sugiere que las dos categorías de producto se mueven en paralelo, aunque a niveles de precio muy distintos.

## Brecha actual por ciudad

¿Dónde es mayor la diferencia entre canales? Estas son las ciudades con la mayor brecha en el mes más reciente:

```sql current_gap_by_city
SELECT
    ciudad_canonical,
    estado_canonical,
    region,
    precio_tortilleria,
    precio_autoservicio,
    gap_absoluto,
    gap_relativo
FROM tortilla.channel_gap
WHERE mes = (SELECT MAX(mes) FROM tortilla.channel_gap)
  AND precio_tortilleria IS NOT NULL
  AND precio_autoservicio IS NOT NULL
ORDER BY gap_relativo DESC
```

<DataTable data={current_gap_by_city} rows=20 search=true>
    <Column id=ciudad_canonical title="Ciudad"/>
    <Column id=estado_canonical title="Estado"/>
    <Column id=region title="Región"/>
    <Column id=precio_tortilleria title="Tortillería" fmt="$#,##0.00"/>
    <Column id=precio_autoservicio title="Autoservicio" fmt="$#,##0.00"/>
    <Column id=gap_absoluto title="Diferencia" fmt="$#,##0.00"/>
    <Column id=gap_relativo title="Brecha %" fmt=pct1 contentType=colorscale/>
</DataTable>

## ¿Por qué importa esta diferencia?

Más allá del precio nominal, esta brecha refleja una elección de consumo común en hogares mexicanos: pagar más por tortilla fresca de nixtamal, o ahorrar comprando tortilla industrial empacada. Ambas tienen su lugar, pero los datos muestran que el ahorro es sustancial — alrededor de **40-60% más barato** comprar en el supermercado, a costa de un producto distinto en sabor, textura y proceso de elaboración.
