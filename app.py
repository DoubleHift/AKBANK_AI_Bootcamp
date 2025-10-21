import streamlit as st
import json
import time
import os
from typing import Dict, List, Literal
from pydantic import BaseModel, Field
import random
from dotenv import load_dotenv

# Environment variables yükle
load_dotenv()

# --- 1. Pydantic Model ---
class Question(BaseModel):
    question_id: int = Field(..., description="Soru numarası.")
    question_text: str = Field(..., description="Soru metni.")
    options: Dict[Literal['A', 'B', 'C', 'D', 'E'], str] = Field(..., description="5 adet seçenek.")
    correct_option: Literal['A', 'B', 'C', 'D', 'E'] = Field(..., description="Doğru cevap anahtarı.")
    explanation: str = Field(..., description="Doğru cevabın kısa açıklaması.")
    question_type: str = Field(..., description="Soru tipi")

class Quiz(BaseModel):
    quiz: List[Question]

# --- SİMÜLASYON VERİSİ ---
BOŞLUK_DOLDURMA_SORULARI = [
    {
        "question_id": 1,
        "question_text": "The rapid ______ of artificial intelligence across various sectors is expected to significantly reshape global labor markets, potentially leading to both job displacement and the creation of new roles requiring specialized skills.",
        "options": {"A": "stagnation", "B": "proliferation", "C": "retraction", "D": "curtailment", "E": "impediment"},
        "correct_option": "B",
        "explanation": "'Proliferation' (yayılma) kelimesi, yapay zekanın hızlı bir şekilde yayılması anlamına gelir ve bağlama uygundur.",
        "question_type": "boşluk doldurma"
    },
    {
        "question_id": 2,
        "question_text": "Despite concerns about data privacy and ethical implications, the widespread adoption of digital technologies ______ an unparalleled opportunity for developing nations to leapfrog traditional stages of economic growth.",
        "options": {"A": "has presented", "B": "presenting", "C": "to present", "D": "having presented", "E": "will have presented"},
        "correct_option": "A",
        "explanation": "'Has presented' doğru zaman yapısını kullanır ve günümüze kadar devam eden bir durumu ifade eder.",
        "question_type": "boşluk doldurma"
    },
    {
        "question_id": 3,
        "question_text": "As global supply chains become increasingly interconnected and reliant on digital infrastructure, they are also becoming more vulnerable to sophisticated cyber-attacks, ______ the urgent need for enhanced international cooperation in cybersecurity.",
        "options": {"A": "thereby mitigating", "B": "consequently alleviating", "C": "thus underscoring", "D": "conversely diminishing", "E": "notwithstanding reducing"},
        "correct_option": "C",
        "explanation": "'Thus underscoring' (böylece vurgulayarak) ifadesi, siber saldırıların uluslararası işbirliği ihtiyacını vurguladığı anlamına gelir.",
        "question_type": "boşluk doldurma"
    }
]

# --- PARAGRAF SORULARI ---
PARAGRAF_SORULARI = [
    {
        "question_id": 1,
        "question_text": "Reading comprehension: The concept of sustainable development has gained significant traction in recent decades, primarily due to growing concerns about environmental degradation and resource depletion. This approach emphasizes meeting the needs of the present without compromising the ability of future generations to meet their own needs. It involves a careful balance between economic growth, environmental protection, and social equity. What is the primary focus of sustainable development?",
        "options": {
            "A": "Maximizing current economic growth at all costs",
            "B": "Balancing present needs with future generations' requirements", 
            "C": "Eliminating all industrial activities",
            "D": "Focusing exclusively on environmental conservation",
            "E": "Prioritizing social equity over economic considerations"
        },
        "correct_option": "B",
        "explanation": "Metinde sürdürülebilir kalkınmanın 'mevcut ihtiyaçları, gelecek nesillerin kendi ihtiyaçlarını karşılama yeteneğinden ödün vermeden karşılama' üzerine odaklandığı belirtilmektedir.",
        "question_type": "paragraf sorusu"
    },
    {
        "question_id": 2,
        "question_text": "Reading comprehension: The Industrial Revolution marked a major turning point in history. During this period, which began in the late 18th century, manual labor was increasingly replaced by machines powered by steam and later electricity. This transformation led to unprecedented economic growth and urbanization but also resulted in significant social and environmental challenges. What was the primary technological innovation that characterized the Industrial Revolution?",
        "options": {
            "A": "The replacement of manual labor with machine-based manufacturing",
            "B": "The discovery of new agricultural techniques", 
            "C": "The development of computer technology",
            "D": "The invention of the printing press",
            "E": "The exploration of space"
        },
        "correct_option": "A",
        "explanation": "Metin, Endüstri Devrimi'nin temel özelliğinin makineleşme ve el emeğinin makinelerle değiştirilmesi olduğunu vurgulamaktadır.",
        "question_type": "paragraf sorusu"
    }
]

# --- KELİME ANLAMI SORULARI ---
KELİME_ANLAMI_SORULARI = [
    {
        "question_id": 1,
        "question_text": "Choose the word that is closest in meaning to 'ubiquitous':",
        "options": {
            "A": "Rare",
            "B": "Widespread", 
            "C": "Complicated",
            "D": "Expensive",
            "E": "Temporary"
        },
        "correct_option": "B",
        "explanation": "'Ubiquitous' kelimesi 'her yerde bulunan, yaygın' anlamına gelir ve 'widespread' ile eş anlamlıdır.",
        "question_type": "kelime anlamı"
    },
    {
        "question_id": 2,
        "question_text": "Choose the word that is closest in meaning to 'ambiguous':",
        "options": {
            "A": "Clear",
            "B": "Vague", 
            "C": "Simple",
            "D": "Direct",
            "E": "Obvious"
        },
        "correct_option": "B",
        "explanation": "'Ambiguous' kelimesi 'belirsiz, iki anlamlı' demektir ve 'vague' ile eş anlamlıdır.",
        "question_type": "kelime anlamı"
    }
]

# --- DİL BİLGİSİ SORULARI ---
DİL_BİLGİSİ_SORULARI = [
    {
        "question_id": 1,
        "question_text": "Choose the correct verb form: If I ______ more time, I would have completed the project successfully.",
        "options": {
            "A": "have had",
            "B": "had had", 
            "C": "would have",
            "D": "had",
            "E": "have"
        },
        "correct_option": "B",
        "explanation": "Type 3 conditional (geçmişe yönelik koşul) yapısında 'if + past perfect, would + have + V3' kullanılır.",
        "question_type": "dil bilgisi"
    },
    {
        "question_id": 2,
        "question_text": "Choose the correct sentence structure:",
        "options": {
            "A": "Neither the students nor the teacher are coming.",
            "B": "Neither the students nor the teacher is coming.", 
            "C": "Neither the students or the teacher is coming.",
            "D": "Neither the students nor the teacher were coming.",
            "E": "Neither the students or the teacher are coming."
        },
        "correct_option": "B",
        "explanation": "'Neither...nor' yapısında fiil, en yakın özneye göre çekimlenir. 'Teacher' tekil olduğu için 'is' kullanılır.",
        "question_type": "dil bilgisi"
    }
]

# --- CLOZE TEST SORULARI ---
CLOZE_TEST_SORULARI = [
    {
        "question_id": 1,
        "question_text": "Cloze test: Climate change represents one of the most pressing challenges of our time. The ______ of greenhouse gases into the atmosphere has led to a gradual increase in global temperatures. This phenomenon, ______ as global warming, has far-reaching consequences for ecosystems worldwide. Scientists warn that without immediate action, the impacts could become ______.",
        "options": {
            "A": "reduction, known, manageable",
            "B": "release, referred, irreversible", 
            "C": "absorption, called, temporary",
            "D": "elimination, termed, beneficial",
            "E": "production, named, insignificant"
        },
        "correct_option": "B",
        "explanation": "Bağlam gereği 'release' (salınım), 'referred' (adlandırılan) ve 'irreversible' (geri dönülemez) kelimeleri metnin anlamına uygundur.",
        "question_type": "cloze test"
    },
    {
        "question_id": 2,
        "question_text": "Cloze test: The development of renewable energy sources has ______ accelerated in recent years. Solar and wind power, in particular, have become increasingly ______ due to technological advancements and decreasing costs. Many countries are now ______ these clean energy options to reduce their carbon emissions.",
        "options": {
            "A": "slowly, expensive, ignoring",
            "B": "rapidly, affordable, adopting", 
            "C": "gradually, complicated, rejecting",
            "D": "slightly, efficient, delaying",
            "E": "never, popular, avoiding"
        },
        "correct_option": "B",
        "explanation": "'Rapidly' (hızlı), 'affordable' (uygun fiyatlı) ve 'adopting' (benimsemek) kelimeleri yenilenebilir enerji bağlamına uygundur.",
        "question_type": "cloze test"
    }
]

# Tüm soruları birleştir
TÜM_SORULAR = BOŞLUK_DOLDURMA_SORULARI + PARAGRAF_SORULARI + KELİME_ANLAMI_SORULARI + DİL_BİLGİSİ_SORULARI + CLOZE_TEST_SORULARI

# --- RAG Fonksiyonları Import ---
try:
    from rag_pipeline import generate_quiz_with_rag
    RAG_AVAILABLE = True
except ImportError as e:
    RAG_AVAILABLE = False
    print(f"RAG modülü yüklenemedi: {e}")

# --- 2. Oturum Durumu Yönetimi ---
def initialize_session_state():
    if 'quiz_data' not in st.session_state:
        st.session_state.quiz_data = []
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'quiz_completed' not in st.session_state:
        st.session_state.quiz_completed = False
    if 'num_questions_value' not in st.session_state:
        st.session_state.num_questions_value = 5
    if 'question_type' not in st.session_state:
        st.session_state.question_type = "karışık"
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'time_limit' not in st.session_state:
        st.session_state.time_limit = None
    if 'remaining_time' not in st.session_state:
        st.session_state.remaining_time = None

def reset_quiz_completely():
    """Sınavı tamamen sıfırlar ve ana menüye döner"""
    st.session_state.quiz_data = []
    st.session_state.current_question_index = 0
    st.session_state.user_answers = {}
    st.session_state.quiz_started = False
    st.session_state.quiz_completed = False
    st.session_state.start_time = None
    st.session_state.time_limit = None
    st.session_state.remaining_time = None
    st.rerun()

# --- 3. Zaman Sayacı Fonksiyonları ---
def calculate_time_limit(num_questions, question_type):
    """Soru sayısı ve tipine göre zaman limitini hesaplar"""
    base_time_per_question = 2.25  # dakika
    
    time_multipliers = {
        "boşluk doldurma": 1.0,
        "kelime anlamı": 0.8,
        "paragraf sorusu": 2.5,
        "dil bilgisi": 1.2,
        "cloze test": 1.5,
        "karışık": 1.3
    }
    
    multiplier = time_multipliers.get(question_type.lower(), 1.0)
    total_minutes = num_questions * base_time_per_question * multiplier
    return total_minutes * 60  # saniyeye çevir

def format_time(seconds):
    """Saniyeyi dakika:saniye formatına çevirir"""
    if seconds is None:
        return "00:00"
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

def update_timer():
    """Zaman sayacını günceller"""
    if (st.session_state.quiz_started and 
        not st.session_state.quiz_completed and 
        st.session_state.start_time and 
        st.session_state.time_limit):
        
        elapsed_time = time.time() - st.session_state.start_time
        st.session_state.remaining_time = max(0, st.session_state.time_limit - elapsed_time)
        
        # Zaman dolduysa sınavı bitir
        if st.session_state.remaining_time <= 0:
            st.session_state.quiz_completed = True
            st.session_state.remaining_time = 0
            st.rerun()

# --- 4. Soru Üretme Fonksiyonları ---
def enhance_simulated_question_with_topic(question, topic, question_type):
    """Simüle edilmiş soruyu konuya uygun hale getirir"""
    question_text = question.get('question_text', '')
    
    # Konuya özel dönüşümler
    if question_type == "boşluk doldurma":
        replacements = [
            ("artificial intelligence", topic),
            ("digital technologies", f"{topic} technologies"),
            ("sustainable development", f"{topic} development"),
            ("global economy", f"{topic} economy"),
            ("scientific research", f"{topic} research"),
            ("climate change", topic),
            ("globalization", topic),
            ("technology", topic)
        ]
        
        for old, new in replacements:
            if old.lower() in question_text.lower():
                question_text = question_text.replace(old, new)
                question_text = question_text.replace(old.title(), new)
                break
        else:
            # Hiçbiri yoksa başa ekle
            if not question_text.startswith("In the context of"):
                question_text = f"In the context of {topic}, {question_text[0].lower() + question_text[1:]}"
    
    elif question_type == "paragraf sorusu":
        if "Reading comprehension:" in question_text:
            question_text = question_text.replace("Reading comprehension:", f"Reading comprehension about {topic}:")
        elif "The concept of" in question_text:
            question_text = question_text.replace("The concept of", f"The concept of {topic}")
    
    elif question_type == "kelime anlamı":
        if "Choose the word" in question_text and topic.lower() not in question_text.lower():
            question_text = f"In {topic} context, {question_text}"
    
    elif question_type == "cloze test":
        if "Cloze test:" in question_text:
            question_text = question_text.replace("Cloze test:", f"Cloze test about {topic}:")
    
    question['question_text'] = question_text
    return question

def get_random_question_type(previous_types, available_types):
    """
    Rastgele soru tipi seçer, aynı tipin arka arkaya max 2 kez gelmesini sağlar
    """
    if len(previous_types) < 2:
        # İlk 2 soru için herhangi bir tip seçilebilir
        return random.choice(available_types)
    
    # Son 2 sorunun tipini kontrol et
    last_two = previous_types[-2:]
    
    # Eğer son 2 soru aynı tipse, farklı bir tip seç
    if len(set(last_two)) == 1:
        # Aynı tipten 2 kez üst üste geldi, farklı bir tip seç
        different_types = [t for t in available_types if t != last_two[0]]
        if different_types:
            return random.choice(different_types)
    
    # Normal rastgele seçim
    return random.choice(available_types)

def generate_quiz(topic, num_questions, question_type):
    """RAG ile istenen sayıda ve tipte soruyu üretir."""
    
    # Her zaman RAG kullanmaya çalış
    use_rag = RAG_AVAILABLE
    
    if use_rag:
        with st.spinner(f"🤖 RAG ile {num_questions} {question_type} sorusu üretiliyor..."):
            rag_questions = generate_quiz_with_rag(topic, num_questions, question_type)
        
        if rag_questions and len(rag_questions) > 0:
            st.session_state.quiz_data = rag_questions
            st.session_state.quiz_started = True
            st.session_state.current_question_index = 0
            st.session_state.user_answers = {}
            st.session_state.num_questions_value = num_questions
            st.session_state.quiz_completed = False
            st.session_state.question_type = question_type
            
            st.session_state.time_limit = calculate_time_limit(num_questions, question_type)
            st.session_state.start_time = time.time()
            st.session_state.remaining_time = st.session_state.time_limit
            
            # Soru tipi dağılımını göster
            if question_type.lower() == "karışık":
                type_count = {}
                for q in rag_questions:
                    q_type = q.get('question_type', 'unknown')
                    type_count[q_type] = type_count.get(q_type, 0) + 1
                type_info = ", ".join([f"{k}: {v}" for k, v in type_count.items()])
                st.toast(f"✅ RAG ile {num_questions} soru üretildi! Dağılım: {type_info}", icon='🤖')
            else:
                st.toast(f"✅ RAG ile {num_questions} {question_type} sorusu üretildi!", icon='🤖')
            
            st.rerun()
            return
    
    # RAG başarısız olursa simülasyona geç
    st.warning("🤖 RAG başarısız oldu, simülasyon modu ile devam ediliyor...")
    
    simulated_quiz_data = []
    mixed_mode = (question_type.lower() == "karışık")
    available_question_types = ["boşluk doldurma", "paragraf sorusu", "kelime anlamı", "dil bilgisi", "cloze test"]
    previous_question_types = []

    for i in range(num_questions):
        if mixed_mode:
            # Akıllı karışık mod - aynı tipin üst üste gelmesini önle
            selected_type = get_random_question_type(previous_question_types, available_question_types)
            previous_question_types.append(selected_type)
            
            # Listeyi sınırla (sadece son 2'yi tut)
            if len(previous_question_types) > 2:
                previous_question_types = previous_question_types[-2:]
        else:
            # Belirli soru tipi seçimi
            selected_type = question_type
        
        # Seçilen tipe göre kaynak belirle
        if selected_type == "boşluk doldurma":
            question_source = BOŞLUK_DOLDURMA_SORULARI
        elif selected_type == "paragraf sorusu":
            question_source = PARAGRAF_SORULARI
        elif selected_type == "kelime anlamı":
            question_source = KELİME_ANLAMI_SORULARI
        elif selected_type == "dil bilgisi":
            question_source = DİL_BİLGİSİ_SORULARI
        else:
            question_source = CLOZE_TEST_SORULARI
        
        original_question = question_source[i % len(question_source)]
        new_question_id = i + 1
        
        # Sorunun kopyasını oluştur (Benzersiz ID'ler için)
        new_question = original_question.copy()
        new_question['question_id'] = new_question_id
        new_question['question_type'] = selected_type
        
        # Konuyu soru metnine entegre et
        new_question = enhance_simulated_question_with_topic(new_question, topic, selected_type)
        
        simulated_quiz_data.append(new_question)
    
    st.session_state.quiz_data = simulated_quiz_data 
    st.session_state.quiz_started = True
    st.session_state.current_question_index = 0
    st.session_state.user_answers = {}
    st.session_state.num_questions_value = num_questions
    st.session_state.quiz_completed = False
    st.session_state.question_type = question_type
    
    # Zaman sayacını başlat
    st.session_state.time_limit = calculate_time_limit(num_questions, question_type)
    st.session_state.start_time = time.time()
    st.session_state.remaining_time = st.session_state.time_limit
    
    mode_text = "karışık mod" if mixed_mode else f"{question_type} modu"
    source_text = "simülasyon"
    st.toast(f"📝 {source_text} ile {num_questions} soruluk {mode_text} başlatıldı! Konu: {topic}", icon='🎯')
    st.rerun()

# --- 5. Navigasyon Fonksiyonu ---
def handle_navigation(num_questions):
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.session_state.current_question_index > 0:
            if st.button("⬅️ Önceki Soru", use_container_width=True):
                st.session_state.current_question_index -= 1
                st.rerun()
        else:
            st.button("⬅️ Önceki Soru", disabled=True, use_container_width=True)
    
    with col2:
        if st.button("❌ Sınavı Bitir", type="primary", use_container_width=True):
            st.session_state.quiz_completed = True
            st.rerun()
    
    with col3:
        if st.session_state.current_question_index < num_questions - 1:
            if st.button("Sonraki Soru ➡️", use_container_width=True):
                st.session_state.current_question_index += 1
                st.rerun()
        else:
            st.button("Son Soru ➡️", disabled=True, use_container_width=True)

# --- 6. Zaman Göstergesi ---
def display_timer():
    """Zaman göstergesini görüntüler"""
    if (st.session_state.quiz_started and 
        not st.session_state.quiz_completed and 
        st.session_state.remaining_time is not None):
        
        update_timer()
        
        # İlerleme yüzdesi
        progress = st.session_state.remaining_time / st.session_state.time_limit
        
        # Renk belirleme
        if progress > 0.5:
            color = "green"
        elif progress > 0.25:
            color = "orange"
        else:
            color = "red"
        
        # Zaman göstergesi
        col1, col2 = st.columns([3, 1])
        with col1:
            st.progress(progress, text=f"Kalan Süre: {format_time(st.session_state.remaining_time)}")
        with col2:
            st.markdown(f"<span style='color: {color}; font-weight: bold; font-size: 18px;'>{format_time(st.session_state.remaining_time)}</span>", 
                       unsafe_allow_html=True)
        
        # Uyarı mesajları
        if st.session_state.remaining_time < 60:
            st.warning("⏰ Son 1 dakika! Hızlanın!")
        elif st.session_state.remaining_time < 300:
            st.info("⏱️ Son 5 dakika kaldı!")

# --- 7. Soru Görüntüleme ---
def display_question(question: dict, num_questions: int): 
    q_id = question.get('question_id', st.session_state.current_question_index + 1)
    q_type = question.get('question_type', 'boşluk doldurma')
    
    # Soru tipi badge'ı
    type_colors = {
        "boşluk doldurma": "blue",
        "paragraf sorusu": "green", 
        "kelime anlamı": "orange",
        "dil bilgisi": "purple",
        "cloze test": "red"
    }
    color = type_colors.get(q_type, "gray")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        # İlerleme Çubuğu
        progress = (st.session_state.current_question_index + 1) / num_questions
        st.progress(progress, text=f"Soru {q_id} / {num_questions}")
    with col2:
        st.markdown(f"<div style='background-color: {color}; color: white; padding: 8px; border-radius: 5px; text-align: center; font-weight: bold;'>{q_type.upper()}</div>", 
                   unsafe_allow_html=True)

    # Soru Metni
    q_text = question.get('question_text', 'Soru metni yüklenemedi.')
    st.markdown(f"**Soru {q_id}:** {q_text}") 
    
    options = question.get('options', {})
    current_answer = st.session_state.user_answers.get(q_id, None)

    # Radyo Butonları
    if options:
        user_selection = st.radio(
            "Cevabınızı Seçin:",
            options=list(options.keys()),
            format_func=lambda x: f"{x}) {options[x]}",
            index=list(options.keys()).index(current_answer) if current_answer and current_answer in options else None,
            key=f"q_{q_id}_index_{st.session_state.current_question_index}" 
        )
        
        if user_selection:
            st.session_state.user_answers[q_id] = user_selection
    else:
        st.error("Seçenekler yüklenemedi.")

# --- 8. Sonuçları Görüntüleme ---
def display_results():
    total_score = 0
    num_questions = len(st.session_state.quiz_data)
    
    # Soru tipi analizi
    type_analysis = {}
    for question in st.session_state.quiz_data:
        q_type = question.get('question_type', 'bilinmiyor')
        q_id = question.get('question_id', 0)
        user_answer = st.session_state.user_answers.get(q_id)
        is_correct = user_answer == question.get('correct_option', None)
        
        if q_type not in type_analysis:
            type_analysis[q_type] = {'total': 0, 'correct': 0}
        
        type_analysis[q_type]['total'] += 1
        if is_correct:
            type_analysis[q_type]['correct'] += 1
            total_score += 1
    
    # Geçen süreyi hesapla
    if st.session_state.start_time:
        elapsed_time = time.time() - st.session_state.start_time
        time_spent = format_time(elapsed_time)
    else:
        time_spent = "Bilinmiyor"
    
    st.title("✅ Sınav Sonuçlarınız")
    
    # Bilgi kartı
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Soru Tipi", st.session_state.question_type)
    with col2:
        st.metric("Toplam Soru", num_questions)
    with col3:
        st.metric("Geçen Süre", time_spent)
    
    # Yeniden Başlat Butonu
    if st.button("🔄 Yeni Sınav Başlat", type="primary", use_container_width=True):
        reset_quiz_completely()
        return
    
    st.markdown("---")
    
    # Soru tipi analizi
    mixed_mode = (st.session_state.question_type.lower() == "karışık")
    if mixed_mode and len(type_analysis) > 1:
        st.subheader("📊 Soru Tipi Bazında Performans")
        for q_type, stats in type_analysis.items():
            correct = stats['correct']
            total = stats['total']
            percentage = (correct / total) * 100 if total > 0 else 0
            st.write(f"**{q_type}:** {correct}/{total} (%{percentage:.1f})")
        st.markdown("---")
    
    # Detaylı sonuçlar
    for question in st.session_state.quiz_data:
        q_id = question.get('question_id', 0)
        user_answer = st.session_state.user_answers.get(q_id)
        q_type = question.get('question_type', 'boşluk doldurma')
        
        is_correct = user_answer == question.get('correct_option', None)
        
        if is_correct:
            icon = "✅"
        else:
            icon = "❌"
        
        st.markdown(f"### {icon} Soru {q_id} - {q_type}")
        st.markdown(f"**{question['question_text']}**")
        
        # Seçenekleri göster
        for key, value in question['options'].items():
            if key == question['correct_option']:
                st.markdown(f"<span style='color:green; font-weight:bold;'>✓ {key}) {value} (Doğru Cevap)</span>", unsafe_allow_html=True)
            elif key == user_answer and not is_correct:
                st.markdown(f"<span style='color:red; font-weight:bold;'>✗ {key}) {value} (Sizin Cevabınız)</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"{key}) {value}")
        
        st.markdown(f"**Açıklama:** {question['explanation']}")
        st.markdown("---")

    # Skor kartı
    percentage = (total_score / num_questions) * 100
    st.success(f"## 🎉 Toplam Skor: {total_score} / {num_questions} (%{percentage:.1f})")
    
    # Performans değerlendirmesi
    if percentage >= 80:
        st.balloons()
        st.success("🏆 Mükemmel! Çok iyi bir performans gösterdiniz!")
    elif percentage >= 60:
        st.success("👍 İyi! Gayet başarılı bir sonuç!")
    elif percentage >= 40:
        st.warning("💪 Orta seviye, biraz daha çalışmak gerekebilir.")
    else:
        st.error("📚 Daha fazla çalışma gerekiyor, pes etmeyin!")
    
    # Alt kısımda tekrar yeni sınav butonu
    st.markdown("---")
    if st.button("🔄 Yeni Sınav Oluştur", type="primary", use_container_width=True):
        reset_quiz_completely()

# --- ANA UYGULAMA ---
def main():
    st.set_page_config(
        page_title="YDS/YÖKDİL Bağlamsal Sınav Oluşturucu", 
        layout="wide",
        page_icon="📚"
    )
    
    st.title("📚 RAG Temelli YDS/YÖKDİL Bağlamsal Sınav Oluşturucu")
    st.subheader("Akbank GenAI Bootcamp Projesi: Yeni Nesil Proje Kampı")

    initialize_session_state()

    # Zaman güncellemesi
    if st.session_state.quiz_started and not st.session_state.quiz_completed:
        update_timer()

    if st.session_state.quiz_completed:
        display_results()
    
    elif st.session_state.quiz_started and st.session_state.quiz_data:
        # Zaman göstergesi
        display_timer()
        st.markdown("---")
        
        current_index = st.session_state.current_question_index
        num_questions = len(st.session_state.quiz_data)
        question_to_display = st.session_state.quiz_data[current_index] 
        
        # Soru görüntüleme
        display_question(question_to_display, num_questions) 
        st.markdown("---")
        
        handle_navigation(num_questions)
    
    else:
        # Sınav başlatma ekranı
        st.markdown("### 🚀 Sınav Oluşturucu")
        st.markdown("Aşağıdaki formu doldurarak sınavınızı oluşturun.")
        
        with st.form("quiz_creation_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                topic = st.text_input(
                    "📝 Sınav Konusu:", 
                    value="yapay zeka", 
                    help="Sınav sorularının odağını belirleyin"
                )
                
                # Radio buton ile soru tipi seçimi
                question_type = st.radio(
                    "🎯 Soru Tipi:",
                    options=["karışık", "boşluk doldurma", "paragraf sorusu", "kelime anlamı", "dil bilgisi", "cloze test"],
                    index=0,
                    help="Sınavda kullanılacak soru tipini seçin"
                )
            
            with col2:
                num_questions = st.slider(
                    "🔢 Soru Sayısı:", 
                    min_value=1,            
                    max_value=80,           
                    value=st.session_state.num_questions_value, 
                    step=1,
                    help="1-80 arasında soru sayısı seçin"
                )
                
                # Tahmini süre hesaplama
                estimated_time = calculate_time_limit(num_questions, question_type) / 60
                st.info(f"⏱️ Tahmini Süre: {estimated_time:.1f} dakika")
            
            st.markdown("**Soru Tipi Açıklamaları:**")
            st.markdown("- **Karışık**: Tüm soru tiplerinden dengeli dağılım")
            st.markdown("- **Boşluk Doldurma**: Klasik YDS boşluk doldurma soruları")
            st.markdown("- **Paragraf Sorusu**: Okuma parçası ve soruları")
            st.markdown("- **Kelime Anlamı**: Kelime bilgisi ve eş anlamlılar")
            st.markdown("- **Dil Bilgisi**: Gramer ve yapı soruları")
            st.markdown("- **Cloze Test**: Metin içi boşluk doldurma")
            
            # RAG durumunu göster
            if RAG_AVAILABLE:
                st.success("🤖 RAG Sistemi: Aktif")
            else:
                st.warning("🤖 RAG Sistemi: Devre dışı - Simülasyon modu kullanılacak")
            
            submitted = st.form_submit_button("🎯 Sınavı Başlat", type="primary")

            if submitted:
                if not topic.strip():
                    st.error("Lütfen bir konu girin!")
                else:
                    safe_num_questions = max(1, min(num_questions, 80))
                    generate_quiz(topic.strip(), safe_num_questions, question_type.strip())

if __name__ == "__main__":
    main()