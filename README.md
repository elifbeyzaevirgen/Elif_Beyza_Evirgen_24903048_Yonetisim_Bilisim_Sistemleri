# KİŞİSEL FİNANS VE HARCAMA TAKİP SİSTEMİ
## BGY210 - Python Programlama II Bahar Dönemi Bireysel Final Proje Ödevi Raporu

**Geliştirici Bilgileri:**
- **Öğrenci Adı Soyadı:** Elif Beyza Evirgen
- **Öğrenci Numarası:** 24903048
- **Bölümü:** Yönetişim Bilişim Sistemleri

---

## 1. PROJE TANIMI VE AMACI
Bu proje, öğrencilerin Python programlama dili ile dönem boyunca öğrendikleri temel ve ileri düzey konuları (modüler yazılım geliştirme, nesne tabanlı programlama, dosya işlemleri, hata yönetimi, Pandas & NumPy ile veri analizi ve Matplotlib ile veri görselleştirme) bir araya getirerek gerçek dünya problemlerine yönelik modüler ve veri odaklı bir yazılım geliştirme yetkinliğini göstermek amacıyla tasarlanmıştır.

Geliştirilen **Kişisel Finans ve Harcama Takip Sistemi**, kullanıcıların gelir ve giderlerini kaydetmesini, listelemesini, Pandas ve NumPy kullanarak ayrıntılı finansal/istatistiksel analizler yapmasını, Matplotlib kütüphanesi yardımıyla bu analizleri görsel grafik raporlara dönüştürmesini ve verilerini kalıcı bir CSV dosyasında saklamasını sağlar.

---

## 2. PROJE KLASÖR YAPISI VE MODÜLLER
Proje, temiz kod (Clean Code) prensiplerine uygun olarak modüler bir mimaride tasarlanmıştır. Dosya ağacı aşağıdaki şekildedir:

```text
Elif_Beyza_Evirgen_24903048_Yonetisim_Bilisim_Sistemleri/
├── main.ipynb            # Projenin ana Jupyter Notebook dosyası (Açıklamalar ve Çalıştırma)
├── finans_modeli.py      # Islem sınıf yapısı ve nesne yönelimli modelleme
├── islem_yonetimi.py      # Gelir ve gider ekleme, listeleme, silme işlemleri
├── dosya_islemleri.py    # CSV formatında veri okuma ve yazma işlemleri
├── analiz.py             # Pandas & NumPy ile istatistiksel hesaplamalar ve özet analizler
├── gorsellestirme.py     # Matplotlib ile çizgi, bar ve pasta grafiklerinin üretilmesi
├── utils.py              # ID üretme, tarih ve sayı doğrulama, konsol menüsü gösterimi
└── proje_ciktilari/      # Otomatik üretilen rapor grafiklerinin ve ekran görüntülerinin bulunduğu dizin
    ├── finans_verileri.csv
    ├── aylik_gelir_gider_cizgi.png
    ├── toplam_gelir_gider_bar.png
    ├── gelir_gider_pasta.png
    ├── ss_console_menu.png
    ├── ss_console_list.png
    ├── ss_console_analysis.png
    └── ss_console_add.png
```

---

## 3. VERİ YAPILARI VE NESNE YÖNELİMLİ PROGRAMLAMA (OOP)
Sistemde veriler dinamik listeler halinde saklanır:
- `gelirler = []`: Sisteme eklenen her bir gelir işlemini temsil eden `Islem` nesnelerini tutan liste.
- `giderler = []`: Sisteme eklenen her bir gider işlemini temsil eden `Islem` nesnelerini tutan liste.

### `finans_modeli.py` - `Islem` Sınıfı Yapısı
Sistemdeki her bir finansal hareket, Nesne Yönelimli Programlama (OOP) ilkelerine uygun olarak `Islem` sınıfından türetilen bir nesnedir:

```python
class Islem:
    def __init__(self, id: int, tutar: float, tarih: str, aciklama: str, tip: str):
        self.id = id
        self.tutar = tutar
        self.tarih = tarih      # YYYY-MM-DD formatında metin
        self.aciklama = aciklama
        self.tip = tip          # 'gelir' veya 'gider'
```

---

## 4. MODÜLLERİN VE ZORUNLU FONKSİYONLARIN GÖREVLERİ

### A. Yardımcı Fonksiyonlar (`utils.py`)
- **`yeni_id_olustur(liste)`**: Belirtilen listedeki (gelirler veya giderler) en yüksek ID'yi bularak 1 artırır ve çakışmayan yeni bir benzersiz ID üretir. Liste boşsa varsayılan olarak `1` değerini döner.
- **`tarih_kontrol(tarih)`**: Kullanıcının girdiği tarihin `YYYY-MM-DD` formatında olup olmadığını kontrol eder. Ayrıca `datetime.strptime` yardımıyla gerçek takvim günlerini doğrular (Örn: "2026-02-31" girilirse geçersiz sayar).
- **`sayi_kontrol(deger)`**: Kullanıcıdan alınan metinsel girdilerin sayısal (float/int) bir değere dönüştürülebilir olup olmadığını kontrol eder, `ValueError` hatalarını yakalar.
- **`menu_goster()`**: Konsol arayüzünün şık ve düzenli ana menüsünü ekrana yazdırır.

### B. İşlem Yönetimi (`islem_yonetimi.py`)
- **`gelir_ekle(gelirler)`**: Kullanıcıdan gelir tutarı, tarih (boşsa otomatik olarak bugün) ve açıklama bilgilerini alır. Girdileri `utils.py` doğrulama fonksiyonlarıyla denetledikten sonra yeni bir `Islem` nesnesi oluşturup `gelirler` listesine ekler.
- **`gider_ekle(giderler)`**: Kullanıcıdan harcama bilgilerini alır, doğrular, yeni bir gider `Islem` nesnesi oluşturarak `giderler` listesine ekler.
- **`islemleri_listele(gelirler, giderler)`**: Tüm gelir ve gider işlemlerini birleştirir, tarihlerine göre kronolojik olarak sıralar ve hizalanmış şık bir tablo formatında ekrana yansıtır.
- **`islem_sil(gelirler, giderler, id)`**: Kullanıcının belirttiği ID numaralı işlemi ilgili listeden bularak siler. Eğer belirtilen ID bulunamazsa hata mesajı gösterir.

### C. Dosya İşlemleri (`dosya_islemleri.py`)
- **`csv_kaydet(dosya_adi, gelirler, giderler)`**: Programdaki tüm gelir ve gider nesnelerini satır satır ayrıştırarak noktalı virgül (`;`) ayracı ile UTF-8 kodlamasında CSV dosyasına kaydeder.
- **`csv_oku(dosya_adi)`**: CSV dosyasındaki tüm kayıtları okur, her satırı doğrulamadan geçirerek `Islem` nesnelerine dönüştürür ve `(gelirler, giderler)` listelerini doldurarak geri döndürür. Dosya yoksa sessizce boş listeler üretir.

### D. Veri Analizi (`analiz.py`)
- **`verileri_dataframe_yap(gelirler, giderler)`**: Gelir ve gider nesnelerindeki verileri sözlük listesine dönüştürür ve Pandas DataFrame yapısına aktarır. Tarih kolonunu `datetime64[ns]` tipine dönüştürerek zaman serisi analizine uygun hale getirir.
- **`toplam_gelir_gider(df)`**: DataFrame filtreleme yöntemlerini kullanarak toplam gelir ve gider tutarlarını tek seferde hesaplar.
- **`aylik_analiz(df)`**: Tarih kolonunu Yıl-Ay periyoduna göre gruplayarak aylık bazda gelir, gider ve net bakiye (kâr/zarar) tablosunu özetler.
- **`numpy_istatistik(df)`**: DataFrame kolonlarını NumPy array (dizi) yapısına dönüştürerek işlem tutarları üzerinde ortalama (mean), minimum (min), maksimum (max) ve standart sapma (std) istatistiklerini hesaplar.

### E. Görselleştirme (`gorsellestirme.py`)
- **`aylik_grafik(df)`**: Aylara göre toplam gelir ve gider hareketlerini karşılaştıran profesyonel bir çizgi grafiği (Line Chart) çizer ve kaydeder.
- **`gelir_gider_bar(df)`**: Toplam gelir ve gider seviyelerini dikey sütun grafiğinde (Bar Chart) karşılaştırarak barların üzerine net değerleri yazdırır ve kaydeder.
- **`pasta_grafik(df)`**: Gelir ve giderlerin bütçe içerisindeki oransal dağılımını gösteren yüzde etiketli şık bir pasta grafiği (Pie Chart) üretir ve kaydeder.

---

## 5. UYGULAMA EKRAN GÖRÜNTÜLERİ (ÇIKTILAR)

Teknik şartnamenin ve Clean Code prensiplerinin gereği olarak, uygulamanın çalıştırılmasıyla elde edilen konsol ekranları ve Matplotlib grafikleri aşağıda sunulmuştur:

### A. Terminal Arayüzü Ekran Görüntüleri

#### 1. Konsol Ana Menüsü (`menu_goster`)
Program çalıştırıldığında kullanıcıyı karşılayan, tüm işlevlerin tetiklendiği interaktif ana menü:
![Konsol Ana Menüsü](proje_ciktilari/ss_console_menu.png)

#### 2. Dinamik İşlem Ekleme ve Kaydetme
Sisteme doğrulama adımlarıyla yeni bir işlem eklenmesi ve CSV dosyasına kaydedilmesi:
![İşlem Ekleme ve CSV Kaydetme](proje_ciktilari/ss_console_add.png)

#### 3. Tüm İşlemlerin Kronolojik Tablo Listesi
Gelir ve gider işlemlerinin tek bir tabloda, hizalı ve tarih sıralı gösterimi:
![İşlemler Tablosu](proje_ciktilari/ss_console_list.png)

#### 4. Pandas ve NumPy Tabanlı İstatistik Analiz Raporu
Pandas ile aylık özet tabloları ve NumPy ile hesaplanan ortalama, standart sapma değerleri:
![Analiz Raporu](proje_ciktilari/ss_console_analysis.png)


### B. Veri Görselleştirme Çıktıları (Matplotlib)

#### 1. Aylık Gelir ve Gider Çizgi Grafiği
Bütçe trendlerini zamana bağlı olarak izlemeyi sağlayan çizgi grafiği:
![Aylık Gelir Gider Çizgi Grafiği](proje_ciktilari/aylik_gelir_gider_cizgi.png)

#### 2. Toplam Gelir ve Gider Bar Grafiği
Net gelir ve gider seviyelerinin dikey sütunlar halinde karşılaştırılması:
![Toplam Gelir Gider Bar Grafiği](proje_ciktilari/toplam_gelir_gider_bar.png)

#### 3. Gelir / Gider Oran Dağılımı Pasta Grafiği
Bütçenin yüzde kaçının harcamalara gittiğini gösteren pasta grafiği:
![Pasta Dağılım Grafiği](proje_ciktilari/gelir_gider_pasta.png)

---

## 6. PROJENİN ÇALIŞTIRILMASI VE KULLANIMI

### Gereksinimler
Proje çalıştırılmadan önce gerekli kütüphanelerin yüklü olduğundan emin olunmalıdır:
```bash
pip install pandas numpy matplotlib seaborn notebook
```

### Jupyter Notebook ile Çalıştırma (`main.ipynb`)
1. Proje klasörünü açın.
2. Terminalden Jupyter Notebook sunucusunu başlatın:
   ```bash
   jupyter notebook
   ```
3. Tarayıcıda açılan arayüzden **`main.ipynb`** dosyasını seçin.
4. Hücreleri sırayla (ya da `Cell > Run All` yaparak) çalıştırarak tüm analizleri ve grafikleri inline görebilir, en alttaki hücreden konsol menüsünü etkileşimli olarak kullanabilirsiniz.

---