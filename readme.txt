GRAFANA VARIABLE
SELECT DISTINCT topic FROM mqtt_consumer
REGEX
iot\/([^\/]+)\/mt\/msg

DASHBOARD QUERY
--SELECT "cpu", "usage_user", "time" FROM "cpu" WHERE "time" >= $__timeFrom AND "time" <= $__timeTo AND "cpu" = 'cpu0'
--SELECT * FROM mqtt_consumer;
SELECT rpm, time
FROM mqtt_consumer
WHERE topic = 'iot/${TERMINAL_ID}/mt/msg'

YOUTUBE LINK
https://www.youtube.com/watch?v=C4aatEAkNao&t=215s
GITHUB LINK
https://github.com/InfluxCommunity/TIG-Stack-using-InfluxDB-3?tab=readme-ov-file