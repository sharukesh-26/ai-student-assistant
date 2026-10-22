import streamlit as st
import re
from datetime import datetime

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Student Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM DESIGN
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Main background */

.stApp {
    min-height: 100vh;

    background:
        radial-gradient(circle at 10% 10%, rgba(99, 102, 241, 0.22), transparent 30%),
        radial-gradient(circle at 90% 15%, rgba(168, 85, 247, 0.20), transparent 32%),
        radial-gradient(circle at 50% 90%, rgba(14, 165, 233, 0.18), transparent 35%),
        linear-gradient(135deg, #070b18 0%, #10152a 50%, #090d1c 100%);

    background-attachment: fixed;
    background-size: cover;

    color: white;
}

/* Make the main content area transparent */
[data-testid="stAppViewContainer"] {
    background: transparent !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

/* Hide Streamlit menu */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* Header */

.hero {
    text-align: center;
    padding: 35px 20px 20px 20px;
}

.hero-icon {
    font-size: 58px;
}

.hero-title {
    font-size: 42px;
    font-weight: 800;
    margin-top: 5px;
    margin-bottom: 8px;
    background: linear-gradient(90deg, #8b5cf6, #38bdf8, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    color: #cbd5e1;
    font-size: 17px;
}

/* Cards */

.glass-card {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 20px;
    padding: 22px;
    backdrop-filter: blur(14px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.25);
}

/* Chat messages */

.user-message {
    background: linear-gradient(
        135deg,
        rgba(99, 102, 241, 0.28),
        rgba(59, 130, 246, 0.18)
    );
    border: 1px solid rgba(129, 140, 248, 0.25);
    padding: 16px;
    border-radius: 18px 18px 5px 18px;
    margin: 12px 0 12px 12%;
}

.bot-message {
    background: rgba(255, 255, 255, 0.07);
    border: 1px solid rgba(255, 255, 255, 0.10);
    padding: 16px;
    border-radius: 18px 18px 18px 5px;
    margin: 12px 12% 12px 0;
}

/* Topic cards */

.topic-card {
    background: rgba(255,255,255,0.055);
    border: 1px solid rgba(255,255,255,0.10);
    padding: 15px;
    border-radius: 15px;
    text-align: center;
    min-height: 95px;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: rgba(5, 8, 20, 0.95);
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* Chat Input */

.stChatInputContainer {
    border-radius: 20px;
}

.stChatInputContainer textarea {
    color: #000000 !important;
    background-color: #ffffff !important;
}

.stChatInputContainer textarea::placeholder {
    color: #64748b !important;
    opacity: 1 !important;
}

.stChatInputContainer textarea:focus {
    color: #000000 !important;
}

/* Buttons */

.stButton > button {
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.12);
    background: rgba(255,255,255,0.07);
    color: white;
    font-weight: 600;
}

.stButton > button:hover {
    border-color: #8b5cf6;
    background: rgba(139,92,246,0.18);
}

/* Stats */

.stat-number {
    font-size: 28px;
    font-weight: 800;
}

.stat-label {
    color: #94a3b8;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# KNOWLEDGE BASE
# =========================================================

knowledge_base = {

    "python": {
        "keywords": ["python", "python language", "python programming"],
        "responses": [
            "Python is a high-level, interpreted programming language known for its simple and readable syntax. It is widely used in AI, Data Science, Machine Learning, automation and web development.",
            "Python is popular in AI&DS because it has powerful libraries such as NumPy, Pandas, Matplotlib and Scikit-learn. Its simple syntax also makes it beginner-friendly."
        ]
    },

    "machine learning": {
        "keywords": [
            "machine learning",
            "ml",
            "learn from data",
            "machines learn"
        ],
        "responses": [
            "Machine Learning is a branch of Artificial Intelligence where computers learn patterns from data and use those patterns to make predictions or decisions.",
            "In Machine Learning, we provide data to an algorithm so it can identify useful patterns. Common types include supervised learning, unsupervised learning and reinforcement learning."
        ]
    },

    "artificial intelligence": {
        "keywords": [
            "artificial intelligence",
            "what is ai",
            "what does ai mean",
            "ai"
        ],
        "responses": [
            "Artificial Intelligence, or AI, is a field of computing focused on creating systems that can perform tasks associated with human intelligence, such as learning, reasoning, understanding language and recognizing patterns.",
            "AI enables computers to perform intelligent tasks using techniques such as Machine Learning, Deep Learning, Natural Language Processing and Computer Vision."
        ]
    },

    "data science": {
        "keywords": [
            "data science",
            "data scientist",
            "what is data science"
        ],
        "responses": [
            "Data Science combines statistics, programming, mathematics and machine learning to extract useful insights from data.",
            "A Data Science workflow commonly includes collecting data, cleaning it, exploring patterns, visualizing results and building predictive models."
        ]
    },

    "nlp": {
        "keywords": [
            "nlp",
            "natural language processing",
            "language processing"
        ],
        "responses": [
            "Natural Language Processing, or NLP, is a branch of AI that enables computers to work with human language. Examples include chatbots, translation, sentiment analysis and text classification.",
            "NLP helps computers process human language. Tasks include tokenization, sentiment analysis, text classification, translation and question answering."
        ]
    },

    "deep learning": {
        "keywords": [
            "deep learning",
            "neural network",
            "neural networks"
        ],
        "responses": [
            "Deep Learning is a subset of Machine Learning that uses neural networks with multiple layers to learn complex patterns from data.",
            "Deep Learning is commonly used in image recognition, speech recognition, natural language processing and other tasks involving large and complex datasets."
        ]
    },

    "pandas": {
        "keywords": [
            "pandas",
            "python pandas",
            "dataframe"
        ],
        "responses": [
            "Pandas is a Python library used for data manipulation and analysis. Its DataFrame structure makes it easy to work with rows and columns of data.",
            "Pandas is commonly used to load datasets, clean missing values, filter records, analyze data and prepare datasets for Machine Learning."
        ]
    },

    "scikit learn": {
        "keywords": [
            "scikit learn",
            "sklearn",
            "scikit-learn"
        ],
        "responses": [
            "Scikit-learn is a Python library that provides Machine Learning algorithms for classification, regression, clustering, preprocessing and model evaluation.",
            "Scikit-learn makes it easier to build Machine Learning models in Python without implementing algorithms from scratch."
        ]
    },

    "streamlit": {
        "keywords": [
            "streamlit",
            "stream lit"
        ],
        "responses": [
            "Streamlit is a Python framework for creating interactive web applications, especially for Data Science and Machine Learning projects.",
            "With Streamlit, Python developers can turn data analysis or Machine Learning code into interactive web interfaces without needing to build a separate frontend."
        ]
    },

    "algorithm": {
        "keywords": [
            "algorithm",
            "algorithms"
        ],
        "responses": [
            "An algorithm is a finite sequence of well-defined steps used to solve a problem or complete a task.",
            "For example, a sorting algorithm provides a systematic process for arranging data in a particular order."
        ]
    },

    "classification": {
        "keywords": [
            "classification",
            "classification algorithm",
            "classify"
        ],
        "responses": [
            "Classification is a supervised Machine Learning technique used to predict a category or class. For example, an email classifier can predict whether a message is spam or not spam.",
            "Classification models work with discrete output categories. Examples include spam detection, disease-risk categories and image classification."
        ]
    },

    "regression": {
        "keywords": [
            "regression",
            "regression algorithm"
        ],
        "responses": [
            "Regression is a supervised Machine Learning technique used to predict continuous numerical values, such as house prices, sales or temperature.",
            "Unlike classification, regression produces a numerical output rather than a category."
        ]
    },

    "database": {
        "keywords": [
            "database",
            "databases",
            "dbms"
        ],
        "responses": [
            "A database is an organized collection of data that can be stored, retrieved, updated and managed efficiently.",
            "DBMS stands for Database Management System. It provides tools for creating, managing and accessing databases."
        ]
    },

    "computer vision": {
        "keywords": [
            "computer vision",
            "image recognition",
            "image processing"
        ],
        "responses": [
            "Computer Vision is a branch of AI that enables computers to interpret and analyze visual information such as images and videos.",
            "Computer Vision is used in applications such as face recognition, object detection, medical image analysis and autonomous systems."
        ]
    }
}

# =========================================================
# RESPONSE ENGINE
# =========================================================

def get_response(user_input):

    text = user_input.lower().strip()

    # Greetings
    if re.search(r"\b(hi|hello|hey|hii|hai|good morning|good evening)\b", text):
        return "Hello! 👋 I'm your AI Student Assistant. Ask me anything about AI, Machine Learning, Python or Data Science."

    # Thanks
    if any(word in text for word in ["thank you", "thanks", "thank"]):
        return "You're welcome! 😊 Keep learning and building amazing AI projects!"

    # Who are you?
    if "who are you" in text or "what are you" in text:
        return "I'm an AI Student Assistant built with Python and Streamlit. I'm designed to help students understand basic AI & Data Science concepts."

    # Help
    if "help" in text or "what can you do" in text:
        return """I can explain many AI & Data Science topics, including:

🤖 Artificial Intelligence
🧠 Machine Learning
📊 Data Science
🐍 Python
💬 NLP
🔬 Deep Learning
📈 Classification
📉 Regression
🐼 Pandas
⚙️ Scikit-learn
🌐 Streamlit
👁️ Computer Vision
🗄️ Databases
📚 Algorithms

Try asking me something specific!"""

    # Compare questions
    if "difference between" in text:

        if "ai" in text and "machine learning" in text:
            return """The main difference is:

🤖 Artificial Intelligence is the broader field of creating intelligent computer systems.

🧠 Machine Learning is a subset of AI where systems learn patterns from data.

In simple terms:

AI → The larger field
Machine Learning → One approach used to achieve AI"""

        if "classification" in text and "regression" in text:
            return """Classification predicts categories.

Example:
Spam → Yes / No

Regression predicts numerical values.

Example:
House price → ₹50,00,000

So:

Classification → Categorical output
Regression → Numerical output"""

    # Question-specific handling
    if "why" in text and "python" in text:
        return """Python is widely used in AI & Data Science because:

1. It has simple and readable syntax.
2. It has many AI and Data Science libraries.
3. It has a large developer community.
4. It supports rapid development.
5. It works well with data analysis and Machine Learning."""

    if "example" in text and "machine learning" in text:
        return """A simple Machine Learning example is spam detection.

The model can learn from previous emails labeled:

• Spam
• Not Spam

After learning patterns from these examples, it can classify a new email."""

    if "types" in text and "machine learning" in text:
        return """The three commonly discussed types of Machine Learning are:

1. Supervised Learning — learns from labeled data.
2. Unsupervised Learning — finds patterns in unlabeled data.
3. Reinforcement Learning — learns through rewards and penalties."""

    # Search knowledge base
    for topic, data in knowledge_base.items():

        for keyword in data["keywords"]:

            if keyword in text:

                # Select response based on question
                if "example" in text:
                    return data["responses"][0]

                if "why" in text:
                    return data["responses"][1]

                if "how" in text:
                    return data["responses"][1]

                return data["responses"][0]

    # Fallback
    return """I don't have a specific answer for that question yet. 🤔

Try asking about:

• Artificial Intelligence
• Machine Learning
• Python
• Data Science
• NLP
• Deep Learning
• Pandas
• Scikit-learn
• Streamlit
• Classification
• Regression
• Computer Vision

You can also ask questions like:
"What is Machine Learning?"
"Why is Python used in AI?"
"Give me an example of classification."
"What is the difference between AI and Machine Learning?"
"""

# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================================================
# HERO SECTION
# =========================================================

st.markdown("""
<div class="hero">

<div class="hero-icon">🤖</div>

<div class="hero-title">
AI Student Assistant
</div>

<div class="hero-subtitle">
Your intelligent learning companion for AI & Data Science
</div>

</div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🤖 AI Student Assistant")

    st.write(
        "A beginner-friendly educational chatbot "
        "for AI & Data Science students."
    )

    st.divider()

    st.markdown("### 📚 Topics")

    topics = [
        "🐍 Python",
        "🤖 Artificial Intelligence",
        "🧠 Machine Learning",
        "📊 Data Science",
        "💬 NLP",
        "🔬 Deep Learning",
        "📈 Classification",
        "📉 Regression",
        "🐼 Pandas",
        "⚙️ Scikit-learn",
        "👁️ Computer Vision"
    ]

    for topic in topics:
        st.write(topic)

    st.divider()

    st.markdown("### 📊 Project Stats")

    st.write("💬 Interactive chatbot")
    st.write("📚 14+ learning topics")
    st.write("⚡ Instant responses")
    st.write("🌐 Streamlit interface")

    st.divider()

    if st.button("🗑️ Clear Conversation", use_container_width=True):

        st.session_state.messages = []

        st.rerun()

# =========================================================
# WELCOME CARD
# =========================================================

if len(st.session_state.messages) == 0:

    st.markdown("""
    <div class="glass-card">

    <h3>👋 Welcome!</h3>

    <p>
    I'm here to help you understand Artificial Intelligence,
    Machine Learning and Data Science concepts.
    </p>

    <p>
    Ask me a question below to get started.
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # Suggested questions

    st.markdown("### 💡 Try asking")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("""
        <div class="topic-card">
        🧠<br>
        <b>What is Machine Learning?</b>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div class="topic-card">
        🐍<br>
        <b>Why is Python used in AI?</b>
        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown("""
        <div class="topic-card">
        🤖<br>
        <b>What is Artificial Intelligence?</b>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f"""
            <div class="user-message">
            👤 <b>You</b><br><br>
            {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="bot-message">
            🤖 <b>AI Assistant</b><br><br>
            {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# CHAT INPUT
# =========================================================

user_input = st.chat_input(
    "Ask me anything about AI & Data Science..."
)

if user_input:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    response = get_response(user_input)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    st.rerun()

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    f"""
    <div style="text-align:center; color:#64748b;">
    🤖 AI Student Assistant &nbsp;•&nbsp;
    Built with Python + Streamlit &nbsp;•&nbsp;
    {datetime.now().year}
    </div>
    """,
    unsafe_allow_html=True
)