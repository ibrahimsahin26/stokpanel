import streamlit as st
from zeep import Client
from zeep.transports import Transport
import requests
import pandas as pd

# WSDL: Doğru adres
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"

# Auth code: streamlit secrets.toml'dan alınıyor
UYE_KODU = st.secrets["TICIMAX_AUTH_CODE"]

# Başlık
st.title("📦 Ticimax Ürünlerini Panele Yükle")

# SOAP servisine bağlan
try:
    transport = Transport(timeout=10)
    client = Client(wsdl=WSDL_URL, transport=transport)
    st.success("✅ Servis bağlantısı başarılı.")
except requests.exceptions.RequestException as e:
    st.error(f"❌ Servis bağlantısı başarısız: {e}")
    st.stop()

# Buton: Ürünleri Al
if st.button("🛒 Ticimax'tan Ürünleri Al"):
    try:
        st.info("Ürünler çekiliyor...")

        # Sayfalama ve filtre parametreleri
        Sayfalama = client.get_type("ns2:UrunSayfalama")(
            BaslangicIndex=0,
            KayitSayisi=50,
            KayitSayisinaGoreGetir=True,
            SiralamaDegeri="ID",
            SiralamaYonu="DESC"
        )

        UrunFiltre = client.get_type("ns2:UrunFiltre")()

        response = client.service.SelectUrun(
            UyeKodu=UYE_KODU,
            f=UrunFiltre,
            s=Sayfalama
        )

        urunler = []
        for urun in response:
            varyasyonlar = urun.Varyasyonlar.Varyasyon if urun.Varyasyonlar else [None]
            for v in varyasyonlar:
                urunler.append({
                    "Ürün ID": urun.ID,
                    "Stok Kodu": v.StokKodu if v else "",
                    "Barkod": v.Barkod if v else "",
                    "Ürün Adı": urun.UrunAdi,
                    "Ana Kategori": urun.AnaKategori,
                    "Marka": urun.Marka,
                    "Tedarikçi ID": urun.TedarikciID,
                    "Stok Adedi": v.StokAdedi if v else "",
                    "Alış Fiyatı": v.AlisFiyati if v else "",
                    "Satış Fiyatı": v.SatisFiyati if v else "",
                    "KDV": v.KdvOrani if v else "",
                })

        df = pd.DataFrame(urunler)
        st.dataframe(df)

        # Export
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 CSV İndir", data=csv, file_name="urunler.csv", mime="text/csv")

    except Exception as e:
        st.error(f"❌ Hata oluştu: {e}")
