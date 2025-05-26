import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

# API bağlantısı ve CSV yolu
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

def ticimax_satis_fiyatlarini_guncelle():
    client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))

    # Filtre ve sıralama
    urun_filtresi = {
        "Aktif": -1, "Firsat": -1, "Indirimli": -1, "Vitrin": -1,
        "KategoriID": 0, "MarkaID": 0, "TedarikciID": -1,
        "ToplamStokAdediBas": 0, "ToplamStokAdediSon": 100, "UrunKartiID": 0
    }
    sayfalama = {
        "BaslangicIndex": 0,
        "KayitSayisi": 100,
        "SiralamaDegeri": "ID",
        "SiralamaYonu": "DESC"
    }

    try:
        sonuc = client.service.SelectUrun(UyeKodu=UYE_KODU, f=urun_filtresi, s=sayfalama)
        if not sonuc or not hasattr(sonuc, 'UrunListesi'):
            return None, "Ürün listesi alınamadı."

        fiyat_dict = {}
        for urun in sonuc.UrunListesi.Urun:
            stok_kodu = getattr(urun, "StokKodu", None)
            satis_fiyati = getattr(urun, "SatisFiyati", None)
            if stok_kodu and satis_fiyati is not None:
                fiyat_dict[str(stok_kodu)] = float(satis_fiyati)

        df = pd.read_csv(CSV_YOLU)

        if "Ofis26_SatisFiyati" not in df.columns:
            df["Ofis26_SatisFiyati"] = None

        df["Ofis26_SatisFiyati"] = df["StokKodu"].apply(
            lambda kod: fiyat_dict.get(str(kod), df[df["StokKodu"] == kod]["Ofis26_SatisFiyati"].values[0])
        )

        df.to_csv(CSV_YOLU, index=False)
        return df, "Satış fiyatları başarıyla güncellendi."

    except Exception as e:
        return None, f"Hata oluştu: {str(e)}"

# Streamlit arayüzü
st.title("Ofis26 Satış Fiyatlarını Güncelle")
if st.button("Satış Fiyatlarını Güncelle"):
    df, mesaj = ticimax_satis_fiyatlarini_guncelle()
    st.success(mesaj) if df is not None else st.error(mesaj)
