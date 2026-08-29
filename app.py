import re
import html
import streamlit as st

from core.verification import verify_article


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="NewsLens",
    page_icon="📰",
    layout="wide",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
"""<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;500;600;700;800&display=swap');

/* =========================
GLOBAL
========================= */

html, body, [class*="css"] {
font-family: 'Inter', -apple-system, sans-serif;
}

.stApp {
background:
radial-gradient(circle at 12% 0%, rgba(91,77,232,0.16), transparent 42%),
radial-gradient(circle at 88% 18%, rgba(37,99,235,0.14), transparent 40%),
radial-gradient(circle at 50% 100%, rgba(20,184,140,0.06), transparent 45%),
#060810;
}

.block-container {
max-width: 1150px;
padding-top: 2rem;
padding-bottom: 3rem;
}

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

::selection {
background: rgba(93,140,255,0.35);
color: #ffffff;
}

/* =========================
HEADER
========================= */

.top-header {
display: flex;
justify-content: space-between;
align-items: center;
padding: 14px 22px;
border: 1px solid #1d2434;
border-radius: 18px;
background: linear-gradient(135deg, rgba(20,26,41,0.85), rgba(13,17,27,0.85));
backdrop-filter: blur(10px);
margin-bottom: 42px;
box-shadow: 0 10px 35px rgba(0,0,0,0.35);
}

.logo {
font-family: 'Space Grotesk', 'Inter', sans-serif;
font-size: 25px;
font-weight: 700;
color: #ffffff;
letter-spacing: -0.5px;
}

.logo span {
background: linear-gradient(90deg, #6ea8ff, #a78bfa);
-webkit-background-clip: text;
background-clip: text;
color: transparent;
}

.tagline {
color: #6b7690;
font-size: 11px;
font-weight: 600;
letter-spacing: 2px;
margin-top: 4px;
}

.online {
color: #6bf0a5;
background: rgba(20,60,40,0.5);
border: 1px solid #23583b;
padding: 8px 14px;
border-radius: 20px;
font-size: 11px;
font-weight: 700;
letter-spacing: 0.3px;
box-shadow: 0 0 14px rgba(107,240,165,0.15);
}

.online::before {
content: "";
display: inline-block;
width: 7px;
height: 7px;
border-radius: 50%;
background: #6bf0a5;
margin-right: 6px;
box-shadow: 0 0 8px #6bf0a5;
}

/* =========================
HERO
========================= */

.hero {
text-align: center;
margin: 30px 0 50px 0;
}

.hero-badge {
display: inline-block;
color: #a9c6ff;
background: rgba(37,60,110,0.35);
border: 1px solid #2c4a80;
padding: 8px 16px;
border-radius: 20px;
font-size: 11px;
font-weight: 700;
letter-spacing: 1.2px;
margin-bottom: 22px;
}

.hero-title {
font-family: 'Space Grotesk', 'Inter', sans-serif;
color: #ffffff;
font-size: 60px;
line-height: 1.08;
font-weight: 700;
letter-spacing: -2px;
margin: 0;
}

.hero-title span {
background: linear-gradient(100deg, #7db4ff 10%, #a78bfa 55%, #f19bd6 100%);
-webkit-background-clip: text;
background-clip: text;
color: transparent;
}

.hero-description {
max-width: 620px;
margin: 20px auto 0 auto;
color: #8f9ab0;
font-size: 16.5px;
line-height: 1.75;
}

/* =========================
INPUT AREA
========================= */

.input-title {
font-family: 'Space Grotesk', 'Inter', sans-serif;
color: #ffffff;
font-size: 23px;
font-weight: 700;
margin-bottom: 6px;
}

.input-description {
color: #7d889d;
font-size: 13.5px;
margin-bottom: 16px;
}

textarea {
background-color: rgba(14,19,29,0.75) !important;
color: #f1f5f9 !important;
border: 1px solid #262f42 !important;
border-radius: 16px !important;
font-size: 15px !important;
line-height: 1.7 !important;
transition: border-color 0.2s, box-shadow 0.2s;
}

textarea:focus {
border-color: #5d8cff !important;
box-shadow: 0 0 0 3px rgba(93,140,255,0.18) !important;
}

div[data-testid="stTextArea"] label { display: none; }

/* =========================
BUTTON
========================= */

.stButton > button {
height: 54px;
border-radius: 14px;
border: none;
background: linear-gradient(90deg, #2563eb, #6d4de8 55%, #a44de8);
background-size: 200% 100%;
color: white;
font-size: 14px;
font-weight: 800;
letter-spacing: 0.6px;
transition: all 0.25s ease;
box-shadow: 0 8px 24px rgba(80,60,220,0.25);
}

.stButton > button:hover {
transform: translateY(-2px);
background-position: 100% 0;
box-shadow: 0 14px 34px rgba(93,110,255,0.35);
}

.stButton > button:active {
transform: translateY(0px);
}

/* =========================
SECTION HEADERS
========================= */

.section {
margin-top: 48px;
margin-bottom: 20px;
}

.section-small {
color: #7986a3;
font-size: 10.5px;
font-weight: 800;
letter-spacing: 1.8px;
text-transform: uppercase;
}

.section-title {
font-family: 'Space Grotesk', 'Inter', sans-serif;
color: #ffffff;
font-size: 26px;
font-weight: 700;
margin-top: 4px;
}

.section-description {
color: #7c869a;
font-size: 13.5px;
margin-top: 4px;
}

/* =========================
SCORE
========================= */

.score-card {
position: relative;
overflow: hidden;
background: linear-gradient(150deg, #131a2b 0%, #0e1420 65%);
border: 1px solid #263047;
border-radius: 20px;
padding: 28px 26px;
margin-bottom: 16px;
box-shadow: 0 20px 45px rgba(0,0,0,0.35);
}

.score-card::before {
content: "";
position: absolute;
top: -60%;
right: -20%;
width: 320px;
height: 320px;
background: radial-gradient(circle, rgba(109,77,232,0.25), transparent 70%);
pointer-events: none;
}

.score-label {
color: #8791a8;
font-size: 10.5px;
font-weight: 800;
letter-spacing: 1.6px;
}

.score-number {
font-family: 'Space Grotesk', 'Inter', sans-serif;
background: linear-gradient(90deg, #ffffff, #b9c6ff);
-webkit-background-clip: text;
background-clip: text;
color: transparent;
font-size: 56px;
font-weight: 700;
letter-spacing: -2px;
margin-top: 6px;
}

.score-number span {
color: #657187;
font-size: 19px;
-webkit-background-clip: initial;
background-clip: initial;
}

.score-text {
color: #8994ab;
font-size: 12.5px;
margin-top: 4px;
}

/* =========================
METRICS
========================= */

.metric {
background: rgba(17,23,32,0.75);
border: 1px solid #242d3b;
border-top: 3px solid #3b5bdb;
border-radius: 16px;
padding: 20px;
min-height: 135px;
transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.metric:hover {
transform: translateY(-3px);
box-shadow: 0 12px 28px rgba(0,0,0,0.3);
}

.metric-label {
color: #737f95;
font-size: 10px;
font-weight: 800;
letter-spacing: 1.3px;
}

.metric-value {
color: #f5f7fb;
font-size: 23px;
font-weight: 750;
margin-top: 10px;
}

.metric-sub {
color: #69758a;
font-size: 11px;
margin-top: 6px;
}

/* =========================
INSIGHT
========================= */

.insight {
background: linear-gradient(150deg, rgba(20,27,40,0.9), rgba(14,19,29,0.9));
border: 1px solid #29344a;
border-left: 3px solid #6d8cff;
border-radius: 16px;
padding: 24px;
color: #cbd3e0;
font-size: 14.5px;
line-height: 1.8;
}

/* =========================
SIGNALS
========================= */

.signal-box {
background: rgba(17,23,32,0.75);
border: 1px solid #242d3b;
border-radius: 16px;
padding: 22px;
min-height: 145px;
}

.signal-title {
color: #ffffff;
font-size: 13.5px;
font-weight: 800;
margin-bottom: 16px;
}

.signal-tag {
display: inline-block;
background: rgba(60,45,15,0.5);
border: 1px solid #59421d;
color: #f6c96b;
border-radius: 8px;
padding: 7px 11px;
margin: 3px;
font-size: 11px;
font-weight: 700;
transition: transform 0.15s ease;
}

.signal-tag:hover {
transform: translateY(-2px) scale(1.03);
}

/* =========================
CLAIM
========================= */

.claim {
background: rgba(16,23,32,0.75);
border: 1px solid #242e3c;
border-left: 3px solid #648fff;
border-radius: 14px;
padding: 18px 20px;
margin-bottom: 12px;
}

.claim-label {
color: #7ba3ff;
font-size: 9.5px;
font-weight: 900;
letter-spacing: 1.5px;
margin-bottom: 8px;
}

.claim-text {
color: #d3dae5;
font-size: 13.5px;
line-height: 1.7;
}

/* =========================
VERIFICATION
========================= */

.verification-summary {
position: relative;
overflow: hidden;
background: linear-gradient(150deg, #10201b 0%, #0d1712 65%);
border: 1px solid #26493a;
border-radius: 18px;
padding: 24px 26px;
box-shadow: 0 20px 45px rgba(0,0,0,0.3);
}

.verification-label {
color: #7c9186;
font-size: 10.5px;
font-weight: 800;
letter-spacing: 1.3px;
}

.verification-score {
font-family: 'Space Grotesk', 'Inter', sans-serif;
background: linear-gradient(90deg, #7ee2a5, #55c9c1);
-webkit-background-clip: text;
background-clip: text;
color: transparent;
font-size: 42px;
font-weight: 700;
margin-top: 4px;
}

.verification-card {
background: rgba(16,23,32,0.75);
border: 1px solid #242e3c;
border-radius: 16px;
padding: 20px;
margin-top: 14px;
transition: transform 0.2s ease;
}

.verification-card:hover {
transform: translateY(-2px);
}

.status-supported {
color: #7ee2a5;
background: rgba(20,40,25,0.6);
border: 1px solid #285537;
padding: 7px 12px;
border-radius: 20px;
font-size: 10.5px;
font-weight: 800;
}

.status-partial {
color: #f6cf69;
background: rgba(40,32,15,0.6);
border: 1px solid #58451d;
padding: 7px 12px;
border-radius: 20px;
font-size: 10.5px;
font-weight: 800;
}

.status-contradicted {
color: #ff9696;
background: rgba(40,20,20,0.6);
border: 1px solid #5a2828;
padding: 7px 12px;
border-radius: 20px;
font-size: 10.5px;
font-weight: 800;
}

.status-unverified {
color: #aeb8c8;
background: rgba(22,27,35,0.6);
border: 1px solid #303846;
padding: 7px 12px;
border-radius: 20px;
font-size: 10.5px;
font-weight: 800;
}

/* =========================
EXPANDERS
========================= */

div[data-testid="stExpander"] {
background: rgba(14,20,29,0.75);
border: 1px solid #242d3b;
border-radius: 14px;
}

/* =========================
PROGRESS BARS
========================= */

div[data-testid="stProgress"] > div > div {
background: linear-gradient(90deg, #2563eb, #a44de8);
}

/* =========================
FOOTER
========================= */

.footer {
text-align: center;
color: #4f596c;
font-size: 11px;
line-height: 1.8;
margin-top: 60px;
padding-top: 26px;
border-top: 1px solid #1c2430;
}
</style>""",
unsafe_allow_html=True,
)


# ============================================================
# ANALYSIS DICTIONARIES
# ============================================================

POSITIVE_WORDS = {
    "success", "successful", "growth", "improve", "improved",
    "benefit", "benefits", "positive", "win", "wins", "victory",
    "progress", "achievement", "opportunity", "hope", "better",
    "increase", "increased", "gain", "gained"
}

NEGATIVE_WORDS = {
    "crisis", "crash", "death", "dead", "disaster", "danger",
    "dangerous", "failure", "failed", "attack", "war", "fear",
    "threat", "threatening", "loss", "lost", "decline", "declined",
    "problem", "protest", "violence", "kill", "killed"
}

SENSATIONAL_WORDS = {
    "shocking", "breaking", "exclusive", "unbelievable",
    "outrageous", "explosive", "massive", "terrifying",
    "horrifying", "stunning", "jaw-dropping", "secret",
    "exposed", "urgent", "disaster", "bombshell", "scandal",
    "you won't believe", "must see", "viral"
}

EMOTIONAL_WORDS = {
    "fear", "afraid", "terrifying", "angry", "anger", "outrage",
    "love", "hate", "shocking", "horrifying", "heartbreaking",
    "tragic", "hope", "proud", "betrayal", "panic"
}

OPINION_MARKERS = {
    "i think", "i believe", "in my opinion", "should",
    "must", "clearly", "obviously", "perhaps", "probably",
    "arguably", "we need", "it seems"
}

FACTUAL_MARKERS = {
    "according to", "reported", "data", "official", "confirmed",
    "announced", "statement", "study", "research", "statistics",
    "percent", "%", "said", "reported by"
}


# ============================================================
# BASIC TEXT FUNCTIONS
# ============================================================

def words(text):
    return re.findall(r"\b[\w'-]+\b", text.lower())


def count_matches(text, vocabulary):
    text_lower = text.lower()
    tokens = words(text)

    count = 0

    for item in vocabulary:

        if " " in item:

            if item in text_lower:
                count += 1

        elif item in tokens:

            count += 1

    return count


def sentence_split(text):
    return [
        s.strip()
        for s in re.split(r"[.!?]+", text)
        if s.strip()
    ]


# ============================================================
# TONE ANALYSIS
# ============================================================

def analyze_tone(text):

    pos = count_matches(
        text,
        POSITIVE_WORDS
    )

    neg = count_matches(
        text,
        NEGATIVE_WORDS
    )

    if pos > neg:
        tone = "Positive"

    elif neg > pos:
        tone = "Negative"

    else:
        tone = "Neutral"

    total = pos + neg

    if total == 0:
        confidence = 50

    else:
        confidence = min(
            95,
            55 + abs(pos - neg) * 8
        )

    return tone, confidence, pos, neg


# ============================================================
# SENSATIONALISM
# ============================================================

def analyze_sensationalism(text):

    matches = count_matches(
        text,
        SENSATIONAL_WORDS
    )

    exclamation_count = text.count("!")
    question_count = text.count("?")

    uppercase_words = re.findall(
        r"\b[A-Z]{3,}\b",
        text
    )

    uppercase_penalty = min(
        4,
        len(uppercase_words)
    )

    score = (
        matches * 12
        + exclamation_count * 7
        + uppercase_penalty * 5
        + min(question_count * 3, 9)
    )

    score = min(
        100,
        score
    )

    if score >= 65:
        label = "High"

    elif score >= 30:
        label = "Moderate"

    else:
        label = "Low"

    return score, label


# ============================================================
# EMOTIONAL FRAMING
# ============================================================

def analyze_emotion(text):

    count = count_matches(
        text,
        EMOTIONAL_WORDS
    )

    if count >= 5:

        return (
            "Strong emotional framing",
            min(95, 55 + count * 6)
        )

    if count >= 2:

        return (
            "Moderate emotional framing",
            min(90, 45 + count * 7)
        )

    return (
        "Low emotional framing",
        25
    )


# ============================================================
# CONTENT TYPE
# ============================================================

def analyze_content_type(text):

    opinion = count_matches(
        text,
        OPINION_MARKERS
    )

    factual = count_matches(
        text,
        FACTUAL_MARKERS
    )

    if opinion >= 2 and opinion > factual:

        return "Opinion / Commentary"

    if factual >= 2 and factual >= opinion:

        return "News / Factual reporting"

    return "Mixed / Unclear"


# ============================================================
# LOADED LANGUAGE
# ============================================================

def detect_loaded_language(text):

    found = []

    lower_text = text.lower()

    for word in SENSATIONAL_WORDS:

        if word in lower_text:

            found.append(word)

    return found[:10]


# ============================================================
# CLAIM EXTRACTION
# ============================================================

def extract_claims(text):

    sentences = sentence_split(text)

    claims = []

    for sentence in sentences:

        lower = sentence.lower()

        has_number = bool(
            re.search(
                r"\b\d+(?:\.\d+)?%?\b",
                sentence
            )
        )

        has_factual_marker = any(
            marker in lower
            for marker in FACTUAL_MARKERS
        )

        has_claim_verb = any(
            verb in lower.split()
            for verb in [
                "is",
                "are",
                "was",
                "were",
                "has",
                "have",
                "will",
                "announced",
                "said",
                "reported",
                "caused",
                "increased",
                "decreased",
            ]
        )

        if (
            has_number
            or has_factual_marker
            or has_claim_verb
        ):

            claims.append(sentence)

    return claims[:6]


# ============================================================
# OVERALL SCORE
# ============================================================

def calculate_score(
    sensationalism,
    emotion_score,
    loaded_count,
    content_type
):

    score = 100

    score -= sensationalism * 0.35

    score -= emotion_score * 0.15

    score -= loaded_count * 3

    if content_type == "Mixed / Unclear":

        score -= 5

    return max(
        0,
        min(
            100,
            round(score)
        )
    )


# ============================================================
# EXPLANATION
# ============================================================

def generate_explanation(
    tone,
    content_type,
    sensational_label,
    emotion_label,
    loaded_words,
    score,
):

    explanations = []

    explanations.append(
        f"The story is classified as {content_type.lower()}."
    )

    explanations.append(
        f"The overall tone is {tone.lower()}."
    )

    if sensational_label == "High":

        explanations.append(
            "The text contains several signals associated "
            "with sensational presentation."
        )

    elif sensational_label == "Moderate":

        explanations.append(
            "The text contains some attention-grabbing "
            "or sensational language."
        )

    else:

        explanations.append(
            "The text shows relatively few sensational "
            "language signals."
        )

    if emotion_label == "Strong emotional framing":

        explanations.append(
            "Strong emotional wording may influence how "
            "readers perceive the story."
        )

    elif emotion_label == "Moderate emotional framing":

        explanations.append(
            "Some emotional language is present and may "
            "influence reader perception."
        )

    if loaded_words:

        explanations.append(
            "Potentially loaded terms detected: "
            + ", ".join(loaded_words[:6])
            + "."
        )

    if score >= 75:

        explanations.append(
            "The presentation appears relatively restrained "
            "based on these signals."
        )

    elif score >= 50:

        explanations.append(
            "The presentation contains some signals that "
            "deserve reader attention."
        )

    else:

        explanations.append(
            "The presentation contains several signals "
            "that deserve careful scrutiny."
        )

    return " ".join(explanations)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """<div class="top-header">

<div>
<div class="logo">
📰 News<span>Lens</span>
</div>

<div class="tagline">
AI NEWS INTELLIGENCE
</div>
</div>

<div class="online">
● SYSTEM ONLINE
</div>

</div>""",
    unsafe_allow_html=True,
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """<div class="hero">

<div class="hero-badge">
✦ AI-POWERED MEDIA ANALYSIS
</div>

<div class="hero-title">
See beyond the <span>headline.</span>
</div>

<div class="hero-description">
Understand how information is written, framed,
and supported before you believe it.
</div>

</div>""",
    unsafe_allow_html=True,
)


# ============================================================
# INPUT
# ============================================================

st.markdown(
    """<div class="input-title">
Analyze a news story
</div>

<div class="input-description">
Paste a headline or full article to uncover
hidden language and information signals.
</div>""",
    unsafe_allow_html=True,
)


news_text = st.text_area(
    "News article",
    height=230,
    placeholder=(
        "Paste a headline or article here...\n\n"
        "Example: Government announces shocking new "
        "education policy that will completely change "
        "the future of millions of students..."
    ),
    label_visibility="collapsed",
)


word_count = (
    len(news_text.split())
    if news_text.strip()
    else 0
)

st.caption(
    f"{word_count} words  •  "
    "Tone  •  Sensationalism  •  Emotion  •  "
    "Claims  •  Evidence"
)


analyze = st.button(
    "✦  ANALYZE STORY",
    use_container_width=True,
    type="primary",
)


# ============================================================
# ANALYSIS
# ============================================================

if analyze:

    if not news_text.strip():

        st.warning(
            "Please paste a headline or news article first."
        )

    elif len(news_text.split()) < 5:

        st.warning(
            "Please provide a little more text "
            "for a meaningful analysis."
        )

    else:

        with st.spinner(
            "NewsLens is analyzing the story..."
        ):

            tone, tone_confidence, pos, neg = (
                analyze_tone(news_text)
            )

            sensational_score, sensational_label = (
                analyze_sensationalism(news_text)
            )

            emotion_label, emotion_score = (
                analyze_emotion(news_text)
            )

            content_type = analyze_content_type(
                news_text
            )

            loaded_words = detect_loaded_language(
                news_text
            )

            claims = extract_claims(
                news_text
            )

            # ------------------------------------------
            # PHASE 2 VERIFICATION
            # ------------------------------------------

            verification_result = None
            verification_error = None

            try:

                verification_result = verify_article(
                    news_text,
                    max_claims=3,
                    sources_per_claim=2,
                )

            except Exception as exc:

                verification_error = str(exc)

            # ------------------------------------------
            # SCORE
            # ------------------------------------------

            overall_score = calculate_score(
                sensational_score,
                emotion_score,
                len(loaded_words),
                content_type,
            )

            explanation = generate_explanation(
                tone,
                content_type,
                sensational_label,
                emotion_label,
                loaded_words,
                overall_score,
            )

        # =================================================
        # RESULTS HEADER
        # =================================================

        st.markdown(
            """<div class="section">

<div class="section-small">
ANALYSIS COMPLETE
</div>

<div class="section-title">
Story intelligence
</div>

<div class="section-description">
A breakdown of the signals detected
in this story.
</div>

</div>""",
            unsafe_allow_html=True,
        )

        # =================================================
        # SCORE
        # =================================================

        st.markdown(
            f"""<div class="score-card">

<div class="score-label">
NEWSLENS PRESENTATION SCORE
</div>

<div class="score-number">
{overall_score}
<span>/100</span>
</div>

<div class="score-text">
Higher scores indicate a more restrained
presentation.
</div>

</div>""",
            unsafe_allow_html=True,
        )

        st.progress(
            overall_score / 100
        )

        # =================================================
        # METRICS
        # =================================================

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.markdown(
                f"""<div class="metric">

<div class="metric-label">
TONE
</div>

<div class="metric-value">
{html.escape(tone)}
</div>

<div class="metric-sub">
{tone_confidence}% confidence
</div>

</div>""",
                unsafe_allow_html=True,
            )

        with col2:

            st.markdown(
                f"""<div class="metric">

<div class="metric-label">
CONTENT TYPE
</div>

<div class="metric-value"
style="font-size:17px;">
{html.escape(content_type)}
</div>

<div class="metric-sub">
Classification
</div>

</div>""",
                unsafe_allow_html=True,
            )

        with col3:

            st.markdown(
                f"""<div class="metric">

<div class="metric-label">
SENSATIONALISM
</div>

<div class="metric-value">
{html.escape(sensational_label)}
</div>

<div class="metric-sub">
{sensational_score}/100 signal score
</div>

</div>""",
                unsafe_allow_html=True,
            )

        with col4:

            st.markdown(
                f"""<div class="metric">

<div class="metric-label">
EMOTIONAL FRAMING
</div>

<div class="metric-value"
style="font-size:16px;">
{html.escape(emotion_label)}
</div>

<div class="metric-sub">
{emotion_score}/100 signal score
</div>

</div>""",
                unsafe_allow_html=True,
            )

        # =================================================
        # EXPLANATION
        # =================================================

        st.markdown(
            """<div class="section">

<div class="section-small">
EXPLAINABILITY
</div>

<div class="section-title">
🧠 Why did NewsLens flag this?
</div>

</div>""",
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""<div class="insight">
{html.escape(explanation)}
</div>""",
            unsafe_allow_html=True,
        )

        # =================================================
        # SIGNALS
        # =================================================

        st.markdown(
            """<div class="section">

<div class="section-title">
Signals detected
</div>

</div>""",
            unsafe_allow_html=True,
        )

        signal_col, breakdown_col = st.columns(2)

        # -------------------------------------------------
        # LOADED LANGUAGE
        # -------------------------------------------------

        with signal_col:

            if loaded_words:

                tags = ""

                for word in loaded_words:

                    tags += (
                        '<span class="signal-tag">'
                        + html.escape(word)
                        + "</span>"
                    )

                st.markdown(
                    f"""<div class="signal-box">

<div class="signal-title">
🚨 Potentially loaded language
</div>

{tags}

</div>""",
                    unsafe_allow_html=True,
                )

            else:

                st.markdown(
                    """<div class="signal-box">

<div class="signal-title">
✓ Language signals
</div>

<div style="
color:#7b879a;
font-size:13px;
line-height:1.6;
">
No major sensational keywords
were detected.
</div>

</div>""",
                    unsafe_allow_html=True,
                )

        # -------------------------------------------------
        # BREAKDOWN
        # -------------------------------------------------

        with breakdown_col:

            st.markdown(
                """<div class="signal-box">

<div class="signal-title">
📊 Signal breakdown
</div>

</div>""",
                unsafe_allow_html=True,
            )

            st.write("Positive language")

            st.progress(
                min(pos / 5, 1.0)
            )

            st.write("Negative language")

            st.progress(
                min(neg / 5, 1.0)
            )

            st.write("Sensationalism")

            st.progress(
                sensational_score / 100
            )

            st.write("Emotional framing")

            st.progress(
                emotion_score / 100
            )

        # =================================================
        # CLAIMS
        # =================================================

        st.markdown(
            """<div class="section">

<div class="section-small">
EXTRACTED INFORMATION
</div>

<div class="section-title">
📌 Potential factual claims
</div>

<div class="section-description">
Statements identified as candidates
for verification.
</div>

</div>""",
            unsafe_allow_html=True,
        )

        if claims:

            for index, claim in enumerate(
                claims,
                start=1,
            ):

                st.markdown(
                    f"""<div class="claim">

<div class="claim-label">
CLAIM {index:02d}
</div>

<div class="claim-text">
{html.escape(claim)}
</div>

</div>""",
                    unsafe_allow_html=True,
                )

            st.caption(
                "Claim extraction identifies statements "
                "that may contain checkable information. "
                "Extraction alone does not establish truth."
            )

        else:

            st.info(
                "No obvious factual claims were extracted "
                "from this text."
            )

        # =================================================
        # VERIFICATION
        # =================================================

        st.markdown(
            """<div class="section">

<div class="section-small">
PHASE 2 EVIDENCE LAYER
</div>

<div class="section-title">
🔎 Claim verification
</div>

<div class="section-description">
Evidence-assisted analysis using
live web sources.
</div>

</div>""",
            unsafe_allow_html=True,
        )

        if verification_error:

            st.error(
                "Verification unavailable: "
                + verification_error
            )

        elif verification_result:

            verification_score = verification_result.get(
                "overall_score",
                0
            )

            claim_count = verification_result.get(
                "claim_count",
                0
            )

            st.markdown(
                f"""<div class="verification-summary">

<div class="verification-label">
OVERALL VERIFICATION SCORE
</div>

<div class="verification-score">
{verification_score}/100
</div>

<div class="verification-label">
{claim_count}
checkable claim(s) analyzed
</div>

</div>""",
                unsafe_allow_html=True,
            )

            verification_claims = (
                verification_result.get(
                    "claims",
                    []
                )
            )

            for index, result in enumerate(
                verification_claims,
                start=1,
            ):

                verdict = result.get(
                    "verdict",
                    "UNVERIFIED"
                )

                confidence = result.get(
                    "confidence",
                    0
                )

                claim = result.get(
                    "claim",
                    ""
                )

                # -----------------------------------------
                # VERDICT BADGE
                # -----------------------------------------

                if verdict == "SUPPORTED":

                    badge = (
                        '<span class="status-supported">'
                        '✓ SUPPORTED'
                        '</span>'
                    )

                elif verdict == "PARTIALLY_SUPPORTED":

                    badge = (
                        '<span class="status-partial">'
                        '⚠ PARTIALLY SUPPORTED'
                        '</span>'
                    )

                elif verdict == "CONTRADICTED":

                    badge = (
                        '<span class="status-contradicted">'
                        '✕ CONTRADICTED'
                        '</span>'
                    )

                else:

                    badge = (
                        '<span class="status-unverified">'
                        '? UNVERIFIED'
                        '</span>'
                    )

                st.markdown(
                    f"""<div class="verification-card">

<div class="claim-label">
CLAIM {index:02d}
</div>

<div style="
color:#d5dce7;
font-size:14px;
line-height:1.65;
margin:10px 0 16px 0;
">
{html.escape(claim)}
</div>

{badge}

<span style="
color:#69758a;
font-size:11px;
margin-left:8px;
">
{confidence}% confidence
</span>

</div>""",
                    unsafe_allow_html=True,
                )

                # -----------------------------------------
                # EVIDENCE
                # -----------------------------------------

                evidence = result.get(
                    "evidence",
                    []
                )

                if evidence:

                    with st.expander(
                        f"View evidence · "
                        f"{len(evidence)} source(s)"
                    ):

                        for source in evidence:

                            title = source.get(
                                "title",
                                "Source"
                            )

                            url = source.get(
                                "url",
                                ""
                            )

                            content = source.get(
                                "content",
                                ""
                            )

                            score = source.get(
                                "search_score",
                                0
                            )

                            st.markdown(
                                f"**{html.escape(title)}**"
                            )

                            if content:

                                st.write(
                                    content[:700]
                                )

                            st.caption(
                                f"Search relevance: "
                                f"{score:.2f}"
                            )

                            if url:

                                st.markdown(
                                    f"[↗ Open source]({url})"
                                )

                            st.divider()

        # =================================================
        # DISCLAIMER
        # =================================================

        st.markdown(
            """<div class="footer">

NewsLens provides evidence-assisted
claim verification using live web sources.

<br>

Results are informational and should be
independently checked.

</div>""",
            unsafe_allow_html=True,
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """<div class="footer">

NewsLens • AI-assisted media literacy
and information analysis

<br>

Built for clearer, more critical news consumption.

</div>""",
    unsafe_allow_html=True,
)