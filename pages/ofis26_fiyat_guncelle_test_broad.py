import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"

def ticimax_test_veri_cek():
    client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))

    # Filtreleri boş ve geniş şekilde ayarladık
    urun_filtresi = {
        "Aktif": -1,
        "Firsat": -1,
        "Indirimli": -1,
        "Vitrin": -1,
        "KategoriID": -1,
        "MarkaID": -1,
        "TedarikciID": -1,
        "ToplamStokAdediBas": 0,
        "ToplamStokAdediSon": 99999,
        "UrunKartiID": 0
    }

    sayfalama = {
        "BaslangicIndex": 0,
        "KayitSayisi": 10,
        "SiralamaDegeri": "ID",
        "SiralamaYonu": "DESC"
    }

    try:
        sonuc = client.service.SelectUrun(UyeKodu=UYE_KODU, f=urun_filtresi, s=sayfalama)
        urun_listesi = getattr(sonuc, 'UrunListesi', None)

        st.write("🔍 UrunListesi tipi:", type(urun_listesi))

        if urun_listesi and hasattr(urun_listesi, "Urun") and len(urun_listesi.Urun) > 0:
            st.write("✅ İlk ürün tipi:", type(urun_listesi.Urun[0]))
            st.write("🧾 İlk ürün içeriği:", urun_listesi.Urun[0])
            return None, "✅ Veri başarıyla alındı."
        else:
            return None, "🚫 Ürün listesi yine alınamadı."

    except Exception as e:
        return None, f"❌ Hata oluştu: {str(e)}"

st.title("Ticimax Geniş Test — Ürün Verisi Çekiliyor")

if st.button("Veri Testini Başlat"):
    df, mesaj = ticimax_test_veri_cek()
    st.success(mesaj) if df is not None else st.error(mesaj)
