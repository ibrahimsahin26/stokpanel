
import streamlit as st
import pandas as pd
from io import BytesIO

# Sayfa basligi
st.title("Stok Sayim Paneli")

# Ornek veri yukleme (demo amacli)
data = {
    "Barkod": [8691927462334, 8690060127001, 8999921546549, 8699435012997],
    "Urun Adi": [
        "Kraf Zimba Teli Sokücü 50G",
        "Delta Tel Sokücü 24/6",
        "Üçgen Proje Kutusu",
        "Assis Pens Tipi Zimba Makinası 24/6"
    ],
    "Kategori": [
        "Zimba Teli Sokücü",
        "Zimba Teli Sokücü",
        "Arşivleme Kutusu",
        "Zimba Makinası"
    ],
    "Marka": ["Kraf", "Delta", "Üçgen", "Cassa"],
    "Mevcut Stok": [115, 2, 0, 7],
    "Alış Fiyatı": [10.80, 4.45, 10.00, 17.11],
    "Raf": [8, 8, None, 2],
}

stok_df = pd.DataFrame(data)
stok_df["Sayim Adedi"] = 0
stok_df["Fark"] = 0

# Ürün seçimi veya barkodla arama
barkod_input = st.text_input("Barkod Girin veya Ürün Seçin")

# Barkodla eşleşen ürün filtrelemesi
temp_df = stok_df.copy()
if barkod_input:
    temp_df = temp_df[temp_df["Barkod"].astype(str).str.contains(barkod_input)]

# Sayim işlemi
for idx, row in temp_df.iterrows():
    sayim = st.number_input(
        f"{row['Urun Adi']} - Mevcut: {row['Mevcut Stok']}",
        min_value=0,
        step=1,
        key=str(idx)
    )
    stok_df.at[idx, "Sayim Adedi"] = sayim
    stok_df.at[idx, "Fark"] = sayim - row["Mevcut Stok"]

# Tabloyu göster
st.subheader("Güncel Sayim Durumu")
st.dataframe(stok_df)

# Excel çıktısı
if st.button("Excel Olarak İndir"):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        stok_df.to_excel(writer, index=False, sheet_name="Sayim")
    st.download_button(
        label="Excel İndir",
        data=output.getvalue(),
        file_name="stok_sayim.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
