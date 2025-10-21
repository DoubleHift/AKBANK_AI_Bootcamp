import pdfplumber
import re
import os

def extract_and_clean_text(pdf_path):
    """PDF'den metin çıkarır ve temizler"""
    all_text = ""
    
    noise_patterns = [
        r'ÖSYM', r'SYM', 
        r'Diğer sayfaya geçiniz\.', r'Go on to the next page\.', 
        r'\d{4}-YDS\s+(İlkbahar|Sonbahar)/İNGİLİZCE',
        r'TEST OF ENGLISH', r'END OF THE TEST\.', 
        r'Sınavda uyulacak kurallar', r'Bu testlerin her hakkı saklıdır',
        r'\s{2,}', 
        r'\n{2,}', 
    ]

    print(f"[{pdf_path}] dosyasından metin çıkarılıyor...")
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    all_text += text + " "

        for pattern in noise_patterns:
            all_text = re.sub(pattern, ' ', all_text, flags=re.IGNORECASE)
            
        all_text = re.sub(r'\s+', ' ', all_text).strip()

        print("Metin temizleme tamamlandı.")
        return all_text
        
    except FileNotFoundError:
        print(f"HATA: '{pdf_path}' dosyası bulunamadı.")
        return None
    except Exception as e:
        print(f"Metin çıkarma sırasında beklenmeyen hata: {e}")
        return None

if __name__ == "__main__":
    # Örnek kullanım
    PDF_FILE = "sample.pdf"  # Kullanıcının kendi PDF dosyası
    
    if not os.path.exists("data"):
        os.makedirs("data")

    # Örnek dataset oluştur (PDF yoksa)
    if not os.path.exists(PDF_FILE):
        print("📝 Örnek veri seti oluşturuluyor...")
        sample_corpus = """ARTIFICIAL INTELLIGENCE AND MODERN SOCIETY

The integration of artificial intelligence into various sectors has revolutionized traditional approaches to problem-solving. Machine learning algorithms can now process vast amounts of data, identify patterns, and make predictions with remarkable accuracy.

CLIMATE CHANGE AND SUSTAINABLE DEVELOPMENT

Climate change represents one of the most pressing challenges facing humanity. Sustainable development requires balancing economic growth with environmental protection and social equity.

THE DIGITAL TRANSFORMATION OF EDUCATION

The digital revolution has fundamentally transformed educational methodologies. Online learning platforms and digital resources have made education more accessible than ever before.

GLOBALIZATION AND CULTURAL EXCHANGE

Globalization has facilitated unprecedented levels of cultural exchange and economic integration across national borders.

ADVANCEMENTS IN RENEWABLE ENERGY

Renewable energy technologies have experienced rapid development. Solar, wind, and hydropower are becoming increasingly competitive with traditional fossil fuels."""
        
        with open("data/cleaned_corpus.txt", "w", encoding="utf-8") as f:
            f.write(sample_corpus)
        
        print("✅ Örnek veri seti 'data/cleaned_corpus.txt' dosyasına kaydedildi.")
    else:
        # PDF varsa işle
        cleaned_corpus = extract_and_clean_text(PDF_FILE)
        
        if cleaned_corpus:
            with open("data/cleaned_corpus.txt", "w", encoding="utf-8") as f:
                f.write(cleaned_corpus)
            
            print(f"✅ Temizlenmiş metin 'data/cleaned_corpus.txt' dosyasına kaydedildi.")
            print(f"📊 Toplam karakter sayısı: {len(cleaned_corpus)}")