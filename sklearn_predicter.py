"""
This module makes predictions from sklearn model.
23.01.2021
Error code 200: compare_data function error
Error code 300: create_picture function error
ÇatıGirişim
"""
import db_connection
import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import train_test_split
import pickle
import os
from PIL import Image, ImageFont, ImageDraw
import messager


# Below function compares prices
def compare_data(tahmin, gercek, tol):
    if tahmin <= gercek*(100-tol)/100:
        return 1
    else:
        return 0


def create_picture(tahmin, ilan_no):
    # veritabanına bağlanıp mesaj atılacak ilanın gerekli bilgileri çekiliyor
    pool_table_name = 'firsatarabam.public.sahibinden_raw_data'
    connection, cursor = db_connection.connect_db()
    cursor.execute("SELECT * FROM {} WHERE ilan_no = {}".format(pool_table_name, ilan_no))
    ilan = cursor.fetchall()[0]
    # çekilen veriler ilgili fieldlara atanıyor
    ilan_no = ilan[0]
    model_name = ",".join([ilan[5], ilan[6], ilan[7]])
    yil = ilan[8]
    ilanFiyat = ilan[3].split()[0]
    #firsatArabamFiyat =
    #fiyatFarki = int(ilanFiyat) - int(firsatArabamFiyat)
    #fiyatFarkiStr = str(fiyatFarki)
    arti = "+"
    tl = " TL"
    km = ilan[11]
    model_split = model_name.split(",")
    marka = model_split[0]
    seri = model_split[1]
    model = model_split[2]

    yakit = ilan[9]
    vites = ilan[10]

    # fotoğraf template kullanılarak veriler fotoğrafa yazılıyor ve gönderilmek üzere hazır hale geliyor
    templates_path = r'C:\ilan_photos\templates'
    message_image = Image.open(r'C:\ilan_photos\templates\firsatarabam.jpeg')
    message_drawer = ImageDraw.Draw(message_image)
    fntBuyuk = ImageFont.truetype("arial.ttf", size=60)
    fntKucuk = ImageFont.truetype("arial.ttf", size=30)

    message_drawer.text((30, 110), yil, font=fntBuyuk, fill=(0, 0, 0))
    message_drawer.text((180, 110), model_name, font=fntBuyuk, fill=(0, 0, 0))
    message_drawer.text((35, 230), ilanFiyat + tl, font=fntBuyuk, fill=(0, 0, 0))
    #message_image.text((320, 375), firsatArabamFiyat + tl, font=fntKucuk, fill=(0, 0, 0))

    '''if fiyatFarki <= 0:
        message_image.text((35, 300), str(fiyatFarki) + tl, font=fntBuyuk, fill=(0, 128, 0))
    else:
        message_image.text((35, 300), arti + str(fiyatFarki) + tl, font=fntBuyuk, fill=(255, 0, 0))
    '''

    message_drawer.text((800, 1210), yil, font=fntKucuk, fill=(0, 0, 0))
    message_drawer.text((800, 1250), str(km), font=fntKucuk, fill=(0, 0, 0))
    message_drawer.text((800, 1290), marka, font=fntKucuk, fill=(0, 0, 0))
    message_drawer.text((800, 1330), seri, font=fntKucuk, fill=(0, 0, 0))
    message_drawer.text((800, 1370), model, font=fntKucuk, fill=(0, 0, 0))
    message_drawer.text((800, 1410), yakit, font=fntKucuk, fill=(0, 0, 0))
    message_drawer.text((800, 1450), vites, font=fntKucuk, fill=(0, 0, 0))
    #message_image.text((800, 1490), kasa, font=fntKucuk, fill=(0, 0, 0))

    # oluşturulan fotoğraf gönderilmek üzere ilan no su ile kaydediliyor
    foto_name = "{}.png".format(ilan_no)
    kayit_folder_path = r'C:\ilan_photos\dones'
    kayit_foto_path = os.path.join(kayit_folder_path, foto_name)

    message_image.save(kayit_foto_path)
    # verileri çek fotoyu yap
    return kayit_foto_path


def predict_data(table_name, price_tolerance):
    model_folder_path = r"C:\MODELS"
    connection, cursor = db_connection.connect_db()
    cursor.execute("SELECT * FROM {}".format(table_name))
    selected = cursor.fetchall()
    keys_ordered = ["ilan_no",
                    "model",
                    "fiyat",
                    "yil",
                    "vites",
                    "km",
                    "beygir",
                    "cc",
                    "sol_on_kapı_boyali",
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
    keys_x = ["yil",
                "vites",
                "km",
                "beygir",
                "cc",
                "sol_on_kapı_boyali",
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
    for ilan in selected:
        model_name = ilan[1]
        model_filename = model_name + '_finalized_model.sav'
        model_path = os.path.join(model_folder_path, model_filename)
        try:
            loaded_model = pickle.load(open(model_path, 'rb'))
        except FileNotFoundError:
            print('There is no sklearn model for "{}", passing...'.format(model_name))
            continue
        # Prediction starts here
        name = "'" + model_name + "'"  # Modelin birleşik adı
        empty_model_dict = {"fiyat": [],
                            "yil": [],
                            "vites": [],
                            "km": [],
                            "beygir": [],
                            "cc": [],
                            "sol_on_kapı_boyali": [],
                            "sol_on_kapı_degisen": [],
                            "sol_arka_kapı_boyali": [],
                            "sol_arka_kapı_degisen": [],
                            "sol_on_camurluk_boyali": [],
                            "sol_on_camurluk_degisen": [],
                            "sol_arka_camurluk_boyali": [],
                            "sol_arka_camurluk_degisen": [],
                            "arka_tampon_boyali": [],
                            "arka_tampon_degisen": [],
                            "arka_kaput_boyali": [],
                            "arka_kaput_degisen": [],
                            "on_tampon_boyali": [],
                            "on_tampon_degisen": [],
                            "sag_on_camurluk_boyali": [],
                            "sag_on_camurluk_degisen": [],
                            "motor_kaputu_boyali": [],
                            "motor_kaputu_degisen": [],
                            "sag_on_kapı_boyali": [],
                            "sag_on_kapı_degisen": [],
                            "sag_arka_kapı_boyali": [],
                            "sag_arka_kapı_degisen": [],
                            "sag_arka_camurluk_boyali": [],
                            "sag_arka_camurluk_degisen": [],
                            "tavan_boyali": [],
                            "tavan_degisen": []}  # Dataframe e çevrilecek dict
        max_number = len(ilan)
        for k in range(2, max_number):  # İlanno ve model adı almadan sadece sayısal verileri alıyor
            empty_model_dict[keys_ordered[k]].append(ilan[k])  # dataframe e çevrilecek dicte kaydediyor
        # X ve Y ayrılıyor
        df = pd.DataFrame(empty_model_dict, columns=keys_ordered[2:])
        X = df[keys_x]
        Y = df['fiyat']
        Y_pred = loaded_model.predict(X)
        print('tahmin:', Y_pred, ilan[0], Y)
        # asagida karsilastirma algoritması
        ilan_no = ilan[0]
        tahmin_fiyat = Y_pred[0]
        gercek_fiyat = Y[0]

        try:
            comparison_result = compare_data(tahmin_fiyat, gercek_fiyat, price_tolerance)
        except:
            print("200: Error")

        if comparison_result:
            #try:
                created_photo_path = create_picture(tahmin_fiyat, ilan_no)
            #except:
                #print("300: Error")
    # messager.send_message(created_photo_path)
    cursor.close()
    connection.close()


'''model_names = {}

# Model isimleri sözlüğünü oluşturuyor
for i in selected:
    model_names[i[1]] = None
# Tek tek model isimleri için yapay zeka modeli oluşturuluyor
for i in model_names:
    empty_model_dict = {"fiyat": [],
                        "yil": [],
                        "vites": [],
                        "km": [],
                        "beygir": [],
                        "cc": [],
                        "sol_on_kapı_boyali": [],
                        "sol_on_kapı_degisen": [],
                        "sol_arka_kapı_boyali": [],
                        "sol_arka_kapı_degisen": [],
                        "sol_on_camurluk_boyali": [],
                        "sol_on_camurluk_degisen": [],
                        "sol_arka_camurluk_boyali": [],
                        "sol_arka_camurluk_degisen": [],
                        "arka_tampon_boyali": [],
                        "arka_tampon_degisen": [],
                        "arka_kaput_boyali": [],
                        "arka_kaput_degisen": [],
                        "on_tampon_boyali": [],
                        "on_tampon_degisen": [],
                        "sag_on_camurluk_boyali": [],
                        "sag_on_camurluk_degisen": [],
                        "motor_kaputu_boyali": [],
                        "motor_kaputu_degisen": [],
                        "sag_on_kapı_boyali": [],
                        "sag_on_kapı_degisen": [],
                        "sag_arka_kapı_boyali": [],
                        "sag_arka_kapı_degisen": [],
                        "sag_arka_camurluk_boyali": [],
                        "sag_arka_camurluk_degisen": [],
                        "tavan_boyali": [],
                        "tavan_degisen": []} # Dataframe e çevrilecek dict
    

    for j in selected:
        max_number = len(j)
        for k in range(2, max_number):  # İlanno ve model adı almadan sadece sayısal verileri alıyor
            empty_model_dict[keys_ordered[k]].append(j[k])  # dataframe e çevrilecek dicte kaydediyor
    # X ve Y ayrılıyor
    df = pd.DataFrame(empty_model_dict, columns=keys_ordered[2:])
    X = df[keys_x]
    Y = df['fiyat']
    # Train ve Test Dataları ayrılıyor
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1, random_state=0)
    regressor = linear_model.LinearRegression().fit(X_train, Y_train)
    Y_pred = regressor.predict(X_test)
    print("Model adı: ", i)
    print(regressor.score(X, Y))
    """Y_test = Y_test.values.tolist()
    for j in range(len(Y_pred)):
        print("Yazılımın Tahmini: {}, Gerçek Fiyat: {}, ilan no: {}".format(Y_pred[j], Y_test[j], i))"""
    model_filename = i + '_finalized_model.sav'
    model_path = os.path.join(model_folder_path, model_filename)
    pickle.dump(regressor, open(model_path, 'wb'))
    # print(regr.coef_)
    #print(regr.intercept_)
    # break  # ilkinden sonra break çakıyor
'''






"""loaded_model = pickle.load(open(filename, 'rb'))
result = loaded_model.score(X_test, Y_test)
print(result)"""