import threading
import time
import db_operations
import weighted_table_creator
import sklearn_model_creator
import sklearn_predicter
import datetime
import os
import messager


# Planned frequency: 1 times for a day:
def run_model_functions():
    """
    First input: Deletes older data than input(in days)
    Second input: Working table
    """
    db_operations.delete_older_data(20, "firsatarabam.public.sahibinden_raw_data")
    """ 
    First input: Working Db Table)
    """
    db_operations.get_model_data("firsatarabam.public.sahibinden_raw_data")
    """
    First input:
    Second input:
    Third input:
    """
    weighted_table_creator.create_weighted_table("firsatarabam.public.model", "firsatarabam.public.model_weighted", 250)

    """
    """
    sklearn_model_creator.create_sklearn_models()
    print("Model thread ended successfully...")


# Planned Frequency: 1 times for every 15
def run_predict_functions():
    db_operations.get_undones("firsatarabam.public.sahibinden_raw_data")
    weighted_table_creator.create_weighted_table("firsatarabam.public.pool", "firsatarabam.public.pool_weighted", 0)
    sklearn_predicter.predict_data('firsatarabam.public.pool_weighted', 10)
    print('Prediction thread ended successfully...')


def time_detector():
    while True:
        current_time = str(datetime.datetime.now()).split()[-1].split('.')[0]
        saat, dakka, saniye = current_time.split(":")
        prediction_dakkas = ['00', '15', '30', '45']
        # Model thread startı, sabah 06:30 günde 1
        if saat == '06':
            if dakka == '30':
                if saniye == '00':
                    print('{}:{}:{} Starting model thread...'.format(saat, dakka, saniye))
                    threading.Thread(target=run_model_functions).start()
        if dakka in prediction_dakkas:
            if saniye == '00':
                print('{}:{}:{} Starting predict thread...'.format(saat, dakka, saniye))
                threading.Thread(target=run_predict_functions).start()
        time.sleep(1)

def message_threader():
    print("Message Threader started")
    photos_path = r'C:\ilan_photos\dones'
    files = os.listdir(photos_path)
    if len(files) >= 10:
        for i in files:
            photo_path = os.path.join(photos_path, i)
            message_thread = threading.Thread(target=messager.send_message, args=(photo_path,))
            message_thread.start()
            while message_thread.is_alive():
                time.sleep(1)


if __name__ == '__main__':
    print("Starting Main Runner...")
    try:
        message_threader_thread = threading.Thread(target=message_threader, args=())
        message_threader_thread.start()
    except:
        print("Whatsapp messager has errors. ")
    time_detector()
