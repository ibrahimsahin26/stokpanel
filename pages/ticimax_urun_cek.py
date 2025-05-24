import streamlit as st
import pandas as pd
from utils import get_ticimax_client  # senin util fonksiyonun
from config import TICIMAX_UYE_KODU  # config'den çekilen sabitler

st.title("📦 Ticimax Ürünlerini Panele Yükle")

# SOAP servisine bağlan
client = get_ticimax_client()
st.success("Servis bağlantısı başarılı.")

if st.button("🛒 Ticimax'tan Ürünleri Al"):
    try:
        st.info("Ürünler çekiliyor...")

        # Sayfalama
        Sayfalama = client.get_type("ns2:UrunSayfalama")(
            BaslangicIndex=0,
            KayitSayisi=50,
            KayitSayisinaGoreGetir=True,
            SiralamaDegeri="ID",
            SiralamaYonu="DESC"
        )

        # Boş filtre
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
                    "Ana Kategori":
