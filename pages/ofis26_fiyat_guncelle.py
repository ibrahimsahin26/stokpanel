import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport
import ast

# Servis bilgileri
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

def ticimax_satis_fiyatlarini_guncelle():
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
        "SiralamaYon": "DESC"
    }

    try:
        sonuc = client.service.SelectUrun(UyeKodu=UYE_KODU, f=urun_filtresi, s=sayfalama)
        urun_listesi = getattr(sonuc, "UrunListesi", None)
        st.write("✅ Ürün verisi çekildi.")

        if urun_listesi is None:
            st.error("❌ UrunListesi boş geldi. Lütfen filtreleri kontrol edin.")
            return

        df_api = pd.DataFrame([{
            "StokKodu": urun.UrunKartiKod,
            "Ticimax_SatisFiyati": urun.SatisFiyati
        } for urun in urun_listesi])

        df_panel = pd.read_csv(CSV_YOLU)
        df_birlesik = df_panel.merge(df_api, left_on="Stok Kodu", right_on="StokKodu", how="left")

        st.dataframe(df_birlesik)
        df_birlesik.to_csv(CSV_YOLU, index=False)
        st.success("✅ Satış fiyatları başarıyla güncellendi ve dosyaya kaydedildi.")

    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")
