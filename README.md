# 📚 RAG TEMELLİ YDS/YÖKDİL BAĞLAMSAL SINAV OLUŞTURUCU

## Akbank GenAI Bootcamp: Yeni Nesil Proje Kampı Teslimatı

Bu proje, RAG (Retrieval Augmented Generation) mimarisi üzerine kurulu bir chatbot geliştirme projesidir. Amaç, kullanıcıların belirlediği konu ve soru adedine göre, akademik İngilizce sınav formatına (YDS/YÖKDİL) uygun, bağlamsal ve interaktif sorular üretmektir.

---

### [cite_start]1. Geliştirme Ortamı (GitHub & README.md) [cite: 3658, 3681]

Proje kodu Python ile geliştirilmiş ve Visual Studio Code (VS Code) ortamında test edilmiştir.

* **Kod Sergileme:** Projenin tamamı (özel dosyalar hariç) bu GitHub reposunda sergilenmektedir.
* **Teknik Anlatımlar:** Tüm RAG mimarisi ve mantıksal kararlar bu `README.md` dosyasında detaylandırılmıştır.
* **Hassas Veri:** API Anahtarı, koddan kaldırılmış ve `.env` dosyası aracılığıyla yönetilmektedir. [cite_start]`.env` dosyası, hassas veri güvenliği gereği `.gitignore` ile GitHub'a push edilmemiştir[cite: 4].

### [cite_start]2. Veri Seti Hazırlama [cite: 3670, 3682]

**Proje Konusu:** YDS/YÖKDİL seviyesinde akademik ve bağlamsal İngilizce metinleri kullanarak dinamik sınav soruları üretmek.

* **Veri Kaynağı:** Geçmiş yıllara ait ÖSYM YDS/YÖKDİL sınavlarının (PDF formatında) akademik metin kısımları toplanmıştır.
* **Hazırlık Metodolojisi (`data_prep.py`):**
    1.  **Metin Çıkarma (Parsing):** `pdfplumber` kütüphanesi kullanılarak PDF'lerden metin içeriği çıkarılmıştır.
    2.  **Temizlik (Cleaning):** Metinler üzerindeki filigran kalıntıları (`ÖSYM`, `SYM`), Türkçe sınav talimatları (`Diğer sayfaya geçiniz`), sayfa numaraları ve başlıklar regex ifadeleri kullanılarak temizlenmiştir.
    3.  **Vektörleştirme Hazırlığı:** Temizlenen metin, `RecursiveCharacterTextSplitter` kullanılarak RAG için uygun (1000 karakter civarında çakışmalı) **bağlamsal parçalara (chunks)** ayrılmıştır.

### [cite_start]3. Çözüm Mimariniz [cite: 3676, 3684]

Proje, **RAG (Retrieval Augmented Generation)** prensiplerine göre tasarlanmıştır:

| Bileşen | Kullanılan Teknoloji | Rolü |
| :--- | :--- | :--- |
| **Generation Model** | [cite_start]**Gemini API** (`gemini-2.5-flash` veya `gemini-1.5-flash`) [cite: 3696] | Geri çekilen bağlamı temel alarak **JSON formatında** yeni, bağlamsal sorular ve çeldiriciler üretmek. |
| **Embedding Model** | [cite_start]Google Embedding Model [cite: 3697] | Metin parçalarını vektörlere dönüştürerek anlamsal aramayı mümkün kılmak. |
| **Vektör Database** | [cite_start]Chroma DB [cite: 3697] | Vektörlerin depolanması ve hızlı, anlamsal olarak alakalı metin parçalarının geri çekilmesi (Retrieval). |
| **RAG Framework** | [cite_start]**LangChain** [cite: 3698] | LLM ve Vektör DB arasındaki zincir yapısını kurmak. |
| **Arayüz (UI)** | **Streamlit** | İnteraktif sınav ortamını sunmak. |

### [cite_start]4. Kodunuzun Çalışma Kılavuzu [cite: 3673, 3683]

Bu proje, yerel makinenizde (VS Code tavsiye edilir) çalıştırılabilir.

**Adım 1: Gereksinimleri Yükleme**

```bash
# Sanal ortamı oluşturun ve etkinleştirin
python -m venv venv
source venv/bin/activate  # macOS/Linux
.\venv\Scripts\activate   # Windows PowerShell

# Gerekli kütüphaneleri yükleyin
pip install -r requirements.txt
