import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

# Ticimax WSDL ve yetki kodu
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

def satis_fiyatlarini_cek():
    try:
        client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))

        # Filtre nesnesi
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

        # Sayfalama nesnesi
        sayfalama = {
            "BaslangicIndex": 0,
            "KayitSayisi": 100,
            "SiralamaDegeri": "ID",
            "SiralamaYonu": "DESC"
        }

        sonuc = client.service.SelectUrun(
            UyeKodu=UYE_KODU,
            f=urun_filtresi,
            s=sayfalama
        )

        if not sonuc or not hasattr(sonuc, "UrunListesi") or not sonuc.UrunListesi:
            return None

        # Urun listesi → pandas DataFrame'e çevir
        urunler = pd.DataFrame([{
            "StokKodu": urun.StokKodu,
            "SatisFiyati": urun.Varyasyonlar[0].SatisFiyati if urun.Varyasyonlar else None
        } for urun in sonuc.UrunListesi])

        return urunler

    except Exception as e:
        st.error(f"Ürün verisi çekilirken hata oluştu: {e}")
        return None

# Streamlit Arayüzü
st.title("🛒 Ticimax Ürün Fiyatlarını Güncelle")

if st.button("📥 Satış Fiyatlarını Ticimax'ten Çek"):
    fiyat_df = satis_fiyatlarini_cek()

    if fiyat_df is None or fiyat_df.empty:
        st.warning("Ürün listesi boş veya çekilemedi.")
    else:
        # Mevcut CSV'den ürün verisi yükle
        ana_df = pd.read_csv(CSV_YOLU)

        # Stok kodu ile eşleştir
        ana_df = ana_df.merge(fiyat_df, how="left", on="StokKodu", suffixes=('', '_Yeni'))

        # Yeni fiyatları güncelle
        ana_df["Ofis26 Satış Fiyatı"] = ana_df["SatisFiyati"]

        st.success("Satış fiyatları başarıyla güncellendi.")
        st.dataframe(ana_df)

        # İstersen CSV'ye yaz:
        ana_df.to_csv(CSV_YOLU, index=False)
