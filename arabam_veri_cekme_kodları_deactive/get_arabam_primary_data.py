import requests
from bs4 import BeautifulSoup
import sqlite3
import os
import datetime
import db_connection

os.chdir("C:\\Users\\Makdos\\Desktop\\firsatarabam\\db\\")
etiket = "?days=1&take=50"

def connect_db():
    return sqlite3.connect('links.db')

def get_links(address_to_get_links, main_address, rng):  # This function gets arabam.com page links etc.
    r = requests.get(address_to_get_links)
    soup = BeautifulSoup(r.text, "lxml")
    data = soup.find_all("a", {"class": "list-item"}, href=True)
    lnks = {}
    for j in range(rng, len(data)):
        i = data[j]
        got_text = "-".join(i.text.split()).lower()
        lnks[got_text] = (main_address + i['href'])
    return lnks

def get_model_page_links(url):  # This function gets page links for model links
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        empty = soup.find_all("span", {"class": "color-red4 bold pl4 bold"})
        if len(empty):
            return None
        full = soup.find_all("span", {"class": "color-red4 bold pl4 fz13"})
        total_ilan_number = int(full[0].text.split()[0][1:])
        total_pages = int(total_ilan_number/50)
        if total_ilan_number%50:
            total_pages += 1
        urls = []
        for i in range(1, total_pages+1):
            page_url = url[:-1] + str(i)
            urls.append(page_url)
        return urls
    except:
        print("Err 123: Requesting page number data error!")
        return None

def update_main_page_links():  # This function updates main page links in db
    links_db = connect_db()
    cur = links_db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS main_page_links_table(site,link)")
    cur.execute("DELETE FROM main_page_links_table WHERE site='arabam'")
    cur.execute("DELETE FROM main_page_links_table WHERE site='sahibinden'")
    cur.execute("INSERT INTO main_page_links_table VALUES(?,?)", ("arabam", "https://www.arabam.com"))
    cur.execute("INSERT INTO main_page_links_table VALUES(?,?)", ("sahibinden", "https://www.sahibinden.com"))
    links_db.commit()
    cur.close()
    links_db.close()

def update_arabam_brand_links():  # This function gets arabam.com brand links and writes to db
    links_db = connect_db()
    cur = links_db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS arabam_brand_links_table(site,brand,link)")
    cur.execute("SELECT * FROM main_page_links_table WHERE site = 'arabam' ")
    link = cur.fetchall()[0][1]
    otomobil_link = "https://www.arabam.com/ikinci-el/otomobil"
    res_links = get_links(otomobil_link, link, 1)
    cur.execute("DELETE FROM arabam_brand_links_table WHERE site='arabam'")  # Deletes old data
    for brand in res_links:
        cur.execute("INSERT INTO arabam_brand_links_table VALUES(?,?,?)", ("arabam", brand, res_links[brand]))
    links_db.commit()
    cur.close()
    links_db.close()

def update_arabam_model_links():  # This function gets arabam.com brand model links and writes to db
    links_db = connect_db()
    cur = links_db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS arabam_brand_model_links_table(site,brand,model,link)")
    cur.execute("SELECT * FROM main_page_links_table WHERE site = 'arabam'")
    main_link = cur.fetchall()[0][1]
    cur.execute("DELETE FROM arabam_brand_model_links_table WHERE site='arabam'")  # Deletes old data
    cur.execute("SELECT * FROM  arabam_brand_links_table  WHERE site = 'arabam' ")
    links = cur.fetchall()
    for i in links:
        links_1 = get_links(i[2], main_link, 2)  # Gets links under initial links
        for j in links_1:
            cur.execute("INSERT INTO arabam_brand_model_links_table VALUES(?,?,?,?)", ("arabam", i[1], j, links_1[j]))
    links_db.commit()
    cur.close()
    links_db.close()

def update_arabam_submodel_links():  # This function gets arabam.com submodel page links and writes to db
    links_db = connect_db()
    cur = links_db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS arabam_brand_model_submodel_links_table(site,brand,model,submodel,submodel1,submodel2,link)")
    cur.execute("SELECT * FROM main_page_links_table WHERE site = 'arabam'")
    main_link = cur.fetchall()[0][1]
    cur.execute("DELETE FROM arabam_brand_model_submodel_links_table WHERE site='arabam'")
    cur.execute("SELECT * FROM  arabam_brand_model_links_table  WHERE site = 'arabam'")
    links = cur.fetchall()
    for i in links:  # i = site, brand, model, link
        links_1 = get_links(i[-1], main_link, 3)
        for j in links_1:
            links_2 = get_links(links_1[j], main_link, 4)
            for k in links_2:
                try:
                    links_3 = get_links(links_2[j], main_link, 5)
                    print(links_3)
                except:
                    None




        """for j in links_1:
            cur.execute("INSERT INTO arabam_brand_model_submodel_links_table VALUES(?,?,?,?,?)",
                        ("arabam", i[1], i[2], j, links_1[j]))"""
    links_db.commit()
    cur.close()
    links_db.close()

def update_arabam_submodel_links():  # This function gets arabam.com submodel1 page links and writes to db
    links_db = connect_db()
    cur = links_db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS arabam_brand_model_submodel_links_table(site,brand,model,submodel,link)")
    cur.execute("SELECT * FROM main_page_links_table WHERE site = 'arabam'")
    main_link = cur.fetchall()[0][1]
    cur.execute("DELETE FROM arabam_brand_model_submodel_links_table WHERE site='arabam'")
    cur.execute("SELECT * FROM  arabam_brand_model_links_table  WHERE site = 'arabam'")
    links = cur.fetchall()
    for i in links:  # i = site, brand, model, link
        links_1 = get_links(i[-1], main_link, 3)
        for j in links_1:
            cur.execute("INSERT INTO arabam_brand_model_submodel_links_table VALUES(?,?,?,?,?)",
                        ("arabam", i[1], i[2], j, links_1[j]))
    links_db.commit()
    cur.close()
    links_db.close()

def update_arabam_submodel1_links():  # This function gets arabam.com brand model page links and writes to db
    links_db = connect_db()
    cur = links_db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS arabam_brand_model_submodel1_links_table(site,brand,model,submodel,submodel1,link)")
    cur.execute("SELECT * FROM main_page_links_table WHERE site = 'arabam'")
    main_link = cur.fetchall()[0][1]
    cur.execute("DELETE FROM arabam_brand_model_submodel1_links_table WHERE site='arabam'")
    cur.execute("SELECT * FROM  arabam_brand_model_submodel_links_table  WHERE site = 'arabam'")
    links = cur.fetchall()
    for i in links:  # i = site, brand, model, submodel, link
        links_1 = get_links(i[-1], main_link, 4)
        for j in links_1:
            cur.execute("INSERT INTO arabam_brand_model_submodel1_links_table VALUES(?,?,?,?,?,?)",
                        ("arabam", i[1], i[2], i[3], j, links_1[j]))
    links_db.commit()
    cur.close()
    links_db.close()

def update_days_links():  # This function gets day's pagelinks for input submodel url's.
    links_db = connect_db()
    cur = links_db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS arabam_days_links(site,brand,model,submodel,submodel1,link,pages)")
    cur.execute("SELECT * FROM main_page_links_table WHERE site = 'arabam'")
    main_link = cur.fetchall()[0][1]
    cur.execute("DELETE FROM arabam_days_links WHERE site='arabam'")  # Delete old data
    cur.execute("SELECT * FROM  arabam_brand_model_submodel1_links_table  WHERE site = 'arabam'")
    submodel_links = cur.fetchall()
    for i in submodel_links:  # i = site, brand, model, submodel, submodel1, link
        link = i[-1] + etiket + "&page=1"
        links = get_model_page_links(link)
        if links:
            page_links = ",".join(links)
            cur.execute("INSERT INTO arabam_days_links VALUES(?,?,?,?,?,?,?)", (i[0], i[1], i[2], i[3], i[4], i[5], page_links))
    links_db.commit()
    cur.close()
    links_db.close()

def renew_arabam_db():  # This function makes a total regeneration for arabam.com db
    print("1) Updating main page links...", datetime.datetime.now())
    update_main_page_links()
    print("2) Updating arabam.com brand links...", datetime.datetime.now())
    update_arabam_brand_links()
    print("3) Updating arabam.com model links...", datetime.datetime.now())
    update_arabam_model_links()
    print("4) Updating arabam.com submodel links...", datetime.datetime.now())
    update_arabam_submodel_links()
    print("5) Updating arabam.com submodel1 links...", datetime.datetime.now())
    update_arabam_submodel1_links()
    print("6) Updating arabam.com day's PageLinks links...", datetime.datetime.now())
    update_days_links()


# renew_arabam_db()
