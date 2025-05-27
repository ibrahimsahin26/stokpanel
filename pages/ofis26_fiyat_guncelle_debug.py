import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

st.set_page_config(page_title="Ofis26 Fiyat Güncelleme", layout="wide")

WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

st.markdown("### 📦 Stok Kodları:")

try:
    df = pd.read_csv(CSV_YOLU)
    stok_kodlari = df["Stok Kodu"].dropna().astype(str).unique()[:10]
    st.table(pd.DataFrame(stok_kodlari, columns=["value"]))
except Exception as e:
    st.error(f"Hata oluştu: {e}")
    st.stop()

if st.button("🛠️ Ofis26 Fiyatlarını Güncelle"):
    try:
        client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))

        urun_filtresi = {
            "Aktif": -1,
            "Barkod": "",
            "KategoriID": 0,
            "MarkaID": 0,
            "ToplamStokAdediBas": 0,
            "ToplamStokAdediSon": 100,
            "UrunKartiID": 0,
            "UrunKartiIDList": None,
            "FiyatFiltre": None,
            "StokKoduList": {"string": list(stok_kodlari)},
        }

        sayfalama = {
            "BaslangicIndex": 0,
            "KayitSayisi": 100,
            "KayitSayisinaGoreGetir": False,
            "SiralamaDegeri": "ID",
            "SiralamaYonu": "DESC"
        }

        sonuc = client.service.SelectUrun(UyeKodu=UYE_KODU, f=urun_filtresi, s=sayfalama)
        urun_listesi = getattr(sonuc, "UrunListesi", None)

        st.markdown("### 📦 Gelen veri:")
        st.write(urun_listesi)

        if urun_listesi:
            st.success("✅ Güncelleme tamamlandı ve dosya yazıldı.")
        else:
            st.warning("⚠️ API çağrısı başarılı ancak veri dönmedi (UrunListesi = None).")

    except Exception as e:
        st.error(f"Hata oluştu: {e}")
