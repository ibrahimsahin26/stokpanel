import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

# Ticimax WSDL ayarları
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

st.title("🛒 Ticimax Ürün Fiyatlarını Güncelle")

def satis_fiyatlarini_cek():
    try:
        # SOAP istemcisi oluştur
        client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))

        # Filtre tanımı
        urun_filtre = {
            "Aktif": -1,
            "Firsat": -1,
            "Indirimli": -1,
            "Vitrin": -1,
            "KategoriID": 0,
            "MarkaID": 0,
            "TedarikciID": -1,
            "ToplamStokAdediBas": 0,
            "ToplamStokAdediSon": 100,
            "UrunKartiID": 0
        }

        # Sayfalama tanımı
        urun_sayfalama = {
            "BaslangicIndex": 0,
            "KayitSayisi": 200,
            "SiralamaDegeri": "ID",
            "SiralamaYonu": "DESC"
        }

        # API çağrısı
        sonuc = client.service.SelectUrun(
            UyeKodu=UYE_KODU,
            f=urun_filtre,
            s=urun_sayfalama
        )

        # Gelen ürün listesi
        urunler = sonuc["UrunListesi"]

        if not urunler:
            return pd.DataFrame()

        # Ürünleri dataframe'e çevir
        veriler = []
        for urun in urunler:
            veriler.append({
                "StokKodu": urun["StokKodu"],
                "SatisFiyati": urun["VaryasyonListesi"][0]["SatisFiyati"] if urun["VaryasyonListesi"] else None
            })

        return pd.DataFrame(veriler)

    except Exception as e:
        st.error(f"Ürün verisi çekilirken hata oluştu: {e}")
        return pd.DataFrame()

if st.button("📉 Satış Fiyatlarını Ticimax'ten Çek"):
    df_csv = pd.read_csv(CSV_YOLU)
    df_fiyat = satis_fiyatlarini_cek()

    if df_fiyat.empty:
        st.warning("Ürün listesi boş veya çekilemedi.")
    else:
        # Eşleştir ve güncelle
        df_csv = df_csv.merge(df_fiyat, on="StokKodu", how="left")
        st.success("Satış fiyatları başarıyla eşleştirildi.")
        st.dataframe(df_csv)
