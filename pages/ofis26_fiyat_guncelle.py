import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

# Ayarlar
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

def satis_fiyatlarini_cek():
    client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))

    urun_filtresi = {
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

    sayfalama = {
        "BaslangicIndex": 0,
        "KayitSayisi": 100,
        "SiralamaDegeri": "ID",
        "SiralamaYonu": "DESC"
    }

    try:
        sonuc = client.service.SelectUrun(UyeKodu=UYE_KODU, f=urun_filtresi, s=sayfalama)

        if not sonuc or not hasattr(sonuc, 'UrunListesi'):
            return None, "Ürün verisi çekilemedi veya boş geldi."

        urunler = sonuc.UrunListesi

        # CSV'yi oku
        df = pd.read_csv(CSV_YOLU)

        # Güncelleme
        for urun in urunler:
            stok_kodu = urun.StokKodu
            fiyat = urun.SatisFiyati
            df.loc[df["Stok Kodu"] == stok_kodu, "Ofis26 Satış Fiyatı"] = fiyat

        # Kaydet
        df.to_csv(CSV_YOLU, index=False)
        return df, "Ofis26 satış fiyatları başarıyla güncellendi."

    except Exception as e:
        return None, f"Ürün verisi çekilirken hata oluştu: {e}"

# Streamlit Arayüz
st.header("🛒 Ticimax Ürün Fiyatlarını Güncelle")

if st.button("📄 Satış Fiyatlarını Ticimax'ten Çek"):
    df_gelen, mesaj = satis_fiyatlarini_cek()
    if df_gelen is not None:
        st.success(mesaj)
        st.dataframe(df_gelen)
    else:
        st.error(mesaj)
