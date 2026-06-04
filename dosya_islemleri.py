# -*- coding: utf-8 -*-
"""
dosya_islemleri.py
Bu modül; gelir ve gider verilerinin CSV dosyasına kaydedilmesi ve 
CSV dosyasından geri okunması işlemlerini gerçekleştirir.
"""

import csv
import os
from finans_modeli import Islem

def csv_kaydet(dosya_adi: str, gelirler, giderler) -> bool:
    """
    Tüm gelir ve gider verilerini belirtilen CSV dosyasına kaydeder.

    Parametreler:
    -------------
    dosya_adi : str
        Kaydedilecek CSV dosyasının adı veya yolu (örn: 'finans_verileri.csv').
    gelirler : list
        Gelir nesnelerini içeren liste.
    giderler : list
        Gider nesnelerini içeren liste.
    """
    try:
        # CSV dosyasını yazma modunda açıyoruz. UTF-8 kodlama Türkçe karakterler için önemlidir.
        with open(dosya_adi, mode='w', newline='', encoding='utf-8') as dosya:
            yazici = csv.writer(dosya, delimiter=';')
            
            # Başlık satırı
            yazici.writerow(['id', 'tutar', 'tarih', 'aciklama', 'tip'])
            
            # Gelirleri yaz
            for islem in gelirler:
                yazici.writerow([islem.id, islem.tutar, islem.tarih, islem.aciklama, islem.tip])
                
            # Giderleri yaz
            for islem in giderler:
                yazici.writerow([islem.id, islem.tutar, islem.tarih, islem.aciklama, islem.tip])
                
        print(f"[BAŞARILI] Veriler başarıyla '{dosya_adi}' dosyasına kaydedildi. Toplam {len(gelirler) + len(giderler)} kayıt.")
        return True
    except Exception as e:
        print(f"[HATA] CSV dosyası kaydedilirken bir hata oluştu: {e}")
        return False

def csv_oku(dosya_adi: str) -> tuple:
    """
    Belirtilen CSV dosyasındaki verileri okuyarak gelir ve gider listelerini oluşturur.
    Dosya bulunamazsa veya boşsa boş listeler döndürür.

    Parametreler:
    -------------
    dosya_adi : str
        Okunacak CSV dosyasının adı veya yolu.

    Geri Dönüş:
    -----------
    tuple : (gelirler, giderler)
        Gelir ve gider nesnelerini barındıran iki ayrı liste.
    """
    gelirler = []
    giderler = []
    
    if not os.path.exists(dosya_adi):
        print(f"[BİLGİ] '{dosya_adi}' dosyası bulunamadı. Boş veri listeleriyle başlanıyor.")
        return gelirler, giderler
        
    try:
        with open(dosya_adi, mode='r', newline='', encoding='utf-8') as dosya:
            okuyucu = csv.reader(dosya, delimiter=';')
            
            # Başlık satırını oku ve atla
            baslik = next(okuyucu, None)
            if baslik is None:
                return gelirler, giderler
                
            for satir in okuyucu:
                if not satir:
                    continue
                # Sütunları ayrıştır
                try:
                    islem_id = int(satir[0])
                    tutar = float(satir[1])
                    tarih = satir[2]
                    aciklama = satir[3]
                    tip = satir[4]
                    
                    islem = Islem(id=islem_id, tutar=tutar, tarih=tarih, aciklama=aciklama, tip=tip)
                    
                    if tip == 'gelir':
                        gelirler.append(islem)
                    elif tip == 'gider':
                        giderler.append(islem)
                except (ValueError, IndexError) as ve:
                    print(f"[UYARI] CSV dosyasında bozuk satır atlandı: {satir}. Hata: {ve}")
                    
        print(f"[BAŞARILI] '{dosya_adi}' dosyasından veriler yüklendi: {len(gelirler)} Gelir, {len(giderler)} Gider.")
        return gelirler, giderler
    except Exception as e:
        print(f"[HATA] CSV dosyası okunurken bir hata oluştu: {e}")
        return [], []
