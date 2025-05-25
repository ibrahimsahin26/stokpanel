import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

# SOAP servis URL'i
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"  # Senin UyeKodu

st.set_page_config(layout="wide")
st.title("🛒 Ticimax Ürünlerini Ana Ürün Listesi İçin Yükle")

client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))
UrunFiltre = client.get_type("ns0:UrunFiltre")
UrunSayfalama = client.get_type("ns0:UrunSayfalama")

urunler = []
sayfa = 0
adet = 50

if st.button("🔄 Tüm Ürünleri Yükle (Ticimax)"):
    while True:
        sayfalama = UrunSayfalama(
            BaslangicIndex=sayfa * adet,
            KayitSayisi=adet,
            KayitSayisinaGoreGetir=True,
            SiralamaDegeri="ID",
            SiralamaYonu="DESC"
        )

        filtre = UrunFiltre()

        response = client.service.SelectUrun(UyeKodu=UYE_KODU, f=filtre, s=sayfalama)

        if not response:
            break

        for urun in response:
            varyasyonlar = urun.Varyasyonlar.Varyasyon if urun.Varyasyonlar else [None]
            for v in varyasyonlar:
                urunler.append({
                    "Ürün ID": urun.ID,
                    "Stok Kodu": v.StokKodu if v else "",
                    "Barkod": v.Barkod if v else "",
                    "Ürün Adı": urun.UrunAdi,
                    "Ana Kategori": urun.AnaKategori,
                    "Alt Kategori": "",
                    "Marka": urun.Marka,
                    "Alış Fiyatı (Ticimax)": v.AlisFiyati if v else 0,
                    "Mikro Stok": "",
                    "Hepcazip Satış": "",
                    "Ofis26 Satış": "",
                    "Kar Marjı (Hepcazip)": "",
                    "Kar Marjı (Ofis26)": "",
                    "Güncel Alış Fiyatı": "",
                    "Güncel Kar (Hepcazip)": "",
                    "Güncel Kar (Ofis26)": "",
                    "Akakçe Fiyatı": "",
                    "Raf Adet": "",
                    "Kasa Adet": "",
                    "Palet Adet": ""
                })

        if len(response) < adet:
            break

        sayfa += 1

    df = pd.DataFrame(urunler)
    st.success(f"{len(df)} ürün başarıyla yüklendi.")
    st.dataframe(df, use_container_width=True)
