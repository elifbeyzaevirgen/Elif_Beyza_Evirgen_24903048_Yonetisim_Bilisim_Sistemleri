# -*- coding: utf-8 -*-
"""
gorsellestirme.py
Bu modül; Matplotlib kütüphanesini kullanarak finansal verileri 
görselleştiren fonksiyonları barındırır. Grafiklerin hem kaydedilmesini 
hem de gösterilmesini sağlar.
"""

import os
import matplotlib.pyplot as plt
import pandas as pd
from analiz import toplam_gelir_gider, aylik_analiz

# Grafiklerin kaydedileceği varsayılan dizin
CIKTI_DIZINI = "proje_ciktilari"

def dizin_kontrol():
    """Grafik çıktılarının kaydedileceği klasörün varlığını kontrol eder, yoksa oluşturur."""
    if not os.path.exists(CIKTI_DIZINI):
        os.makedirs(CIKTI_DIZINI)

def aylik_grafik(df: pd.DataFrame):
    """
    Aylık gelir ve giderleri karşılaştıran çizgi grafiği oluşturur.
    Grafiği hem gösterir hem de PNG dosyası olarak kaydeder.

    Parametreler:
    -------------
    df : pd.DataFrame
        İşlem verilerini içeren DataFrame.
    """
    if df.empty:
        print("[UYARI] Grafik çizmek için veri bulunamadı.")
        return
        
    dizin_kontrol()
    
    # Aylık analizi alalım
    aylik_df = aylik_analiz(df)
    if aylik_df.empty:
        return
        
    # Yıl_Ay indeksini stringe dönüştürüp sıralayalım
    aylik_df = aylik_df.sort_index()
    aylar = [str(x) for x in aylik_df.index]
    
    plt.figure(figsize=(10, 6), dpi=100)
    
    # Çizgi grafiğini çizelim
    plt.plot(aylar, aylik_df['Toplam_Gelir'], marker='o', linewidth=2.5, color='#2ec4b6', label='Toplam Gelir (TL)')
    plt.plot(aylar, aylik_df['Toplam_Gider'], marker='s', linewidth=2.5, color='#e71d36', label='Toplam Gider (TL)')
    
    # Grafiği süsleyelim
    plt.title('Aylara Göre Gelir ve Gider Karşılaştırması', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Dönem (Yıl-Ay)', fontsize=11, labelpad=10)
    plt.ylabel('Tutar (TL)', fontsize=11, labelpad=10)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(frameon=True, facecolor='white', edgecolor='none', shadow=True, fontsize=10)
    plt.tight_layout()
    
    # Dosyaya kaydet
    dosya_yolu = os.path.join(CIKTI_DIZINI, 'aylik_gelir_gider_cizgi.png')
    plt.savefig(dosya_yolu, bbox_inches='tight')
    print(f"[BAŞARILI] Aylık çizgi grafiği kaydedildi: {dosya_yolu}")
    plt.show()
    plt.close()

def gelir_gider_bar(df: pd.DataFrame):
    """
    Toplam gelir ve gider değerlerini karşılaştıran sütun grafiği oluşturur.
    Grafiği hem gösterir hem de PNG dosyası olarak kaydeder.

    Parametreler:
    -------------
    df : pd.DataFrame
        İşlem verilerini içeren DataFrame.
    """
    if df.empty:
        print("[UYARI] Grafik çizmek için veri bulunamadı.")
        return
        
    dizin_kontrol()
    
    toplam_gelir, toplam_gider = toplam_gelir_gider(df)
    
    kategoriler = ['Toplam Gelir', 'Toplam Gider']
    degerler = [toplam_gelir, toplam_gider]
    renkler = ['#2ec4b6', '#e71d36'] # Gelir için turkuaz, Gider için kırmızımsı pembe
    
    plt.figure(figsize=(8, 6), dpi=100)
    
    # Sütunları çizelim
    barlar = plt.bar(kategoriler, degerler, color=renkler, width=0.5, edgecolor='none', zorder=3)
    
    # Sütunların üzerine değerleri yazalım
    for bar in barlar:
        yukseklik = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yukseklik + (max(degerler) * 0.01),
                 f'{yukseklik:,.2f} TL', ha='center', va='bottom', fontsize=10, fontweight='bold')
                 
    # Grafiği süsleyelim
    plt.title('Toplam Gelir ve Gider Durumu', fontsize=14, fontweight='bold', pad=15)
    plt.ylabel('Tutar (TL)', fontsize=11, labelpad=10)
    plt.grid(True, axis='y', linestyle='--', alpha=0.5, zorder=0)
    
    # Y ekseni limitini biraz arttıralım ki sayılar sığsın
    plt.ylim(0, max(degerler) * 1.15 if max(degerler) > 0 else 100)
    plt.tight_layout()
    
    # Dosyaya kaydet
    dosya_yolu = os.path.join(CIKTI_DIZINI, 'toplam_gelir_gider_bar.png')
    plt.savefig(dosya_yolu, bbox_inches='tight')
    print(f"[BAŞARILI] Toplam sütun grafiği kaydedildi: {dosya_yolu}")
    plt.show()
    plt.close()

def pasta_grafik(df: pd.DataFrame):
    """
    Toplam gelir ve gider oranlarını gösteren pasta grafiği oluşturur.
    Grafiği hem gösterir hem de PNG dosyası olarak kaydeder.

    Parametreler:
    -------------
    df : pd.DataFrame
        İşlem verilerini içeren DataFrame.
    """
    if df.empty:
        print("[UYARI] Grafik çizmek için veri bulunamadı.")
        return
        
    dizin_kontrol()
    
    toplam_gelir, toplam_gider = toplam_gelir_gider(df)
    
    if toplam_gelir == 0 and toplam_gider == 0:
        print("[UYARI] Grafik çizmek için sıfırdan büyük gelir veya gider verisi olmalıdır.")
        return
        
    kategoriler = ['Gelir Oranı', 'Gider Oranı']
    degerler = [toplam_gelir, toplam_gider]
    renkler = ['#2ec4b6', '#e71d36']
    
    plt.figure(figsize=(7, 7), dpi=100)
    
    # Pasta dilimlerini çizelim
    # autopct yardımıyla yüzde oranlarını gösterelim
    explode = (0.05, 0) if toplam_gelir > 0 and toplam_gider > 0 else (0, 0) # Gelir dilimini hafifçe öne çıkaralım
    
    plt.pie(degerler, labels=kategoriler, colors=renkler, autopct='%1.1f%%',
            startangle=140, explode=explode, shadow=True, 
            textprops={'fontsize': 11, 'fontweight': 'bold'},
            wedgeprops={'edgecolor': 'white', 'linewidth': 1})
            
    plt.title('Toplam Gelir / Gider Dağılımı (%)', fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    
    # Dosyaya kaydet
    dosya_yolu = os.path.join(CIKTI_DIZINI, 'gelir_gider_pasta.png')
    plt.savefig(dosya_yolu, bbox_inches='tight')
    print(f"[BAŞARILI] Gelir/gider dağılım pasta grafiği kaydedildi: {dosya_yolu}")
    plt.show()
    plt.close()
