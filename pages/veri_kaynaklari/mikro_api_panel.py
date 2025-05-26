
import streamlit as st
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth

st.set_page_config(page_title="Mikro Güncelleme", layout="wide")

st.title("HEpcazip Mikro API Entegrasyonu")
uploaded_file = st.file_uploader("Lütfen ana_urun_listesi.csv dosyasını yükleyin", type=["csv"])

def get_mikro_stok_ozet(stok_kodu):
    try:
        url = f"http://192.168.1.222:2222/mikroapi/stok_ozet.php?stok_kodu={stok_kodu}"
        response = requests.get(url, auth=HTTPBasicAuth('hpczp', '%689+3*--'))
        if response.status_code == 200:
            return response.json()
    except:
        return None
    return None

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df["Stok Kodu"] = df["Stok Kodu"].astype(str).str.strip()

    st.write("Dosya yüklendi. Güncelleniyor...")

    stok_listesi = []
    alis_listesi = []
    satis_listesi = []

    progress = st.progress(0)
    total = len(df)

    for i, row in df.iterrows():
        kod = row["Stok Kodu"]
        data = get_mikro_stok_ozet(kod)
        if data:
            stok_listesi.append(data.get("stok"))
            alis_listesi.append(data.get("alis_fiyati"))
            satis_listesi.append(data.get("satis_miktari_3ay"))
        else:
            stok_listesi.append("")
            alis_listesi.append("")
            satis_listesi.append("")
        progress.progress((i + 1) / total)

    df["Mikro Stok"] = stok_listesi
    df["Mikro Alış Fiyatı"] = alis_listesi
    df["HEpcazip 3 Aylık Satış"] = satis_listesi

    st.success("Güncelleme tamamlandı.")
    st.download_button("Güncellenmiş Dosyayı İndir", df.to_csv(index=False).encode("utf-8"), file_name="ana_urun_listesi_guncel.csv", mime="text/csv")
    st.dataframe(df)
