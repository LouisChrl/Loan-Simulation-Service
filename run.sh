# External Communication Network
docker network inspect loan_app_backend >/dev/null 2>&1 || docker network create loan_app_backend

# Optional : Sonarqube
# docker run -d --name sonarqube -p 9000:9000 \
#   -v sonarqube_data:/opt/sonarqube/data \
#   -v sonarqube_extensions:/opt/sonarqube/extensions \
#   -v sonarqube_logs:/opt/sonarqube/logs \
#   sonarqube:community

# Stack A : Loan Simulation Service
docker compose --project-name loan --env-file ./.env -f docker-compose.yml up -d

# Stack B : Camunda
docker compose --project-name camunda --env-file ./camunda/.env -f camunda/docker-compose-web-modeler.yaml -f camunda/docker-compose-core.yaml up -d