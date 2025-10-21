import pdfplumber
import re
import os

# Tüm sınavları tek bir metne dönüştürür.
def extract_and_clean_text(pdf_path):
    all_text = ""
    # Kaldırılacak yaygın gürültü ve Türkçe/Sınav talimatları (regex kullanılır)
    noise_patterns = [
        r'ÖSYM', r'SYM', 
        r'Diğer sayfaya geçiniz\.', r'Go on to the next page\.', 
        r'\d{4}-YDS\s+(İlkbahar|Sonbahar)/İNGİLİZCE', # Başlıklar
        r'TEST OF ENGLISH', r'END OF THE TEST\.', 
        r'Sınavda uyulacak kurallar', r'Bu testlerin her hakkı saklıdır', # Sınav kuralları
        r'\s{2,}', # Birden fazla boşluğu tek boşluğa indir
        r'\n{2,}', # Birden fazla satır boşluğunu tek satıra indir
    ]

    print(f"[{pdf_path}] dosyasından metin çıkarılıyor...")
    
    # PDF'i açma ve metin çıkarma
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text += text + " "

    # Temizleme
    for pattern in noise_patterns:
        all_text = re.sub(pattern, ' ', all_text, flags=re.IGNORECASE)
        
    all_text = re.sub(r'\s+', ' ', all_text).strip()

    print("Metin temizleme tamamlandı.")
    return all_text

if __name__ == "__main__":
    PDF_FILE = "ilovepdf_merged (1).pdf" # Kendi PDF dosyanızın adı
    
    # data klasörünü oluştur
    if not os.path.exists("data"):
        os.makedirs("data")

    try:
        cleaned_corpus = extract_and_clean_text(PDF_FILE)
        
        # Temizlenmiş Metni Kaydetme
        with open("data/cleaned_corpus.txt", "w", encoding="utf-8") as f:
            f.write(cleaned_corpus)
        
        print(f"\nTemizlenmiş metin 'data/cleaned_corpus.txt' dosyasına kaydedildi.")
        print(f"Toplam karakter sayısı: {len(cleaned_corpus)}")
    except FileNotFoundError:
        print(f"HATA: '{PDF_FILE}' dosyası bulunamadı. Lütfen dosyanın kök dizininde olduğundan emin olun.")
    except Exception as e:
        print(f"Metin çıkarma sırasında beklenmeyen hata: {e}")