"""
This module creates machine learning db table creation process
19.10.2020

ÇatıGirişim
"""
import db_connection
import datetime
import re
import string
import time
import os


def weight_line(line, modl):

    site = 'sahibinden'
    hasar_dict = {'Sol Ön Kapı': None, 'Sol Arka Kapı': None, 'Sol Ön Çamurluk': None, 'Sol Arka Çamurluk': None,
                  'Arka Tampon': None, 'Arka Kaput': None, 'Ön Tampon': None, 'Sağ Ön Çamurluk': None,
                  'Motor Kaputu': None,'Sağ Ön Kapı': None, 'Sağ Arka Kapı': None, 'Sağ Arka Çamurluk': None,
                  'Tavan': None}

    def baslik_processor(baslik):
        return baslik

    def fiyat_processor(fiyat):
        if site == 'sahibinden':
            if "," not in fiyat:
                return int(fiyat.split()[0].replace(".", ""))
            else:
                return int(fiyat.split()[0].split(",")[0].replace(".", ""))
        else:
            return int(fiyat)

    def sehir_processor(sehir):
        sehir = sehir.replace("İ", "I")
        sehir = sehir.replace("Ç", "C")
        sehir = sehir.replace("Ü", "U")
        sehir = sehir.replace("Ş", "S")
        sehir = sehir.replace("Ö", "O")
        if site == "sahibinden":
            return sehir
        else:
            il, ilce = re.findall('[A-Z][^A-Z]*', sehir)
            return il

    def yil_processor(yil):
        return int(yil)

    def yakit_processor(yakit):
        return yakit

    def vites_processor(vites):
        vites_dict = {"Manuel": 0,
                      "Yarı Otomatik": 1,
                      "Otomatik": 2}
        return vites_dict[vites]

    def km_processor(km):
        if site == 'sahibinden':
            return int(km.replace(".", ""))
        else:
            return int(km)

    def beygir_processor(bg):
        return int(bg.split()[0])

    def motor_processor(cc):
        return 1

    def hasar_processor(hasarkaydi):

        def delete_orj_titles(lst):
            try:
                lst.pop(hasarkaydi.index("Aracın boyası orijinaldir"))
            except:
                None
            try:
                lst.pop(hasarkaydi.index(" sonradan boyanan parçası yoktur"))
            except:
                None
            try:
                lst.pop(hasarkaydi.index('Aracın parçaları orijinaldir'))
            except:
                None
            try:
                lst.pop(hasarkaydi.index(' sonradan değişen parçası yoktur'))
            except:
                None
            return lst

        hasar_kaydi = {"boyali": [], "degisen": []}

        if site == "sahibinden":
            # PROCESSING hasarkaydi PARAMETER
            if hasarkaydi == "Aracın tüm parçaları orijinaldır. Değişen ve boyalı parçası bulunmamaktadır.":
                None
            else:
                hasarkaydi = hasarkaydi.split(",")
                hasarkaydi = delete_orj_titles(hasarkaydi)
                degisenindex = hasarkaydi.index('Değişen Parçalar')
                for i in range(2, degisenindex):
                    hasar_kaydi['boyali'].append(hasarkaydi[i])
                for i in range(degisenindex + 1, len(hasarkaydi)):
                    hasar_kaydi['degisen'].append(hasarkaydi[i])
            # print(hasar_kaydi)
        else:
            None  # Buraya arabam.com processoru gelecek

        return hasar_kaydi

    def result_line_creator(lst):

        def replacer(a):
            a = a.lower()
            a = a.replace("ö", "o")
            a = a.replace("ç", "c")
            a = a.replace("ğ", "g")
            a = "_".join(a.split())
            return a

        res = []
        keys_ordered = ["sol_on_kapı_boyali",
                        "sol_on_kapı_degisen",
                        "sol_arka_kapı_boyali",
                        "sol_arka_kapı_degisen",
                        "sol_on_camurluk_boyali",
                        "sol_on_camurluk_degisen",
                        "sol_arka_camurluk_boyali",
                        "sol_arka_camurluk_degisen",
                        "arka_tampon_boyali",
                        "arka_tampon_degisen",
                        "arka_kaput_boyali",
                        "arka_kaput_degisen",
                        "on_tampon_boyali",
                        "on_tampon_degisen",
                        "sag_on_camurluk_boyali",
                        "sag_on_camurluk_degisen",
                        "motor_kaputu_boyali",
                        "motor_kaputu_degisen",
                        "sag_on_kapı_boyali",
                        "sag_on_kapı_degisen",
                        "sag_arka_kapı_boyali",
                        "sag_arka_kapı_degisen",
                        "sag_arka_camurluk_boyali",
                        "sag_arka_camurluk_degisen",
                        "tavan_boyali",
                        "tavan_degisen"]

        empty_hasar_dict = {"sol_on_kapı_boyali": 0,
                            "sol_on_kapı_degisen": 0,
                            "sol_arka_kapı_boyali": 0,
                            "sol_arka_kapı_degisen": 0,
                            "sol_on_camurluk_boyali": 0,
                            "sol_on_camurluk_degisen": 0,
                            "sol_arka_camurluk_boyali": 0,
                            "sol_arka_camurluk_degisen": 0,
                            "arka_tampon_boyali": 0,
                            "arka_tampon_degisen": 0,
                            "arka_kaput_boyali": 0,
                            "arka_kaput_degisen": 0,
                            "on_tampon_boyali": 0,
                            "on_tampon_degisen": 0,
                            "sag_on_camurluk_boyali": 0,
                            "sag_on_camurluk_degisen": 0,
                            "motor_kaputu_boyali": 0,
                            "motor_kaputu_degisen": 0,
                            "sag_on_kapı_boyali": 0,
                            "sag_on_kapı_degisen": 0,
                            "sag_arka_kapı_boyali": 0,
                            "sag_arka_kapı_degisen": 0,
                            "sag_arka_camurluk_boyali": 0,
                            "sag_arka_camurluk_degisen": 0,
                            "tavan_boyali": 0,
                            "tavan_degisen": 0}
        for i in lst[:-1]:
            res.append(i)
        boyali_detected = lst[-1]['boyali']
        degisen_detected = lst[-1]['degisen']
        # Boyali parçaların dictteki değerini 1 yapıyor
        for i in boyali_detected:
            converted = replacer(i) + "_boyali"
            empty_hasar_dict[converted] = 1
        # Degisen parçaların dictteki değerini 1 yapıyor
        for i in degisen_detected:
            converted = replacer(i) + "_boyali"
            empty_hasar_dict[converted] = 1
        # res listine hasar parametrelerini ekliyor
        for i in keys_ordered:
            res.append(empty_hasar_dict[i])
        return res

    ilan_no = line[0]
    baslik = baslik_processor(line[2])
    fiyat = fiyat_processor(line[3])
    sehir = sehir_processor(line[4])
    yil = yil_processor(line[8])
    yakit = yakit_processor(line[9])
    vites = vites_processor(line[10])
    km = km_processor(line[11])
    beygir = beygir_processor(line[12])
    cc = motor_processor(line[13])
    hasarkaydi = hasar_processor(line[-1])
    combined = (ilan_no, modl, fiyat/100000, (yil-2000)/10, vites, km/100000, beygir/100, cc, hasarkaydi)
    weighted = result_line_creator(combined)

    return weighted


def create_weighted_table(table_in, table_out, min_ad_number):
    general_dict = {}
    print("Reading input data...".format(table_in))
    con, cur = db_connection.connect_db()
    cur.execute("DELETE FROM {}".format(table_out))
    cur.execute("SELECT * FROM {}".format(table_in))
    selected = cur.fetchall()
    tot = len(selected)
    print("Read total {} data, weighting process is starting...".format(tot))
    # Returning db lines and separating car models into general_dict
    for i in selected:
        unique_model = ",".join([i[5], i[6], i[7]])
        if unique_model in general_dict:
            general_dict[unique_model].append(i)
        else:
            general_dict[unique_model] = [i]
    model_list = []
    # Counting car model ads and takes only ones with enough number of ads
    tot_proper_ads = 0
    for i in general_dict:
        tot_ad_number = len(general_dict[i])
        if tot_ad_number > min_ad_number:  # Includes only models with enough ads
            model_list.append(i)
            tot_proper_ads += tot_ad_number
    # Weighting lines
    print("Starting weighting process for {} lines...".format(tot_proper_ads))
    counter = 1
    twenty_percent = int(0.2*tot_proper_ads)
    for i in model_list:
        for j in general_dict[i]:
            weighted_line = tuple(weight_line(j, i))
            cur.execute("INSERT INTO {} VALUES %s".format(table_out), (weighted_line,))
            if counter % twenty_percent == 0:
                print("%", int(counter*100/tot_proper_ads))
                con.commit()
            counter += 1
    cur.close()
    con.close()


# create_weighted_table("firsatarabam.public.model", "firsatarabam.public.model_weighted", 50)
# create_weighted_table("firsatarabam.public.pool", "firsatarabam.public.pool_weighted", 0)