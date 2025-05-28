
import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="📦 Mikro Stok Güncelle", layout="wide")

st.title("📦 Mikro Stok Güncelle")

CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"
API_URL = "http://192.168.1.75/mikroapi/stok_ozet.php"

@st.cache_data
def ana_liste_yukle():
    return pd.read_csv(CSV_YOLU).dropna(subset=["Stok Kodu"]).astype({"Stok Kodu": str})

def stok_ozet_al(stok_kodu):
    try:
        response = requests.post(API_URL, data={"stok_kodu": stok_kodu}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                "stok_miktari": data.get("stok_miktari", None),
                "alis_fiyat": data.get("alis_fiyat", None),
                "satis_adedi": data.get("satis_adedi", None)
            }
    except Exception as e:
        st.warning(f"Hata ({stok_kodu}): {e}")
    return {"stok_miktari": None, "alis_fiyat": None, "satis_adedi": None}

df = ana_liste_yukle()

st.dataframe(df[["Stok Kodu", "Ürün Adı"]], use_container_width=True)

if st.button("🔁 Mikro'dan Güncelle"):
    st.write("Güncelleme başladı...")

    for idx, row in df.iterrows():
        stok_kodu = row["Stok Kodu"]
        sonuc = stok_ozet_al(stok_kodu)

        df.at[idx, "Mevcut Alış Fiyatı"] = sonuc["alis_fiyat"]
        df.at[idx, "Mikro Stok"] = sonuc["stok_miktari"]
        df.at[idx, "3 Ayda Satış"] = sonuc["satis_adedi"]

    df.to_csv(CSV_YOLU, index=False)
    st.success("Güncelleme tamamlandı ve dosya kaydedildi.")
    st.dataframe(df, use_container_width=True)
