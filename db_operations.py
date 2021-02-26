"""
This module makes standart db operations between determined intervals.
26.08.2020

Error Codes:
Error Code 100 : Database Connection Error - db_connect.py

"""
import db_connection
import datetime
import weighted_table_creator

# This function deletes old data, 1 run for a day
def delete_older_data(tolerance, table_name):  # This function deletes old data
    print("Starting deleting old data (older than {} days)".format(tolerance))
    date_now = datetime.datetime.now().timetuple().tm_yday
    if date_now < tolerance:
        date_now += 365
    con, cur = db_connection.connect_db()
    cur.execute("SELECT * FROM {} WHERE {}-day > {}".format(table_name, date_now, tolerance))
    tot = len(cur.fetchall())
    print("Deleting total {} data...".format(tot))
    cur.execute("DELETE FROM {} WHERE {}-day > {}".format(table_name, date_now, tolerance))
    print("Deleted...")
    con.commit()
    cur.close()
    con.close()

# This function gets model ads to model table, çalışma sıklıgı gunde 1
def get_model_data(table_name):  # This function gets model ads to model table
    print("Starting to transfer model data to {} table".format(table_name))
    con, cur = db_connection.connect_db()
    cur.execute("DELETE FROM firsatarabam.public.model")
    cur.execute("SELECT * FROM {} WHERE renk = 'done'".format(table_name))
    selected = cur.fetchall()
    tot = len(selected)
    print("Transferring total {} number of data".format(tot))
    for i in selected:
        cur.execute("INSERT INTO firsatarabam.public.model VALUES %s".format(table_name), (i,))
    print("Transferred...")
    con.commit()
    cur.close()
    con.close()

# This function gets undone ads to pool table , cok sık calısacak 10dkda bır vs
def get_undones(table_name):  # This function gets undone ads to pool table
    print("Starting to transfer predict data to {} table".format(table_name))
    con, cur = db_connection.connect_db()
    cur.execute("DELETE FROM firsatarabam.public.pool")
    cur.execute("SELECT * FROM {} WHERE renk != 'done'".format(table_name))
    selected = cur.fetchall()
    tot = len(selected)
    print("Transferring total {} number of data".format(tot))
    keys = []
    for i in selected:  # Carrying selecteds to pool
        cur.execute("INSERT INTO firsatarabam.public.pool VALUES %s", (i,))
        keys.append(i[0])
    for i in keys:  # Updating renks to done
        cur.execute("UPDATE {} SET renk = 'done' where ilan_no = {}".format(table_name, i))
    print("Transferred...")
    con.commit()
    cur.close()
    con.close()



# delete_older_data(20, "firsatarabam.public.sahibinden_raw_data")
# get_model_data("firsatarabam.public.sahibinden_raw_data")
# get_undones("firsatarabam.public.sahibinden_raw_data")



# weighted_table_creator.create_weighted_table("firsatarabam.public.model", "firsatarabam.public.model_weighted", 250)
# weighted_table_creator.create_weighted_table("firsatarabam.public.pool", "firsatarabam.public.pool_weighted", 0)