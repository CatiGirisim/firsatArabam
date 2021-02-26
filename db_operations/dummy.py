degisen_dict = {'Sol Ön Kapı': 'sol_on_kapı',
                'Sol Arka Kapı': 'sol_arka_kapı',
                'Sol Ön Çamurluk': 'sol_on_camurluk',
                'Sol Arka Çamurluk': 'sol_arka_camurluk',
                'Arka Tampon': 'arka_tampon',
                'Arka Kaput': 'arka_kaput',
                'Ön Tampon': 'on_tampon',
                'Sağ Ön Çamurluk': 'sag_on_camurluk',
                'Motor Kaputu': 'motor_kaputu',
                'Sağ Ön Kapı': 'sag_on_kapı',
                'Sağ Arka Kapı': 'sag_arka_kapı',
                'Sağ Arka Çamurluk': 'sag_arka_camurluk',
                'Tavan': 'tavan'}
def replacer(a):
    a = a.lower()
    a = a.replace("ö", "o")
    a = a.replace("ç", "c")
    a = a.replace("ğ", "g")
    a = "_".join(a.split())
    return a
for i in degisen_dict:
    degisen_dict[i] = replacer(i)
for i in degisen_dict:
    print(degisen_dict[i] + "_boyali int,")
    print(degisen_dict[i] + "_degisen int,")
"""
CREATE TABLE public.model_weighted
(ilan_no int NOT NULL,
fiyat int,
yil int,
vites int,
km int,
beygir int,
cc int,
sol_on_kapı_boyali int,
sol_on_kapı_degisen int,
sol_arka_kapı_boyali int,
sol_arka_kapı_degisen int,
sol_on_camurluk_boyali int,
sol_on_camurluk_degisen int,
sol_arka_camurluk_boyali int,
sol_arka_camurluk_degisen int,
arka_tampon_boyali int,
arka_tampon_degisen int,
arka_kaput_boyali int,
arka_kaput_degisen int,
on_tampon_boyali int,
on_tampon_degisen int,
sag_on_camurluk_boyali int,
sag_on_camurluk_degisen int,
motor_kaputu_boyali int,
motor_kaputu_degisen int,
sag_on_kapı_boyali int,
sag_on_kapı_degisen int,
sag_arka_kapı_boyali int,
sag_arka_kapı_degisen int,
sag_arka_camurluk_boyali int,
sag_arka_camurluk_degisen int,
tavan_boyali int,
tavan_degisen int,
PRIMARY KEY (ilan_no))
"""