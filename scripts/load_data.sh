echo "IP"
hostname -i

echo "Sleeping for 10 seconds…"
sleep 10

echo "Start script"

ls -l .

psql postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@db_master:$POSTGRES_PORT/$POSTGRES_DB -c "\copy public.user (name, sur_name, birth_date, sex, city, interest) from 'user_data.csv' (format csv, header true, delimiter ';', encoding 'UTF8');"
