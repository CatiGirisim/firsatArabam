"""
This module grabs raw data from sahibinden.com.

Error Codes:
Error Code: 600 : Data Grabbing Error - insert_arabam_data_into_db.py
Error Code: 601 : Database periodic insertion error - insert_arabam_data_into_db.py
Error Code: 602 : Database remaining insertion error - insert_arabam_data_into_db.py
Error Code: 603 : No ads for today error - insert_arabam_data_into_db.py

ÇatıGirişim
"""

import requests
from bs4 import BeautifulSoup
import sqlite3
import datetime
import db_connection
import get_arabam_primary_data
import get_arabam_secondary_data
import gc
import time


def get_all_data_from_local_db():
    local_db = sqlite3.connect(r"C:\Users\Makdos\Desktop\firsatarabam\db\data.db")
    local_cur = local_db.cursor()
    local_cur.execute("SELECT * FROM arabam_first_data WHERE site = 'arabam'")
    fetched = local_cur.fetchall()
    return fetched


def get_ilan_data(tpl):
    try:
        day = datetime.datetime.now().timetuple().tm_yday
        baslik = tpl[7]
        fiyat = tpl[6]
        sehir = tpl[10]
        marka = tpl[1]
        seri = tpl[2]
        yil = tpl[8]
        km = tpl[9]
        renk = None
        r = requests.get(tpl[11])
        soup = BeautifulSoup(r.text, "lxml")
        ilan_no = soup.find_all("span", {"class": "bli-particle semi-bold"})[0].text.split()[0]
        model = " ".join(soup.find_all("span", {"class": "bli-particle"})[9].text.split())
        yakit = " ".join(soup.find_all("span", {"class": "bli-particle"})[13].text.split())
        vites = " ".join(soup.find_all("span", {"class": "bli-particle"})[15].text.split())
        beygir = " ".join(soup.find_all("span", {"class": "bli-particle"})[19].text.split())
        motor = " ".join(soup.find_all("span", {"class": "bli-particle"})[17].text.split())
        degisen_list = soup.find_all("li", class_="vertical-half-offset")
        aciklama = soup.find_all("div", id="js-hook-description")[0].text
        degisen_temp = []
    except:
        print("     600 - Data Grabbing Error")
        return None
    for i in degisen_list:
        degisen_temp.append(" ".join(i.text.split()))
    degisen = ",".join(degisen_temp)
    data = (ilan_no, day, baslik, fiyat, sehir, marka, seri, model, yil, yakit, vites, km, beygir, motor, renk,
            aciklama, degisen)
    return data


def insert_arabam_data():
    counter = 1
    data_list = []
    start_time = float(time.time())
    print("     Fetching all url data from local database...")
    all_fetched = get_all_data_from_local_db()
    print("     Connecting to global database...")
    connection, cursor = db_connection.connect_db()
    print("     Starting data grabbing process..")
    for i in all_fetched:
        data = get_ilan_data(i)
        if data:
            data_list.append(data)
        else:
            continue
        if counter % 50 == 0:
            print("       Importing periodic data into database...")
            for j in data_list:
                try:
                    cursor.execute(
                        "INSERT INTO firsatarabam.public.arabam_raw_data VALUES %s ON CONFLICT DO NOTHING", (j,))
                except:
                    print("       601 Error - Database Periodic Insertion Error")
            connection.commit()
            data_list = []
        counter += 1
    if data_list:
        print("       Importing remaining data into database...")
        for i in data_list:
            try:
                cursor.execute("INSERT INTO firsatarabam.public.arabam_raw_data VALUES %s ON CONFLICT DO NOTHING",
                               (i,))
            except:
                print("       602 Error - Database Remaining Insertion Error")
        connection.commit()
    print("     Total grabbing process time: ", round(float(time.time()) - start_time, 2), " seconds")
    print("     Total grabbed ads: ", counter)


def main_runner():
    start_time = time.time()
    print("Starting arabam.com whole process...")
    get_arabam_primary_data.renew_arabam_db()
    get_arabam_secondary_data.get_arabam_first_ilan_data()
    insert_arabam_data()
    print("Whole process is done...")
    print("Total process time is: ", round(float(time.time()) - start_time, 2), " seconds")
    gc.collect()


if __name__ == "__main__":
    main_runner()
