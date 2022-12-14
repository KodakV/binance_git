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
    delete_table_query='''DROP TABLE symbols'''
    cursor.execute(delete_table_query)
    create_table_query='''CREATE TABLE symbols
                          (ID INT PRIMARY KEY     NOT NULL,
                          SYMBOL           TEXT    NOT NULL); '''
    cursor.execute(create_table_query)
    connection.commit()
    print('ok')
except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")
