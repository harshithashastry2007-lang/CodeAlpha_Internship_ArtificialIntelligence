import streamlit as st
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(
    page_title="AI FAQ Chatbot",
    page_icon="🤖",
    layout="centered"
)

# ---------------- UI Styling ----------------
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
    }

    .subtitle {
        text-align: center;
        color: gray;
        font-size: 17px;
        margin-bottom: 25px;
    }

    .footer {
        text-align: center;
        color: gray;
        font-size: 14px;
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="main-title">🤖 AI FAQ Chatbot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Ask questions and get intelligent FAQ-based answers</div>',
    unsafe_allow_html=True
)

# ---------------- FAQ Dataset ----------------
faqs = {
    "What is Artificial Intelligence?":
        "Artificial Intelligence is the ability of machines to simulate human intelligence such as learning, reasoning, and decision-making.",

    "What is Machine Learning?":
        "Machine Learning is a branch of AI that enables computers to learn patterns from data and make predictions or decisions.",

    "What is Deep Learning?":
        "Deep Learning is a subset of Machine Learning that uses multi-layered neural networks to learn complex patterns from large amounts of data.",

    "What is NLP?":
        "Natural Language Processing is a field of AI that helps computers understand, interpret, and generate human language.",

    "What is a chatbot?":
        "A chatbot is a software application designed to simulate conversation with users through text or voice.",

    "What is Python?":
        "Python is a high-level programming language widely used in AI, Machine Learning, Data Science, automation, and web development.",

    "What is supervised learning?":
        "Supervised learning is a machine learning method where a model learns from labeled training data.",

    "What is unsupervised learning?":
        "Unsupervised learning is a machine learning method where the model discovers patterns in data without predefined labels.",

    "What is a neural network?":
        "A neural network is a computing model inspired by the human brain, consisting of interconnected layers of artificial neurons.",

    "What is computer vision?":
        "Computer Vision is a field of AI that enables machines to understand and analyze images and videos.",

    "What is data science?":
        "Data Science involves collecting, analyzing, and interpreting data to discover useful insights and support decision-making.",

    "What is an algorithm?":
        "An algorithm is a step-by-step procedure used to solve a problem or perform a specific task.",

    "What is cosine similarity?":
        "Cosine similarity measures how similar two text vectors are based on the angle between them.",

    "What is TF-IDF?":
        "TF-IDF stands for Term Frequency-Inverse Document Frequency. It is used to represent text based on the importance of words in documents.",

    "What is CodeAlpha?":
        "CodeAlpha is a software development company that provides internship opportunities and practical project experience across different technology domains."
}

questions = list(faqs.keys())

# ---------------- Text Preprocessing ----------------
def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    return text.strip()

processed_questions = [preprocess(q) for q in questions]

# ---------------- TF-IDF Model ----------------
vectorizer = TfidfVectorizer(stop_words="english")
faq_vectors = vectorizer.fit_transform(processed_questions)

# ---------------- Chat Function ----------------
def get_answer(user_question):
    cleaned_question = preprocess(user_question)

    user_vector = vectorizer.transform([cleaned_question])

    similarities = cosine_similarity(
        user_vector,
        faq_vectors
    )[0]

    best_index = similarities.argmax()
    best_score = similarities[best_index]

    if best_score < 0.20:
        return (
            "Sorry, I could not find a suitable answer. "
            "Please try asking the question in a different way.",
            best_score
        )

    return faqs[questions[best_index]], best_score

# ---------------- Session State ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- Display Previous Chat ----------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ---------------- User Input ----------------
user_input = st.chat_input("Ask me an AI-related question...")

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    answer, score = get_answer(user_input)

    with st.chat_message("assistant"):
        st.write(answer)
        st.caption(f"Similarity Confidence: {score * 100:.1f}%")

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

# ---------------- Clear Chat ----------------
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# ---------------- Suggested Questions ----------------
st.divider()

st.subheader("💡 Try asking")

st.write(
    "• What is Artificial Intelligence?\n"
    "• What is Machine Learning?\n"
    "• What is NLP?\n"
    "• What is a chatbot?\n"
    "• What is computer vision?"
)

# ---------------- Footer ----------------
st.divider()

st.markdown(
    """
    <div class="footer">
    Developed for CodeAlpha Artificial Intelligence Internship<br>
    AI FAQ Chatbot
    </div>
    """,
    unsafe_allow_html=True
)