import pandas as pd
import streamlit as st
from zeep import Client
from zeep.transports import Transport

# API bilgileri
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

def satis_fiyatlarini_cek():
    # SOAP istemcisi oluştur
    client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))

    # Tip nesnelerini al
    UrunFiltre = client.get_type("ns0:UrunFiltre")
    UrunSayfalama = client.get_type("ns0:UrunSayfalama")

    urun_filtre = UrunFiltre(
        Aktif=-1, Firsat=-1, Indirimli=-1, Vitrin=-1,
        KategoriID=0, MarkaID=0, TedarikciID=-1,
        UrunKartiID=0, ToplamStokAdediBas=0, ToplamStokAdediSon=9999
    )

    urun_sayfalama = UrunSayfalama(
        BaslangicIndex=0, KayitSayisi=200, SiralamaDegeri="ID", SiralamaYonu="DESC"
    )

    # API çağrısı
    sonuc = client.service.SelectUrun(
        UyeKodu=UYE_KODU,
        UrunFiltre=urun_filtre,
        UrunSayfalama=urun_sayfalama
    )

    # Gelen ürünleri liste olarak al
    urunler = sonuc.SelectUrunResult.Urunler.Urun
    data = []
    for urun in urunler:
        stok_kodu = urun.StokKodu
        fiyat = urun.SatisFiyati if hasattr(urun, "SatisFiyati") else None
        data.append({"Stok Kodu": stok_kodu, "Ofis26 Satış Fiyatı": fiyat})
    return pd.DataFrame(data)

def main():
    st.title("🛒 Ticimax Ürün Fiyatlarını Güncelle")

    if st.button("📥 Satış Fiyatlarını Ticimax'ten Çek"):
        with st.spinner("Fiyatlar çekiliyor..."):
            df_gelen = satis_fiyatlarini_cek()
            df_csv = pd.read_csv(CSV_YOLU)

            # Güncelleme işlemi
            df_csv = df_csv.merge(df_gelen, how="left", on="Stok Kodu", suffixes=('', '_Yeni'))
            df_csv["Ofis26 Satış Fiyatı"] = df_csv["Ofis26 Satış Fiyatı_Yeni"].combine_first(df_csv["Ofis26 Satış Fiyatı"])
            df_csv.drop(columns=["Ofis26 Satış Fiyatı_Yeni"], inplace=True)

            # CSV'ye yaz
            df_csv.to_csv(CSV_YOLU, index=False)
            st.success("Satış fiyatları başarıyla güncellendi.")

if __name__ == "__main__":
    main()
