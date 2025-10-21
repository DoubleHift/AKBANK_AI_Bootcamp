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

if not API_KEY:
    print("❌ GEMINI_API_KEY environment variable bulunamadı!")
    RAG_AVAILABLE = False
else:
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')
        RAG_AVAILABLE = True
        print("✅ Gemini API başarıyla yapılandırıldı")
    except Exception as e:
        print(f"❌ Gemini API yapılandırma hatası: {e}")
        RAG_AVAILABLE = False

def clean_json_response(response_text):
    """LLM yanıtından saf JSON çıkarır"""
    try:
        cleaned_text = response_text.replace('```json', '').replace('```', '').strip()
        json_match = re.search(r'\{.*\}', cleaned_text, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            parsed_json = json.loads(json_str)
            return parsed_json
    except Exception as e:
        print(f"JSON temizleme hatası: {e}")
    return None

def generate_quiz_with_rag(topic, num_questions, question_type):
    """RAG ile İngilizce quiz soruları üretir"""
    
    if not RAG_AVAILABLE:
        print("❌ RAG kullanılamıyor, simülasyon moduna geçiliyor...")
        return None
    
    try:
        print(f"🎯 RAG ile {num_questions} soru üretiliyor...")
        
        questions = []
        available_types = ["cloze test", "reading comprehension", "vocabulary", "grammar"]
        previous_types = []
        
        for i in range(num_questions):
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
                type_mapping = {
                    "boşluk doldurma": "cloze test",
                    "paragraf sorusu": "reading comprehension", 
                    "kelime anlamı": "vocabulary",
                    "dil bilgisi": "grammar",
                    "cloze test": "cloze test"
                }
                selected_type = type_mapping.get(question_type, "cloze test")
            
            print(f"🔍 Soru {i+1}: {selected_type}")
            
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

            Return ONLY JSON, no other text.
            """
            
            try:
                response = model.generate_content(prompt)
                cleaned_json = clean_json_response(response.text)
                
                if cleaned_json and 'quiz' in cleaned_json and cleaned_json['quiz']:
                    question_data = cleaned_json['quiz'][0]
                    question_data['question_id'] = i + 1
                    reverse_type_mapping = {
                        "cloze test": "boşluk doldurma",
                        "reading comprehension": "paragraf sorusu",
                        "vocabulary": "kelime anlamı", 
                        "grammar": "dil bilgisi"
                    }
                    question_data['question_type'] = reverse_type_mapping.get(selected_type, selected_type)
                    questions.append(question_data)
                    print(f"✅ Soru {i+1} başarıyla üretildi")
                else:
                    questions.append(create_fallback_question(i + 1, selected_type, topic))
                    print(f"⚠️ Soru {i+1} için fallback kullanıldı")
                    
            except Exception as e:
                print(f"❌ Soru {i+1} hatası: {e}")
                questions.append(create_fallback_question(i + 1, selected_type, topic))
        
        print(f"✅ Toplam {len(questions)} soru üretildi")
        return questions
        
    except Exception as e:
        print(f"❌ RAG pipeline hatası: {e}")
        return None

def create_fallback_question(question_id, question_type, topic):
    """İngilizce yedek soru oluştur"""
    
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
            "question_text": f"The rapid development of {topic} has ______ significant changes across various industries.",
            "options": {
                "A": "triggered", 
                "B": "reduced", 
                "C": "prevented", 
                "D": "ignored", 
                "E": "complicated"
            },
            "correct_option": "A",
            "explanation": "'Triggered' means started or initiated, which fits the context of development causing changes.",
            "question_type": "boşluk doldurma"
        },
        "reading comprehension": {
            "question_text": f"Reading comprehension: The integration of {topic} into modern society has fundamentally transformed how we communicate and work. According to the passage, what is the primary impact of {topic}?",
            "options": {
                "A": "It has no substantial effect on daily life",
                "B": "It has fundamentally transformed communication and work", 
                "C": "It only affects specialized technical fields",
                "D": "Its benefits are limited to developed nations",
                "E": "It primarily creates social problems"
            },
            "correct_option": "B",
            "explanation": "The passage explicitly states that the integration has fundamentally transformed communication and work.",
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
            "explanation": "'Innovation' refers to introducing new methods or ideas, making 'breakthrough' the closest synonym.",
            "question_type": "kelime anlamı"
        },
        "grammar": {
            "question_text": f"Choose the correct verb form: Research in {topic} ______ that new applications are being developed rapidly.",
            "options": {
                "A": "has shown", 
                "B": "showing", 
                "C": "have shown", 
                "D": "are showing", 
                "E": "show"
            },
            "correct_option": "A",
            "explanation": "'Has shown' is correct because 'research' is a singular noun requiring a singular verb form.",
            "question_type": "dil bilgisi"
        }
    }
    
    template = fallbacks.get(english_type, fallbacks["cloze test"])
    question = template.copy()
    question["question_id"] = question_id
    return question

if __name__ == '__main__':
    if RAG_AVAILABLE:
        print("🧪 RAG Test Ediliyor...")
        test_questions = generate_quiz_with_rag("technology", 2, "boşluk doldurma")
        if test_questions:
            print("✅ RAG çalışıyor!")
        else:
            print("❌ RAG çalışmıyor!")
    else:
        print("❌ RAG kullanılamıyor")