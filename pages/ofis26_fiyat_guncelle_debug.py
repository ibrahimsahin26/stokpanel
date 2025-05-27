import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

st.set_page_config(page_title="🛠️ Ofis26 Fiyat Güncelleme (Debug)", layout="wide")
st.title("📦 Stok Kodları:")

# AYARLAR
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

try:
    df = pd.read_csv(CSV_YOLU)
    stok_kodlari = df["Stok Kodu"].dropna().astype(str).unique()[:10]
    st.dataframe(pd.DataFrame(stok_kodlari, columns=["value"]))
except Exception as e:
    st.error(f"Hata: CSV dosyası okunamadı: {e}")
    st.stop()

if st.button("🛠️ Ofis26 Fiyatlarını Güncelle"):
    with st.spinner("API çağrısı yapılıyor..."):
        try:
            client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))
            
            urun_filtresi = {
                "Aktif": -1
            }

            sayfalama = {
                "BaslangicIndex": 0,
                "KayitSayisi": 10,
                "KayitSayisinaGoreGetir": True
            }

            sonuc = client.service.SelectUrun(
                UyeKodu=UYE_KODU,
                f=urun_filtresi,
                s=sayfalama
            )

            urun_listesi = getattr(sonuc, "UrunListesi", None)
            st.subheader("📦 Gelen veri:")
            if urun_listesi is None:
                st.warning("⚠️ API çağrısı başarılı ancak veri dönmedi (UrunListesi = None).")
            else:
                veri_df = pd.DataFrame([dict(u) for u in urun_listesi])
                st.success("✅ Veri başarıyla çekildi.")
                st.dataframe(veri_df)

        except Exception as e:
            st.error(f"❌ Hata oluştu: {e}")
