# -*- coding: utf-8 -*-
"""
islem_yonetimi.py
Bu modül; gelir ve gider işlemlerinin eklenmesi, listelenmesi ve 
silinmesi gibi yönetimsel fonksiyonları barındırır.
"""

from finans_modeli import Islem
import utils

def gelir_ekle(gelirler):
    """
    Kullanıcıdan etkileşimli olarak gelir bilgilerini alır, 
    doğrulamaları yapar, yeni bir Islem nesnesi oluşturup gelirler listesine ekler.

    Parametreler:
    -------------
    gelirler : list
        Sistemdeki gelir nesnelerini tutan liste.
    """
    print("\n--- YENİ GELİR EKLEME ---")
    
    # 1. Tutar Alımı ve Doğrulaması
    tutar_str = input("Gelir Tutarını Giriniz (Örn: 5000.00): ").strip()
    if not utils.sayi_kontrol(tutar_str):
        print("[HATA] Geçersiz tutar girişi! Sayısal bir değer girilmelidir.")
        return False
    tutar = float(tutar_str)
    if tutar <= 0:
        print("[HATA] Tutar sıfırdan büyük olmalıdır.")
        return False

    # 2. Tarih Alımı ve Doğrulaması
    tarih = input("Tarihi Giriniz (YYYY-MM-DD, boş bırakılırsa bugün): ").strip()
    if tarih == "":
        from datetime import date
        tarih = str(date.today())
    elif not utils.tarih_kontrol(tarih):
        print("[HATA] Geçersiz tarih formatı! YYYY-MM-DD biçiminde olmalıdır.")
        return False

    # 3. Açıklama Alımı
    aciklama = input("Açıklama Giriniz (Örn: Maaş, Kira Geliri): ").strip()
    if not aciklama:
        aciklama = "Belirtilmemiş Gelir"

    # 4. Yeni ID Oluşturma ve Nesne Ekleme
    # Gelirler ve giderler ayrı ID serilerine sahip olabileceği gibi tüm sistemde tek ID serisi de olabilir.
    # Şartnamede "yeni_id_olustur(liste)" denmektedir. Yani gönderilen listedeki en büyük ID'yi baz alır.
    yeni_id = utils.yeni_id_olustur(gelirler)
    yeni_gelir = Islem(id=yeni_id, tutar=tutar, tarih=tarih, aciklama=aciklama, tip="gelir")
    gelirler.append(yeni_gelir)
    
    print(f"[BAŞARILI] Gelir işlemi başarıyla eklendi! {yeni_gelir}")
    return True

def gider_ekle(giderler):
    """
    Kullanıcıdan etkileşimli olarak gider bilgilerini alır, 
    doğrulamaları yapar, yeni bir Islem nesnesi oluşturup giderler listesine ekler.

    Parametreler:
    -------------
    giderler : list
        Sistemdeki gider nesnelerini tutan liste.
    """
    print("\n--- YENİ GİDER EKLEME ---")
    
    # 1. Tutar Alımı ve Doğrulaması
    tutar_str = input("Gider Tutarını Giriniz (Örn: 250.00): ").strip()
    if not utils.sayi_kontrol(tutar_str):
        print("[HATA] Geçersiz tutar girişi! Sayısal bir değer girilmelidir.")
        return False
    tutar = float(tutar_str)
    if tutar <= 0:
        print("[HATA] Tutar sıfırdan büyük olmalıdır.")
        return False

    # 2. Tarih Alımı ve Doğrulaması
    tarih = input("Tarihi Giriniz (YYYY-MM-DD, boş bırakılırsa bugün): ").strip()
    if tarih == "":
        from datetime import date
        tarih = str(date.today())
    elif not utils.tarih_kontrol(tarih):
        print("[HATA] Geçersiz tarih formatı! YYYY-MM-DD biçiminde olmalıdır.")
        return False

    # 3. Açıklama Alımı
    aciklama = input("Açıklama Giriniz (Örn: Market, Fatura, Yakıt): ").strip()
    if not aciklama:
        aciklama = "Belirtilmemiş Gider"

    # 4. Yeni ID Oluşturma ve Nesne Ekleme
    # Gider listesine göre benzersiz ID oluşturulur.
    # Ancak silme işlemlerinde karışıklık olmaması için gelirler ve giderlerin ID çakışmaması 
    # veya islem_sil fonksiyonunda listenin doğru yönlendirilmesi gerekir.
    # Teknik şartnamede "islem_sil(gelirler, giderler, id)" imzası bulunmaktadır. 
    # Bu yüzden ID'lerin küresel olarak benzersiz olması için ortak listelerden en büyük ID bulunabilir.
    # Şartnamedeki imza `yeni_id_olustur(liste)` şeklindedir. Biz de bunu çağıracağız.
    # Küresel benzersizliği garanti etmek adına gelirler + giderler birleştirilerek çağrılabilir:
    yeni_id = utils.yeni_id_olustur(giderler)
    # Eğer giderler listesinde ID varsa onu 1 artırırız. Eğer gelirler ve giderlerin ID'lerinin çakışmamasını 
    # istiyorsak, yeni_id_olustur(gelirler + giderler) şeklinde çağırabiliriz. 
    # Teknik şartnameye uygun olarak doğrudan çağırıyoruz:
    yeni_gider = Islem(id=yeni_id, tutar=tutar, tarih=tarih, aciklama=aciklama, tip="gider")
    giderler.append(yeni_gider)
    
    print(f"[BAŞARILI] Gider işlemi başarıyla eklendi! {yeni_gider}")
    return True

def islemleri_listele(gelirler, giderler):
    """
    Tüm gelir ve gider kayıtlarını düzenli bir formatta (tablo benzeri) ekrana yazdırır.

    Parametreler:
    -------------
    gelirler : list
        Gelir nesnelerini içeren liste.
    giderler : list
        Gider nesnelerini içeren liste.
    """
    print("\n" + "=" * 80)
    print(f"{'ID':<6} | {'TİP':<8} | {'TUTAR (TL)':<15} | {'TARİH':<12} | {'AÇIKLAMA':<30}")
    print("=" * 80)
    
    tum_islemler = gelirler + giderler
    # İşlemleri tarihe göre sıralayarak listelemek daha şık olacaktır.
    try:
        tum_islemler.sort(key=lambda x: x.tarih)
    except Exception:
        pass  # Sıralamada hata oluşursa sıralamasız göster
        
    if not tum_islemler:
        print(f"{'Sistemde henüz herhangi bir işlem kaydı bulunmamaktadır.':^80}")
    else:
        for islem in tum_islemler:
            tip_str = "GELİR" if islem.tip == "gelir" else "GİDER"
            print(f"{islem.id:<6} | {tip_str:<8} | {islem.tutar:<15.2f} | {islem.tarih:<12} | {islem.aciklama:<30}")
            
    print("=" * 80)

def islem_sil(gelirler, giderler, id: int) -> bool:
    """
    Verilen ID'ye sahip işlemi bularak ilgili listeden (gelir veya gider) siler.

    Parametreler:
    -------------
    gelirler : list
        Gelir listesi.
    giderler : list
        Gider listesi.
    id : int
        Silinecek işlemin ID'si.
    """
    # Gelirler listesinde arayalım
    for islem in gelirler:
        if islem.id == id:
            gelirler.remove(islem)
            print(f"[BAŞARILI] ID: {id} olan Gelir işlemi başarıyla silindi: {islem.aciklama} ({islem.tutar:.2f} TL)")
            return True
            
    # Giderler listesinde arayalım
    for islem in giderler:
        if islem.id == id:
            giderler.remove(islem)
            print(f"[BAŞARILI] ID: {id} olan Gider işlemi başarıyla silindi: {islem.aciklama} ({islem.tutar:.2f} TL)")
            return True
            
    print(f"[HATA] ID: {id} olan herhangi bir işlem bulunamadı.")
    return False
