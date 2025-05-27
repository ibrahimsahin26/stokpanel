import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport
import ast

# Ticimax WSDL ve UyeKodu bilgileri
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

def ticimax_satis_fiyatlarini_guncelle():
    try:
        df = pd.read_csv(CSV_YOLU)
        stok_kodlari = df["Stok Kodu"].dropna().astype(str).unique()[:10]  # Sadece ilk 10 ürün

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
            "KayitSayisinaGoreGetir": True,
            "SiralamaDegeri": "ID",
            "SiralamaYonu": "DESC"
        }

        sonuc = client.service.SelectUrun(UyeKodu=UYE_KODU, f=urun_filtresi, s=sayfalama)
        urun_listesi = getattr(sonuc, "UrunListesi", None)

        if urun_listesi is None:
            st.warning("⚠️ API çağrısı başarılı ancak veri dönmedi (UrunListesi = None).")
            return

        fiyat_dict = {}
        for urun in urun_listesi:
            urun_json = ast.literal_eval(str(urun))
            kod = urun_json.get("StokKodu")
            fiyat = urun_json.get("SatisFiyati")
            fiyat_dict[kod] = fiyat

        # Fiyatları ana tabloya yaz
        df["Ofis26 Satış Fiyatı"] = df["Stok Kodu"].map(fiyat_dict)
        df.to_csv(CSV_YOLU, index=False)

        st.success("✅ Güncelleme tamamlandı ve dosya yazıldı.")
        st.dataframe(df)

    except Exception as e:
        st.error(f"Hata oluştu: {e}")

# Streamlit arayüzü
st.markdown("### 📦 St
