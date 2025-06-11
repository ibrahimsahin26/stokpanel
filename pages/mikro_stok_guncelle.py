import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="📦 Mikro Stok Güncelle", layout="wide")
st.title("📦 Mikro Stok Güncelle")

CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"
API_URL = "http://192.168.1.75/mikroapi/stok_ozet.php"

@st.cache_data
def ana_liste_yukle():
    df = pd.read_csv(CSV_YOLU).dropna(subset=["Stok Kodu"]).astype({"Stok Kodu": str})
    # Eğer "3 Ayda Satış" yoksa ekle
    if "3 Ayda Satış" not in df.columns:
        df["3 Ayda Satış"] = None
    return df

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
        else:
            st.warning(f"Hata ({stok_kodu}): API yanıtı 200 değil! ({response.status_code})")
    except Exception as e:
        st.warning(f"Hata ({stok_kodu}): {e}")
    return {"stok_miktari": None, "alis_fiyat": None, "satis_adedi": None}

df = ana_liste_yukle()

st.dataframe(df[["Stok Kodu", "Ürün Adı"]], use_container_width=True)

if st.button("🔁 Mikro'dan Güncelle"):
    st.write("Güncelleme başladı...")

    progress = st.progress(0)
    toplam = len(df)
    hata_listesi = []

    for idx, row in df.iterrows():
        stok_kodu = row["Stok Kodu"]
        sonuc = stok_ozet_al(stok_kodu)

        # CSV başlıklarıyla birebir eşleşiyor!
        df.at[idx, "Tedarikçi Güncel Alış Fiyatı"] = sonuc["alis_fiyat"]
        df.at[idx, "Mikro Stok"] = sonuc["stok_miktari"]
        df.at[idx, "3 Ayda Satış"] = sonuc["satis_adedi"]

        if sonuc["stok_miktari"] is None:
            hata_listesi.append(stok_kodu)
        
        progress.progress((idx + 1) / toplam)

    df.to_csv(CSV_YOLU, index=False)
    st.success("Güncelleme tamamlandı ve dosya kaydedildi.")

    if hata_listesi:
        st.error(f"Aşağıdaki stok kodları için veri çekilemedi:\n{', '.join(hata_listesi)}")

    # Dosyayı güncelledikten sonra yeniden oku ve göster
    df = pd.read_csv(CSV_YOLU)
    st.dataframe(df, use_container_width=True)
