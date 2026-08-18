import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import io

st.set_page_config(
    page_title="AI Language Translator",
    page_icon="🌐",
    layout="centered"
)

# ---------- Styling ----------
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
    }

    .subtitle {
        text-align: center;
        font-size: 17px;
        color: gray;
        margin-bottom: 25px;
    }

    .footer {
        text-align: center;
        color: gray;
        font-size: 14px;
        margin-top: 30px;
    }

    div.stButton > button {
        border-radius: 10px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown(
    '<div class="main-title">🌐 AI Language Translator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Translate text instantly across multiple languages using AI'
    '</div>',
    unsafe_allow_html=True
)

# ---------- Languages ----------
languages = {
    "English": "en",
    "Kannada": "kn",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Bengali": "bn",
    "Gujarati": "gu",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Italian": "it",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese": "zh-CN"
}

# ---------- Session State ----------
if "source" not in st.session_state:
    st.session_state.source = "English"

if "target" not in st.session_state:
    st.session_state.target = "Kannada"

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""

# ---------- Language Selection ----------
col1, col2, col3 = st.columns([5, 1, 5])

with col1:
    source = st.selectbox(
        "From",
        list(languages.keys()),
        index=list(languages.keys()).index(st.session_state.source)
    )

with col2:
    st.write("")
    st.write("")

    if st.button("🔄"):
        st.session_state.source, st.session_state.target = (
            st.session_state.target,
            st.session_state.source
        )
        st.rerun()

with col3:
    target = st.selectbox(
        "To",
        list(languages.keys()),
        index=list(languages.keys()).index(st.session_state.target)
    )

st.session_state.source = source
st.session_state.target = target

# ---------- Input ----------
text = st.text_area(
    "✍️ Enter text to translate",
    value=st.session_state.input_text,
    placeholder="Type your text here...",
    height=150
)

st.session_state.input_text = text

# ---------- Buttons ----------
btn1, btn2 = st.columns(2)

with btn1:
    translate = st.button(
        "🌐 Translate",
        use_container_width=True,
        type="primary"
    )

with btn2:
    clear = st.button(
        "🗑️ Clear",
        use_container_width=True
    )

# ---------- Clear ----------
if clear:
    st.session_state.input_text = ""
    st.session_state.translated_text = ""
    st.rerun()

# ---------- Translation ----------
if translate:

    if not text.strip():
        st.warning("⚠️ Please enter some text.")

    elif source == target:
        st.warning("⚠️ Please select two different languages.")

    else:
        try:
            with st.spinner("Translating..."):

                translated = GoogleTranslator(
                    source=languages[source],
                    target=languages[target]
                ).translate(text)

                st.session_state.translated_text = translated

            st.success("✅ Translation completed successfully!")

        except Exception:
            st.error(
                "❌ Translation failed. Please check your internet connection."
            )

# ---------- Output ----------
if st.session_state.translated_text:

    st.subheader("✨ Translated Text")

    st.text_area(
        "Translation",
        value=st.session_state.translated_text,
        height=150,
        disabled=True
    )

    # Copy-friendly output
    st.code(
        st.session_state.translated_text,
        language=None
    )

    st.caption("📋 Use the copy icon above to copy the translation.")

    # ---------- Text to Speech ----------
    try:
        audio = io.BytesIO()

        speech = gTTS(
            text=st.session_state.translated_text,
            lang=languages[target]
        )

        speech.write_to_fp(audio)
        audio.seek(0)

        st.write("🔊 **Listen to Translation**")
        st.audio(audio, format="audio/mp3")

    except Exception:
        st.info(
            "🔊 Audio is not available for this language."
        )

# ---------- Footer ----------
st.divider()

st.markdown(
    """
    <div class="footer">
    Developed for CodeAlpha Artificial Intelligence Internship<br>
    AI Language Translation Tool
    </div>
    """,
    unsafe_allow_html=True
)