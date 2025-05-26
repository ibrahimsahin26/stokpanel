import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

st.title("Ticimax Ofis26 Satış Fiyatı Güncelle")

# Ana ürün listesini yükle
csv_path = "pages/veri_kaynaklari/ana_urun_listesi.csv"
df = pd.read_csv(csv_path)

# Butonla işlemi tetikle
if st.button("Ticimax Ofis26 Satış Fiyatlarını Güncelle"):
    st.info("Ticimax API'den satış fiyatları çekiliyor...")

    # SOAP API ayarları
    url = "https://ofis26.ticimax.com/servis/servis.asmx"
    headers = {"Content-Type": "text/xml; charset=utf-8", "SOAPAction": "http://tempuri.org/SelectUrun"}

    uye_kodu = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"
    baslangic_index = 0
    kayit_sayisi = 100
    fiyatlar = {}

    while True:
        # SOAP XML talebi
        payload = f"""<?xml version="1.0" encoding="utf-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/" xmlns:ns="http://schemas.datacontract.org/2004/07/">
   <soapenv:Header/>
   <soapenv:Body>
      <tem:SelectUrun>
         <tem:UyeKodu>{uye_kodu}</tem:UyeKodu>
         <tem:f>
            <ns:Aktif>-1</ns:Aktif>
            <ns:Firsat>-1</ns:Firsat>
            <ns:Indirimli>-1</ns:Indirimli>
            <ns:Vitrin>-1</ns:Vitrin>
            <ns:KategoriID>0</ns:KategoriID>
            <ns:MarkaID>0</ns:MarkaID>
            <ns:TedarikciID>-1</ns:TedarikciID>
            <ns:ToplamStokAdediBas>0</ns:ToplamStokAdediBas>
            <ns:ToplamStokAdediSon>100000</ns:ToplamStokAdediSon>
            <ns:UrunKartiID>0</ns:UrunKartiID>
         </tem:f>
         <tem:s>
            <ns:BaslangicIndex>{baslangic_index}</ns:BaslangicIndex>
            <ns:KayitSayisi>{kayit_sayisi}</ns:KayitSayisi>
            <ns:SiralamaDegeri>ID</ns:SiralamaDegeri>
            <ns:SiralamaYonu>DESC</ns:SiralamaYonu>
         </tem:s>
      </tem:SelectUrun>
   </soapenv:Body>
</soapenv:Envelope>"""

        response = requests.post(url, data=payload, headers=headers)
        soup = BeautifulSoup(response.content, 'xml')
        urunler = soup.find_all("Urun")

        if not urunler:
            break  # Daha fazla kayıt yok

        for urun in urunler:
            stok_kodu = urun.find("StokKodu")
            satis_fiyati = urun.find("SatisFiyati")
            if stok_kodu and satis_fiyati:
                fiyatlar[stok_kodu.text.strip()] = float(satis_fiyati.text.strip())

        baslangic_index += kayit_sayisi

    # Ana tabloya satış fiyatlarını yaz
    df["Ofis26 Satış Fiyatı"] = df["Stok Kodu"].apply(lambda x: fiyatlar.get(str(x), ""))

    # Güncel tabloyu göster
    st.success("Satış fiyatları güncellendi.")
    st.dataframe(df)

    # Güncel CSV'ye yaz
    df.to_csv(csv_path, index=False)
    st.info("CSV dosyasına yazıldı.")
