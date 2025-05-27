
import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

def ticimax_satis_fiyatlarini_guncelle():
    try:
        df = pd.read_csv(CSV_YOLU)
        stok_kodlari = df["Stok Kodu"].dropna().astype(str).unique()[:100]

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
            "ToplamStokAdediSon": 9999,
            "UrunKartiID": 0
        }

        sayfalama = {
            "BaslangicIndex": 0,
            "KayitSayisi": 100,
            "SiralamaDegeri": "ID",
            "SiralamaYonu": "DESC"
        }

        sonuc = client.service.SelectUrun(UyeKodu=UYE_KODU, f=urun_filtresi, s=sayfalama)
        urun_listesi = getattr(sonuc, "UrunListesi", None)

        if not urun_listesi:
            st.error("❌ Ticimax yanıtı boş geldi. Filtreleri daraltmayı deneyin.")
            return

        guncel_dict = {}
        for urun in urun_listesi:
            kod = getattr(urun, "UrunKartiKod", None)
            fiyat = getattr(urun, "SatisFiyati", None)
            if kod and fiyat is not None and kod in stok_kodlari:
                guncel_dict[kod] = fiyat

        if "Ticimax_SatisFiyati" not in df.columns:
            df["Ticimax_SatisFiyati"] = None

        df["Ticimax_SatisFiyati"] = df.apply(
            lambda row: guncel_dict.get(str(row["Stok Kodu"]), row["Ticimax_SatisFiyati"]),
            axis=1
        )

        df.to_csv(CSV_YOLU, index=False)
        st.success("✅ İlk 100 ürünün fiyatı güncellendi.")
        st.dataframe(df.head(100))

    except Exception as e:
        st.error(f"🚨 Hata oluştu: {e}")
