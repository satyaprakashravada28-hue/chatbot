# chatbot
🚀 Project Title: AgriAssist: Smart Multilingual Farmer Chatbot + Crop Recommendation System 🧠 Summary: AgriAssist is an all-in-one AI-powered assistant designed for farmers. It offers: 💬 A multilingual chatbot that can answer farming-related queries (supports Hindi, Telugu, English, and more). 🌾 A crop recommendation system using machine learning. 🗣️ Voice-based input and output (speech-to-text and text-to-speech). 🌐 A clean web interface built with Flask and Bootstrap. ⚙️ All APIs, models, and logic built in-house – no external APIs used, ensuring cost-efficiency, faster access, and offline-readiness.

🎯 Key Features: 🧠 In-house Trained Crop Prediction Model Trained using a custom dataset with 14+ input features.

Supports features like: N, P, K values Temperature, Humidity Soil type, Season, District Water availability, Fertilizer used Sunlight hours, etc. Model is saved as .pkl and served through Flask.

🤖 AI Chatbot — Multilingual Support Handles FAQs, jokes, motivational messages, fertilizer suggestions, irrigation tips, etc. Trained using a custom dataset. Languages Supported: English 🇬🇧 Hindi 🇮🇳 Telugu 🇮🇳 (Ready to expand to 10+ languages)

🎤 Voice Support Voice Input: Users can ask questions using mic (Web Speech API). Voice Output: Bot responds using Text-to-Speech (TTS). Works across devices for accessibility.

📊 Accurate Predictions Model accuracy tested using sklearn.metrics.accuracy_score — achieved high precision. Uses LabelEncoder + StandardScaler for categorical and scaled input handling. for the accuracy of the crop prediction form : 1.logistic Regression accuracy:97.5% 2. Random forest classifier accuracy:99.5%

💰 No External APIs Used No OpenAI, Google APIs, or paid third-party services used. Entire chatbot and prediction system work on local/internal logic. Reduces cost, improves speed, and allows offline readiness for rural deployments.

🧩 Modular Code Structure app.py → Main Flask app utils/chatbot_logic.py → Chatbot logic model/ → Trained .pkl model files templates/ → HTML templates static/ → CSS, JS, assets

🧪 Fully Functional Prototype Judges in evaluation sessions spent 3x more time on this project (30 min instead of 10 min). Received strong positive feedback and suggestions. Already suitable for integration into mobile apps/web apps for real-world usage.

Layer	Tools Used
Frontend	HTML, CSS, Bootstrap, JavaScript
Backend	Python (Flask)
ML Model	scikit-learn, Pandas, NumPy,matplotlib,seaborn
Voice Input	Web Speech API
Voice Output	JavaScript TTS
Chatbot	Transformers (Hugging Face), Custom logic
Deployment	Localhost / Ready for cloud/app integration
🔐 No API Keys Required This project runs 100% locally with zero need for: API tokens Auth headers Key management This makes it perfectly deployable in rural/remote settings where internet cost and API latency are issues.

💡 Unique Points: ✅ Built without any paid third-party APIs ✅ Supports real-time voice interaction ✅ Custom multilingual chatbot for farmer-centric topics ✅ Advanced crop prediction using enriched dataset ✅ Offline deployment ready ✅ Judges during evaluation session spent extra time due to the project’s originality and execution ✅ Expandable to mobile app or smart devices

✅ Future Scope: Add image-based disease detection (CV) Integrate farmer Q&A via mobile app Expand language support to 15+ Add fertilizer and pesticide usage prediction Deploy via Streamlit or Android app wrapper
