import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

# Ticimax SOAP Ayarları
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"

def satis_fiyatlarini_cek():
    client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))

    # Tip tanımları (namespace belirtilmeli)
    UrunFiltre = client.get_type("ns0:UrunFiltre")
    UrunSayfalama = client.get_type("ns0:UrunSayfalama")

    urun_filtre = UrunFiltre(
        Aktif=-1,
        Firsat=-1,
        Indirimli=-1,
        Vitrin=-1,
        KategoriID=0,
        MarkaID=0,
        TedarikciID=-1,
        ToplamStokAdediBas=0,
        ToplamStokAdediSon=100,
        UrunKartiID=0
    )

    urun_sayfalama = UrunSayfalama(
        BaslangicIndex=0,
        KayitSayisi=100,
        SiralamaDegeri="ID",
        SiralamaYonu="DESC"
    )

    # API Çağrısı
    response = client.service.SelectUrun(UyeKodu=UYE_KODU, f=urun_filtre, s=urun_sayfalama)

    # Ürün listesini işleyelim
    if response and hasattr(response, 'UrunListesi'):
        data = []
        for urun in response.UrunListesi:
            for varyasyon in urun.VaryasyonListesi:
                data.append({
                    "Ürün Adı": urun.UrunAdi,
                    "Stok Kodu": varyasyon.StokKodu,
                    "Satış Fiyatı": varyasyon.SatisFiyati
                })
        return pd.DataFrame(data)
    else:
        st.warning("Herhangi bir ürün verisi alınamadı.")
        return pd.DataFrame()

# Streamlit Arayüz
st.title("🛒 Ticimax Ürün Fiyatlarını Güncelle")
if st.button("📥 Satış Fiyatlarını Ticimax'ten Çek"):
    try:
        df = satis_fiyatlarini_cek()
        if not df.empty:
            st.success("Satış fiyatları başarıyla çekildi.")
            st.dataframe(df)
        else:
            st.error("Hiç veri alınamadı.")
    except Exception as e:
        st.exception(e)
