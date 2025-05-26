import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

# Ticimax WSDL ve Yetki
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

def satis_fiyatlarini_cek():
    try:
        client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))

        urun_filtre = {
            "Aktif": -1,
            "Firsat": -1,
            "Indirimli": -1,
            "Vitrin": -1,
            "KategoriID": 0,
            "MarkaID": 0,
            "TedarikciID": -1,
            "ToplamStokAdediBas": 0,
            "ToplamStokAdediSon": 100,
            "UrunKartiID": 0,
        }

        urun_sayfalama = {
            "BaslangicIndex": 0,
            "KayitSayisi": 100,
            "SiralamaDegeri": "ID",
            "SiralamaYonu": "DESC",
        }

        sonuc = client.service.SelectUrun(
            UyeKodu=UYE_KODU,
            f=urun_filtre,
            s=urun_sayfalama
        )

        if not sonuc or not hasattr(sonuc, "UrunListesi") or not sonuc.UrunListesi:
            return pd.DataFrame()

        urunler = []
        for urun in sonuc.UrunListesi:
            try:
                urunler.append({
                    "UrunAdi": urun.UrunAdi,
                    "Barkod": urun.Barkod,
                    "SatisFiyati": urun.Varyasyonlar[0].SatisFiyati if urun.Varyasyonlar else None,
                })
            except Exception:
                continue

        return pd.DataFrame(urunler)

    except Exception as e:
        st.error(f"Ürün verisi çekilirken hata oluştu: {e}")
        return pd.DataFrame()


st.markdown("## 🛒 Ticimax Ürün Fiyatlarını Güncelle")

if st.button("📥 Satış Fiyatlarını Ticimax'ten Çek"):
    df = satis_fiyatlarini_cek()
    if df.empty:
        st.warning("Ürün listesi boş veya çekilemedi.")
    else:
        ana_liste = pd.read_csv(CSV_YOLU)
        ana_liste["Barkod"] = ana_liste["Barkod"].astype(str)
        df["Barkod"] = df["Barkod"].astype(str)
        birlesik = pd.merge(ana_liste, df[["Barkod", "SatisFiyati"]], how="left", on="Barkod")
        st.success("Fiyatlar başarıyla çekildi ve eşleştirildi.")
        st.dataframe(birlesik)
