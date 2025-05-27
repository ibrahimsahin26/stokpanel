import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

st.title("🔧 Kod başladı")

WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

df = pd.read_csv(CSV_YOLU)
stok_kodlari = df["Stok Kodu"].dropna().astype(str).unique()[:10]

st.subheader("📦 Stok Kodları:")
st.dataframe(pd.DataFrame(stok_kodlari, columns=["value"]))

if st.button("🛠️ Ofis26 Fiyatlarını Güncelle"):
    try:
        client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))

        urun_filtresi = {
            "Aktif": -1,
            "Firsat": -1,
            "Indirimli": -1,
            "Vitrin": -1,
            "KategoriID": -1,
            "MarkaID": -1,
            "TedarikciID": -1
        }

        sayfalama = {
            "BaslangicIndex": 0,
            "KayitSayisi": 100,
            "KayitSayisinaGoreGetir": True
        }

        sonuc = client.service.SelectUrun(UyeKodu=UYE_KODU, f=urun_filtresi, s=sayfalama)
        urun_listesi = getattr(sonuc, "UrunListesi", None)

        st.subheader("📦 Gelen veri:")
        if urun_listesi is None:
            st.warning("⚠️ API çağrısı başarılı ancak veri dönmedi (UrunListesi = None).")
        else:
            gelen_df = pd.DataFrame([vars(u) for u in urun_listesi])
            st.dataframe(gelen_df.head(20))
            st.success("✅ Güncelleme tamamlandı ve veri görüntülendi.")
    except Exception as e:
        st.error(f"❌ Hata oluştu: {e}")
