import requests
from bs4 import BeautifulSoup
import sqlite3
import datetime
import os
import get_arabam_primary_data

os.chdir("C:\\Users\\Makdos\\Desktop\\firsatarabam\\db\\")


def connect_links_db():
    return sqlite3.connect('links.db')


def connect_data_db():
    return sqlite3.connect('data.db')


def fetchall_from_links_db(sql):
    links_db = connect_links_db()
    cur = links_db.cursor()
    cur.execute(sql)
    fetched = cur.fetchall()
    cur.close()
    links_db.close()
    return fetched


def get_ilan_first_data(lnk):  # This function gets first ilan data
    main_link = lnk.split(".com")[0] + ".com"
    r = requests.get(lnk)
    soup = BeautifulSoup(r.text, "lxml")
    model = soup.find_all("td", {"class": "listing-modelname pr"})  # Model Name
    title = soup.find_all("td", {"horizontal-half-padder-minus pr"})  # ilan title
    price = soup.find_all("td", {"pl8 pr8 tac pr"})  # Price
    rest = soup.find_all("tr", {"listing-list-item pr should-hover bg-white"})
    data = soup.find_all("a", {"class": "listing-text-new word-break"}, href=True)
    ilan_data = []
    for i in range(0, len(model)):
        href_link = main_link + data[i]['href']
        try:
            resting = rest[i].text.split(title[i].text)[1].split("KarşılaştırKarşılaştırmadan")[0].split()
        except:
            continue
        year = int(resting[0])
        km = int("".join(resting[1].split()[0].split(".")))
        region = resting[-1]

        ilan_data.append([model[i].text.lower(),                                # Model
                          int("".join(price[i].text.split()[0].split("."))),    # Price
                          title[i].text.lower(),                                # Title
                          year,                                                 # Year
                          km,                                                   # KM
                          region[4:],                                           # Region
                          href_link])                                           # Href Link
    return ilan_data


def get_arabam_data():  # This function gathers all first data for arabam.com and writes it to db
    data_db = connect_data_db()
    cur_data = data_db.cursor()
    fetched = fetchall_from_links_db("SELECT * FROM arabam_days_links WHERE site = 'arabam'")
    date_now = datetime.datetime.now().timetuple().tm_yday
    cur_data.execute("CREATE TABLE IF NOT EXISTS arabam_first_data('site','brand','model','submodel','submodel1',"
                     "'smodel','price','title','year','km','region','link','date')")
    cur_data.execute("DELETE FROM arabam_first_data WHERE site = 'arabam'")
    for i in fetched:  # i = site, brand, model, submodel, submodel1, link, pages
        try:
            pages = i[6].split(",")
        except:
            pages = [i[6]]
        for k in pages:
            data = get_ilan_first_data(k)
            for j in data:  # j = submodel, price, title, year, km, region, link
                smodel = "-".join(j[0].split())
                cur_data.execute("INSERT INTO arabam_first_data VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                            (i[0], i[1], i[2], i[3], i[4], smodel, j[1], j[2], j[3], j[4], j[5], j[6], date_now))
    cur_data.close()
    data_db.commit()
    data_db.close()


def get_arabam_first_ilan_data():
    print("7) Grabbing day's first ilan data for arabam.com...", datetime.datetime.now())
    get_arabam_data()
    print("Creating arabam.com local databese process is done...", datetime.datetime.now())


