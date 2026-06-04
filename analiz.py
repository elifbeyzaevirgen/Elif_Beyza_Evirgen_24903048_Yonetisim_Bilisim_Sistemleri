# -*- coding: utf-8 -*-
"""
analiz.py
Bu modül; gelir ve gider verilerini Pandas DataFrame yapısına dönüştürür,
Pandas ve NumPy kullanarak istatistiksel ve özet finansal analizler yapar.
"""

import pandas as pd
import numpy as np

def verileri_dataframe_yap(gelirler, giderler) -> pd.DataFrame:
    """
    Gelir ve gider listelerindeki Islem nesnelerini birleştirerek 
    bir Pandas DataFrame yapısına dönüştürür.
    Eğer veri yoksa gerekli sütunlara sahip boş bir DataFrame döner.

    Parametreler:
    -------------
    gelirler : list
        Gelir nesnelerini içeren liste.
    giderler : list
        Gider nesnelerini içeren liste.
    """
    # Her bir işlem nesnesinin özniteliklerini sözlük formatına getiriyoruz.
    veri_listesi = []
    
    for islem in gelirler:
        veri_listesi.append({
            'id': islem.id,
            'tutar': islem.tutar,
            'tarih': islem.tarih,
            'aciklama': islem.aciklama,
            'tip': islem.tip
        })
        
    for islem in giderler:
        veri_listesi.append({
            'id': islem.id,
            'tutar': islem.tutar,
            'tarih': islem.tarih,
            'aciklama': islem.aciklama,
            'tip': islem.tip
        })
        
    df = pd.DataFrame(veri_listesi)
    
    if df.empty:
        # Eğer veri yoksa boş ama doğru sütunlara sahip DataFrame oluşturulur.
        df = pd.DataFrame(columns=['id', 'tutar', 'tarih', 'aciklama', 'tip'])
        
    # 'tarih' sütununu datetime formatına çevirelim (tarih tabanlı gruplamalar için)
    df['tarih'] = pd.to_datetime(df['tarih'])
    return df

def toplam_gelir_gider(df: pd.DataFrame) -> tuple:
    """
    DataFrame üzerinden toplam gelir ve toplam gider değerlerini hesaplar.
    
    Parametreler:
    -------------
    df : pd.DataFrame
        İşlem verilerini içeren DataFrame.

    Geri Dönüş:
    -----------
    tuple : (toplam_gelir, toplam_gider)
    """
    if df.empty:
        return 0.0, 0.0
        
    # Gelir ve gider satırlarını süzüp 'tutar' sütunlarının toplamını alıyoruz.
    toplam_gelir = df[df['tip'] == 'gelir']['tutar'].sum()
    toplam_gider = df[df['tip'] == 'gider']['tutar'].sum()
    
    return float(toplam_gelir), float(toplam_gider)

def aylik_analiz(df: pd.DataFrame) -> pd.DataFrame:
    """
    Verileri tarihe göre (Yıl-Ay bazında) gruplayarak aylık bazda özet analiz oluşturur.
    Her ay için toplam gelir, toplam gider ve net bakiye (kâr/zarar) durumunu gösterir.

    Parametreler:
    -------------
    df : pd.DataFrame
        İşlem verilerini içeren DataFrame.
    """
    if df.empty:
        print("[UYARI] Analiz edilecek veri bulunamadı.")
        return pd.DataFrame()
        
    # Tarih kolonundan Yıl-Ay (YYYY-MM) bilgisini türetelim.
    df_temp = df.copy()
    df_temp['Yil_Ay'] = df_temp['tarih'].dt.to_period('M')
    
    # Pivot tablo oluşturarak aylara göre gelir ve giderleri toplayalım.
    aylik_pivot = df_temp.pivot_table(
        index='Yil_Ay', 
        columns='tip', 
        values='tutar', 
        aggfunc='sum'
    ).fillna(0)
    
    # Gerekli kolonların varlığını garanti edelim
    if 'gelir' not in aylik_pivot.columns:
        aylik_pivot['gelir'] = 0.0
    if 'gider' not in aylik_pivot.columns:
        aylik_pivot['gider'] = 0.0
        
    # Net Bakiye ve Kümülatif Bakiye kolonlarını hesaplayalım
    aylik_pivot['Net_Bakiye'] = aylik_pivot['gelir'] - aylik_pivot['gider']
    
    # Tabloyu daha anlaşılır kolon isimleriyle güncelleyelim.
    aylik_pivot = aylik_pivot.rename(columns={'gelir': 'Toplam_Gelir', 'gider': 'Toplam_Gider'})
    
    return aylik_pivot

def numpy_istatistik(df: pd.DataFrame) -> dict:
    """
    NumPy kullanarak veri (tutar) üzerinde ortalama, minimum, maksimum ve 
    standart sapma hesaplar. Analizi tüm işlemler, gelirler ve giderler olarak ayırır.

    Parametreler:
    -------------
    df : pd.DataFrame
        İşlem verilerini içeren DataFrame.
    """
    istatistikler = {
        'genel': {'ortalama': 0.0, 'min': 0.0, 'mak': 0.0, 'std_sapma': 0.0},
        'gelir': {'ortalama': 0.0, 'min': 0.0, 'mak': 0.0, 'std_sapma': 0.0},
        'gider': {'ortalama': 0.0, 'min': 0.0, 'mak': 0.0, 'std_sapma': 0.0}
    }
    
    if df.empty:
        return istatistikler
        
    # NumPy dizilerine (array) dönüştürüp istatistikleri hesaplıyoruz.
    tutarlar_genel = df['tutar'].to_numpy()
    if len(tutarlar_genel) > 0:
        istatistikler['genel']['ortalama'] = np.mean(tutarlar_genel)
        istatistikler['genel']['min'] = np.min(tutarlar_genel)
        istatistikler['genel']['mak'] = np.max(tutarlar_genel)
        istatistikler['genel']['std_sapma'] = np.std(tutarlar_genel)
        
    tutarlar_gelir = df[df['tip'] == 'gelir']['tutar'].to_numpy()
    if len(tutarlar_gelir) > 0:
        istatistikler['gelir']['ortalama'] = np.mean(tutarlar_gelir)
        istatistikler['gelir']['min'] = np.min(tutarlar_gelir)
        istatistikler['gelir']['mak'] = np.max(tutarlar_gelir)
        istatistikler['gelir']['std_sapma'] = np.std(tutarlar_gelir)
        
    tutarlar_gider = df[df['tip'] == 'gider']['tutar'].to_numpy()
    if len(tutarlar_gider) > 0:
        istatistikler['gider']['ortalama'] = np.mean(tutarlar_gider)
        istatistikler['gider']['min'] = np.min(tutarlar_gider)
        istatistikler['gider']['mak'] = np.max(tutarlar_gider)
        istatistikler['gider']['std_sapma'] = np.std(tutarlar_gider)
        
    return istatistikler
