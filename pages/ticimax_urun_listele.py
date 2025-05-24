
import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Ticimax Ürün Listele", layout="wide")

st.title("🛒 Ticimax Ürün Listesi")
st.markdown("### Ticimax’tan Ürünleri Al")

if st.button("Ticimax'tan Ürünleri Al"):
    try:
        # API endpoint ve bilgiler buraya girilmeli
        API_URL = "https://api.ticimax.com/ws/UrunService.asmx"
        HEADERS = {
            "Content-Type": "application/soap+xml; charset=utf-8"
        }
        # Not: Buraya gerçek SOAP body yazılması gerekir. Aşağıda örnek yapılandırma
        body = '''<?xml version="1.0" encoding="utf-8"?>
        <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                         xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                         xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
          <soap12:Body>
            <UrunListele xmlns="http://tempuri.org/">
              <bayiKodu>XXXXX</bayiKodu>
              <kullaniciAdi>XXXXX</kullaniciAdi>
              <sifre>XXXXX</sifre>
            </UrunListele>
          </soap12:Body>
        </soap12:Envelope>'''

        response = requests.post(API_URL, headers=HEADERS, data=body)
        response.raise_for_status()

        # TODO: XML parse işlemi yapılmalı
        st.success("Ürünler başarıyla çekildi! (Not: Örnek veriyle devam ediliyor)")

        # Simülasyon amaçlı örnek veri
        data = [
            {
                "Ürün ID": 101,
                "Barkod": "1234567890123",
                "Stok Kodu": "ABC001",
                "Ürün Adı": "Örnek Kalem",
                "Marka": "Faber",
                "Ana Kategori": "Yazı Gereçleri",
                "Alt Kategori": "Tükenmez Kalem",
                "Stok Adedi (Mikro)": 150,
                "Hepcazip Satış": 24.99,
                "Ofis26 Satış": 22.99,
                "Akakçe Fiyatı": 23.50,
                "Tedarikçi Güncel Alış Fiyatı": 18.75,
                "Hepcazip Kar Oranı": "25%",
                "Ofis26 Kar Oranı": "22%",
                "Kar Hesaplama": "✔︎"
            }
        ]
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"Hata oluştu: {str(e)}")
else:
    st.info("Ürünleri getirmek için yukarıdaki butona tıklayın.")
