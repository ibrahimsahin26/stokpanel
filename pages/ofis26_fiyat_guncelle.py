import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

# Ticimax ayarları
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

def satis_fiyatlarini_cek():
    try:
        client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))

        # Filtre ve sayfalama ayarları
        urun_filtre = {
            "Aktif": -1, "Firsat": -1, "Indirimli": -1, "Vitrin": -1,
            "KategoriID": 0, "MarkaID": 0, "TedarikciID": -1,
            "ToplamStokAdediBas": 0, "ToplamStokAdediSon": 100,
            "UrunKartiID": 0
        }

        urun_sayfalama = {
            "BaslangicIndex": 0,
            "KayitSayisi": 100,
            "SiralamaDegeri": "ID",
            "SiralamaYonu": "DESC"
        }

        sonuc = client.service.SelectUrun(
            UyeKodu=UYE_KODU,
            f=urun_filtre,
            s=urun_sayfalama
        )

        if not sonuc or not hasattr(sonuc, "UrunListesi") or not sonuc.UrunListesi:
            st.warning("Ürün listesi boş veya çekilemedi.")
            return None

        # Satış fiyatı ve barkod eşleştir
        fiyat_df = pd.DataFrame([{
            "Barkod": urun.Barkod,
            "SatisFiyati": urun.SatisFiyati
        } for urun in sonuc.UrunListesi if hasattr(urun, "Barkod") and hasattr(urun, "SatisFiyati")])

        return fiyat_df

    except Exception as e:
        st.error(f"Ürün verisi çekilirken hata oluştu: {e}")
        return None

st.title("🛒 Ticimax Ürün Fiyatlarını Güncelle")

if st.button("📉 Satış Fiyatlarını Ticimax'ten Çek"):
    fiyat_df = satis_fiyatlarini_cek()
    if fiyat_df is not None:
        try:
            ana_tablo = pd.read_csv(CSV_YOLU)
            birlesik_df = pd.merge(ana_tablo, fiyat_df, on="Barkod", how="left")
            birlesik_df.to_csv(CSV_YOLU, index=False)
            st.success("Satış fiyatları başarıyla güncellendi.")
        except Exception as e:
            st.error(f"CSV güncellenirken hata oluştu: {e}")
