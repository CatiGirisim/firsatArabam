"""
This module creates sklearn models.
21.10.2020

ÇatıGirişim
"""

import db_connection
import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import train_test_split
import pickle
import os


def create_sklearn_models():
    model_folder_path = r"C:\MODELS"
    connection, cursor = db_connection.connect_db()
    cursor.execute("SELECT * FROM firsatarabam.public.model_weighted")
    selected = cursor.fetchall()
    model_names = {}
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
        name = "'" + i + "'"  # Modelin birleşik adı
        cursor.execute("SELECT * FROM firsatarabam.public.model_weighted WHERE model={}".format(name))
        selected = cursor.fetchall()

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

    cursor.close()
    connection.close()