-- Solución facil eliminar duplicados
CREATE OR REPLACE TABLE `INTEGRATION.integration_prueba_tecnica` AS
SELECT DISTINCT *,
FROM `proyecto-prueba-tecnica-494717.SANDBOX_weather_valencia.weather_daily`;

-- Otra opción
CREATE OR REPLACE TABLE `INTEGRATION.integration_prueba_tecnica` AS
SELECT temp.*
FROM (
  SELECT ARRAY_AGG(t LIMIT 1)[OFFSET(0)] AS temp
  FROM `proyecto-prueba-tecnica-494717.SANDBOX_weather_valencia.weather_daily` AS t
  GROUP BY TO_JSON_STRING(t)
);