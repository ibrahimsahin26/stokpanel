
import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv

st.set_page_config(page_title="Ticimax Ürün Çekme", layout="wide")
st.title("🛒 Ticimax Ürünlerini Çek")

# .env dosyasını yükle
load_dotenv()
API_KEY = os.getenv("TICIMAX_API_KEY")

if not API_KEY:
    st.error("API anahtarı bulunamadı. Lütfen .env dosyasına 'TICIMAX_API_KEY' olarak ekleyin.")
    st.stop()

# API bilgileri
URL = "https://api.ticimax.com/api/Urun/Listele"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
payload = {
    "Dil": "tr",
    "Baslangic": 0,
    "Adet": 50
}

# API çağrısı
if st.button("🔄 Ürünleri Getir"):
    try:
        response = requests.post(URL, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            urunler = data.get("Data", [])
            if urunler:
                df = pd.DataFrame(urunler)
                st.success(f"{len(df)} ürün yüklendi.")
                st.dataframe(df)
            else:
                st.warning("Ürün bulunamadı.")
        else:
            st.error(f"Hata kodu: {response.status_code}")
            st.text(response.text)
    except Exception as e:
        st.error(f"Bağlantı hatası: {e}")
