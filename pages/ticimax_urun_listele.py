import streamlit as st
import requests

st.set_page_config(page_title="Ticimax Ürün Çekme", layout="wide")
st.title("🛒 Ticimax Ürünlerini Çek")

st.write("Sayfa yüklendi")  # Test için kontrol satırı

# Yetki kodunu Streamlit Cloud üzerinden secrets.toml'dan alıyoruz
AUTH_CODE = st.secrets["TICIMAX_AUTH_CODE"]

# API bağlantısı için başlıklar
headers = {
    "Authorization": f"Bearer {AUTH_CODE}",
    "Content-Type": "application/json"
}

# Örnek API endpoint ve veri
url = "https://ofis26.ticimax.com/api/Urun/Listele"  # Ticimax dokümantasyonuna göre güncellenmeli
payload = {
    "Dil": "tr",
    "Baslangic": 0,
    "Adet": 50
}

# Butona basılınca API'den veri çekilir
if st.button("🔄 Ürünleri Getir"):
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            st.success("Ürün verisi başarıyla çekildi.")
            st.json(data)
        else:
            st.error(f"Hata: {response.status_code}")
            st.text(response.text)
    except Exception as e:
        st.error(f"Bağlantı hatası: {e}")
