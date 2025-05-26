# pages/ticimax_fiyat_cek.py
import streamlit as st
import pandas as pd
from zeep import Client
import os

st.title("Ticimax Fiyat Güncelleme")

# CSV yolu
csv_path = "pages/veri_kaynaklari/ana_urun_listesi.csv"

# SOAP bağlantısı
wsdl_url = "https://ws.ticimax.com/Service.asmx?WSDL"
client = Client(wsdl=wsdl_url)

# Yetki kodu (Ticimax tarafından verilir)
uye_kodu = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"

# SOAP parametreleri
filtre = {
    "Aktif": -1,
    "Firsat": -1,
    "Indirimli": -1,
    "Vitrin": -1,
    "KategoriID": 0,
    "MarkaID": 0,
    "TedarikciID": -1,
    "ToplamStokAdediBas": 0,
    "ToplamStokAdediSon": 100000
}
sirala = {
    "BaslangicIndex": 0,
    "KayitSayisi": 1000,
    "SiralamaDegeri": "ID",
    "SiralamaYonu": "DESC"
}

# Ürünleri çek
try:
    response = client.service.SelectUrun(UyeKodu=uye_kodu, f=filtre, s=sirala)
    if not response:
        st.error("Ticimax'ten yanıt alınamadı.")
    else:
        ticimax_urunler = response.SelectUrunResult.TicimaxUrunDetaylari.TicimaxUrunDetay
        data = []
        for urun in ticimax_urunler:
            data.append({
                "StokKodu": urun.StokKodu,
                "SatisFiyati": urun.SatisFiyati
            })
        fiyat_df = pd.DataFrame(data)

        # Ana tabloyu oku
        ana_df = pd.read_csv(csv_path)

        # Satış fiyatlarını eşleştir
        ana_df = ana_df.merge(fiyat_df, how="left", left_on="Stok Kodu", right_on="StokKodu")
        ana_df["Ofis26 Satış Fiyatı"] = ana_df["SatisFiyati"]
        ana_df.drop(columns=["StokKodu", "SatisFiyati"], inplace=True)

        # Güncellenmiş tabloyu kaydet
        ana_df.to_csv(csv_path, index=False)
        st.success("Ofis26 Satış Fiyatı başarıyla güncellendi!")
        st.dataframe(ana_df)

except Exception as e:
    st.error(f"Hata oluştu: {e}")
