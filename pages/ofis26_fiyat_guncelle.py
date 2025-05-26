import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

# API Ayarları
WSDL_URL = "http://ofis26.com/servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

def satis_fiyatlarini_cek():
    try:
        client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))

        # Filtre ayarları
        urun_filtre = {
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

        sayfalama = {
            "BaslangicIndex": 0,
            "KayitSayisi": 100,
            "SiralamaDegeri": "ID",
            "SiralamaYonu": "DESC",
        }

        response = client.service.SelectUrun(UyeKodu=UYE_KODU, f=urun_filtre, s=sayfalama)

        if not hasattr(response, 'UrunListesi') or response.UrunListesi is None:
            st.warning("Ürün listesi boş veya çekilemedi.")
            return None

        urunler = response.UrunListesi
        data = []

        for urun in urunler:
            stok_kodu = getattr(urun, 'StokKodu', None)
            fiyat = getattr(urun, 'SatisFiyati', None)
            data.append({
                "StokKodu": stok_kodu,
                "Ofis26 Satış Fiyatı": fiyat
            })

        return pd.DataFrame(data)

    except Exception as e:
        st.error(f"Ürün verisi çekilirken hata oluştu: {e}")
        return None


def main():
    st.title("🛒 Ticimax Ürün Fiyatlarını Güncelle")
    if st.button("📥 Satış Fiyatlarını Ticimax'ten Çek"):
        df_api = satis_fiyatlarini_cek()
        if df_api is not None:
            try:
                df_csv = pd.read_csv(CSV_YOLU)
                df_csv = df_csv.merge(df_api, on="StokKodu", how="left", suffixes=('', '_Yeni'))
                df_csv["Ofis26 Satış Fiyatı"] = df_csv["Ofis26 Satış Fiyatı_Yeni"]
                df_csv.drop(columns=[col for col in df_csv.columns if col.endswith("_Yeni")], inplace=True)
                df_csv.to_csv(CSV_YOLU, index=False)
                st.success("Ofis26 satış fiyatları başarıyla güncellendi.")
            except Exception as e:
                st.error(f"Güncelleme sırasında hata oluştu: {e}")

if __name__ == "__main__":
    main()
