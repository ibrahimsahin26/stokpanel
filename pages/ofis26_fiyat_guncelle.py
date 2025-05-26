import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport
import requests

# Ticimax ayarları
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

def satis_fiyatlarini_cek():
    try:
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

        urun_sayfalama = {
            "BaslangicIndex": 0,
            "KayitSayisi": 200,  # Gerekirse artır
            "SiralamaDegeri": "ID",
            "SiralamaYonu": "DESC"
        }

        response = client.service.SelectUrun(UyeKodu=UYE_KODU, UrunFiltre=urun_filtresi, UrunSayfalama=urun_sayfalama)

        if not hasattr(response, 'UrunListesi'):
            return []

        urunler = response.UrunListesi
        urun_listesi = []

        for urun in urunler:
            urun_listesi.append({
                "StokKodu": urun["StokKodu"],
                "SatisFiyati": urun["SatisFiyati"]
            })

        return urun_listesi

    except Exception as e:
        st.error(f"Ürün verisi çekilirken hata oluştu: {e}")
        return []

def main():
    st.title("🛒 Ticimax Ürün Fiyatlarını Güncelle")

    if st.button("🧾 Satış Fiyatlarını Ticimax'ten Çek"):
        urun_listesi = satis_fiyatlarini_cek()

        if not urun_listesi:
            st.warning("Ürün listesi boş veya çekilemedi.")
            return

        df_ana = pd.read_csv(CSV_YOLU)
        df_fiyat = pd.DataFrame(urun_listesi)

        # Ofis26 Satış Fiyatı sütununu güncelle
        df_ana = df_ana.merge(df_fiyat, how="left", left_on="Stok Kodu", right_on="StokKodu")
        df_ana["Ofis26 Satış Fiyatı"] = df_ana["SatisFiyati"]
        df_ana.drop(columns=["StokKodu", "SatisFiyati"], inplace=True)

        # CSV'ye geri yaz
        df_ana.to_csv(CSV_YOLU, index=False)
        st.success("Ofis26 satış fiyatları başarıyla güncellendi.")

if __name__ == "__main__":
    main()
