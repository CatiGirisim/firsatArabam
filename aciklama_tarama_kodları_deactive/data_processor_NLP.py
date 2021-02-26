"""
This module processes specific elements of raw data and converts them into numbers which can be used by artificial
intelligence.

ÇatıGirişim
"""
import re
import string
import time
import words_dict


def baslik_processor(baslik, site):
    return baslik


def fiyat_processor(fiyat, site):
    if site == 'sahibinden':
        if "," not in fiyat:
            return int(fiyat.split()[0].replace(".", ""))
        else:
            return int(fiyat.split()[0].split(",")[0].replace(".", ""))
    else:
        return int(fiyat)


def sehir_processor(sehir, site):
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


def yil_processor(yil, site):
    return int(yil)


def yakit_processor(yakit, site):
    return yakit


def vites_processor(vites, site):
    return vites


def km_processor(km, site):
    if site == 'sahibinden':
        return 1000*float(km)
    else:
        return int(km)


def beygir_processor(bg, site):
    return bg


def motor_processor(cc, site):
    return cc


def hasar_processor(baslik, aciklama, hasarkaydi, site, ilan_numarasi):

    hasar_words, exact_words, remove_words, replaces, hasar_unwanted_words, numbers, baslamasin,\
        primary_letters, alphabet = words_dict.return_words()

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

    def replacer(st):
        for i in replaces:
            st = st.replace(i, replaces[i])
        for i in st:
            if i not in alphabet:
                st = st.replace(i, " ")
        return st

    def check_mobile_number_or_not(no):
        if len(no) > 1:  # Gelen numaralar 1 den fazlaysa birleştiriyor
            no = ["".join(no)]
        if no[0].isnumeric():
            # if len(no[0]) == 10 or len(no[0]) == 11 or len(no[0]) == 12:
            for i in numbers:
                if no[0].startswith(i):
                    return True
        return False

    def check_sasi_no_or_not(no):
        charac = 0
        number = 0
        if len(no) == 17:
            for i in no:
                if i.isnumeric():
                    number += 1
                elif i.isalpha():
                    charac += 1
            if charac > 2 and number > 5:
                return True
        return False

    def check_date_or_not(no):  # This function returns True if value is date or tire knowledge
        """if len(no) == 3:
            if 32 > int(no[0]) > 0:
                if 32 > int(no[1]) > 0:
                    if 2030 > int(no[2]) > 1900:
                        return True
            if 32 > int(no[0]) > 0:
                if 32 > int(no[1]) > 0:
                    if 30 > int(no[2]) > 00:
                        return True
            if 2030 > int(no[0]) > 1900:
                if 32 > int(no[1]) > 0:
                    if 32 > int(no[2]) > 0:
                        return True
            if 30 > int(no[0]) > 00:
                if 32 > int(no[1]) > 0:
                    if 32 > int(no[2]) > 0:
                        return True
        if len(no) == 2:
            if 32 > int(no[0]) > 0:
                if 2030 > int(no[1]) > 1900:
                    return True
            if 2030 > int(no[0]) > 1900:
                if 32 > int(no[1]) > 0:
                    return True"""
        if len(no) == 3:
            if (len(no[0]) == 2) or (len(no[0]) == 1):
                if (len(no[1]) == 2) or (len(no[1]) == 1):
                    if (len(no[2]) == 5) or (len(no[2]) == 4) or (len(no[2]) == 3) or (len(no[2]) == 2):
                        return True
        if len(no) == 3:
            if (len(no[0]) == 5) or (len(no[0]) == 4) or (len(no[0]) == 3) or (len(no[0]) == 2):
                if (len(no[1]) == 2) or (len(no[1]) == 1):
                    if (len(no[2]) == 2) or (len(no[2]) == 1):
                        return True
        return False

    def check_thousand_number(no):
        if len(no) == 3:
            if len(no[1]) == 3:
                if len(no[2]) == 2:
                    return True
        return False

    def remove_pnc(text_data):
        text_data = text_data.lower()
        string_data = string.punctuation.replace(".", "").replace(",", "")
        table = str.maketrans(string_data, ' '*len(string_data))
        cleaned = text_data.translate(table)
        cleaned = " ".join(cleaned.replace("\n", " ").split())
        cleaned = replacer(cleaned).split()
        res_0 = []
        res_1 = []
        res_f0 = []
        res_f1 = []
        res_f2 = []
        res_f3 = []

        for i in cleaned:  # Alfabe içermesi kontrolü
            for j in primary_letters:
                if j in i:
                    res_0.append(i)
                    break

        for i in res_0:
            for j in hasar_words:
                if j in i:  # Kelimenin istenen, hasar belirtebilecek kelimeler arasında olması kontrolü
                    res_1.append(i)
                    break
            if i in exact_words:  # Kelimenin, tam olarak istenebilecek kelimeler arasında olması kontrolü
                res_1.append(i)

        for i in res_1:
            if i not in remove_words:  # Kelimenin istenmeyen kelimeler arasında olması kontrolü
                if not check_mobile_number_or_not([i]):  # Kelimenin 11 haneli telefon numarası olması kontrolü
                    if not check_sasi_no_or_not(i):
                        res_f0.append(i)

        for i in res_f0:
            if "." in i:  # Kelimenin arasında saçma "." var mı kontrolü
                while i.startswith("."):  # Nokta ile başlıyorsa noktaları siliyor
                    i = i[1:]
                while i.endswith("."):  # Nokta ile bitiyorsa noktaları siliyor
                    i = i[:-1]
                if "." not in i:  # Eğer içinde nokta kalmadıysa geçiyor
                    continue
                i = i.split(".")  # Noktalardan split edip tekrar birleştiriyor tek nokta olsun diye
                b = ""
                for j in i:
                    if j != "":
                        b = b + "." + j
                i = b[1:]
                if i.replace(".", "").isnumeric():  # noktalar harici full sayıysa buraya giriyor
                    try:
                        halfs = i.split(".")
                        dot_number = len(halfs)-1
                        if check_date_or_not(halfs):  # Tarihse direk geçiyor
                            continue
                        if check_mobile_number_or_not(halfs):  # Tel no ise geçiyor
                            continue
                        if check_thousand_number(halfs):  # Sonu 2 basamak paraysa ekliyor
                            res_f1.append(halfs[0] + halfs[1])
                            continue
                        if dot_number > 1:  # Üstteki checklerin üzerine hala nokta 1'den fazlaysa geçiyor direk
                            continue
                        res_f1.append(i)
                    except:
                        print(i)
                if i.replace(".", "").isalpha():  # Eğer her taraf yazıysa ayrı ayrı ekliyor
                    halfs = i.split(".")
                    for l in halfs:
                        res_f1.append(l)
                else:  # Sayı-yazı karışıksa buraya giriyor
                    res_f1.append(i)
            else:
                res_f1.append(i)  # sonradan aktifle
                None

        for i in res_f1:  # İçerisinde istenmeyen betik geçen kelimeleri eliyor
            existence = False
            for k in hasar_unwanted_words:
                if k in i:
                    existence = True
                    break
            if existence == False:
                res_f2.append(i)

        for i in res_f2:
            basliyor = False
            for j in baslamasin:
                if i.startswith(j):
                    basliyor = True
                    break
            if not basliyor:
                res_f3.append(i)

        return res_f3


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

    # PROCESSING baslik PARAMETER
    baslik_cleaned = remove_pnc(baslik)
    # PROCESSING aciklama PARAMETER
    aciklama_cleaned = remove_pnc(aciklama)

    return baslik_cleaned, aciklama_cleaned, hasar_kaydi



