import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

# Dosya yolu
CSV_PATH = "veri_kaynaklari/ana_urun_listesi.csv"

# API bilgileri
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"  # Gerçek kodunuz

def ticimax_fiyat_cek():
    try:
        client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))
        UrunFiltre = client.get_type("ns0:UrunFiltre")
        UrunListele = client.service.UrunListele

        filtre = UrunFiltre(
            UyeKodu=UYE_KODU,
            Resim=False,
            Marka=False,
            Tedarikci=False,
            Ozellik=False,
            Varyant=False,
            Kategori=False
        )

        result = UrunListele(filtre)
        urunler = result["UrunListe"] if result and "UrunListe" in result else []
        return urunler

    except Exception as e:
        st.error(f"API hatası: {e}")
        return []

def main():
    st.set_page_config(layout="wide")
    st.title("🔄 Ofis26 Satış Fiyatlarını Güncelle")

    try:
        df = pd.read_csv(CSV_PATH)
    except FileNotFoundError:
        st.error("Ana ürün listesi dosyası bulunamadı.")
        return

    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("Ofis26 Satış Fiyatlarını API ile Güncelle"):
            urunler_api = ticimax_fiyat_cek()
            if urunler_api:
                api_df = pd.DataFrame(urunler_api)
                api_df = api_df.rename(columns={"StokKodu": "Stok Kodu", "SatisFiyati": "Ofis26 Satış Fiyatı (TL)"})
                df = df.drop(columns=["Ofis26 Satış Fiyatı (TL)"], errors="ignore")
                df = pd.merge(df, api_df[["Stok Kodu", "Ofis26 Satış Fiyatı (TL)"]], on="Stok Kodu", how="left")
                df.to_csv(CSV_PATH, index=False)
                st.success("Ofis26 fiyatları güncellendi ✅")

    with col2:
        st.dataframe(df)

if __name__ == "__main__":
    main()
