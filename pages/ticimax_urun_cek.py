import streamlit as st
import pandas as pd
from zeep import Client

st.title("📦 Ticimax Ürünlerini Panele Yükle")

# SOAP Client başlat
WSDL_URL = "https://api.ticimax.com/service.asmx?WSDL"
TICIMAX_UYE_KODU = st.secrets["TICIMAX_AUTH_CODE"]

client = Client(wsdl=WSDL_URL)
st.success("Servis bağlantısı başarılı.")

if st.button("🛒 Ticimax'tan Ürünleri Al"):
    try:
        st.info("Ürünler çekiliyor...")

        # Sayfalama ve filtre objeleri
        Sayfalama = client.get_type("ns2:UrunSayfalama")(
            BaslangicIndex=0,
            KayitSayisi=50,
            KayitSayisinaGoreGetir=True,
            SiralamaDegeri="ID",
            SiralamaYonu="DESC"
        )
        UrunFiltre = client.get_type("ns2:UrunFiltre")()

        response = client.service.SelectUrun(
            UyeKodu=TICIMAX_UYE_KODU,
            f=UrunFiltre,
            s=Sayfalama
        )

        urunler = []

        for urun in response:
            varyasyonlar = urun.Varyasyonlar.Varyasyon if urun.Varyasyonlar else [None]
            for varyasyon in varyasyonlar:
                urunler.append({
                    "Ürün ID": urun.ID,
                    "Stok Kodu": varyasyon.StokKodu if varyasyon else "",
                    "Barkod": varyasyon.Barkod if varyasyon else "",
                    "Ürün Adı": urun.UrunAdi,
                    "Ana Kategori": urun.AnaKategori,
                    "Alt Kategori": urun.Kategoriler.int[-1] if urun.Kategoriler and urun.Kategoriler.int else "",
                    "Marka": urun.Marka,
                    "Alış Fiyatı": varyasyon.AlisFiyati if varyasyon else 0,
                    "Mikro Stok": urun.ToplamStokAdedi
                })

        df = pd.DataFrame(urunler)
        st.dataframe(df)

    except Exception as e:
        st.error(f"Hata oluştu: {e}")
