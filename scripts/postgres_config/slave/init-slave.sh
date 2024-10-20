#!/bin/bash
echo "===================================================="
echo "===================================================="
echo "                  init-slave.sh                     "
echo "   hostname:      "$(hostname)


echo "===================================================="
echo "Creating master backup ..."

PGDATA="/var/lib/postgresql/data"

# Очистка директории данных (на всякий случай)
rm -rf $PGDATA/*

export PGPASSWORD=$REPLICATION_PASSWORD

# Выполнение pg_basebackup для инициализации реплики
pg_basebackup -h master_social_network_db -D $PGDATA -U $REPLICATION_USER -Fp -Xs -P -R -C -S "$(hostname)" -v


psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    ALTER SYSTEM SET primary_conninfo = 'user=$REPLICATION_USER password=$REPLICATION_PASSWORD channel_binding=prefer host=master_social_network_db port=$POSTGRES_PORT sslmode=prefer sslcompression=0 sslcertmode=allow sslsni=1 ssl_min_protocol_version=TLSv1.2 gssencmode=prefer krbsrvname=postgres gssdelegation=0 target_session_attrs=any load_balance_hosts=disable application_name=slave_social_network_db';
EOSQL

echo "===================================================="
echo "Configuring postgresql.conf ..."
cat >> ${PGDATA}/postgresql.conf <<EOF
# Сетевые настройки
listen_addresses = '*'
port = 5432

hot_standby = on
EOF

echo "===================================================="
echo "Configuring pg_hba.conf ..."
cat >> ${PGDATA}/pg_hba.conf <<EOF
host    replication     all      172.23.0.2/16   md5
EOF


unset PGPASSWORD

