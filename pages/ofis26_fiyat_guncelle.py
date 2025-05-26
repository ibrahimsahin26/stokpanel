import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

# WSDL ve Üye Bilgileri
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

# Fiyatları çek
def satis_fiyatlarini_cek():
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
        "KayitSayisi": 200,
        "SiralamaDegeri": "ID",
        "SiralamaYonu": "DESC"
    }

    # API çağrısı
    sonuc = client.service.SelectUrun(UyeKodu=UYE_KODU, f=urun_filtresi, s=sayfalama)

    try:
        urunler = sonuc["UrunListesi"]
        if not urunler:
            return pd.DataFrame()
        df = pd.DataFrame([
            {
                "StokKodu": u["StokKodu"],
                "SatisFiyati": u["Varyasyonlar"][0]["SatisFiyati"] if u["Varyasyonlar"] else None
            } for u in urunler
        ])
        return df
    except Exception as e:
        st.error(f"Ürün verisi çekilirken hata oluştu: {e}")
        return pd.DataFrame()

# Arayüz
st.markdown("## 🛒 Ticimax Ürün Fiyatlarını Güncelle")

if st.button("📥 Satış Fiyatlarını Ticimax'ten Çek"):
    fiyat_df = satis_fiyatlarini_cek()

    if fiyat_df.empty:
        st.warning("Ürün listesi boş veya çekilemedi.")
    else:
        try:
            ana_df = pd.read_csv(CSV_YOLU)
            ana_df["Ofis26 Satış Fiyatı"] = ana_df["Stok Kodu"].map(
                fiyat_df.set_index("StokKodu")["SatisFiyati"]
            )
            ana_df.to_csv(CSV_YOLU, index=False)
            st.success("Satış fiyatları başarıyla güncellendi.")
        except Exception as e:
            st.error(f"Güncelleme sırasında hata oluştu: {e}")
