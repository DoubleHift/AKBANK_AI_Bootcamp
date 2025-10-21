# 🎯 YDS/YÖKDİL RAG Quiz Generator

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28-FF4B4B.svg)
![RAG](https://img.shields.io/badge/RAG-Architecture-green.svg)
![Gemini](https://img.shields.io/badge/Gemini-AI-orange.svg)

**Akbank GenAI Bootcamp Projesi - Context-Aware English Exam Generator**

[🚀 Live Demo](#) • [📚 Documentation](#) • [💡 Features](#features)

</div>

## 📖 Overview

YDS/YÖKDİL RAG Quiz Generator, Retrieval Augmented Generation (RAG) teknolojisi kullanarak konuya özel İngilizce sınav soruları üreten akıllı bir uygulamadır. Geleneksel sabit soru bankaları yerine, kullanıcının belirlediği herhangi bir konuda anlamlı ve bağlamsal sorular oluşturur.

## 🎯 Features

### 🤖 Smart Question Generation
- **Context-Aware**: RAG mimarisi ile konuya özgü sorular
- **Multiple Question Types**: Cloze tests, reading comprehension, vocabulary, grammar
- **Adaptive Difficulty**: YDS/YÖKDİL seviyesine uygun akademik İngilizce
- **Mixed Mode**: Akıllı karışık soru dağılımı

### ⚡ Real-time Experience
- **Live Timer**: Gerçek zamanlı sınav deneyimi
- **Instant Feedback**: Anlık sonuç ve detaylı analiz
- **Progress Tracking**: Soru tipi bazında performans takibi

### 🎨 User-Friendly Interface
- **Streamlit UI**: Modern ve responsive arayüz
- **Topic Customization**: Her konuda sınav oluşturma
- **Flexible Settings**: Soru sayısı ve tipi özelleştirme
##🚀 Quick Start
###Prerequisites
-Python 3.8 or higher
-Google Gemini API Key href(Get it here)
## 🏗️ Architecture

```mermaid
graph TB
    A[User Input] --> B[Topic & Settings]
    B --> C[RAG Pipeline]
    C --> D[Vector Database]
    D --> E[Gemini AI]
    E --> F[Question Generation]
    F --> G[Quiz Engine]
    G --> H[Streamlit UI]
    H --> I[Results & Analytics]
🚀 Quick Start
