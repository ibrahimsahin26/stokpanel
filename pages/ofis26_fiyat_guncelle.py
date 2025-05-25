import streamlit as st
import pandas as pd
from zeep import Client
from zeep.transports import Transport
import os

# CSV dosyasının yolu
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

# SOAP servis bilgileri
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc?wsdl"
UYE_KODU = "HVEKN1K1USEAD0VAXTVKP8FWGN3AE"

# Streamlit sayfa ayarı
st.set_page_config(layout="wide")
st.title("\U0001f504 Ofis26 Satış Fiyatlarını Güncelle")

# Ana işlev
if st.button("\U0001f4be Fiyatları Güncelle (Ticimax)"):
    if not os.path.exists(CSV_YOLU):
        st.error("Ana ürün listesi dosyası bulunamadı.")
    else:
        try:
            # CSV oku
            df = pd.read_csv(CSV_YOLU)
            if "Stok Kodu" not in df.columns:
                st.error("CSV'de 'Stok Kodu' sütunu eksik.")
            else:
                # SOAP istemci
                client = Client(wsdl=WSDL_URL, transport=Transport(timeout=60))
                UrunFiltre = client.get_type("ns0:UrunFiltre")
                SelectUrun = client.get_type("ns0:SelectUrun")

                ofis26_fiyatlar = []
                
                for stok_kodu in df["Stok Kodu"].dropna().astype(str):
                    stok_kodu_normalize = stok_kodu.strip().upper()
                    filtre = UrunFiltre(
                        UyeKodu=UYE_KODU,
                        StokKodu=stok_kodu_normalize
                    )
                    try:
                        sonuc = client.service.SelectUrun(filtre)
                        if sonuc and hasattr(sonuc, "Urun"):
                            satis_fiyati = sonuc.Urun.SatisFiyati
                            ofis26_fiyatlar.append((stok_kodu_normalize, satis_fiyati))
                            st.write(f"{stok_kodu_normalize}: {satis_fiyati}")
                        else:
                            ofis26_fiyatlar.append((stok_kodu_normalize, None))
                            st.warning(f"{stok_kodu_normalize}: Fiyat bilgisi bulunamadı.")
                    except Exception as ex:
                        st.warning(f"{stok_kodu_normalize}: Hata - {str(ex)}")
                        ofis26_fiyatlar.append((stok_kodu_normalize, None))

                # Fiyatları DataFrame'e aktar
                fiyat_df = pd.DataFrame(ofis26_fiyatlar, columns=["Stok Kodu", "Ofis26 Satış Fiyatı"])
                df["Stok Kodu"] = df["Stok Kodu"].astype(str).str.strip().str.upper()
                df = df.merge(fiyat_df, on="Stok Kodu", how="left", suffixes=("", "_Yeni"))
                
                # Yeni fiyat sütununu mevcut sütuna aktar
                if "Ofis26 Satış Fiyatı_Yeni" in df.columns:
                    df["Ofis26 Satış Fiyatı"] = df["Ofis26 Satış Fiyatı_Yeni"]
                    df.drop(columns=["Ofis26 Satış Fiyatı_Yeni"], inplace=True)

                # CSV'ye kaydet
                df.to_csv(CSV_YOLU, index=False)
                st.success("Ofis26 satış fiyatları başarıyla güncellendi.")

        except Exception as e:
            st.error(f"Hata oluştu: {e}")
