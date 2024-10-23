#!/bin/bash
echo "===================================================="
echo "===================================================="
echo "                  init-master.sh                     "
echo "   hostname:      "$(hostname)


export PGPASSWORD=$POSTGRES_PASSWORD
set -e

echo "===================================================="
echo "Configuring postgresql.conf ..."
cat >> ${PGDATA}/postgresql.conf <<EOF
# Сетевые настройки
listen_addresses = '*'
port = 5432

# Настройки для репликации
wal_level = replica
max_wal_senders = 10
wal_keep_size = 64MB


hot_standby = on
hot_standby_feedback=on

synchronous_commit = on
synchronous_standby_names='*'
EOF

echo "===================================================="
echo "Configuring pg_hba.conf ..."
cat >> ${PGDATA}/pg_hba.conf <<EOF
host    replication     all      172.23.0.2/16   md5
EOF

# Создаем пользователя для репликации
echo "===================================================="
echo "Creating replication user  ..."
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE ROLE $REPLICATION_USER WITH REPLICATION LOGIN PASSWORD '$REPLICATION_PASSWORD';
    SELECT pg_create_physical_replication_slot('replica_slot');
EOSQL

unset PGPASSWORD