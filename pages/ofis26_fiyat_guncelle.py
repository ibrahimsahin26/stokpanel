import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

# Ticimax WSDL ve yetkiimport streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport

# Ticimax WSDL ve Yetki
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

def satis_fiyatlarini_cek():
    client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))

    # Filtre ayarları (tüm ürünler için boş filtre)
    urun_filtresi = {
        "Aktif": -1,
        "Firsat": -1,
        "Indirimli": -1,
        "Vitrin": -1,
        "KategoriID": 0,
        "MarkaID": 0,
        "TedarikciID": -1,
        "ToplamStokAdediBas": 0,
        "ToplamStokAdediSon": 100,
        "UrunKartiID": 0
    }

    urun_sayfalama = {
        "BaslangicIndex": 0,
        "KayitSayisi": 200,
        "SiralamaDegeri": "ID",
        "SiralamaYonu": "DESC"
    }

    try:
        yanit = client.service.SelectUrun(
            UyeKodu=UYE_KODU,
            f=urun_filtresi,
            s=urun_sayfalama
        )

        # doğrudan liste dönerse direkt kullan
        if isinstance(yanit, list):
            urun_listesi = yanit
        elif hasattr(yanit, "UrunListesi"):
            urun_listesi = yanit.UrunListesi
        else:
            urun_listesi = []

        if not urun_listesi:
            st.warning("Ürün listesi boş veya çekilemedi.")
            return pd.DataFrame()

        df = pd.DataFrame([{
            "StokKodu": urun.StokKodu,
            "SatisFiyati": urun.SatisFiyati
        } for urun in urun_listesi if hasattr(urun, "StokKodu") and hasattr(urun, "SatisFiyati")])

        # Ana tabloyla eşleştir
        ana_df = pd.read_csv(CSV_YOLU)
        ana_df = ana_df.merge(df, on="StokKodu", how="left")
        ana_df.rename(columns={"SatisFiyati": "Ofis26 Satış Fiyatı"}, inplace=True)
        ana_df.to_csv(CSV_YOLU, index=False)

        st.success("Satış fiyatları başarıyla güncellendi.")
        return ana_df

    except Exception as e:
        st.error(f"Hata oluştu: {e}")
        return pd.DataFrame()
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"  # teknik destekten gelen kod
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

def satis_fiyatlarini_cek():
    client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))

    # Filtre ve sayfalama
    urun_filtre = {
        "Aktif": -1,
        "Firsat": -1,
        "Indirimli": -1,
        "Vitrin": -1,
        "KategoriID": 0,
        "MarkaID": 0,
        "TedarikciID": -1,
        "ToplamStokAdediBas": 0,
        "ToplamStokAdediSon": 1000,
        "UrunKartiID": 0
    }
    urun_sayfalama = {
        "BaslangicIndex": 0,
        "KayitSayisi": 1000,
        "SiralamaDegeri": "ID",
        "SiralamaYonu": "DESC"
    }

    try:
        sonuc = client.service.SelectUrun(UyeKodu=UYE_KODU, f=urun_filtre, s=urun_sayfalama)
        if not sonuc or not sonuc[0]["UrunListesi"]:
            return pd.DataFrame()
        liste = sonuc[0]["UrunListesi"]
        veri = [{
            "StokKodu": urun.get("StokKodu"),
            "SatisFiyati": urun.get("Varyasyonlar", [{}])[0].get("SatisFiyati", None)
        } for urun in liste if urun.get("StokKodu")]

        return pd.DataFrame(veri)
    except Exception as e:
        st.error(f"Hata oluştu: {str(e)}")
        return pd.DataFrame()

def main():
    st.title("🛒 Ticimax Ürün Fiyatlarını Güncelle")

    if st.button("📥 Satış Fiyatlarını Ticimax'ten Çek"):
        df_ticimax = satis_fiyatlarini_cek()
        if df_ticimax.empty:
            st.warning("Ürün listesi boş veya çekilemedi.")
            return

        try:
            df_csv = pd.read_csv(CSV_YOLU)
            df_guncel = pd.merge(df_csv, df_ticimax, how="left", on="StokKodu")
            df_guncel.to_csv(CSV_YOLU, index=False)
            st.success("Ofis26 satış fiyatları başarıyla güncellendi.")
            st.dataframe(df_guncel[["StokKodu", "SatisFiyati"]].dropna())
        except Exception as e:
            st.error(f"CSV güncellenirken hata oluştu: {str(e)}")

if __name__ == "__main__":
    main()
