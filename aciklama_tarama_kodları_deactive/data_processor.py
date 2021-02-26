"""
This module processes specific elements of raw data and converts them into numbers which can be used by artificial
intelligence.

ÇatıGirişim
"""
import re
import string
import db_connection  #
import time


def baslik_processor(baslik, site):
    return baslik


def fiyat_processor(fiyat, site):
    if site == 'sahibinden':
        if "," not in fiyat:
            return 1000*float(fiyat.split()[0])
        else:
            return 1000 * float(fiyat.split()[0].split(",")[0])
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


def hasar_processor(baslik, aciklama, hasarkaydi, site):
    hasar_words = ["mevcut",  "bolge", "harici", "sadece", "hasar", "kay", "var", "par", "parca", "tem", "bucuk", "yok",
                   "ayri", "kaza", "olm", "leke",
                   "hata", "kusur", "kısur", "kusır", "heta",
                   "degisen", "degsn",  "deg", "tramer", "trm", "garantili",
                   "bi", "bir", "iki", "uc", "dort", "bes",
                   "buc", "prc", "orj", "ori", "1", "1.5", "2.5", "2", "3", "4", "5", "6", "7", "8", "9",
                   "komple", "kumple", "kmple", "kompile", "komp le", "orda", "orada", "orta", "bel", "alti",
                   "cm",
                   "yarim", "yarm",
                   "lukal", "local", "lokal", "lokel",
                   "boya", "boy", "boyali",
                   "sok", "tak", "kapag", "kapak", "bagaj",
                   "cizik", "ciz", "ezik", "ezilme",
                   "duzeltme", "gocuk", "goc", "duz",
                   "sol", "sul", "sag", "seg", "on", "arka", "alt", "ust",
                   "depo",
                   "kaput", "kapt",
                   "tampon", "tampn", "tanpon", "tanp",
                   "camurluk", "cam", "camr"
                   "tavan", "tavn"
                   "marspiyer", "mars", "masp",
                   "tavn", "tava",  "kapi", "direk",
                   "sase", "sasi", "sasu", "pod", "pud", "drk", "direk", "dire",
                   "tamam",
                   ]
    exact_words = ["tl", "ve"]
    dummy_words = [" hatasiz ", " boyasiz ", "full", " garaj ", " kapali ",
                   " otomotivden ", " otomoti̇v ", " ruzgarlik ", " ruzgar "
                   " model ", ".xxx"
                   " aracimizin ", " aracimiz ", "aracimiz ", " aracim ",
                   "hayirli olsun", "hayirli ugurlu olsun", "simdiden", "ford", "vw", "bilen bilir",
                   "keyifle kullaniyorum", "ihtiyacdan", "satiliktir", "yol tutusu", "bakimlari yenidir",
                   " kmdedi̇r ", " km orjinal dir ", " km orjinaldir ", " kmsi orjinaldir ",
                   "muaynesi", "muayenesi",
                   " kesinlikle ",
                   " takilmamis ",
                   "masrafi yoktur", " masrafsizdir ", "masraf etmeden binebilirsiniz", "masraf etmeden binebilir",
                   "tramer kayidi yoktur", "tramer kaydi yoktur", "tramer kaydi yokdur", "tramersiz", "yuklenmistir",
                   "ici disi", " aralik ", " kasim ", " ocak ", " subat ", " mart ", " nisan ", " mayis ", " haziran ",
                   " eylul ", " ekim ", " temmuz ", " agustos ", " 2020 ", " 2021 ", " 2022 ", " 2019 ", " 2018 ",
                   " cikislidir ", " trafige ", " kazasi yoktur ", " ihtiyacdan ", " ihtiyactan ", " yildir ",
                   " sahibinden ", " ayina ", " kadar ", " durumu ", " cok ", " guzeldir ", " guzel ", " binicisine ",
                   " alicisina ", " yokus ", " kalkis ", " destegi ", " kendi ", " kendine ", " park ", " muhafaza ",
                   " edilmistir ", " verilecektir ", " katlanir ", " km orjinal dir ", " alana ", " kmsi orjinaldir ",
                   " km orjinaldir ", " temizdir ", " temiz ", " tertemiz ", " mukemmel ", " mukemmeldir ", " aliciya",
                   " alicisina ", " arac ", " alana ", " ayna ", " etme ", "kmde ", "km de ", " aracimda ",
                   "aracimizin ", " modelidir ", " orjinalleriyle ", " sorunsuz ", " binmekteyim ", " bakımları ",
                   " zamanında ", " yapılmıştır ", " resimi ", " resmi ", " resimleri ", " arabami ", " irtibat ",
                   " tel ", " takas ", " takaslar ", " ev ", " arsa ", " cek ", " senet ", " gecmisi ", " takildi ",
                   " taktirdim ", " taktirildi ", " takti ", " 4 lastik yenidir ", " lastikler ", " lastik ", " kislik "
                    ' 2017 ',

                   ' model ', ' renault ', ' 1.5 ', ' 90 ', ' otomati̇k ', ' vi̇tes ', ' paket ', ' aracin ',
                   ' ozelli̇kleri̇ ', ' startstop ', ' abs ', ' asr ', ' hiz ', ' sabi̇tleme ', ' kli̇ma ', ' deri̇ ',
                   ' di̇reksi̇yon ',
                   ' calar ', ' yol ', ' bi̇lgi̇sayari ', ' 4 ', ' cam ', ' bluetooth ', ' si̇s ', ' fari ',
                   ' dokunmati̇k ', ' ekran ',
                   ' on ', ' kol ', ' dayama ', ' kumandali ', ' merkezi̇ ', ' ki̇li̇t ', ' arka ', ' sensoru ',
                   ' yan ', ' aynalar ',
                   ' yagmur ', ' far ', ' eksperti̇z ', ' aracimizda ', ' yoktur ', ' km ', ' 15 ', ' 16 ', ' 17 ',
                   ' anlasmali ', ' uygun ', ' kredi̇ ', ' i̇mkani ', ' fi̇nans ', ' 30 ', ' hafta ',
                   ' i̇ci̇ ', ' ve ', ' 2010 ', ' bin ', ' herhangi ', ' bir ', ' raporlari ', ' .. ', ' 2016 ',
                   ' touch ',
                   ' kesi̇nli̇kle ', ' kumas ', ' koltuk ', ' elektri̇kli̇ ', ' di̇ki̇z ', ' aynasi ',
                   ' i̇sofi̇x ', ' camlar ', ' cd ', ' usb ', ' aux ', ' gi̇ri̇si̇ ', ' 1.3 ', ' manuel ', ' kazasiz ',
                   ' sifir ',
                   ' ayarinda ', ' filmi ', ' double ', ' cikisli ', ' 8 ', ' 2 ', ' yil ', ' start ', ' stop ',
                   ' geri ',
                   ' vardir. ', ' pazarlik ', ' aracim ', ' en ', ' dolu ', ' 1.2 ', ' . ', ' butun ', ' bakimlari ',
                   ' yapilmistir ', ' zenon ', ' sis ', ' var ', ' ayrica ', ' otomatik ', ' yag ', ' her ', ' 1 ',
                   ' masraf ', ' payi ', ' bey ', ' orji̇nal ', ' i̇lk ', ' gunku ', ' yeni̇ ', ' temi̇z ',
                   ' i̇stedi̇gi̇ni̇z ',
                   ' yere ', ' son ', ' bakimi ', ' yapildi ', ' tri̇ger ', ' agir ', ' yapildi. ', ' ̇ ', ' e ',
                   ' kurus ',
                   ' masrafi ', ' ozelli̇kler ', ' sahi̇bi̇nden ', ' araci ', ' olarak ', ' kullanilmistir. ', ' 2014 ',
                   ' i̇leri̇ ', ' bi̇n ', ' ki̇lometre ', ' de ', ' yapilmistir. ', ' gayet ', ' i̇c ', ' herhangi̇ ',
                   ' bi̇r ',
                   ' deforme ', ' yedek ', ' anahtari ', ' sabi̇tleyi̇ci̇ ', ' anahtarsiz ', ' calistirma ', ' 7 ',
                   ' i̇nc ',
                   ' si̇stemi̇ ', ' navi̇gasyon ', ' baglantisi ', ' di̇ji̇tal ', ' eco ', ' celi̇k ', ' jant ',
                   ' gunduz ',
                   ' led ', ' destegi̇ ', ' isitmali ', ' plaka ', ' no ', ' cikis ', ' muayene ', ' bilgisi ',
                   ' kaza ',
                   ' parcalar ', ' yok ', ' kasko ', ' kredi ', ' 12 ', ' ay ', ' i̇le ', ' donanim ', ' klima ',
                   ' elektrikli ', ' radyo ', ' bilgisayari ', ' direksiyon ', ' buz ', ' el ', ' yetki̇li̇ ',
                   ' servi̇s ',
                   ' satis ', ' adres ', ' aractir ', ' nokta ', ' ezi̇k ', ' ci̇zi̇k ', ' ki̇tapciklari ', ' 18 ',
                   ' telefon ',
                   ' geri̇ ', ' gorus ', ' takilmistir ', ' binde ', ' orjinal ', ' kilometre ', ' istediginiz ',
                   ' araca ',
                   ' tup ', ' once ', ' garantisi ', ' mevcut ', ' 6 ', ' aracta ', ' ekspertiz ', ' raporu ',
                   ' fotograflarda ',
                   ' hp ', ' makyajli ', ' uzerinde ', ' ilk ', ' daha ', ' dir. ', ' tarafimizca ', ' benzin ',
                   ' kucuk ',
                   ' ezik ', ' gocuk ', ' ile ', ' yeni ', ' aracimin ', ' bakimli ', ' ek ', ' di̇zel ', ' farkli ',
                   ' surus ',
                   ' modu ', ' renk ', ' acilir ', ' kamerasi ', ' alasimli ', ' spor ', ' jantlar ', ' gi̇ri̇s ',
                   ' sinifinin ',
                   ' satisa ', ' oldukca ', ' yakit ', ' servis ', ' olup ', ' motorunda ', ' kusur ', ' duzenli ',
                   ' gore ',
                   ' bakimlidir ', ' araclarla ', ' piril ', ' bu ', ' kitapciklari ', ' tum ', ' 9 ', ' veya ',
                   ' yapilir ',
                   ' ekstra ', ' aile ', ' alacagim ', ' dan ', ' satiyorum ', ' di̇ger ', ' araclarimiz ', ' i̇ci̇n ',
                   ' aya ',
                   ' opel ', ' peugeot ', ' yetkili ', ' 0 ', ' i̇stanbul ', ' sahibinden ', ' resi̇mlerde ',
                   ' mevcut. ',
                   ' akti̇f ', ' genel ', ' motor ', ' yagi ', ' sanziman ', ' fren ', ' balatalari ', ' marka ',
                   ' bende ', ' az ',
                   ' geni̇s ', ' yuksek ', ' si̇mdi̇den ', ' 1.6 ', ' lpg ', ' diger ', ' i̇lanlarimiz ', ' i̇cin ',
                   ' i̇leti̇si̇m ', ' 80 ',
                   ' motoru ', ' yuruyeni̇ ', ' sorunsuzdur ', ' gi̇bi̇ ', ' bi̇lgi̇si̇ ', ' mevcuttur. ', ' detayli ',
                   ' bi̇lgi̇ ',
                   ' kasa ', ' vs. ', ' tamamen ', ' disinda ', ' cikmasi ', ' icin ', ' bakim ', ' uzun ', ' yolda ',
                   ' elden ',
                   ' hic ', ' aktif ', ' buna ', ' bagli ', ' lastikleri ', ' sehir ', ' icinde ', ' dusuk ', ' fiyat ',
                   ' satilik ',
                   ' vade ', ' 2015 ', ' turbo ', ' sofor ', ' farlari ', ' lasti̇k ', ' kusursuz ', ' uc ', ' yarim ',
                   ' mantikli ',
                   ' olan ', ' olur ', ' gonul ', ' arayiniz ', ' fi̇lmi̇ ', ' tam ', ' yapilmis ', ' arac ',
                   ' yuruyen ', ' eksi̇ksi̇z ',
                   ' bilgi ', ' pazar ', ' kullanilmistir ', ' aldim ', ' su ', ' dir ', ' hepsi ', ' ben ', ' alan ',
                   ' kisi ',
                   ' diye ', ' bi ', ' ozellikleri ', ' extra ', ' alirken ', ' lutfen ', ' bos ', ' ozel ', ' mp3 ',
                   ' beyaz ',
                   ' zamaninda ', ' sorunu ', ' iki ', ' fazla ', ' mesaj ', ' gun ', ' donus ', ' paketi ',
                   ' aydinlatma ',
                   ' celik ', ' filtresi ', ' degisti ', ' masrafsiz ', ' plus ', ' i̇ki̇ ', ' kapagi ', ' hari̇ci̇ ',
                   ' hayirli ',
                   ' disi ', ' ses ', ' i̇ci̇nde ', ' fonksiyonel ', ' auto ', ' gunleri̇ ', ' aciktir ', ' taki̇p ',
                   ' degisik ',
                   ' da ', ' acik ', ' bi̇lgi̇leri̇ ', ' alacak ', ' hicbir ', ' sorun ', ' triger ', ' vites ',
                   ' almak ', ' dizel ',
                   ' anahtar ', ' basinc ', ' cruise ', ' control ', ' elektroni̇k ', ' bayi̇ ', ' tarafindan ',
                   ' ... ',
                   ' takilmistir. ', ' eksper ', ' resimlerde ', ' sikintisi ', ' calismayan ', ' i̇steni̇len ',
                   ' alt ', ' takim ',
                   ' aku ', ' kullanilmis ', ' sekilde ', ' baska ', ' 2000 ', ' yenidir ', ' 2012 ', ' aractir. ',
                   ' dis ',
                   ' sanzuman ', ' crui̇se ', ' sabitleme ', ' naki̇t ', ' 1.4 ', ' yururu ', ' numara ', ' gibi ',
                   ' orijinal ',
                   ' vs ', ' 2013 ', ' fonksi̇yonel ', ' goruldugu ', ' di̇ledi̇gi̇ni̇z ', ' oldugu ', ' ustaya ',
                   ' sabitleyici ',
                   ' dahil ', ' ruhsata ', ' toyota ', ' 10 ', ' aksami ', ' aracimda ', ' ici ', ' 34 ', ' yok. ',
                   ' pasta ',
                   ' araba ', ' dahi ', ' lastigi ', ' sigara ', ' koruma ', ' ic ', ' durumdadir. ', ' sistemi ',
                   ' elektronik ',
                   ' destek ', ' cocuk ', ' koltugu ', ' isofix ', ' kontrol ', ' merkezi ', ' kilit ', ' duzgun ',
                   ' oto ',
                   ' arkadaslar ', ' lasti̇kler ', ' si̇gara ', ' akusu ', ' sunroof ', ' aracimi ', ' iyi ', ' not ',
                   ' 2011 ',
                   ' rahatligiyla ', ' cikarsa ', ' cift ', ' servi̇se ', ' tefek ', ' mesafe ', ' i̇yi̇ ', ' saat ',
                   ' satin ',
                   ' car ', ' 0532 ', ' herkese ', ' ust ', ' den ', ' olsa ', ' esp ', ' ayni ', ' hi̇cbi̇r ',
                   ' olmayan ',
                   ' araclar ', ' sahibi ', ' toplam ', ' performansi ', ' koltuklarinda ', ' yaptirdim ',
                   ' servi̇ste ',
                   ' deri ', ' ye ', ' baski ', ' balata ', ' aracidir ', ' yari ', ' lasti̇kleri̇ ', ' satiyorum. ',
                   ' ama ',
                   ' basinda ', ' kapida ', ' gerek ', ' arkadas ', ' bakimlidir. ', ' ayinda ', ' takimi ', ' aksam ',
                   ' sonra ',
                   ' hi̇droli̇k ', ' ayarlanabi̇li̇r ', ' koltuklar ', ' yanik ', ' yirtik ', ' zaman ', ' xenon ',
                   ' si̇yah ',
                   ' ci̇ft ', ' motors ', ' onun ', ' makam ', ' kararan ', ' dikiz ', ' olur. ', ' perde ',
                   ' adapti̇f ', ' yikama ',
                   ' kamera ', ' freni̇ ', ' yonlu ', ' uzaktan ', ' blok ', ' farlar ', ' doseme ', ' garanti̇li̇ ',
                   ' soz ', ' 2. ',
                   ' sahibiyim ', ' sifirdan ', ' degil ', ' sey ', ' kis ', ' di̇r ', ' tertemi̇z ', ' lira ',
                   ' sene ', ' cila ',
                   ' seti ', ' isitma ', ' sikinti ', ' hidrolik ', ' ayarli ', ' kaplama ', ' navigasyon ', ' 100 ',
                   ' x ', ' 19 ',
                   ' 2.0 ', ' atma ', ' yakma ', ' kumanda ', ' teyp ', ' kayisi ', ' krom ', ' duyarli ',
                   ' yuksekli̇k ', ' ayari ',
                   ' ciddi ', ' taksi̇t ', ' verilecektir. ', ' stoplar ', ' dijital ', ' buyuk ', ' dahi̇l ', ' diri ',
                   ' yeni̇di̇r ',
                   ' deformasyon ', ' alicilar ', ' konusu ', ' torpi̇do ', ' bej ', ' fi̇rmamiz ', ' aksaminda ',
                   ' durumdadir ',
                   ' sogutmali ', ' o ', ' kartina ', ' sport ', ' 20 ', ' hayalet ', ' ambi̇yans ', ' koltuklarda ',
                   ' gosterge ',
                   ' elekti̇ri̇kli̇ ', ' paketi̇ ', ' kisa ', ' hafizali ', ' mekani̇k ', ' hold ', ' ne ',
                   ' panorami̇k ', ' asi̇stani ',
                   ' yorgunluk ', ' onarka ', ' sikintisiz ', ' yani ', ' ozenle ', ' a ', ' isik ', ' bile ', ' • ',
                   ' bmw ',
                   ' mercedes ', ' honda ', ' comfort ', ' f1 ', ' · ', ' passat ', ' tdi ', ' m ', ' dsg ', ' amg ',
                   ' tdi̇ ',
                   ' volkswagen ', ' audi̇ ',
                                   ' 2017 ', '2017', ' 2017', '2017 ', ' 2016 ', '2016', ' 2016', '2016 ', ' aracim ',
                   'aracim ',
                   ' aracimizda ', 'aracimizda ', 'aracimin ', ' aracimin ', ' kislik ', 'kislik ', '. ', 'sensoru ',
                   ' . ',
                   ' sensoru ', ' piril ', 'piril ',
                   ' gosterebi̇li̇rsi̇ni̇z ', 'gostere bi̇li̇rsi̇ni̇z ', ' pakettir ', 'pakettir ', ' sahibinden ',
                   'sahibinden ', ' mah ',
                   'mah ', 'zaten ', ' zaten ', ' arabasi ', 'arabasi ', ' aracimda ', 'aracimda ', ' olur ', 'olur ',
                   ' ci̇la ', 'ci̇la ', ' aracin ', 'aracin ', ' oldu ', '...', ' alinmistir ', 'alinmistir ',
                   ' hazir ', 'hazir ', ' gosterebilirsiniz ', ' s ',
                   ' arasi ', 'arasi ', '..', ' bg ', ' 2.el ', ' vb ', ' ayarindadir ', ' arayiniz ', ' yukseltmek ',
                   ' vs ', ' olsun ',
                   ' cli̇o ', ' dci̇ ', ' edc ', ' multi̇medya ', ' i̇rti̇bat ', ' 0533 ', ' 45 ', ' 0212 ',
                   ' kefi̇lsi̇z ', ' evraksiz ', ' hi̇zmeti̇ni̇zdeyi̇z ', ' clio ', ' motor ', ' problem ', ' fakat ',
                   ' 3000 ', ' megane ', ' joy ', ' fabrika ', ' kokusu ', ' ustunde ', ' bayi ', ' faturalari ',
                   ' 2020 ', ' 2005 ', ' ozellikler ', ' gelen ', ' uzeri̇nde ', ' koltuklari ', ' eksperti̇ze ',
                   ' aciktir ', ' 60 ', ' seti̇ ', ' ai̇le ', ' beygi̇r ', ' duzenli̇ ', ' karti ', ' sinirlayici ',
                   ' acma ', ' usbaux ', ' mod ', ' 06 ', ' tarihi ', ' boyanan ', ' 24 ', ' ayarlanabilir ',
                   ' i̇ki̇nci̇ ', ' motorlu ', ' yetki̇ ', ' num ', ' hi̇zmet ', ' lasti̇gi̇ ', ' symbol ', ' 13 ',
                   ' kdv ',
                   ' garanti̇ ', ' 2004 ', ' belli ', ' garantili ', ' miktarda ', ' 75 ', ' ki ', ' 110 ', ' kirmizi ',
                   ' ozelli̇k ', ' aracidir ', ' kendi̇ ', ' hazirdir ', ' beygir ', ' ekonomik ', ' cimrisi ',
                   ' temizlikte ',
                   ' anahtarlari ', ' kilometresi ', ' banka ', ' yapilir ', ' sifir ', ' aninda ', ' yolu ',
                   ' ankara ', ' 44 ', ' 11 ', ' 00 ', ' memnunum ', ' benzi̇n ', ' analog ', ' tari̇hi̇ne ',
                   ' yaptirabi̇li̇rsi̇ni̇z ', ' 55 ', ' sanzimani ', ' yapmaz ', ' fatura ', ' emsalsi̇z ', ' sorgusu ',
                   ' bi̇rsey ', ' durumunda ', ' masraflariniz ', ' ai̇tti̇r ', ' olmak ', ' turlu ', ' ekspertize ',
                   ' servi̇si̇nde ', ' suan ', ' gosterebilir ', ' nakit ', ' 2015 ', ' i̇ceri̇si̇nde ', ' kismi ',
                   ' tas ', ' sehi̇r ', ' disindan ', ' 532 ', ' paketti̇r ', ' 2014 ', ' dur ', ' 95 ', ' ori̇ji̇nal ',
                   ' cad ', ' i̇ci ', ' oncelikle ', ' merhaba ', ' modeldir ', ' ise ', ' performans ',
                   ' karistirmayin ',
                   ' kablosuz ', ' araci ', ' istenilen ', ' ucunda ', ' 2007 ', ' lansman ', ' rengi ', ' torpido ',
                   ' sogutma ', ' buji ', ' parcalari ', ' di̇r ', ' olmasi ', ' dci ', ' yipranma ', ' bazi ',
                   ' modeli ',
                   ' 150 ', ' arkadasa ', ' degisimi ', ' yillik ', ' benden ', ' aldigimda ', ' durum ', ' alindi ',
                   ' aylik ',
                   ' di̇reksi̇yondan ', ' onleme ', ' araclariniz ', ' fiat ', ' guvencesi̇yle ', ' araclarimizin ',
                   ' 70 ', ' koc ',
                   ' fi̇at ', ' arasinda ', ' kayitlari ', ' eksiksiz ', ' experti̇ze ', ' arayiniz ', ' acigiz ',
                   ' sedan ',
                   ' temi̇zli̇gi̇ ', ' masrafsizdir ', ' aracda ', ' km’de ', ' fotograflari ', ' i̇mmobi̇li̇zer ',
                   ' baglanti ',
                   ' gi̇bi̇di̇r ', ' araclarimizi ', ' degeri̇nde ', ' alinir ', ' ki̇lometresi̇ ', ' alim ',
                   ' etmeden ', ' telefonda ',
                   ' 36 ', ' fiyati ', ' araclarimiza ', ' vizesi ', ' yasina ', ' araclara ', ' tari̇hi̇ ',
                   ' asagida ', ' 2012 ',
                   ' ta ', ' 500 ', ' dolusu ', ' si̇z ', ' seki̇lde ', ' degi̇si̇k ', ' sahi̇bi̇nden ',
                   ' takilmamistir ',
                   ' yenidir ', ' – ', ' icilmemistir ', ' temizligi ', ' tarihinde ', ' ozelligi ', ' acil ',
                   ' konfor ',
                   ' multimedya ', ' orta ', ' yakin ', ' curuk ', ' plastik ', ' alici ', ' gelecek ', ' rahatligi ',
                   ' tanki ', ' si̇ ', ' dosemeleri̇ ', ' alasim ', ' 2013 ', ' 25 ', ' gunluk ', ' 2001 ',
                   ' balatalar ', ' 14 ',
                   ' temiz ', ' 2011 ', ' filtre ', ' birsey ', ' masraflar ', ' siz ', ' trafi̇k ', ' olur. ',
                   ' bulunan ',
                   ' sarj ', ' binilecek ', ' yerinde ', ' normal ', ' bakimlarini ',
                   ' koyup ', ' calisiyor ', ' otomoti̇vden ', ' sahibine ', ' stepne ', ' a.s ',
                   ' degerlendi̇ri̇li̇r ', ' sanruf ', ' satislar ', ' cm ', ' si̇stem ', ' ti̇caret ', ' dahi̇ ',
                   ' modeli̇di̇r ',
                   ' hem ', ' sinirlama ', ' noter ', ' geregi ', ' aracima ', ' aracimiza ', ' herseyi ', ' muayne ',
                   ' guncel ', ' masraflari ', ' hoparlor ', ' yenilendi ', ' degistirildi ', ' yazlik ',
                   ' calisir ', ' fotolarda ', ' aci̇l ', ' gaz ', ' orjinal ', ' cuzi ', ' sorgulama ', ' hafif ',
                   ' cikisi ', ' iyidir ', ' rahat ', ' aksatilmadan ', ' isofi̇x ', ' gecerli̇di̇r ', ' whatsapp ',
                   ' 85 ',
                   ' aksamlari ', ' aldigim ', ' polen ', ' hersey ', ' balatasi ', ' konusunda ', ' standart ',
                   ' karartmali ',
                   ' degeri̇ ', ' i̇s ', ' 0530 ', ' sirali ', ' kullanilmamis ', ' gorulmeye ', ' deger ',
                   ' kisminda ',
                   ' teslim ', ' modelidir ', ' giris ', ' freni ', ' d ', ' 2006 ', ' yoluyla ', ' arabasidir ',
                   ' dosta ',
                   ' turkce ', ' galeri̇ci̇ler ', ' si̇tesi̇ ', ' sensorleri̇ ', ' alarm ', ' sanzumani ',
                   ' sorunsuzdur ',
                   ' yakiti ', ' tesli̇m ', ' bucuk ', ' kullaniyorum ', ' garajda ', ' seramik ', ' beri ',
                   ' kullanim ',
                   ' yuzden ', ' tarihine ', ' teklif ', ' star ', ' rot ', ' degi̇smi̇s ', ' aynalari ', ' ileri ',
                   ' gecen ',
                   ' gorundugu ', ' bana ', ' ekranli ', ' dosemeleri̇nde ', ' cevap ', ' iletisime ', ' degerinde ',
                   ' otomotiv ', ' 23 ', ' yukseklik ', ' akilli ', ' girisi ', ' lambalari ', ' kollari ', ' lambasi ',
                   ' detay ', ' ya ', ' ikinci ', ' oldugumuz ', ' c ', ' yili ', ' ediyor ', ' lt ', ' ucu ',
                   ' derece ',
                   ' ustu ', ' boyalari ', ' cikiyor ', ' mevcut ', ' kisiye ', ' duman ', ' yapilan ', ' v ',
                   ' fabri̇kasyon ',
                   ' yaptirdim ', ' turki̇ye ', ' plakasi ', ' ebd ', ' kullanilmamistir ', ' hiza ', ' muzi̇k ',
                   ' durmaktadir ',
                   ' sunnettir ', ' korumasi ', ' bunun ', ' kasasi ', ' 4 ', ' lik ', ' aldim ', ' arabam ',
                   ' aractir ',
                   ' li ', ' kredi̇ni̇z ', ' arayin ', ' vadeli̇ ', ' trafik ', ' ekrani ', ' veri̇lecekti̇r ',
                   ' paspas ', ' dedir ',
                   ' aracimizi ', ' karsilanacaktir ', ' 2018 ', ' play ', ' bircok ', ' ozellik ', ' 2008 ',
                   ' trafi̇ge ',
                   ' kac ', ' yillar ', ' yasi ', ' dosemeleri ', ' i̇cinde ', ' fi̇yati ', ' digital ', ' kartlarina ',
                   ' gormek ', ' kart ', ' ledli̇ ', ' sistem ', ' arabanin ', ' kullandigim ', ' gecisleri ',
                   ' periyodik ',
                   ' hemen ', ' amacli ', ' kuafor ', ' vs. ', ' ariza ', ' gostergesi̇ ', ' deri̇nli̇k ', ' detayi ',
                   ' egzoz ',
                   ' keyless ', ' dosemeler ', ' modlari ', ' di̇gi̇tal ', ' satisi ', ' kredi̇si̇ ', ' yapilmaktadir ',
                   ' 10.000 ', ' rengi̇ ', ' gazi ', ' bakimlar ', ' etmektedi̇r ', ' apple ', ' ki̇tapcigi ',
                   ' bayi̇i̇ ',
                   ' panel ', ' fi̇yat ', ' tutulan ', ' cikmistir ', ' dokunmatik ', ' muzik ', ' black ',
                   ' tarafimizdan ',
                   ' temi̇zli̇kte ', ' temi̇zdi̇r ', ' asla ', ' sayamadigim ', ' aramasin ', ' bagajda ', ' alip ',
                   ' klimasi ',
                   ' destekli̇ ', ' faturasi ', ' disk ', ' ci̇ddi̇ ', ' ki̇li̇di̇ ', ' yeni̇di̇r ', ' azda ',
                   ' aleykum ',
                   ' 2009 ', ' 92 ', ' 1000 ', ' para ', ' amerikan ', ' genis ', ' yardim ', ' brc ', ' sahibiyim ',
                   ' si ', ' gelip ', ' bi̇nde ', ' 50 ', ' yilinda ', ' paspaslar ', ' edi̇ti̇on ', ' sokuk ', ' go ',
                   ' fonksi̇yonlu ', ' klimali ', ' mekanik ', ' isteyen ', ' olabilir ', ' kisacasi ', ' oluculer ',
                   ' renkli̇ ', ' sd ', ' kitapcigi ', ' ki̇si̇ ', ' siyah ', ' film ', ' al ', ' alumi̇nyum ',
                   ' hakkinda ', ' aracla ', ' gunu ', ' tertemizdir ', ' 3m ', ' ancak ', ' satisimiz ', ' kadardir ',
                   ' sahip ', ' sigorta ', ' donanimlar ', ' paneli̇ ', ' vi̇raj ', ' tespi̇t ', ' i̇lk ', ' v.s ',
                   ' uygulamasi ',
                   ' bilgileri ', ' dilediginiz ', ' fabri̇ka ', ' jetta ', ' 1500 ', ' yazdim ', ' li̇ ', ' serami̇k ',
                   ' farki ', ' takilan ', ' far ', ' 35 ', ' kalan ', ' vize ', ' isteyene ', ' yilina ', ' yaklasik ',
                   ' tane ', ' servise ', ' i̇stediginiz ', ' sure ', ' r ', ' evraklari ', ' daki̇kada ',
                   ' i̇steyene ',
                   ' takildi ', ' tiklayiniz ', ' si̇gorta ', ' nesi̇l ', ' kor ', ' uyari ', ' sahiptir ', ' 1 ',
                   ' icerisinde ',
                   ' yer ', ' atiker ', ' tasit ', ' 120 ', ' kefilim ', ' gecerlidir ', ' 40 ', ' bank ', ' ✅ ',
                   ' dosemelerinde ', ' gece ', ' immobilizer ', ' focus ', ' 200 ', ' z ', ' makul ', ' aractir. ',
                   ' inc ', ' ozelli̇gi̇ ', ' tarafimca ', ' borusan ', ' gri̇ ', ' ₺ ', ' trend ', ' kollu ',
                   ' kullanildi ', ' detaylar ', ' hyundai ', ' tum ', ' distan ', ' kayar ', ' karartilmis ',
                   ' style ', ' asistani ', ' polo ', ' bi̇xenon ', ' aydinlatmasi ', ' birlikte ', ' skoda ',
                   ' koltuklar ',
                   ' bolgeli̇ ', ' hyundai̇ ', ' elegance ', ' bixenon ', ' onleyi̇ci̇ ', ' astra ', ' elektrokrom ',
                   ' audi ',
                   ' golf ', ' hafiza ', ' seat ', ' seri̇t ', ' li̇ne ', ' a3 ', ' recaro ', ' comfortline ', ' tsi ',
                   ' comfortli̇ne ', ' dogus ', ' ahsap ', ' tsi̇ ', ' egea ', ' corolla ', ' vakumlu ', ' corsa ',
                   ' 2020 ', '2020 ' ' 2015 ', '2015 ', ' 2014 ', '2014 ', ' araci ', 'araci ', ' arayiniz ',
                   'arayiniz ',
                   ' 2012 ', '2012 ', ' sahi̇bi̇nden ', 'sahi̇bi̇nden ', ' 2013 ', '2013 ', 'temiz ',
                   ' temiz ', ' 2011 ', '2011 ', ' yuzde ', 'yuzde ', ' 98 ', ' 2018 ', '2018 ', ' i̇lk ', 'i̇lk ',
                   ' olur. ',
                   ' olur.', ' merhaba ', 'merhaba ', ' elektirikli ', ' elektirikli '
                   ]
    remove_words = ["☑", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021",
                    "2022", "2023", "1.6", "1.7", "2024",
                    "1.8", "2.0", "1.9", "1.0", "1.1", "1.2", "1.3", "1.4", "park", "marka"]

    def replacer(st):
        replaces = {"ş": "s", "ö": "o", "ü": "u", "ğ": "g", "ı": "i", "ç": "c"}
        for i in replaces:
            st = st.replace(i, replaces[i])
        return st

    def remove_pnc(text_data):
        text_data = text_data.lower()
        table = str.maketrans("", "", string.punctuation.replace(".", ""))
        cleaned = text_data.translate(table)
        cleaned = " ".join(cleaned.replace("\n", " ").split())
        cleaned = replacer(cleaned).split()
        res = []
        res_f = []
        for i in cleaned:
            for j in hasar_words:
                if j in i:
                    res.append(i)
                    break
            if i in exact_words:
                res.append(i)
        for i in res:
            if i not in remove_words:
                res_f.append(i)

        return res_f, cleaned

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
    # PROCESSING baslik PARAMETER
    baslik_cleaned = remove_pnc(baslik)
    # PROCESSING aciklama PARAMETER
    aciklama_cleaned, aciklama_half_cleaned = remove_pnc(aciklama)
    # print(aciklama)
    """print("a")
    print(aciklama)
    print(aciklama_cleaned)"""
    return baslik_cleaned, aciklama_cleaned, aciklama_half_cleaned


def word_finder_dummy():
    connection, cursor = db_connection.connect_db()

    cursor.execute("SELECT * FROM firsatarabam.public.sahibinden_raw_data WHERE 'renk'!='done'")
    selected = cursor.fetchall()
    connection.close()
    out = open("output.txt", "w", encoding="utf8")
    for i in selected:
        baslik, aciklama, hasar_kaydi = hasar_processor(i[2], i[15], i[16], "sahibinden")
        print("\n")
        print(hasar_kaydi)
        print(aciklama)
        print(aciklama, file=out, flush=True)
    out.close()

"""
def word_finder_dummy():
    data = []
    connection, cursor = db_connection.connect_db()

    cursor.execute("SELECT * FROM firsatarabam.public.sahibinden_raw_data WHERE 'renk'!='done'")
    selected = cursor.fetchall()
    connection.close()
    words = {}
    out = open("output.txt", "w", encoding="utf8")
    for i in selected:
        baslik, aciklama, hasar_kaydi = hasar_processor(i[2], i[15], i[16], "sahibinden")
        data.append(aciklama)
    for i in data:
        word = i.split()
        for j in word:
            if j in words:
                words[j] = words[j] + 1
            else:
                words[j] = 0
    for i in words:
        print(i, words[i], file=out)
    out.close()"""
start = time.time()
word_finder_dummy()
print(time.time() - start)