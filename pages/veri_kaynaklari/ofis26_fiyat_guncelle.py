
import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"

def satis_fiyati_guncelle(df):
    client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))

    urun_filtresi = {
        "Aktif": -1, "Firsat": -1, "Indirimli": -1, "Vitrin": -1,
        "KategoriID": 0, "MarkaID": 0, "TedarikciID": -1,
        "ToplamStokAdediBas": 0, "ToplamStokAdediSon": 100, "UrunKartiID": 0
    }

    sayfalama = {
        "BaslangicIndex": 0,
        "KayitSayisi": 100,
        "SiralamaDegeri": "ID",
        "SiralamaYonu": "DESC"
    }

    try:
        sonuc = client.service.SelectUrun(UyeKodu=UYE_KODU, f=urun_filtresi, s=sayfalama)
        urun_listesi = getattr(sonuc, "UrunListesi", None)
        if urun_listesi:
            for urun in urun_listesi:
                stok_kodu = getattr(urun, "StokKodu", None)
                satis_fiyati = getattr(urun, "SatisFiyati", None)
                if stok_kodu and satis_fiyati is not None:
                    df.loc[df["Stok Kodu"] == stok_kodu, "Ticimax Satis Fiyati"] = satis_fiyati
            return df
        else:
            st.warning("Ticimax yanıtı boş geldi.")
            return df
    except Exception as e:
        st.error(f"Hata oluştu: {str(e)}")
        return df
