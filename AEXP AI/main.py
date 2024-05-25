import json
from difflib import get_close_matches as yakinsonuc
from datetime import datetime
import os

def kullaniciVtYukle(kullanici):
    dosyayolu = f'{kullanici}_veritabani.json'
    if os.path.exists(dosyayolu):
        with open(dosyayolu, 'r') as dosya:
            return json.load(dosya)
    else:
        print("Kullanıcı veritabanı bulunamadı. Yeni bir veritabanı oluşturulacak.")
        return {"sorular": []}

def kullaniciVtKaydet(kullanici, veritabani):
    dosyayolu = f'{kullanici}_veritabani.json'
    with open(dosyayolu, 'w') as dosya:
        json.dump(veritabani, dosya, indent=2)

def kullaniciVtSifirla(kullanici):
    dosyayolu = f'{kullanici}_veritabani.json'
    with open(dosyayolu, 'w') as dosya:
        json.dump({"sorular": []}, dosya, indent=2)

def yakinCevap(soru, sorular):
    eslesen = yakinsonuc(soru, sorular, n=1, cutoff=0.6)
    return eslesen[0] if eslesen else None

def kullaniciCevapBul(soru, veritabani):
    for cevaplar in veritabani["sorular"]:
        if cevaplar["soru"] == soru:
            return cevaplar["cevap"], cevaplar.get("eklenmetarihi", "Bilinmiyor")
    return None, None

def yeniSoruEkle(kullanici, soru, cevap, veritabani):
    tarih = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    veritabani["sorular"].append({"soru": soru, "cevap": cevap, "eklenmetarihi": tarih})
    kullaniciVtKaydet(kullanici, veritabani)

def vtleriListele():
    print("Şuana kadar oluşturulan kullanıcı veritabanı adları:")
    dosya_adlari = [dosya for dosya in os.listdir() if dosya.endswith("_veritabani.json")]
    for dosya_adı in dosya_adlari:
        print(dosya_adı[:-17])

def kullaniciKaydi():
    while True:
        kullanici = input("Kullanıcı Adı: ")
        sifre = input("Şifre: ")

        with open('veritabani.json', 'r') as dosya:
            kullanici_veritabani = json.load(dosya)

        if kullanici in kullanici_veritabani:
            print("Bu kullanıcı adı zaten mevcut. Başka bir kullanıcı adı seçin.")
        else:
            kullanici_veritabani[kullanici] = sifre
            with open('veritabani.json', 'w') as dosya:
                json.dump(kullanici_veritabani, dosya, indent=2)
            print("Kullanıcı kaydı başarıyla oluşturuldu.")
            return kullanici

def kullaniciGirisi():
    while True:
        kullanici = input("Kullanıcı Adı: ")
        sifre = input("Şifre: ")

        with open('veritabani.json', 'r') as dosya:
            kullanici_veritabani = json.load(dosya)

        if kullanici in kullanici_veritabani and kullanici_veritabani[kullanici] == sifre:
            return kullanici
        else:
            print("Hatalı kullanıcı adı veya şifre. Tekrar deneyin.")

vtleriListele()

if __name__ == '__main__':
    print("Giriş yapmak için:")
    print("1-Yeni Kullanıcı Kaydı Oluştur")
    print("2-Giriş Yap")
    secim = input("Seçiminiz: ")

    if secim == '1':
        kullanici = kullaniciKaydi()
    elif secim == '2':
        kullanici = kullaniciGirisi()
    else:
        print("Geçersiz seçim. Program sonlandırılıyor.")
        exit()

    kullanici_veritabani = kullaniciVtYukle(kullanici)

    while True:
        soru = input("Siz: ")
        if soru == 'çık':
            break
        elif soru.startswith('VT sıfırla:'):
            sorusil = soru.replace('VT sıfırla:', '').strip()
            kullaniciVtSifirla(kullanici)
            print(f"AEXP AI: '{sorusil}' sorusu ve cevabı veritabanından silindi.")
        elif soru.startswith('VT ne zaman:'):
            sorgu_soru = soru.replace('VT ne zaman:', '').strip()
            cevap, eklenmetarihi = kullaniciCevapBul(sorgu_soru, kullanici_veritabani)
            if cevap:
                print(f"AEXP AI: '{sorgu_soru}' sorusunun cevabını {eklenmetarihi} tarihinde öğrendim. Cevap: {cevap}")
            else:
                print(f"AEXP AI: '{sorgu_soru}' sorusunun cevabı veritabanında bulunamadı.")
        else:
            gelencevap = yakinCevap(soru, [cevaplar["soru"] for cevaplar in kullanici_veritabani["sorular"]])
            if gelencevap:
                verilecekcevap = kullaniciCevapBul(gelencevap, kullanici_veritabani)
                print(f"AEXP AI: {verilecekcevap[0]}")
            else:
                print("AEXP AI: Bunu nasıl cevaplayacağımı bilmiyorum. Öğretir misiniz?")
                yenicevap = input("Öğretmek için yazabilir veya 'geç' diyebilirsiniz:  ")

                if yenicevap != 'geç':
                    yeniSoruEkle(kullanici, soru, yenicevap, kullanici_veritabani)
                    print("AEXP AI: Teşekkürler, sayenizde yeni bir şey öğrendim.")