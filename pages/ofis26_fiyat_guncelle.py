import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

# Ticimax ayarları
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

def satis_fiyatlarini_cek():
    client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))

    # Filtre parametresi
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
        "KayitSayisi": 200
    }

    # API çağrısı
    sonuc = client.service.SelectUrun(
        UyeKodu=UYE_KODU,
        f=urun_filtresi,
        s=urun_sayfalama
    )

    try:
        urun_listesi = sonuc["UrunListesi"]
        df_ticimax = pd.DataFrame(urun_listesi)
        return df_ticimax[["Barkod", "SatisFiyati"]]
    except:
        return pd.DataFrame(columns=["Barkod", "SatisFiyati"])

def ana_tabloya_yaz(gelen_fiyatlar):
    df_ana = pd.read_csv(CSV_YOLU)
    df_ana["Barkod"] = df_ana["Barkod"].astype(str)

    # Eşleştir ve güncelle
    df_ana = df_ana.merge(gelen_fiyatlar, on="Barkod", how="left", suffixes=('', '_Yeni'))
    df_ana["Ofis26 Satış Fiyatı"] = df_ana["SatisFiyati"].fillna(df_ana["Ofis26 Satış Fiyatı"])
    df_ana.drop(columns=["SatisFiyati"], inplace=True)

    df_ana.to_csv(CSV_YOLU, index=False)
    return df_ana

# Streamlit Arayüzü
st.title("🛒 Ticimax Ürün Fiyatlarını Güncelle")

if st.button("📉 Satış Fiyatlarını Ticimax'ten Çek"):
    fiyatlar = satis_fiyatlarini_cek()
    if fiyatlar.empty:
        st.warning("Ürün listesi boş veya çekilemedi.")
    else:
        ana_tabloya_yaz(fiyatlar)
        st.success("Ofis26 satış fiyatları başarıyla güncellendi.")
