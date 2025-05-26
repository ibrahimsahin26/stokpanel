import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

# API bilgileri
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

st.title("🛒 Ticimax Ürün Fiyatlarını Güncelle")

if st.button("📉 Satış Fiyatlarını Ticimax'ten Çek"):
    try:
        client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))

        # Filtre
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

        # Sayfalama
        urun_sayfalama = {
            "BaslangicIndex": 0,
            "KayitSayisi": 200,
            "SiralamaDegeri": "ID",
            "SiralamaYonu": "DESC"
        }

        # API çağrısı
        sonuc = client.service.SelectUrun(
            UyeKodu=UYE_KODU,
            f=urun_filtresi,
            s=urun_sayfalama
        )

        if not sonuc or not hasattr(sonuc, 'UrunListesi') or sonuc.UrunListesi is None:
            st.warning("Ürün listesi boş veya çekilemedi.")
        else:
            gelen_liste = sonuc.UrunListesi
            df_api = pd.DataFrame([{
                "StokKodu": urun.StokKodu,
                "SatisFiyati": urun.Varyasyonlar[0].SatisFiyati if urun.Varyasyonlar else None
            } for urun in gelen_liste])

            df_csv = pd.read_csv(CSV_YOLU)

            if "Stok Kodu" not in df_csv.columns:
                st.error("Ana ürün listesinde 'Stok Kodu' sütunu bulunamadı.")
            else:
                df_csv = df_csv.merge(df_api, left_on="Stok Kodu", right_on="StokKodu", how="left")
                df_csv["Ofis26 Satış Fiyatı"] = df_csv["SatisFiyati"]
                df_csv.drop(columns=["StokKodu", "SatisFiyati"], inplace=True)
                df_csv.to_csv(CSV_YOLU, index=False)
                st.success("Ofis26 satış fiyatları başarıyla güncellendi.")

    except Exception as e:
        st.error(f"Ürün verisi çekilirken hata oluştu: {str(e)}")
