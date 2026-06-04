# -*- coding: utf-8 -*-
"""
utils.py
Bu modül, doğrulama, ID yönetimi ve kullanıcı arayüzü (menü) için 
yardımcı fonksiyonları barındırır.
"""

from datetime import datetime
import re

def yeni_id_olustur(liste) -> int:
    """
    Verilen listedeki en büyük ID'yi bulup bir artırarak yeni benzersiz ID üretir.
    Eğer liste boş ise 1 değerini döner.

    Parametreler:
    -------------
    liste : list
        İçerisinde işlem nesneleri barındıran gelirler veya giderler listesi.
    """
    if not liste:
        return 1
    # Liste içerisindeki her bir nesnenin id özniteliğini alıp maksimumu buluruz.
    en_buyuk_id = max(islem.id for islem in liste)
    return en_buyuk_id + 1

def tarih_kontrol(tarih: str) -> bool:
    """
    Girilen tarihin doğru formatta (YYYY-MM-DD) ve gerçek bir tarih 
    olup olmadığını kontrol eder.

    Parametreler:
    -------------
    tarih : str
        Kontrol edilecek tarih metni.
    """
    # Düzenli ifade ile biçim kontrolü (YYYY-MM-DD)
    biçim_regex = r"^\d{4}-\d{2}-\d{2}$"
    if not re.match(biçim_regex, tarih):
        return False
    
    # Gerçek takvim tarihi kontrolü (Örn: 2026-02-30 geçersiz olmalı)
    try:
        datetime.strptime(tarih, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def sayi_kontrol(deger) -> bool:
    """
    Kullanıcıdan alınan değerin sayıya (float veya int) dönüştürülebilir 
    olup olmadığını kontrol eder.

    Parametreler:
    -------------
    deger : str veya any
        Kontrol edilecek değer.
    """
    try:
        float(deger)
        return True
    except (ValueError, TypeError):
        return False

def menu_goster():
    """
    Programın ana menüsünü kullanıcıya ekrana yazdırır.
    """
    print("\n" + "=" * 50)
    print("      KİŞİSEL FİNANS VE HARCAMA TAKİP SİSTEMİ")
    print("=" * 50)
    print("  1. Gelir Ekle")
    print("  2. Gider Ekle")
    print("  3. Tüm İşlemleri Listele")
    print("  4. Finansal Analiz Yap (Pandas & NumPy)")
    print("  5. Grafiksel Rapor Göster (Matplotlib)")
    print("  6. Verileri CSV Dosyasına Kaydet")
    print("  7. Çıkış")
    print("=" * 50)
