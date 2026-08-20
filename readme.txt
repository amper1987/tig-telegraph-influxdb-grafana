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


//DOCKER INSTALL
sudo apt remove docker docker-engine docker.io containerd runc -y
sudo apt update
sudo apt install ca-certificates curl gnupg lsb-release -y
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y
docker --version
docker compose version
docker compose up -d

SELECT rpm, time
FROM mqtt_consumer
WHERE topic = 'iot/${TERMINAL}/mt/msg'
AND $__timeFilter(time);
