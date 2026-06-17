{{ config(materialized='table') }}

with daily as (
    select
        f.city_id,
        c.ciudad_canonical,
        c.estado_canonical,
        c.region,
        f.canal,
        f.fecha,
        f.precio_kg
    from {{ ref('fct_tortilla_prices_daily') }} f
    inner join {{ ref('dim_city') }} c using (city_id)
),

monthly as (
    select
        city_id,
        ciudad_canonical,
        estado_canonical,
        region,
        canal,
        date_trunc('month', fecha) as mes,
        avg(precio_kg) as precio_mensual
    from daily
    group by 1, 2, 3, 4, 5, 6
),

with_change_flag as (
    select
        *,
        case
            when precio_mensual != lag(precio_mensual) over (
                partition by city_id, canal order by mes
            ) then 1
            else 0
        end as changed
    from monthly
),

first_real_change as (
    select
        city_id,
        canal,
        min(mes) as primera_observacion_real
    from with_change_flag
    where changed = 1
    group by city_id, canal
),

eligible as (
    select m.*
    from monthly m
    inner join first_real_change r
        on m.city_id = r.city_id
       and m.canal = r.canal
    where m.mes >= r.primera_observacion_real + interval '12 months'
),

with_lags as (
    select
        *,
        lag(precio_mensual, 1)  over w as precio_mes_anterior,
        lag(precio_mensual, 12) over w as precio_ano_anterior,
        avg(precio_mensual) over (
            partition by city_id, canal
            order by mes
            rows between 11 preceding and current row
        ) as precio_promedio_12m
    from eligible
    window w as (partition by city_id, canal order by mes)
)

select
    city_id,
    ciudad_canonical,
    estado_canonical,
    region,
    canal,
    mes,
    precio_mensual,
    precio_mes_anterior,
    precio_ano_anterior,
    precio_promedio_12m,
    case
        when precio_mes_anterior is not null and precio_mes_anterior > 0
        then (precio_mensual - precio_mes_anterior) / precio_mes_anterior
    end as inflacion_mom,
    case
        when precio_ano_anterior is not null and precio_ano_anterior > 0
        then (precio_mensual - precio_ano_anterior) / precio_ano_anterior
    end as inflacion_yoy
from with_lags
