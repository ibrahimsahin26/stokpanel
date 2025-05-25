import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

# Ticimax SOAP Ayarları
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1K1USEAD0VAXTVKP8FWGN3AE"

CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

def urun_fiyatlarini_cek():
    client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))

    # Tip tanımları
    UrunFiltre = client.get_type("ns0:UrunFiltre")
    UrunSayfalama = client.get_type("ns0:UrunSayfalama")

    urun_filtre = UrunFiltre()  # Boş filtre: tüm ürünler
    urun_sayfalama = UrunSayfalama(BaslangicIndex=0, KayitSayisi=200)  # 200 ürün al

    # API çağrısı
    sonuc = client.service.SelectUrun(UyeKodu=UYE_KODU, UrunFiltre=urun_filtre, UrunSayfalama=urun_sayfalama)

    # Sonuçlardan satış fiyatlarını ve stok kodunu çek
    fiyat_listesi = []
    for urun in sonuc.Urunler:
        if urun.Varyasyonlar:
            for varyasyon in urun.Varyasyonlar:
                fiyat_listesi.append({
                    "StokKodu": varyasyon.StokKodu,
                    "SatisFiyati": varyasyon.SatisFiyati
                })

    return pd.DataFrame(fiyat_listesi)

# Arayüz
st.set_page_config(layout="wide")
st.title("🔄 Ofis26 Satış Fiyatlarını Güncelle")

if st.button("💾 Fiyatları Güncelle (Ticimax)"):
    try:
        fiyat_df = urun_fiyatlarini_cek()
        ana_df = pd.read_csv(CSV_YOLU)

        # Verileri birleştir (Stok Kodu ile eşleştir)
        guncel_df = ana_df.merge(fiyat_df, on="StokKodu", how="left")

        # Ofis26 Satış Fiyatı sütununu güncelle
        guncel_df["Ofis26 Satış Fiyatı"] = guncel_df["SatisFiyati"]
        guncel_df.drop(columns=["SatisFiyati"], inplace=True)

        # CSV dosyasını güncelle
        guncel_df.to_csv(CSV_YOLU, index=False)
        st.success("Ofis26 satış fiyatları başarıyla güncellendi.")
    except Exception as e:
        st.error(f"Hata oluştu: {e}")
