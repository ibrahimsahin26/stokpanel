import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

# WSDL ve yetki bilgisi
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

def satis_fiyatlarini_cek():
    try:
        client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))

        # API parametreleri (filtreleme ve sayfalama)
        filtre = {
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

        sayfalama = {
            "BaslangicIndex": 0,
            "KayitSayisi": 100,
            "SiralamaDegeri": "ID",
            "SiralamaYonu": "DESC"
        }

        # Servis çağrısı
        response = client.service.SelectUrun(
            UyeKodu=UYE_KODU,
            f=filtre,
            s=sayfalama
        )

        # Yanıtın içinden veri çekme
        urun_listesi = response['UrunListesi'] if hasattr(response, 'UrunListesi') else []
        if not urun_listesi:
            return pd.DataFrame()

        # Ürünlerden StokKodu ve ilk SatisFiyati alanlarını al
        veri = []
        for urun in urun_listesi:
            stok_kodu = getattr(urun, 'StokKodu', None)
            fiyatlar = getattr(urun, 'SatisFiyati', [])
            if stok_kodu and fiyatlar and isinstance(fiyatlar, list) and len(fiyatlar) > 0:
                veri.append({
                    "StokKodu": stok_kodu,
                    "Ofis26 Satış Fiyatı": fiyatlar[0]
                })

        return pd.DataFrame(veri)

    except Exception as e:
        st.error(f"Ürün verisi çekilirken hata oluştu: {e}")
        return pd.DataFrame()

# Streamlit Arayüz
st.title("🛒 Ticimax Ürün Fiyatlarını Güncelle")

if st.button("📥 Satış Fiyatlarını Ticimax'ten Çek"):
    df_gelen = satis_fiyatlarini_cek()

    if df_gelen.empty:
        st.warning("Ürün listesi boş veya çekilemedi.")
    else:
        try:
            df_ana = pd.read_csv(CSV_YOLU)
            df_ana = df_ana.merge(df_gelen, on="StokKodu", how="left", suffixes=("", "_Yeni"))
            df_ana["Ofis26 Satış Fiyatı"] = df_ana["Ofis26 Satış Fiyatı_Yeni"].combine_first(df_ana["Ofis26 Satış Fiyatı"])
            df_ana.drop(columns=[col for col in df_ana.columns if col.endswith("_Yeni")], inplace=True)
            df_ana.to_csv(CSV_YOLU, index=False)
            st.success("Ofis26 satış fiyatları başarıyla güncellendi.")
        except Exception as e:
            st.error(f"CSV dosyasına yazılırken hata oluştu: {e}")
