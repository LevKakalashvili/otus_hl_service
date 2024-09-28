FROM postgres:13

COPY ./scripts/fixtures/user_data.csv user_data.csv
COPY ./scripts/load_data.sh load_data.sh

CMD ./load_data.sh
