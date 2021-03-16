from PIL import Image, ImageDraw, ImageFont

img = Image.open(r'C:\ilan_photos\templates\firsatarabam.jpg')

d =ImageDraw.Draw(img)
firsatAraci = "Renault Megane 1.5 dci Ambition"
yil = "2018"
ilanFiyat = "217000"
firsatArabamFiyat = "212000"
fiyatFarki = int(ilanFiyat) - int(firsatArabamFiyat)
fiyatFarkiStr = str(fiyatFarki)
arti = "+"
tl =  " TL"
km = "53000"
marka = "Renault"
seri = "Megane"
model = "Ambition"
yakit = "Benzin"
vites = "Otomatik"
kasa = "Hatchback"

fntCokBuyuk = ImageFont.truetype("arialbd.ttf", size=65)
fntBuyuk = ImageFont.truetype("arialbd.ttf", size=40)
fntOrta = ImageFont.truetype("arialbd.ttf", size=35)
fntKucuk = ImageFont.truetype("arial.ttf", size=30)

if len(firsatAraci) <= 26:
    d.text((120, 170), yil, font=fntBuyuk, fill=(0, 0, 0))
    d.text((220, 170), firsatAraci, font=fntBuyuk, fill=(0, 0, 0))
else:
    d.text((120, 155), yil, font=fntCokBuyuk, fill=(0, 0, 0))
    d.text((290, 152), marka +" "+ seri, font=fntOrta, fill=(0, 0, 0))
    d.text((290, 195), "1.5 dci "+model, font=fntOrta, fill=(0, 0, 0))

d.text((370,340), ilanFiyat+tl, font=fntBuyuk, fill=(0,0,0))
d.text((500,510), firsatArabamFiyat+tl, font=fntBuyuk, fill=(0,0,0))


d.text((580,660), yil, font=fntKucuk, fill=(0,0,0))
d.text((580,695), str(km), font=fntKucuk, fill=(0,0,0))
d.text((580,730), marka, font=fntKucuk, fill=(0,0,0))
d.text((580,765), seri, font=fntKucuk, fill=(0,0,0))
d.text((580,800), model, font=fntKucuk, fill=(0,0,0))
d.text((580,835), yakit, font=fntKucuk, fill=(0,0,0))
d.text((580,870), vites, font=fntKucuk, fill=(0,0,0))
d.text((580,905), kasa, font=fntKucuk, fill=(0,0,0))


img.show()