import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport
import traceback

st.title("🔧 Kod başladı")

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
            "ToplamStokAdediSon": 100,
            "UrunKartiID": 0,
        }

        sayfalama = {
            "BaslangicIndex": 0,
            "KayitSayisi": 100,
            "KayitSayisinaGoreGetir": True,
            "SiralamaDegeri": "ID",
            "SiralamaYonu": "DESC"
        }

        st.write("🔍 Stok Kodları:")
        st.dataframe(pd.DataFrame(stok_kodlari, columns=["value"]))

        sonuc = client.service.SelectUrun(UyeKodu=UYE_KODU, f=urun_filtresi, s=sayfalama)
        urun_listesi = getattr(sonuc, 'UrunListesi', None)

        st.write("📦 Gelen veri:", urun_listesi)

        st.success("✅ Güncelleme tamamlandı ve dosya yazıldı.")
        return urun_listesi

    except Exception as e:
        st.error("Hata oluştu: " + str(e))
        st.text(traceback.format_exc())

if st.button("🛠️ Ofis26 Fiyatlarını Güncelle"):
    ticimax_satis_fiyatlarini_guncelle()
