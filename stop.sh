# Stack A : Loan Simulation Service
docker compose --project-name loan --env-file ./.env -f docker-compose.yml down

# Stack B : Camunda
docker compose --project-name camunda --env-file ./camunda/.env -f camunda/docker-compose-web-modeler.yaml -f camunda/docker-compose-core.yaml down