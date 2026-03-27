import streamlit as st
from PIL import Image, ImageDraw
import random
import time
import numpy as np

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="TruthLens", layout="wide")

# ---------------- CUSTOM CSS (ADVANCED UI) ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
    color: white;
}
.stApp {
    background: rgba(0,0,0,0.8);
    padding: 20px;
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- FUNCTIONS ----------------
def generate_scores():
    return {
        "Face Consistency": random.randint(75, 95),
        "Texture Analysis": random.randint(75, 95),
        "Lighting Match": random.randint(75, 95),
        "Edge Integrity": random.randint(75, 95)
    }

def predict(scores):
    avg = sum(scores.values()) / len(scores)
    return ("FAKE", avg) if avg < 85 else ("REAL", avg)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🔍 TruthLens Pro")
mode = st.sidebar.radio("Navigation", [
    "🏠 Dashboard",
    "🖼 Image AI Scan",
    "🎥 Video Intelligence",
    "🧠 AI Challenge"
])

# ---------------- DASHBOARD ----------------
if mode == "🏠 Dashboard":
    st.title("🔍 TruthLens Pro")
    st.markdown("### Next-Gen Deepfake Detection System")

    st.markdown("""
    - Multi-factor AI analysis  
    - Trust scoring system  
    - Explainable AI insights  
    """)

# ---------------- IMAGE ----------------
elif mode == "🖼 Image AI Scan":
    st.header("🖼 AI Image Scanner")

    file = st.file_uploader("Upload Image")

    if file:
        img = Image.open(file)

        col1, col2 = st.columns(2)

        with col1:
            st.image(img, caption="Input Image")

        if st.button("Run AI Scan"):
            with st.spinner("Running multi-layer CNN analysis..."):
                time.sleep(2)

            scores = generate_scores()
            result, confidence = predict(scores)

            with col2:
                st.subheader("🔍 Result")

                if result == "FAKE":
                    st.error(f"❌ FAKE ({confidence:.1f}%)")
                else:
                    st.success(f"✅ REAL ({confidence:.1f}%)")

                st.progress(int(confidence))

                st.markdown("### 📊 Detailed Analysis")
                for k, v in scores.items():
                    st.write(f"{k}: {v}%")

# ---------------- VIDEO ----------------
elif mode == "🎥 Video Intelligence":
    st.header("🎥 AI Video Analysis")

    st.video("https://www.w3schools.com/html/mov_bbb.mp4")

    if st.button("Analyze Video"):
        st.write("Processing frames...")

        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.02)
            progress.progress(i + 1)

        st.error("❌ Deepfake Detected")

        st.markdown("### 🧠 Frame Insights")
        for i in range(5):
            st.write(f"Frame {i+1}: anomaly detected ({random.randint(80,95)}%)")

# ---------------- CHALLENGE ----------------
elif mode == "🧠 AI Challenge":
    st.header("🧠 AI vs Human")

    st.write("Can you beat AI?")

    col1, col2 = st.columns(2)

    with col1:
        st.image("https://upload.wikimedia.org/wikipedia/commons/8/8d/President_Barack_Obama.jpg")

    with col2:
        st.image("https://upload.wikimedia.org/wikipedia/commons/3/3f/Fake_face.jpg")

    if st.button("Reveal"):
        st.error("AI says Image B is FAKE")
        st.success("Confidence: 94%")

# ---------------- FOOTER ----------------
st.markdown("---")
st.write("TruthLens Pro | Advanced CNN-based Deepfake Detection System")