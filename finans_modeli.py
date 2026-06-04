# -*- coding: utf-8 -*-
"""
finans_modeli.py
Bu modül, finansal işlemleri temsil eden veri modellerini içerir.
Final Projesi gereksinimlerine uygun olarak Islem sınıfını tanımlar.
"""

class Islem:
    """
    Kişisel finans ve harcama takip sistemindeki her bir işlemi temsil eden sınıf.
    """
    def __init__(self, id: int, tutar: float, tarih: str, aciklama: str, tip: str):
        """
        Islem sınıfının yapıcı (constructor) metodu.

        Parametreler:
        -------------
        id : int
            İşlemin benzersiz kimlik numarası (ID).
        tutar : float
            İşlem tutarı (örn: 1500.50).
        tarih : str
            İşlemin gerçekleştiği tarih (Format: YYYY-MM-DD).
        aciklama : str
            İşleme dair açıklama.
        tip : str
            İşlemin türü. 'gelir' veya 'gider' değerlerini alır.
        """
        self.id = id
        self.tutar = tutar
        self.tarih = tarih
        self.aciklama = aciklama
        self.tip = tip

    def __str__(self) -> str:
        """
        İşlem nesnesinin okunabilir string gösterimi.
        """
        return f"ID: {self.id} | Tip: {self.tip.upper()} | Tutar: {self.tutar:.2f} TL | Tarih: {self.tarih} | Açıklama: {self.aciklama}"
