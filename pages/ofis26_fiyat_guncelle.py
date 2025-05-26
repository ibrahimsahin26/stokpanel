import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

# Ticimax WSDL URL ve Yetki
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"  # teknik destekten gelen kod

CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

def satis_fiyatlarini_cek():
    client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))

    # Boş filtre (tüm ürünler)
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

    # Sayfalama (ilk 200 ürün için örnek)
    urun_sayfalama = {
        "BaslangicIndex": 0,
        "KayitSayisi": 200,
        "SiralamaDegeri": "ID",
        "SiralamaYonu": "DESC"
    }

    # API çağrısı
    sonuc = client.service.SelectUrun(
        UyeKodu=UYE_KODU,
        f=urun_filtre,
        s=urun_sayfalama
    )

    urunler = sonuc.UrunListesi.Urun  # gelen ürün listesi

    veri = []
    for urun in urunler:
        veri.append({
            "StokKodu": urun.StokKodu,
            "SatisFiyati": urun.SatisFiyati
        })

    return pd.DataFrame(veri)

# Streamlit arayüzü
st.title("🛒 Ticimax Ürün Fiyatlarını Güncelle")

if st.button("📉 Satış Fiyatlarını Ticimax'ten Çek"):
    try:
        df_gelen = satis_fiyatlarini_cek()
        df_csv = pd.read_csv(CSV_YOLU)

        df_birlesik = df_csv.merge(df_gelen, how="left", on="StokKodu")
        df_birlesik.to_csv(CSV_YOLU, index=False)

        st.success("Ticimax satış fiyatları başarıyla güncellendi.")
        st.dataframe(df_birlesik)

    except Exception as e:
        st.error(f"Hata oluştu: {str(e)}")
