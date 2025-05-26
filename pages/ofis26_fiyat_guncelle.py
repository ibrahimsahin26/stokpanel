import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

# Ticimax API bilgileri
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"

st.title("🛒 Ticimax Ürün Fiyatlarını Güncelle")

if st.button("📉 Satış Fiyatlarını Ticimax'ten Çek"):
    try:
        client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))

        # Filtre yapısı
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

        # Sayfalama yapısı
        sayfalama = {
            "BaslangicIndex": 0,
            "KayitSayisi": 50,
            "SiralamaDegeri": "ID",
            "SiralamaYonu": "DESC"
        }

        # API çağrısı
        sonuc = client.service.SelectUrun(
            UyeKodu=UYE_KODU,
            f=urun_filtresi,
            s=sayfalama
        )

        # 👇 Gelen cevabı yazdıralım: nasıl bir veri geldiğini görelim
        st.write("Gelen Yanıt:")
        st.write(sonuc)

        # Eğer veri varsa tabloya çevir
        if sonuc and hasattr(sonuc, "UrunListesi") and sonuc.UrunListesi:
            urunler = sonuc.UrunListesi
            df = pd.DataFrame(urunler)
            st.success("Ürün verisi başarıyla alındı.")
            st.dataframe(df)
        else:
            st.warning("Ürün listesi boş veya çekilemedi.")

    except Exception as e:
        st.error(f"Hata oluştu: {e}")
