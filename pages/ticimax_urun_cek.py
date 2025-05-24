from zeep.helpers import serialize_object

...

if not response:
    st.warning("Hiç ürün bulunamadı.")
else:
    st.success(f"{len(response)} ürün başarıyla çekildi.")
    for idx, urun in enumerate(response, 1):
        st.markdown(f"### {idx}. Ürün")
        u = serialize_object(urun)

        urun_adi = u.get("UrunAdi")
        marka = u.get("Marka")
        stok_kodu = u.get("Varyasyonlar", {}).get("Varyasyon", [{}])[0].get("StokKodu")
        satis_fiyati = u.get("Varyasyonlar", {}).get("Varyasyon", [{}])[0].get("SatisFiyati")
        stok_adedi = u.get("ToplamStokAdedi")
        resimler = u.get("Resimler", {}).get("string", [])

        st.write(f"📦 **Ürün Adı:** {urun_adi}")
        st.write(f"🏷️ **Marka:** {marka}")
        st.write(f"🔖 **Stok Kodu:** {stok_kodu}")
        st.write(f"💰 **Satış Fiyatı:** {satis_fiyati}")
        st.write(f"📦 **Stok Adedi:** {stok_adedi}")

        if resimler:
            st.image(resimler[0], width=200)
        else:
            st.write("🖼️ Resim yok")
        
        st.markdown("---")
