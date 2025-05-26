import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

# Ticimax WSDL URL ve Yetki Kodu
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"  # teknik destekten gelen kod

# CSV yolu
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

def satis_fiyatlarini_cek():
    client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))

    # Filtre tanımları
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
        "UrunKartiID": 0
    }

    urun_sayfalama = {
        "BaslangicIndex": 0,
        "KayitSayisi": 200,
        "SiralamaDegeri": "ID",
        "SiralamaYonu": "DESC"
    }

    try:
        response = client.service.SelectUrun(UyeKodu=UYE_KODU, f=urun_filtre, s=urun_sayfalama)
        urunler = response['UrunListesi']
        return urunler
    except Exception as e:
        st.error(f"Hata oluştu: {str(e)}")
        return []

def guncelle():
    st.title("🛒 Ticimax Ürün Fiyatlarını Güncelle")

    if st.button("📉 Satış Fiyatlarını Ticimax'ten Çek"):
        urunler = satis_fiyatlarini_cek()

        if not urunler:
            st.warning("Ürün listesi boş veya çekilemedi.")
            return

        try:
            df = pd.read_csv(CSV_YOLU)
            df['Ofis26 Satış Fiyatı'] = None

            for urun in urunler:
                try:
                    barkod = urun.get('Barkod')
                    fiyat = urun.get('Varyasyonlar')[0].get('SatisFiyati') if urun.get('Varyasyonlar') else None
                    if barkod and fiyat is not None:
                        df.loc[df['Barkod'] == str(barkod), 'Ofis26 Satış Fiyatı'] = float(fiyat)
                except Exception as e:
                    print(f"Barkod eşleşme hatası: {e}")

            df.to_csv(CSV_YOLU, index=False)
            st.success("Ofis26 satış fiyatları başarıyla güncellendi.")
        except Exception as e:
            st.error(f"Güncelleme sırasında hata: {e}")

if __name__ == "__main__" or True:
    guncelle()
