from zeep.helpers import serialize_object

...

for idx, urun in enumerate(response, 1):
    st.markdown(f"### {idx}. Ürün")

    if urun is None:
        st.error("Bu ürün verisi 'NoneType' döndü. Atlanıyor.")
        continue

    u = serialize_object(urun)

    if not isinstance(u, dict):
        st.error("Ürün verisi beklenmedik biçimde geldi. Atlanıyor.")
        continue

    urun_adi = u.get("UrunAdi", "Belirsiz")
    marka = u.get("Marka", "Belirsiz")
    varyasyon = u.get("Varyasyonlar", {}).get("Varyasyon")
    
    if isinstance(varyasyon, list) and varyasyon:
        stok_kodu = varyasyon[0].get("StokKodu", "Yok")
        satis_fiyati = varyasyon[0].get("SatisFiyati", "Yok")
    elif isinstance(varyasyon, dict):
        stok_kodu = varyasyon.get("StokKodu", "Yok")
        satis_fiyati = varyasyon.get("SatisFiyati", "Yok")
    else:
        stok_kodu = "Yok"
        satis_fiyati = "Yok"

    stok_adedi = u.get("ToplamStokAdedi", "Yok")
    resimler = u.get("Resimler", {}).get("string", [])

    st.write(f"📦 **Ürün Adı:** {urun_adi}")
    st.write(f"🏷️ **Marka:** {marka}")
    st.write(f"🔖 **Stok Kodu:** {stok_kodu}")
    st.write(f"💰 **Satış Fiyatı:** {satis_fiyati}")
    st.write(f"📦 **Stok Adedi:** {stok_adedi}")

    if isinstance(resimler, list) and resimler:
        st.image(resimler[0], width=200)
    elif isinstance(resimler, str) and resimler:
        st.image(resimler, width=200)
    else:
        st.write("🖼️ Resim yok")

    st.markdown("---")
