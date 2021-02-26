"""
This module runs data processor module.
02.10.2020
ÇatıGirişim
"""
import data_processor_NLP
import time
import db_connection
import gc
import threading
from multiprocessing import Process


class DataHolder:
    ilan_list = []

    def __init__(self, ilan):
        self.ilan_no = ilan
        self.fiyat = None
        self.aciklama = None
        self.baslik = None
        self.hasar_kaydi = None


def store_data(i):
    ilan_no = i[0]
    DataHolder.ilan_list.append(ilan_no)
    DataHolder(ilan_no).fiyat = data_processor_NLP.fiyat_processor(i[3], "sahibinden")
    DataHolder(ilan_no).baslik, DataHolder(ilan_no).aciklama,\
    DataHolder(ilan_no).hasar_kaydi = data_processor_NLP.hasar_processor(i[2], i[15], i[16], "sahibinden", i[0])


def word_finder_dummy():
    st = time.time()
    connection, cursor = db_connection.connect_db()
    cursor.execute("SELECT * FROM firsatarabam.public.sahibinden_raw_data WHERE 'renk'!='done'")
    selected = cursor.fetchall()
    ###
    yazilanlar = {}
    connection.close()
    out = open("output.txt", "w", encoding="utf8")
    dict = {}
    tot_number = len(selected)
    percent_five = int(1 * tot_number / 100)
    ctr = 1
    ######
    for i in selected:
        store_data(i)
        for j in DataHolder(i).aciklama:
            print(j)
        if ctr % percent_five == 0:
            print("Percentage: ", str(int(ctr * 100 / tot_number)), time.time() - st)
            for k in dict:
                try:
                    a = yazilanlar[k]  # eğer yazilanlarda k diye bir şey varsa a ya atar
                except:
                    try:
                        k = float(k)
                    except:
                        print(k, "\t", dict[k], file=out, flush=True)
                    yazilanlar[k] = None
            dict = {}
        ctr += 1
        out.close()
        ctr += 1
    """
    yazilanlar = {}

    connection.close()
    out = open("output.txt", "w", encoding="utf8")
    dict = {}

    for j in aciklama:
        dict[j] = i[0]
    if ctr % percent_five == 0:
        print("Percentage: ", str(int(ctr*100/tot_number)), time.time() - st)
        for k in dict:
            try:
                a = yazilanlar[k]  # eğer yazilanlarda k diye bir şey varsa a ya atar
            except:
                try:
                    k = float(k)
                except:
                    print(k, "\t", dict[k], file=out, flush=True)
                yazilanlar[k] = None
        dict = {}
    ctr += 1
    out.close()"""
if __name__ == "__main__":
    start = time.time()
    word_finder_dummy()
    print(time.time() - start)
