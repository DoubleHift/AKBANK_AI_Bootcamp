# rag_pipeline.py
import os
import json
import re
import random
import google.generativeai as genai
from dotenv import load_dotenv

# Environment variables yükle
load_dotenv()

# --- API Anahtarı ve Model Ayarları ---
API_KEY = os.getenv("GEMINI_API_KEY")

print(f"🔑 API Key kontrol ediliyor: {'*' * len(API_KEY) if API_KEY else 'BULUNAMADI'}")

if not API_KEY:
    print("❌ GEMINI_API_KEY environment variable bulunamadı!")
    print("📋 .env dosyasını kontrol edin: GEMINI_API_KEY=your_actual_api_key_here")
    RAG_AVAILABLE = False
else:
    try:
        print("🔄 Gemini API yapılandırılıyor...")
        genai.configure(api_key=API_KEY)
        
        # Mevcut modelleri kontrol et
        print("📋 Mevcut modeller kontrol ediliyor...")
        available_models = []
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                available_models.append(model.name)
                print(f"   ✅ {model.name}")
        
        # En uygun modeli seç
        if 'models/gemini-2.0-flash-exp' in available_models:
            MODEL_NAME = 'models/gemini-2.0-flash-exp'
        elif 'models/gemini-1.5-flash' in available_models:
            MODEL_NAME = 'models/gemini-1.5-flash'
        elif 'models/gemini-pro' in available_models:
            MODEL_NAME = 'models/gemini-pro'
        else:
            MODEL_NAME = available_models[0] if available_models else None
        
        print(f"🎯 Seçilen model: {MODEL_NAME}")
        
        if MODEL_NAME:
            model = genai.GenerativeModel(MODEL_NAME)
            
            # Basit bir test
            print("🧪 API bağlantı testi yapılıyor...")
            test_response = model.generate_content("Hello, test message. Just reply 'Connection Successful'.")
            print(f"✅ API Test Response: {test_response.text}")
            
            RAG_AVAILABLE = True
            print("🎉 RAG System successfully started!")
        else:
            print("❌ No suitable model found!")
            RAG_AVAILABLE = False
            
    except Exception as e:
        print(f"❌ Gemini API configuration error: {e}")
        RAG_AVAILABLE = False

def clean_json_response(response_text):
    """LLM yanıtından saf JSON çıkarır"""
    print(f"🔧 RAW RESPONSE: {response_text[:200]}...")
    
    try:
        # Backtick'leri temizle
        cleaned_text = response_text.replace('```json', '').replace('```', '').strip()
        
        # JSON'u bul
        json_match = re.search(r'\{.*\}', cleaned_text, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            print(f"🔧 FOUND JSON: {json_str[:100]}...")
            parsed_json = json.loads(json_str)
            print("✅ JSON successfully parsed")
            return parsed_json
    except Exception as e:
        print(f"❌ JSON cleaning error: {e}")
    
    return None

def generate_quiz_with_rag(topic, num_questions, question_type):
    """RAG ile İngilizce quiz soruları üretir"""
    
    if not RAG_AVAILABLE:
        print("❌ RAG not available, switching to simulation mode...")
        return None
    
    try:
        print(f"🚀 Generating {num_questions} questions with RAG...")
        print(f"   📝 Topic: {topic}")
        print(f"   🎯 Type: {question_type}")
        
        questions = []
        available_types = ["cloze test", "reading comprehension", "vocabulary", "grammar", "cloze test"]
        previous_types = []
        
        for i in range(num_questions):
            # Soru tipini seç
            if question_type.lower() == "karışık":
                if len(previous_types) >= 2 and previous_types[-1] == previous_types[-2]:
                    available = [t for t in available_types if t != previous_types[-1]]
                    selected_type = random.choice(available) if available else random.choice(available_types)
                else:
                    selected_type = random.choice(available_types)
                previous_types.append(selected_type)
                if len(previous_types) > 2:
                    previous_types = previous_types[-2:]
            else:
                # Türkçe tipi İngilizce'ye çevir
                type_mapping = {
                    "boşluk doldurma": "cloze test",
                    "paragraf sorusu": "reading comprehension", 
                    "kelime anlamı": "vocabulary",
                    "dil bilgisi": "grammar",
                    "cloze test": "cloze test"
                }
                selected_type = type_mapping.get(question_type, "cloze test")
            
            print(f"\n🔍 QUESTION {i+1}/{num_questions}: {selected_type}")
            
            # İngilizce prompt
            prompt = f"""
            CREATE ONE ENGLISH {selected_type.upper()} QUESTION IN JSON FORMAT:

            TOPIC: {topic}
            QUESTION TYPE: {selected_type}

            OUTPUT MUST BE IN THIS EXACT JSON FORMAT:
            {{
                "quiz": [
                    {{
                        "question_id": 1,
                        "question_text": "English question text here related to {topic}",
                        "options": {{
                            "A": "Option A text",
                            "B": "Option B text",
                            "C": "Option C text",
                            "D": "Option D text",
                            "E": "Option E text"
                        }},
                        "correct_option": "A",
                        "explanation": "Explanation in English why this is correct",
                        "question_type": "{selected_type}"
                    }}
                ]
            }}

            IMPORTANT:
            - Use ACADEMIC ENGLISH level appropriate for YDS/YÖKDİL exams
            - Make the question challenging but fair
            - Options should be semantically close but only one correct
            - Return ONLY JSON, no other text
            """
            
            try:
                print("   🤖 Sending request to LLM...")
                response = model.generate_content(prompt)
                print(f"   📥 Response received ({len(response.text)} characters)")
                
                cleaned_json = clean_json_response(response.text)
                
                if cleaned_json and 'quiz' in cleaned_json and cleaned_json['quiz']:
                    question_data = cleaned_json['quiz'][0]
                    question_data['question_id'] = i + 1
                    # Türkçe arayüz için orijinal tipi koru
                    reverse_type_mapping = {
                        "cloze test": "boşluk doldurma",
                        "reading comprehension": "paragraf sorusu",
                        "vocabulary": "kelime anlamı", 
                        "grammar": "dil bilgisi"
                    }
                    question_data['question_type'] = reverse_type_mapping.get(selected_type, selected_type)
                    questions.append(question_data)
                    print(f"   ✅ Question {i+1} SUCCESSFULLY generated!")
                else:
                    print(f"   ⚠️ Using fallback for question {i+1}")
                    questions.append(create_fallback_question(i + 1, selected_type, topic))
                    
            except Exception as e:
                print(f"   ❌ Question {i+1} error: {e}")
                questions.append(create_fallback_question(i + 1, selected_type, topic))
        
        print(f"\n🎉 TOTAL {len(questions)} questions generated!")
        return questions
        
    except Exception as e:
        print(f"❌ RAG pipeline error: {e}")
        return None

def create_fallback_question(question_id, question_type, topic):
    """İngilizce yedek soru oluştur"""
    
    # Türkçe tipi İngilizce'ye çevir
    type_mapping = {
        "boşluk doldurma": "cloze test",
        "paragraf sorusu": "reading comprehension",
        "kelime anlamı": "vocabulary", 
        "dil bilgisi": "grammar",
        "cloze test": "cloze test"
    }
    english_type = type_mapping.get(question_type, "cloze test")
    
    fallbacks = {
        "cloze test": {
            "question_text": f"The rapid development of {topic} has ______ significant changes across various industries and requires continuous adaptation from professionals.",
            "options": {
                "A": "triggered", 
                "B": "reduced", 
                "C": "prevented", 
                "D": "ignored", 
                "E": "complicated"
            },
            "correct_option": "A",
            "explanation": "'Triggered' means started or initiated, which fits the context of development causing changes across industries.",
            "question_type": "boşluk doldurma"
        },
        "reading comprehension": {
            "question_text": f"Reading comprehension: The integration of {topic} into modern society has fundamentally transformed how we communicate, work, and access information. This technological revolution presents both unprecedented opportunities and significant challenges that require careful consideration through education and regulation. According to the passage, what is the primary impact of {topic}?",
            "options": {
                "A": "It has no substantial effect on daily life",
                "B": "It has fundamentally transformed communication, work, and information access", 
                "C": "It only affects specialized technical fields",
                "D": "It simplifies communication but complicates professional work",
                "E": "Its benefits are limited to developed nations"
            },
            "correct_option": "B",
            "explanation": "The passage explicitly states that the integration has fundamentally transformed communication, work, and information access.",
            "question_type": "paragraf sorusu"
        },
        "vocabulary": {
            "question_text": f"In the context of {topic}, choose the word closest in meaning to 'innovation':",
            "options": {
                "A": "breakthrough", 
                "B": "tradition", 
                "C": "stagnation", 
                "D": "repetition", 
                "E": "imitation"
            },
            "correct_option": "A",
            "explanation": "'Innovation' refers to introducing new methods or ideas, making 'breakthrough' the closest synonym as both imply significant advances.",
            "question_type": "kelime anlamı"
        },
        "grammar": {
            "question_text": f"Choose the correct verb form: Research in {topic} ______ that new applications are being developed at an accelerating pace.",
            "options": {
                "A": "has shown", 
                "B": "showing", 
                "C": "have shown", 
                "D": "are showing", 
                "E": "show"
            },
            "correct_option": "A",
            "explanation": "'Has shown' is correct because 'research' is a singular noun requiring a singular verb form in present perfect tense.",
            "question_type": "dil bilgisi"
        }
    }
    
    template = fallbacks.get(english_type, fallbacks["cloze test"])
    question = template.copy()
    question["question_id"] = question_id
    return question

# Debug için test
if __name__ == '__main__':
    print("\n" + "="*60)
    print("🧪 RAG SYSTEM DEBUG TEST - ENGLISH QUESTIONS")
    print("="*60)
    
    if RAG_AVAILABLE:
        print("🎯 RAG system active, starting test...")
        test_questions = generate_quiz_with_rag("artificial intelligence", 2, "karışık")
        if test_questions:
            print("\n✅ RAG SYSTEM WORKING!")
            for i, q in enumerate(test_questions):
                print(f"\n📊 Question {i+1}:")
                print(f"   Type: {q['question_type']}")
                print(f"   Text: {q['question_text']}")
                print(f"   Correct: {q['correct_option']}")
        else:
            print("\n❌ RAG SYSTEM NOT WORKING!")
    else:
        print("❌ RAG SYSTEM NOT AVAILABLE!")