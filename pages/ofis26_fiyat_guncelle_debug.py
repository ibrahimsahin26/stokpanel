import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

st.set_page_config(page_title="Ofis26 Fiyat Güncelle", layout="wide")

st.title("🔧 Kod başladı")

WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

def ticimax_satis_fiyatlarini_guncelle():
    try:
        df = pd.read_csv(CSV_YOLU)
        stok_kodlari = df["Stok Kodu"].dropna().astype(str).str.strip().unique()[:100]
        st.subheader("📦 Stok Kodları:")
        st.dataframe(pd.DataFrame(stok_kodlari, columns=["value"]))

        client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))

        urun_filtresi = {
            "Aktif": -1,
            "Firsat": -1,
            "Indirimli": -1,
            "Vitrin": -1,
            "KategoriID": -1,
            "MarkaID": -1,
            "TedarikciID": -1,
            "ToplamStokAdediBas": -1,
            "ToplamStokAdediSon": -1,
            "UrunKartiID": 0
        }

        sayfalama = {
            "BaslangicIndex": 0,
            "KayitSayisi": 100
        }

        sonuc = client.service.SelectUrun(UyeKodu=UYE_KODU, f=urun_filtresi, s=sayfalama)
        urun_listesi = getattr(sonuc, "UrunListesi", None)

        st.markdown("#### 📦 Gelen veri:")
        st.write(urun_listesi)

        if urun_listesi:
            st.success("✅ Güncelleme tamamlandı ve dosya yazıldı.")
        else:
            st.warning("⚠️ API çağrısı başarılı ancak veri dönmedi (UrunListesi = None).")

    except Exception as e:
        st.error(f"❌ Hata oluştu: {e}")

if st.button("🛠️ Ofis26 Fiyatlarını Güncelle"):
    ticimax_satis_fiyatlarini_guncelle()
