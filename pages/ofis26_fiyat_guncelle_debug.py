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
        stok_kodlari = df["Stok Kodu"].dropna().astype(str).unique()

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
            "UrunAdi": "",
            "StokKodu": "",
            "Barkod": "",
        }

        sayfalama = {
            "BaslangicIndex": 0,
            "KayitSayisi": 100,
            "KayitSayisinaGoreGetir": True,
            "SiralamaDegeri": "ID",
            "SiralamaYonu": "DESC"
        }

        sonuc = client.service.SelectUrun(UyeKodu=UYE_KODU, f=urun_filtresi, s=sayfalama)
        urun_listesi = getattr(sonuc, "UrunListesi", None)
        return urun_listesi

    except Exception as e:
        st.error(f"Hata oluştu: {e}")
        return None

st.markdown("### 📦 Stok Kodları:")
urun_listesi_df = pd.read_csv(CSV_YOLU)
stok_kodlari_df = pd.DataFrame({"value": urun_listesi_df["Stok Kodu"].dropna().astype(str).unique()})
st.dataframe(stok_kodlari_df, hide_index=True)

if st.button("🛠️ Ofis26 Fiyatlarını Güncelle"):
    veri = ticimax_satis_fiyatlarini_guncelle()
    st.markdown("### 📦 Gelen veri:")
    st.write(veri if veri is not None else "⚠️ API çağrısı başarılı ancak veri dönmedi (UrunListesi = None).")
