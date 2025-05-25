import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport
from requests import Session
from requests.auth import HTTPBasicAuth

# Auth bilgisi
UYE_KODU = st.secrets["TICIMAX_AUTH_CODE"]
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"

# Streamlit başlığı
st.title("📦 Ticimax Ürünlerini Panele Yükle")

# SOAP client oluştur
try:
    session = Session()
    transport = Transport(session=session)
    client = Client(wsdl=WSDL_URL, transport=transport)
    st.success("Servis bağlantısı başarılı.")
except Exception as e:
    st.error(f"Servis bağlantısı başarısız: {e}")
    st.stop()

# Buton
if st.button("🛒 Tüm Ürünleri Ticimax'tan Al"):
    all_products = []
    sayfa = 0
    batch = 50  # 50 ürünlük sayfalarla çek

    while True:
        st.info(f"{sayfa * batch + 1}-{(sayfa + 1) * batch} arası ürünler alınıyor...")

        try:
            response = client.service.SelectUrun(
                UyeKodu=UYE_KODU,
                f={},  # Boş filtre, tüm ürünler
                s={
                    "BaslangicIndex": sayfa * batch,
                    "KayitSayisi": batch,
                    "KayitSayisinaGoreGetir": True,
                    "SiralamaDegeri": "",
                    "SiralamaYonu": ""
                }
            )

            urunler = response  # Bu doğrudan liste
            if not urunler or len(urunler) == 0:
                break

            for urun in urunler:
                # Varyasyon varsa al, yoksa tekil ürüne None yaz
                varyasyon = None
                if urun.Varyasyonlar and urun.Varyasyonlar.Varyasyon:
                    varyasyon = urun.Varyasyonlar.Varyasyon[0]

                all_products.append({
                    "Ürün ID": urun.ID,
                    "Stok Kodu": varyasyon.StokKodu if varyasyon and hasattr(varyasyon, "StokKodu") else None,
                    "Barkod": varyasyon.Barkod if varyasyon and hasattr(varyasyon, "Barkod") else None,
                    "Ürün Adı": urun.UrunAdi,
                    "Ana Kategori": urun.AnaKategori,
                    "Marka": urun.Marka,
                    "Tedarikçi ID": urun.TedarikciID,
                    "Stok Adedi": varyasyon.StokAdedi if varyasyon and hasattr(varyasyon, "StokAdedi") else None,
                    "Satış Fiyatı": varyasyon.SatisFiyati if varyasyon and hasattr(varyasyon, "SatisFiyati") else None
                })

            sayfa += 1

        except Exception as e:
            st.error(f"Hata oluştu: {e}")
            break

    if all_products:
        df = pd.DataFrame(all_products)
        st.success(f"{len(all_products)} ürün başarıyla yüklendi.")
        st.dataframe(df)
    else:
        st.warning("Hiç ürün bulunamadı.")
