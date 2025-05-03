#!/bin/sh

echo "Aguardando Databases estarem prontos..."

# Função para esperar um serviço ficar disponível
wait_for_service() {
  local host=$1
  local port=$2
  while ! nc -z $host $port; do
    echo "Aguardando $host:$port..."
    sleep 5
  done
}

# Esperar OpenSearch e Keycloak
wait_for_service "postgres-db-source" "5432"
wait_for_service "postgres-db-target" "5432"
wait_for_service "source_db_api" "8000"

echo "Todos os serviços estão prontos. Iniciando aplicação..."
exec "$@"