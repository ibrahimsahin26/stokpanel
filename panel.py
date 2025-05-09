
import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(layout="wide")
st.title("📋 Merkezi Ürün - Stok - Fiyat - Tedarikçi Paneli")

# Ana tablo başlat
if "urun_tablosu" not in st.session_state:
    st.session_state.urun_tablosu = pd.DataFrame(columns=[
        "Barkod", "Ürün Adı", "Kategori", "Marka",
        "Alış Fiyatı", "Kar Marjı", "Satış Fiyatı", "Piyasa Fiyatı", "Akakçe Linki",
        "Mevcut Stok", "Raf No", "Raf Adet", "Kasa No", "Kasa Adet", "Palet No", "Palet Adet",
        "Tedarikçi 1", "Fiyat 1", "Notlar"
    ])

df = st.session_state.urun_tablosu

# İşlem seçimi
islem = st.sidebar.selectbox("🔧 İşlem Seç", [
    "➕ Yeni Ürün Ekle",
    "💹 Fiyat Güncelle",
    "📦 Stok Sayımı",
    "🔗 Tedarikçi Bilgisi",
    "📄 Tüm Tabloyu Görüntüle / İndir"
])

# Yeni ürün ekleme
if islem == "➕ Yeni Ürün Ekle":
    st.subheader("Yeni Ürün Girişi")
    with st.form("yeni_urun"):
        col1, col2, col3 = st.columns(3)
        with col1:
            barkod = st.text_input("Barkod")
            urun_adi = st.text_input("Ürün Adı")
            kategori = st.text_input("Kategori")
            marka = st.text_input("Marka")
        with col2:
            alis = st.number_input("Alış Fiyatı", min_value=0.0, step=0.01)
            kar = st.slider("Kar Marjı (%)", 0, 100, 20)
            satis = round(alis * (1 + kar / 100), 2)
            piyasa = st.number_input("Piyasa Fiyatı", min_value=0.0, step=0.01)
        with col3:
            link = st.text_input("Akakçe Linki")
            stok = st.number_input("Mevcut Stok", min_value=0, step=1)
            notlar = st.text_area("Notlar")
        submitted = st.form_submit_button("Ekle")

        if submitted:
            yeni = {
                "Barkod": barkod, "Ürün Adı": urun_adi, "Kategori": kategori, "Marka": marka,
                "Alış Fiyatı": alis, "Kar Marjı": kar, "Satış Fiyatı": satis, "Piyasa Fiyatı": piyasa,
                "Akakçe Linki": link, "Mevcut Stok": stok,
                "Raf No": "", "Raf Adet": 0, "Kasa No": "", "Kasa Adet": 0,
                "Palet No": "", "Palet Adet": 0,
                "Tedarikçi 1": "", "Fiyat 1": 0, "Notlar": notlar
            }
            st.session_state.urun_tablosu = pd.concat([df, pd.DataFrame([yeni])], ignore_index=True)
            st.success("✅ Ürün eklendi.")

# Fiyat güncelleme
elif islem == "💹 Fiyat Güncelle":
    st.subheader("Alış Fiyatı & Kar Marjı Güncelle")
    for idx, row in df.iterrows():
        st.markdown(f"**{row['Ürün Adı']}**")
        col1, col2 = st.columns(2)
        with col1:
            alis = st.number_input("Alış Fiyatı", value=row["Alış Fiyatı"], step=0.01, key=f"alis_{idx}")
        with col2:
            kar = st.slider("Kar Marjı (%)", 0, 100, int(row["Kar Marjı"]), key=f"kar_{idx}")
        df.at[idx, "Alış Fiyatı"] = alis
        df.at[idx, "Kar Marjı"] = kar
        df.at[idx, "Satış Fiyatı"] = round(alis * (1 + kar / 100), 2)

# Stok sayımı
elif islem == "📦 Stok Sayımı":
    st.subheader("Raf - Kasa - Palet Sayımı")
    raflar = [f"R{str(i).zfill(2)}" for i in range(1, 21)]
    kasalar = [f"K{str(i).zfill(2)}" for i in range(1, 21)]
    paletler = [f"P{str(i).zfill(2)}" for i in range(1, 11)]

    for idx, row in df.iterrows():
        st.markdown(f"**{row['Ürün Adı']}**")
        col1, col2, col3 = st.columns(3)
        with col1:
            raf_no = st.selectbox("Raf No", raflar, key=f"raf_no_{idx}")
            raf_adet = st.number_input("Raf Adeti", min_value=0, step=1, key=f"raf_adet_{idx}")
        with col2:
            kasa_no = st.selectbox("Kasa No", kasalar, key=f"kasa_no_{idx}")
            kasa_adet = st.number_input("Kasa Adeti", min_value=0, step=1, key=f"kasa_adet_{idx}")
        with col3:
            palet_no = st.selectbox("Palet No", paletler, key=f"palet_no_{idx}")
            palet_adet = st.number_input("Palet Adeti", min_value=0, step=1, key=f"palet_adet_{idx}")
        df.at[idx, "Raf No"] = raf_no
        df.at[idx, "Raf Adet"] = raf_adet
        df.at[idx, "Kasa No"] = kasa_no
        df.at[idx, "Kasa Adet"] = kasa_adet
        df.at[idx, "Palet No"] = palet_no
        df.at[idx, "Palet Adet"] = palet_adet

# Tedarikçi bilgisi
elif islem == "🔗 Tedarikçi Bilgisi":
    st.subheader("Tedarikçi ve Fiyat Girişi")
    for idx, row in df.iterrows():
        st.markdown(f"**{row['Ürün Adı']}**")
        tedarikci = st.text_input("Tedarikçi 1", value=row["Tedarikçi 1"], key=f"tedarikci_{idx}")
        fiyat = st.number_input("Fiyat 1", value=row["Fiyat 1"], step=0.01, key=f"tfiyat_{idx}")
        df.at[idx, "Tedarikçi 1"] = tedarikci
        df.at[idx, "Fiyat 1"] = fiyat

# Tablonun tamamını göster
elif islem == "📄 Tüm Tabloyu Görüntüle / İndir":
    st.subheader("Tüm Ürün Tablosu")
    st.dataframe(df)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name="UrunTablosu")

    st.download_button(
        label="📥 Excel İndir",
        data=output.getvalue(),
        file_name="urun_paneli_tek_tablo.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
