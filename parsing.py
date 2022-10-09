import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

try:
    # Подключение к существующей базе данных
    connection = psycopg2.connect(user="postgres",
                                  # пароль, который указали при установке PostgreSQL
                                  password="rootroot",
                                  host="localhost",
                                  port="5432",
                                  database="binance")
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    # Курсор для выполнения операций с базой данных
    cursor = connection.cursor()
    cursor.execute("""SELECT table_name FROM information_schema.tables
           WHERE table_schema = 'public'""")


    create_table_query='''CREATE TABLE IF NOT EXISTS symbols
                          (id INT PRIMARY KEY     NOT NULL,
                          SYMBOL           varchar(10)    NOT NULL); '''
    cursor.execute("DROP TABLE kline_data_5m")
    cursor.execute(create_table_query)
    create_table_query2='''CREATE TABLE IF NOT EXISTS kline_data_5m
    (id SERIAL PRIMARY KEY NOT NULL,
    open_price NUMERIC NOT NULL,
    high_price NUMERIC NOT NULL,
    low_price NUMERIC NOT NULL,
    close_price NUMERIC NOT NULL,
    volume NUMERIC NOT NULL,
    open_time BIGINT NOT NULL,
    close_time BIGINT NOT NULL,
    quote_asset_volume NUMERIC NOT NULL,
    number_trades BIGINT NOT NULL,
    buy_quote_volume NUMERIC NOT NULL,
    buy_base_volume NUMERIC NOT NULL);
    '''
    cursor.execute(create_table_query2)

    connection.commit()
    print('ok')
except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")

