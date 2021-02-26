"""
This module separates brand names according to their weight to subserver tables.
26.08.2020
ÇatıGirişim
"""

import db_connection
import datetime


def main(servers):
    print("     Starting Process...", datetime.datetime.now())

    def split_brands(brnds):  # Splits brands dict equally weighted
        dummy_server_dict = {}
        for i in range(0, servers):
            dummy_server_dict[i + 1] = {}
        dummy_list = []
        for i in brnds:
            dummy_list.append({i[1]: int(i[0])})
        while dummy_list:
            for i in range(0, servers):
                try:
                    popped = dummy_list.pop()
                    popped_key = list(popped.keys())[0]
                    popped_val = popped[popped_key]
                    dummy_server_dict[i+1][popped_key] = popped_val
                except:
                    None
        tol = 5
        counter = 1
        while True:
            sums = []
            for i in dummy_server_dict:
                sum = 0
                for j in dummy_server_dict[i]:
                    sum += dummy_server_dict[i][j]
                sums.append(sum)
            if max(sums) - min(sums) < tol:
                break
            verici = sums.index(max(sums)) + 1
            alici = sums.index(min(sums)) + 1
            min_key = None
            min_val = 9999
            for i in dummy_server_dict[verici]:
                if dummy_server_dict[verici][i] < min_val:
                    min_val = dummy_server_dict[verici][i]
                    min_key = i
            popped = dummy_server_dict[verici].pop(min_key)
            dummy_server_dict[alici][min_key] = popped
            if counter >= 100:
                tol += 5
                counter = 0
            counter += 1
        return dummy_server_dict

    connection, cursor = db_connection.connect_db()
    server_table_names = [" "]
    print("     Cleaning server brand databases...")
    for i in range(0, servers):
        server_table_name = "firsatarabam.public.server" + str(i+1)
        server_table_names.append(server_table_name)
        cursor.execute("DELETE FROM {}".format(server_table_name))
    print("     Getting all brand data from database...")
    cursor.execute("SELECT * FROM firsatarabam.public.brands")
    all_brands = cursor.fetchall()
    print("     Splitting brands to server tables according to their weights...")
    splitted = split_brands(all_brands)
    for i in splitted:
        table_name = server_table_names[i]
        for j in splitted[i]:
            cursor.execute("INSERT INTO {} (dummy, brand) VALUES {}".format(table_name, (splitted[i][j], j)))
    cursor.close()
    connection.commit()
    connection.close()
    print("     Process is done, database is closed...", datetime.datetime.now())


if __name__ == "__main__":
    main(3)
