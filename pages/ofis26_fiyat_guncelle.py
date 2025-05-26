import streamlit as st
import pandas as pd
import requests
from lxml import etree

# Ticimax API ayarları
WSDL_URL = "https://www.ofis26.com/Servis/UrunServis.svc"
UYE_KODU = "HVEKN1KK1USEAD0VAXTVKP8FWGN3AE"
CSV_YOLU = "pages/veri_kaynaklari/ana_urun_listesi.csv"

def satis_fiyatlarini_cek():
    headers = {
        "Content-Type": "text/xml;charset=UTF-8",
        "SOAPAction": "http://tempuri.org/IUrunServis/SelectUrun"
    }

    soap_body = f"""
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/" xmlns:ns="http://schemas.datacontract.org/2004/07/">
       <soapenv:Header/>
       <soapenv:Body>
          <tem:SelectUrun>
             <tem:UyeKodu>{UYE_KODU}</tem:UyeKodu>
             <tem:f>
                <ns:Aktif>-1</ns:Aktif>
                <ns:Firsat>-1</ns:Firsat>
                <ns:Indirimli>-1</ns:Indirimli>
                <ns:Vitrin>-1</ns:Vitrin>
                <ns:KategoriID>0</ns:KategoriID>
                <ns:MarkaID>0</ns:MarkaID>
                <ns:TedarikciID>-1</ns:TedarikciID>
                <ns:ToplamStokAdediBas>0</ns:ToplamStokAdediBas>
                <ns:ToplamStokAdediSon>100</ns:ToplamStokAdediSon>
                <ns:UrunKartiID>0</ns:UrunKartiID>
             </tem:f>
             <tem:s>
                <ns:BaslangicIndex>0</ns:BaslangicIndex>
                <ns:KayitSayisi>200</ns:KayitSayisi>
             </tem:s>
          </tem:SelectUrun>
       </soapenv:Body>
    </soapenv:Envelope>
    """

    response = requests.post(WSDL_URL, data=soap_body.encode("utf-8"), headers=headers)
    tree = etree.fromstring(response.content)
    
    ns = {
        'a': 'http://schemas.datacontract.org/2004/07/',
        's': 'http://schemas.xmlsoap.org/soap/envelope/'
    }

    urunler = tree.xpath('.//a:Urun', namespaces=ns)
    data = []
    for urun in urunler:
        stok_kodu = urun.findtext('a:StokKodu', namespaces=ns)
        satis_fiyati = urun.findtext('a:SatisFiyati', namespaces=ns)
        data.append({
            "Stok Kodu": stok_kodu,
            "Ofis26 Satış Fiyatı": float(satis_fiyati or 0)
        })

    return pd.DataFrame(data)

def main():
    st.title("🛒 Ticimax Ürün Fiyatlarını Güncelle")

    if st.button("📥 Satış Fiyatlarını Ticimax'ten Çek"):
        try:
            df_ticimax = satis_fiyatlarini_cek()
            if df_ticimax.empty:
                st.warning("Ürün listesi boş veya çekilemedi.")
                return

            df_local = pd.read_csv(CSV_YOLU)
            df_local = df_local.merge(df_ticimax, how="left", on="Stok Kodu", suffixes=('', '_yeni'))

            # Yeni gelen fiyatı güncelle
            df_local['Ofis26 Satış Fiyatı'] = df_local['Ofis26 Satış Fiyatı_yeni'].fillna(df_local['Ofis26 Satış Fiyatı'])
            df_local.drop(columns=['Ofis26 Satış Fiyatı_yeni'], inplace=True)

            df_local.to_csv(CSV_YOLU, index=False)
            st.success("Satış fiyatları başarıyla güncellendi.")
        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")

main()
