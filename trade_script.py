import handlers as h
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import time
import pandas as pd
import numpy as np

from structure import candle
symbols=h.getAllSymbols()
print(symbols)

intervals={
    "interval":['1m','3m','5m','15m','30m','1h','2h','4h','6h','8h','12h','1d','3d','1w','1M'],
}
# limit=5
# for symbol in symbols[0:3]:
#     klineData=h.getKline(symbol,intervals['interval'][3],limit)
#     klineAmplitudePercent=[]
#     print('symbol', symbol)
#     for i in range(limit):
#         c1=candle(klineData[i][0],klineData[i][6],klineData[i][1],klineData[i][4],klineData[i][3],klineData[i][2],klineData[i][5])
#         print(c1.getAmplitude())

# print(h.getKline('ETHUSDT',intervals['interval'][2],100))

def insert_db():
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

        for kline in h.getKline('ETHUSDT',intervals['interval'][2],1):
            insert_query=f'''INSERT INTO kline_data_5m (open_price,high_price,low_price,close_price,volume,open_time,close_time,quote_asset_volume,number_trades,buy_quote_volume,buy_base_volume)
            VALUES ({kline[1]},{kline[2]},{kline[3]},{kline[4]},{kline[5]},{kline[0]},{kline[6]},{kline[7]},{kline[8]},{kline[9]},{kline[10]});'''
            print(kline)
            cursor.execute(insert_query)
        connection.commit()
        print('ok')
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")

def select_db(query):
    try:
        connection=psycopg2.connect(user="postgres", password ="rootroot", host="localhost", port="5432", database ="binance")
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor=connection.cursor()
        cursor.execute(query)
        data=cursor.fetchall()
        return data
    except (Exception,Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")

def create_csv_data(table):
    query_all_data=f"SELECT * from {table}"
    data=select_db(query_all_data)
    query_columns_name=f'''SELECT column_name FROM information_schema.columns WHERE table_name = '{table}';'''
    columns=select_db(query_columns_name)
    columns_name=[]
    for i in range(len(columns)):
        columns_name.append(columns[i][0])
    df=pd.DataFrame(data, columns=columns_name, index=None).set_index("id")
    print(df)
    # df.to_csv(f'{table}.csv', sep=',')


while True:
    insert_db()
    create_csv_data("kline_data_5m")
    time.sleep(5)