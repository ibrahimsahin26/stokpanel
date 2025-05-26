import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

# Ticimax WSDL ayarları
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

def satis_fiyatlarini_cek():
    client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))

    # Filtre ayarları (tüm ürünler için boş filtre)
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
    }

    urun_sayfalama = {
        "BaslangicIndex": 0,
        "KayitSayisi": 200
    }

    try:
        response = client.service.SelectUrun(
            UyeKodu=UYE_KODU,
            f=urun_filtresi,
            s=urun_sayfalama
        )

        # response zaten bir liste
        urunler = response
        if not urunler or not isinstance(urunler, list):
            return pd.DataFrame()

        # Sadece satış fiyatı ve stok kodu alalım
        data = []
        for urun in urunler:
            if hasattr(urun, "StokKodu") and hasattr(urun, "SatisFiyati"):
                data.append({
                    "StokKodu": urun.StokKodu,
                    "TicimaxSatisFiyati": urun.SatisFiyati
                })

        return pd.DataFrame(data)

    except Exception as e:
        st.error(f"Ürün verisi çekilirken hata oluştu: {e}")
        return pd.DataFrame()

def main():
    st.title("🛒 Ticimax Ürün Fiyatlarını Güncelle")

    if st.button("📉 Satış Fiyatlarını Ticimax'ten Çek"):
        df_ticimax = satis_fiyatlarini_cek()
        if df_ticimax.empty:
            st.warning("Ürün listesi boş veya çekilemedi.")
        else:
            st.success("Ürünler başarıyla çekildi.")
            st.dataframe(df_ticimax)

if __name__ == "__main__":
    main()
