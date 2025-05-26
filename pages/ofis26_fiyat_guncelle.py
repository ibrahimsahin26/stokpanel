import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

# Ticimax SOAP ayarları
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

def satis_fiyatlarini_cek():
    try:
        client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))

        # Filtreler (SelectUrun parametreleri)
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
            "KayitSayisi": 200
        }

        sonuc = client.service.SelectUrun(UyeKodu=UYE_KODU, f=urun_filtre, s=urun_sayfalama)

        if not sonuc or not hasattr(sonuc, "UrunListesi") or sonuc.UrunListesi is None:
            return pd.DataFrame()

        veri = []
        for urun in sonuc.UrunListesi[0]:  # Liste içindeki ürünleri çekiyoruz
            veri.append({
                "StokKodu": urun.StokKodu,
                "SatisFiyati": urun.SatisFiyati
            })

        return pd.DataFrame(veri)

    except Exception as e:
        st.error(f"Ürün verisi çekilirken hata oluştu: {e}")
        return pd.DataFrame()

# Arayüz
st.title("🛒 Ticimax Ürün Fiyatlarını Güncelle")

if st.button("📥 Satış Fiyatlarını Ticimax'ten Çek"):
    df_ticimax = satis_fiyatlarini_cek()

    if df_ticimax.empty:
        st.warning("Ürün listesi boş veya çekilemedi.")
    else:
        try:
            df_ana = pd.read_csv(CSV_YOLU)
            df_ana["StokKodu"] = df_ana["StokKodu"].astype(str)
            df_ticimax["StokKodu"] = df_ticimax["StokKodu"].astype(str)

            # Satış fiyatlarını güncelle
            df_ana = df_ana.merge(df_ticimax, on="StokKodu", how="left", suffixes=("", "_Yeni"))
            df_ana["Ofis26 Satış Fiyatı"] = df_ana["SatisFiyati"].combine_first(df_ana["Ofis26 Satış Fiyatı"])
            df_ana.drop(columns=["SatisFiyati"], inplace=True)

            df_ana.to_csv(CSV_YOLU, index=False)
            st.success("Satış fiyatları başarıyla güncellendi.")
        except Exception as e:
            st.error(f"Güncelleme sırasında hata oluştu: {e}")
