import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

def ticimax_satis_fiyatlarini_guncelle():
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

        # 🧪 Gelişmiş test çıktısı
        st.write("=== Gelişmiş Test ===")
        urun_listesi = getattr(sonuc, 'UrunListesi', None)
        st.write("UrunListesi tipi:", type(urun_listesi))

        if urun_listesi and hasattr(urun_listesi, "Urun") and len(urun_listesi.Urun) > 0:
            st.write("İlk ürün tipi:", type(urun_listesi.Urun[0]))
            st.write("İlk ürün:", urun_listesi.Urun[0])

        return None, "Bu sadece test dosyasıdır. Güncelleme yapılmadı."

    except Exception as e:
        return None, f"Hata oluştu: {str(e)}"

st.title("Ofis26 Satış Fiyatlarını Güncelle (TEST)")
if st.button("Satış Fiyatlarını Güncelle"):
    df, mesaj = ticimax_satis_fiyatlarini_guncelle()
    st.success(mesaj) if df is not None else st.error(mesaj)
