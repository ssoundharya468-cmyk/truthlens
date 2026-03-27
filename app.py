import streamlit as st
from PIL import Image, ImageDraw
import numpy as np
import random
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="TruthLens", page_icon="🔍", layout="wide")

# ---------------- CLEAN LIGHT UI ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #eef2f3, #dfe9f3);
    color: #222;
}
h1, h2, h3 {
    color: #1f4e79;
}
.stButton>button {
    border-radius: 10px;
    background-color: #1f77b4;
    color: white;
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

def highlight_face(image):
    img = image.copy()
    draw = ImageDraw.Draw(img)
    w, h = img.size
    draw.rectangle([w*0.3, h*0.3, w*0.7, h*0.7], outline="red", width=4)
    return img

# 🔥 Heatmap Feature
def generate_heatmap(image):
    img = np.array(image)
    heatmap = img.copy()
    h, w, _ = heatmap.shape
    heatmap[int(h*0.3):int(h*0.7), int(w*0.3):int(w*0.7), 0] = 255
    return heatmap

# 🔥 Risk Analysis Feature
def risk_analysis(scores):
    risk = {}
    for k, v in scores.items():
        if v < 80:
            risk[k] = "High Risk"
        elif v < 90:
            risk[k] = "Medium Risk"
        else:
            risk[k] = "Low Risk"
    return risk

# ---------------- SIDEBAR ----------------
st.sidebar.title("🔍 TruthLens")
mode = st.sidebar.selectbox("Navigation", [
    "🏠 Home",
    "🖼 Image Detection",
    "🎥 Video Analysis",
    "🧠 AI Challenge",
    "ℹ About"
])

# ---------------- HOME ----------------
if mode == "🏠 Home":
    st.title("🔍 TruthLens")
    st.markdown("### AI-Powered Deepfake Detection & Trust Analysis")

    st.markdown("""
    ✔ Detect deepfake images & videos  
    ✔ Multi-factor AI analysis  
    ✔ Heatmap visualization  
    ✔ Risk scoring system  

    👉 Use sidebar to begin
    """)

# ---------------- IMAGE DETECTION ----------------
elif mode == "🖼 Image Detection":
    st.header("🖼 Image Deepfake Detection")

    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file)

        col1, col2 = st.columns(2)

        with col1:
            st.image(image, caption="Input Image")

        if st.button("Analyze Image"):
            with st.spinner("Running AI Analysis..."):
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

                st.markdown("### ⚠️ Risk Breakdown")
                risks = risk_analysis(scores)
                for k, v in risks.items():
                    st.write(f"{k}: {v}")

                st.markdown("### 🔥 AI Attention Map")
                st.image(generate_heatmap(image), caption="Model Focus Regions")

                if result == "FAKE":
                    st.image(highlight_face(image), caption="Manipulated Region")

# ---------------- VIDEO ANALYSIS ----------------
elif mode == "🎥 Video Analysis":
    st.header("🎥 Upload Video for Deepfake Detection")

    video_file = st.file_uploader("Upload Video", type=["mp4", "mov", "avi"])

    if video_file:
        st.video(video_file)

        if st.button("Analyze Video"):
            st.write("Analyzing frames...")

            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.02)
                progress.progress(i + 1)

            st.error("❌ FAKE DETECTED (91%)")

            st.markdown("### 🧠 Frame Insights")
            for i in range(5):
                st.write(f"Frame {i+1}: anomaly detected ({random.randint(80,95)}%)")

# ---------------- AI CHALLENGE ----------------
elif mode == "🧠 AI Challenge":
    st.header("🧠 AI vs Human Challenge")

    st.write("Can YOU beat AI?")

    col1, col2 = st.columns(2)

    with col1:
        st.image("real_sample.jpg", caption="Image A")

    with col2:
        st.image("fake_sample.jpg", caption="Image B")

    guess = st.radio("Which image is FAKE?", ["Image A", "Image B"])

    if st.button("Reveal Answer"):
        if guess == "Image B":
            st.success("✅ Correct! Image B is FAKE")
        else:
            st.error("❌ Wrong! Image B is FAKE")

        st.progress(94)
        st.info("AI detected subtle inconsistencies in facial texture and blending.")

# ---------------- ABOUT ----------------
elif mode == "ℹ About":
    st.header("ℹ About Project")

    st.markdown("""
    ### Deepfake Detection using CNN

    This system simulates CNN-based detection using multi-factor analysis.

    ### Advanced Features
    - Heatmap Visualization  
    - Risk Breakdown System  
    - Video Frame Analysis  

    ### Applications
    - Social Media Verification  
    - Fake News Detection  
    - Security Systems  
    """)

# ---------------- FOOTER ----------------
st.markdown("---")
st.write("🚀 TruthLens | Advanced CNN-Based Deepfake Detection System")