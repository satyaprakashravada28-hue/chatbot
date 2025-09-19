import pandas as pd
from transformers import pipeline
from langdetect import detect
import random

# Load dataset
try:
    df = pd.read_csv("agriassist_multilang_greeting.csv")
except Exception as e:
    print("❌ Error loading dataset:", e)
    df = pd.DataFrame(columns=["Name", "Use (English)", "Use (Telugu)", "Use (Hindi)", "Category"])

# Try to load QA pipeline
try:
    qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
except Exception as e:
    print("❌ Error loading transformers pipeline:", e)
    qa_pipeline = None

# Short replies dictionary (multi-language support)
shortcuts = {
    "en": {
        "hi": "Hello! I'm AgriAssist — your farming buddy.",
        "joke": "😂 Why did the scarecrow win an award? Because he was outstanding in his field!"
    },
    "kn": {
        "ನಮಸ್ಕಾರ.": "ಹಲೋ! ನಾನು ಅಗ್ರಿಅಸಿಸ್ಟ್ — ನಿಮ್ಮ ಕೃಷಿ ಗೆಳೆಯ.",
        "joke": "😂 ಭೂತದ ಗುಡ್ಡಗೆ ಬಹುಮಾನ ಯಾಕೆ ಸಿಕ್ಕಿತು? ಏಕೆಂದರೆ ಅವನು ತನ್ನ ಹೊಲದಲ್ಲಿ ಅಸಾಧಾರಣನಾಗಿದ್ದ!"
    },
    "ml": {
        "നമസ്കാരം.": "ഹലോ! ഞാനാണ് അഗ്രിഅസിസ്റ്റ് — നിങ്ങളുടെ കൃഷിസ്ഥലം കൂട്ടുകാരന്‍.",
        "joke": "😂 കാക്കയെ ഭയപ്പെടുത്തുന്ന മോഡലിന് അവാർഡ് ലഭിച്ചത് എന്തുകൊണ്ട്? കാരണം അത് തന്റെ വയലിൽ മികച്ചതായിരുന്നു!"
    },
    "pa": {
        "hi": "ਹੈਲੋ! ਮੈਂ ਅੈਗਰੀਅਸਿਸਟ ਹਾਂ — ਤੁਹਾਡਾ ਖੇਤੀਬਾੜੀ ਸਾਥੀ.",
        "joke": "😂 ਡਰਾਉਣੀ ਪਤਲ ਨੂੰ ਇਨਾਮ ਕਿਉਂ ਮਿਲਿਆ? ਕਿਉਂਕਿ ਉਹ ਆਪਣੇ ਖੇਤ ਵਿੱਚ ਸ਼ਾਨਦਾਰ ਸੀ!"
    },
    "gu": {
        "hi": "હેલો! હું એગ્રીઅસિસ્ટ છું — તમારો ખેતી સહાયક.",
        "joke": "😂 ભૂતિયા કાકડાને એવોર્ડ શા માટે મળ્યો? કારણ કે તે પોતાની ખેતરમાં ઉત્કૃષ્ટ હતો!"
    },
    "or": {
        "hi": "ନମସ୍କାର! ମୁଁ ଅଗ୍ରିଅସିଷ୍ଟ — ଆପଣଙ୍କର କୃଷି ସହଯୋଗୀ।",
        "joke": "😂 କାଉକୁ ଭୟ ପକାଉଥିବା ଝୁଲାକୁ ପୁରସ୍କାର ମିଳିଲା କାହିଁକି? କାରଣ ସେ ତାଙ୍କର ଖେତରେ ଅସାଧାରଣ ଥିଲେ!"
    },
    "bn": {
        "hi": "হ্যালো! আমি এগ্রিঅ্যাসিস্ট — আপনার কৃষি বন্ধু।",
        "joke": "😂 কাকভীতির মূর্তিকে পুরস্কার দেওয়া হয়েছিল কেন? কারণ সে তার খেতে অসাধারণ ছিল!"
    },
    "as": {
        "hi": "নমস্কাৰ! মই এগ্ৰিঅছিষ্ট — আপোনাৰ খেতি সহায়ক।",
        "joke": "😂 কেঁচা মানুহজনক পুৰস্কাৰ কিয় দিয়া হৈছিল? কাৰণ তেওঁ নিজৰ খেতিত অতি উৎকৃষ্ট আছিল!"
    },
    "te": {
        "హాయ్.": "👋 హాయ్ రైతూ! ఎలా ఉన్నావు?",
        "హలో.": "🌱 హలో! నేను నీ వ్యవసాయ స్నేహితుడు AgriAssist.",
        'హెల్.':"🌱 హలో! నేను నీ వ్యవసాయ స్నేహితుడు AgriAssist.",
        "ఏమన్నావు.": "😃 నువ్వే చెప్పు రైతూ, నీకు ఏం కావాలి?",
        "ఎం రా బాబు.": "😂 నేనే AgriAssist బాబు, నీకు సహాయం చేయడానికి వచ్చాను!",
        "జోక్ చెప్పు.": "😂 ఓ రైతు ఎందుకు ఆనందంగా ఉన్నాడు? ఎందుకంటే పంట బాగుంది!",
        "నువ్వెవరు.": "🤖 నేను AgriAssist — నీ డిజిటల్ వ్యవసాయ స్నేహితుడు.",
        "ఎలా ఉన్నావు?": "😇 బాగున్నాను! రైతులకు సహాయం చేయడం నా ఆనందం.",
        "వాతావరణం.": "🌦️ వాతావరణ సమాచారం కావాలా? అడుగు.",
        "పంట.": "🌾 ఏ పంట గురించి తెలుసుకోవాలి?",
        "ధన్యవాదాలు.": "🙏 ధన్యవాదాలు! ఎప్పుడూ సహాయం చేస్తాను."
    },
    "hi": {
        "नमस्ते।": "👋 नमस्ते किसान! मैं AgriAssist हूँ — आपका खेती साथी।",
        "नमस्ते।": "👋 नमस्ते किसान! मैं AgriAssist हूँ — आपका खेती साथी।",
        "जोक": "😂 डरावना पुतला इनाम क्यों जीता? क्योंकि वह खेत में सबसे शानदार खड़ा था!",
        "आप कौन हो?": "🤖 मैं AgriAssist हूँ — आपका खेती सहायक।",
        "कैसे हो?": "😇 मैं अच्छा हूँ! किसानों की मदद करना ही खुशी है।",
        "मौसम।": "🌦️ मौसम की जानकारी चाहिए?",
        "फसल।": "🌾 किस फसल के बारे में जानना है?",
        "धन्यवाद।": "🙏 धन्यवाद! हमेशा मदद करूंगा।"
    }
}

# === MAIN FUNCTION ===
def generate_chatbot_response(user_input):
    try:
        if not user_input.strip():
            return "Please ask something related to farming or crops."

        if qa_pipeline is None:
            return "⚠️ Chatbot model not loaded. Please check the backend."

        cleaned_input = user_input.strip().lower()

        # --- Detect language (default English if fail)
        try:
            lang_detected = detect(user_input)
        except:
            lang_detected = "en"

        if lang_detected.startswith("te"):
            lang = "te"
            response_column = "Use (Telugu)"
        elif lang_detected.startswith("kn"):
            lang = "kn"
        elif lang_detected.startswith("hi"):
            lang = "hi"
            response_column = "Use (Kannada)"
        elif lang_detected.startswith("ml"):
            lang = "ml"
            response_column = "Use (Malayalam)"
        elif lang_detected.startswith("pa"):
            lang = "pa"
            response_column = "Use (Punjabi)"
        elif lang_detected.startswith("gu"):
            lang = "gu"
            response_column = "Use (Gujarati)"
        elif lang_detected.startswith("or"):
            lang = "or"
            response_column = "Use (Odia)"
        elif lang_detected.startswith("bn"):
            lang = "bn"
            response_column = "Use (Bengali)"
        elif lang_detected.startswith("as"):
            lang = "as"
            response_column = "Use (Assamese)"
        else:
            lang = "en"
            response_column = "Use (English)"

        # --- 1. Shortcuts (multi-language)
        if cleaned_input in shortcuts.get(lang, {}):
            return shortcuts[lang][cleaned_input]

        # --- 2. Exact match on 'Name'
        exact = df[df["Name"].str.lower() == cleaned_input]
        if not exact.empty:
            return exact.iloc[0].get(response_column, exact.iloc[0]["Use (English)"])

        # --- 3. Partial match on 'Name'
        partial = df[df["Name"].str.lower().str.contains(cleaned_input)]
        if not partial.empty:
            return partial.iloc[0].get(response_column, partial.iloc[0]["Use (English)"])

        # --- 4. Category match
        category_match = df[df["Category"].str.lower() == cleaned_input]
        if not category_match.empty:
            return random.choice(category_match[response_column].dropna().tolist())

        # --- 5. QA Fallback
        full_context = "\n".join([f"{row['Name']}: {row.get(response_column, row.get('Use (English)', ''))}"
                                  for _, row in df.iterrows()])

        result = qa_pipeline({
            "context": full_context,
            "question": user_input
        })

        answer = result.get("answer", "")
        score = result.get("score", 0)

        if score > 0.3 and len(answer) > 3:
            return answer.strip()
        else:
            return {
                "en": "🤔 I'm not sure. Try asking about crops, soil, fertilizers, irrigation, or weather.",
                "te": "🤔 నాకు ఖచ్చితంగా తెలియదు. పంటలు, ఎరువులు, నీటి పారుదల లేదా వాతావరణం గురించి అడగండి.",
                "hi": "🤔 मुझे यकीन नहीं है। फसल, उर्वरक, सिंचाई या मौसम के बारे में पूछें।",
                "kn": " ನನಗೆ ಖಚಿತವಿಲ್ಲ. ದಯವಿಟ್ಟು ಬೆಳೆಗಳು, ರಸಗೊಬ್ಬರೆಗಳು ಅಥವಾ ಹವಾಮಾನದ ಬಗ್ಗೆ ಕೇಳಿ.",
                "ml": " എനിക്ക് ഉറപ്പില്ല. വിളകൾ, വളങ്ങൾ, കാലാവസ്ഥ എന്നിവയെക്കുറിച്ച് ചോദിക്കൂ.",
                "pa": " ਮੈਨੂੰ ਪਤਾ ਨਹੀਂ। ਫਸਲਾਂ, ਖਾਦਾਂ ਜਾਂ ਮੌਸਮ ਬਾਰੇ ਪੁੱਛੋ ਜੀ।",
                "gu": " મને ખાતરી નથી. કૃપા કરીને પાકો, ખાતરો, સિંચાઈ અથવા હવામાન વિશે પૂછો.",
                "or": " ମୋତେ ନିଶ୍ଚିତ ନୁହେଁ। ଫସଲ, ସର୍ବରାହ, ବର୍ଷା ବିଷୟରେ ପଚାରନ୍ତୁ।",
                "bn": " আমি নিশ্চিত নই। দয়া করে ফসল, সার, বা আবহাওয়া সম্পর্কে জিজ্ঞাসা করুন।",
                "as": " মই নিশ্চিত নহয়। অনুগ্ৰহ কৰি খেতি, সাৰ বা বতৰৰ বিষয়ে সোধক।"
                }.get(lang, "🤔 I'm not sure.")
    except Exception as e:
        return f"⚠️ Error in chatbot response: {str(e)}"
