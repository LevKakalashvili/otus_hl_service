# Social Network Backend
> "Сервис социальной сети для учебного проекта"
> 
> ## Установка и запуск (локально)
Необходимо иметь `python==^3.11`, `poetry`, и `postgresql`

### Клонирование
```shell
git clone https://github.com/LevKakalashvili/otus_hl_service.git
cd otus_hl_service
```

### Установка зависимостей
```shell
poetry config virtualenvs.in-project false # автоматически создает виртуальное окружение вне проекта 
poetry install
```

### Конфигурация
Создать файл в папке проекта `.env` (название файла окружения устанавливается в `otus_hl_service/app/core/settings/general_settings.py:18`) либо поместить конфигурационные данные в переменные окружения (прим. `export ENVIROMENT=dev`)

### База данных
Необходимо создать базу данных средствами postgresql
```shell
createdb social_network_db
alembic upgrade head # накатить миграции
```
Информация о подключении к базе данных указывается в файле конфигурации `.env`


### Запуск
#### В виртуальном окружении (предварительно активировав его)
```shell
python main.py
```
#### Не в виртуальном окружении
```shell
poetry run python main.py
```

## Установка и запуск (контейнеризация)
### Docker
```shell
docker build -t social_network_backend .
docker run -p PORT:PORT social_network_backend
```