import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

# WSDL ve yetki
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

def satis_fiyatlarini_cek():
    try:
        client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))

        # Boş filtre - tüm ürünleri almak için
        urun_filtresi = {
            "Aktif": -1,
            "Firsat": -1,
            "Indirimli": -1,
            "Vitrin": -1,
            "KategoriID": 0,
            "MarkaID": 0,
            "TedarikciID": -1,
            "ToplamStokAdediBas": 0,
            "ToplamStokAdediSon": 1000,
            "UrunKartiID": 0,
        }

        sayfalama = {
            "BaslangicIndex": 0,
            "KayitSayisi": 200,
            "SiralamaDegeri": "ID",
            "SiralamaYonu": "DESC"
        }

        sonuc = client.service.SelectUrun(
            UyeKodu=UYE_KODU,
            f=urun_filtresi,
            s=sayfalama
        )

        if not hasattr(sonuc, 'UrunListesi') or sonuc.UrunListesi is None:
            return pd.DataFrame()

        urunler = sonuc.UrunListesi
        fiyat_df = pd.DataFrame([
            {
                "StokKodu": urun.StokKodu,
                "SatisFiyati": urun.Varyasyonlar[0].SatisFiyati if urun.Varyasyonlar else None
            }
            for urun in urunler
            if hasattr(urun, 'StokKodu') and hasattr(urun, 'Varyasyonlar')
        ])

        return fiyat_df

    except Exception as e:
        st.error(f"Ürün verisi çekilirken hata oluştu: {e}")
        return pd.DataFrame()

def main():
    st.title("🛒 Ticimax Ürün Fiyatlarını Güncelle")

    if st.button("📉 Satış Fiyatlarını Ticimax'ten Çek"):
        df_ana = pd.read_csv(CSV_YOLU)
        df_fiyat = satis_fiyatlarini_cek()

        if df_fiyat.empty:
            st.warning("Ürün listesi boş veya çekilemedi.")
            return

        if "StokKodu" not in df_ana.columns or "Ofis26 Satış Fiyatı" not in df_ana.columns:
            st.error("Ana CSV'de gerekli sütunlar eksik.")
            return

        # Stok kodu üzerinden eşleştirme ve fiyat güncelleme
        df_ana.set_index("StokKodu", inplace=True)
        df_fiyat.set_index("StokKodu", inplace=True)

        df_ana.update(df_fiyat.rename(columns={"SatisFiyati": "Ofis26 Satış Fiyatı"}))
        df_ana.reset_index(inplace=True)

        # Güncellenmiş veriyi kaydet
        df_ana.to_csv(CSV_YOLU, index=False)
        st.success("Ofis26 satış fiyatları başarıyla güncellendi.")

if __name__ == "__main__":
    main()
