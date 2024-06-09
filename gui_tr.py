import json
import os
from difflib import get_close_matches as yakinsonuc
from datetime import datetime
from customtkinter import *

def ikonekle(pencere):
    pencere.iconbitmap('AEXP AI Logo.ico')

anaPencere = CTk()
anaPencere.title('AEXP AI')
anaPencere.geometry('1366x768')
anaPencere.iconbitmap('AEXP AI Logo.ico')

def veritabaniYukle(dosyayolu):
    if os.path.exists(dosyayolu):
        with open(dosyayolu, 'r', encoding='utf-8') as dosya:
            return json.load(dosya)
    else:
        print(f"{dosyayolu} bulunamadı. Yeni bir veritabanı oluşturulacak.")
        return {"sorular": []}

def veritabaniKaydet(dosyayolu, veritabani):
    with open(dosyayolu, 'w', encoding='utf-8') as dosya:
        json.dump(veritabani, dosya, indent=2)

def kullaniciVtSifirla(kullanici):
    dosyayolu = f'{kullanici}_veritabani.json'
    with open(dosyayolu, 'w', encoding='utf-8') as dosya:
        json.dump({"sorular": []}, dosya, indent=2)

def yakinCevap(soru, sorular):
    eslesen = yakinsonuc(soru, sorular, n=1, cutoff=0.6)
    return eslesen[0] if eslesen else None

def kullaniciCevapBul(soru, veritabani):
    for cevaplar in veritabani["sorular"]:
        if cevaplar["soru"] == soru:
            return cevaplar["cevap"], cevaplar.get("eklenmetarihi", "Bilinmiyor")
    return None, None

def yeniSoruEkle(dosyayolu, soru, cevap, veritabani):
    tarih = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    veritabani["sorular"].append({"soru": soru, "cevap": cevap, "eklenmetarihi": tarih})
    veritabaniKaydet(dosyayolu, veritabani)

def kullaniciKaydi(kullanici, sifre):
    with open('veritabani.json', 'r', encoding='utf-8') as dosya:
        kullanici_veritabani = json.load(dosya)

    if kullanici in kullanici_veritabani:
        return False
    else:
        kullanici_veritabani[kullanici] = sifre
        with open('veritabani.json', 'w', encoding='utf-8') as dosya:
            json.dump(kullanici_veritabani, dosya, indent=2)
        return True

def kullaniciGirisi(kullanici, sifre):
    with open('veritabani.json', 'r', encoding='utf-8') as dosya:
        kullanici_veritabani = json.load(dosya)

    if kullanici in kullanici_veritabani and kullanici_veritabani[kullanici] == sifre:
        return True
    else:
        return False

def kullaniciGirisPenceresi():
    girisPencere = CTkToplevel()
    girisPencere.title('Kullanıcı Girişi')
    girisPencere.geometry('600x400')
    ikonekle(girisPencere)
    girisPencere.grab_set() 

    def giris():
        kullanicigiris = kullaniciAdi.get()
        sifregiris = sifre.get()
        if kullaniciGirisi(kullanicigiris, sifregiris):
            global kullanici
            global kullanici_veritabani
            kullanici = kullanicigiris
            kullanici_veritabani = veritabaniYukle(f'{kullanici}_veritabani.json')
            girisPencere.destroy()
            konusmaEkraniniGoster()
        else:
            hataYazisi.configure(text="Hatalı kullanıcı adı veya şifre")

    cerceve = CTkFrame(girisPencere, corner_radius=10)
    cerceve.pack(pady=20, padx=20, fill="both", expand=True)

    CTkLabel(cerceve, text="Kullanıcı Adı:", font=("Helvetica", 16)).pack(pady=10)
    kullaniciAdi = CTkEntry(cerceve)
    kullaniciAdi.pack(pady=10)
    
    CTkLabel(cerceve, text="Şifre:", font=("Helvetica", 16)).pack(pady=10)
    sifre = CTkEntry(cerceve, show="*")
    sifre.pack(pady=10)
    
    hataYazisi = CTkLabel(cerceve, text="", text_color="red")
    hataYazisi.pack(pady=10)
    
    CTkButton(cerceve, text="Giriş Yap", command=giris, fg_color="#1e90ff").pack(pady=10)

def kullaniciKayitPenceresi():
    kayitPencere = CTkToplevel()
    kayitPencere.geometry('600x400')
    kayitPencere.title("Kullanıcı Kaydı")
    ikonekle(kayitPencere)
    kayitPencere.grab_set()  

    def kayit():
        kayitAd = kullaniciAdi.get()
        kayitSifre = sifre.get()
        if kullaniciKaydi(kayitAd, kayitSifre):
            global kullanici
            global kullanici_veritabani
            kullanici = kayitAd
            kullanici_veritabani = veritabaniYukle(f'{kullanici}_veritabani.json')
            kayitPencere.destroy()
            konusmaEkraniniGoster()
        else:
            hataYazisi.configure(text="Bu kullanıcı adı zaten mevcut.")

    cerceve = CTkFrame(kayitPencere, corner_radius=10)
    cerceve.pack(pady=20, padx=20, fill="both", expand=True)

    CTkLabel(cerceve, text="Kullanıcı Adı:", font=("Helvetica", 16)).pack(pady=10)
    kullaniciAdi = CTkEntry(cerceve)
    kullaniciAdi.pack(pady=10)
    
    CTkLabel(cerceve, text="Şifre:", font=("Helvetica", 16)).pack(pady=10)
    sifre = CTkEntry(cerceve, show="*")
    sifre.pack(pady=10)
    
    hataYazisi = CTkLabel(cerceve, text="", text_color="red")
    hataYazisi.pack(pady=10)
    
    CTkButton(cerceve, text="Kayıt Ol", command=kayit, fg_color="#1e90ff").pack(pady=10)

def konusmaEkraniniGoster():
    soruPenceresi = CTkToplevel()
    soruPenceresi.title('Soru Penceresi')
    soruPenceresi.geometry('600x400')
    ikonekle(soruPenceresi)
    soruPenceresi.grab_set()

    def konus():
        kullaniciSoru = soruGirisi.get()
        if kullaniciSoru == 'çık':
            soruPenceresi.destroy()
            anaPencere.deiconify()
        else:
            gelencevap = yakinCevap(kullaniciSoru, [cevaplar["soru"] for cevaplar in kullanici_veritabani["sorular"]])
            if gelencevap:
                verilecekcevap, _ = kullaniciCevapBul(gelencevap, kullanici_veritabani)
                cevapYazisi.configure(text=f"AEXP AI: {verilecekcevap}")
            else:
                yenicevap = CTkInputDialog(text="Bunu nasıl cevaplayacağımı bilmiyorum. Öğretir misiniz?", title="AEXP AI").get_input()
                if yenicevap != 'geç':
                    if kullanici:
                        yeniSoruEkle(f'{kullanici}_veritabani.json', kullaniciSoru, yenicevap, kullanici_veritabani)
                    else:
                        yeniSoruEkle('veritabani.json', kullaniciSoru, yenicevap, kullanici_veritabani)
                    cevapYazisi.configure(text="AEXP AI: Teşekkürler, sayenizde yeni bir şey öğrendim.")

    cerceve = CTkFrame(soruPenceresi, corner_radius=10)
    cerceve.pack(pady=20, padx=20, fill="both", expand=True)

    soruGirisi = CTkEntry(cerceve, height=50, width=300)
    soruGirisi.pack(pady=10)
    
    CTkButton(cerceve, text="Sor", command=konus, fg_color="#1e90ff").pack(pady=10)
    cevapYazisi = CTkLabel(cerceve, text="", wraplength=500, font=("Helvetica", 14))
    cevapYazisi.pack(pady=20)

def cikis():
    anaPencere.destroy()

anacerceve = CTkFrame(anaPencere, corner_radius=10)
anacerceve.pack(pady=20, padx=20, fill="both", expand=True)

CTkLabel(anacerceve, text="AEXP AI", font=("Helvetica", 24, "bold")).pack(pady=20)
CTkButton(anacerceve, text="Kullanıcı Girişi", command=kullaniciGirisPenceresi, fg_color="#1e90ff", font=("Helvetica", 16)).pack(pady=10)
CTkButton(anacerceve, text="Kullanıcı Kaydı", command=kullaniciKayitPenceresi, fg_color="#1e90ff", font=("Helvetica", 16)).pack(pady=10)
CTkButton(anacerceve, text="Konuşmayı Aç", command=konusmaEkraniniGoster, fg_color="#1e90ff", font=("Helvetica", 16)).pack(pady=10)
CTkButton(anaPencere, text="Kapat", command=cikis).pack(side="top", anchor="se", padx=10, pady=10)

cevapYazisi = CTkLabel(anacerceve, text="", wraplength=1000, font=("Helvetica", 14))
cevapYazisi.pack(pady=20)

kullanici_veritabani = veritabaniYukle('veritabani.json')

anaPencere.mainloop()