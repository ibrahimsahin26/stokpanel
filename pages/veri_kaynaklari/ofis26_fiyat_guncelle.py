
import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport
import ast  # Güvenli string -> dict dönüşümü

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
        "SiralamaYonu": "DESC"
    }

    try:
        sonuc = client.service.SelectUrun(UyeKodu=UYE_KODU, f=urun_filtresi, s=sayfalama)
        urun_listesi = getattr(sonuc, "UrunListesi", None)

        if urun_listesi is None:
            st.warning("Ticimax: Ürün verisi alınamadı.")
            return

        df = pd.read_csv(CSV_YOLU)
        fiyat_verileri = {}

        for urun in urun_listesi:
            try:
                fiyat_verileri[urun.UrunKodu] = urun.SatisFiyati
            except:
                continue

        df["satis_fiyati_ofis26"] = df["Stok Kodu"].map(fiyat_verileri)
        df.to_csv(CSV_YOLU, index=False)
        st.success("Ofis26 satış fiyatları başarıyla güncellendi.")

    except Exception as e:
        st.error(f"Ticimax servisinden veri alınamadı: {e}")
        return

# Butonla çağırmak için arayüz kısmı
st.title("📦 Ofis26 Satış Fiyatlarını Güncelle")
if st.button("Fiyatları Güncelle"):
    ticimax_satis_fiyatlarini_guncelle()
