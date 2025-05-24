import streamlit as st
import pandas as pd
from utils import get_ticimax_client
from config import TICIMAX_UYE_KODU

st.title("📦 Ticimax Ürünlerini Panele Yükle")

client = get_ticimax_client()
st.success("Servis bağlantısı başarılı.")

if st.button("🛒 Ticimax'tan Ürünleri Al"):
    try:
        st.info("Ürünler çekiliyor...")

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
                    "Alt Kategori": urun.Kategoriler["int"][-1] if urun.Kategoriler and "int" in urun.Kategoriler else "",
                    "Marka": urun.Marka,
                    "Alış Fiyatı": varyasyon.AlisFiyati if varyasyon else 0,
                    "Mikro Stok": urun.ToplamStokAdedi,
                    "Hepcazip Satış": "",  # dış kaynaklı veri
                    "Ofis26 Satış": varyasyon.SatisFiyati if varyasyon else 0,
                    "Kar Marjı": ""  # hesaplanacaksa ayrıca yapılır
                })

        df = pd.DataFrame(urunler)
        st.success(f"{len(df)} ürün başarıyla çekildi.")
        st.dataframe(df)

    except Exception as e:
        st.error(f"Hata oluştu: {e}")
