"""
This module makes connection to db and returns connection and cursor objects.
26.08.2020

Error Codes:
Error Code: 100 : Database Connection Error - db_connect.py

ÇatıGirişim
"""
import psycopg2


def connect_db():
    try:
        conn = psycopg2.connect(host="185.122.201.37", password="A95993da95", database="firsatarabam", user="postgres")
        cur = conn.cursor()
    except:
        print("***** 100 Error *****")
        return
    return conn, cur
