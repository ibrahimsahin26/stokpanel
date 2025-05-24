import streamlit as st
from zeep import Client
from zeep.helpers import serialize_object

st.set_page_config(page_title="Ticimax Ürün Çek", layout="wide")
st.title("📦 Ticimax Ürünlerini Panele Yükle")

# Yetki kodu ve servis adresi
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"
SERVICE_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"

try:
    client = Client(wsdl=SERVICE_URL)
    st.success("Servis bağlantısı başarılı.")
except Exception as e:
    st.error(f"Servis bağlantısı başarısız: {e}")
    st.stop()

if st.button("🔄 Ticimax'tan Ürünleri Al"):
    try:
        response = client.service.SelectUrun(
            UyeKodu=UYE_KODU,
            f={},
            s={"BaslangicIndex": 0, "KayitSayisi": 5, "KayitSayisinaGoreGetir": True, "SiralamaDegeri": "", "SiralamaYonu": ""}
        )
        
        # Eğer gelen veri boşsa uyarı ver
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
    
    except Exception as e:
        st.error(f"Hata oluştu: {e}")
