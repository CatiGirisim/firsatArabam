import db_connection
import datetime
import weighted_table_creator


# This function gets undone ads to pool table , cok sık calısacak 10dkda bır vs
def get_undones(table_name):  # This function gets undone ads to pool table
    print("Starting to transfer predict data to {} table".format(table_name))
    con, cur = db_connection.connect_db()
    cur.execute("DELETE FROM firsatarabam.public.pool")
    cur.execute("SELECT * FROM {}".format(table_name))
    selected = cur.fetchall()
    tot = len(selected)
    print(tot)

    con.commit()
    cur.close()
    con.close()

get_undones("firsatarabam.public.sahibinden_raw_data")