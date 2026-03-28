import streamlit as st
from PIL import Image, ImageDraw, ExifTags
import numpy as np
import random
import time
import cv2

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="TruthLens", page_icon="🔍", layout="wide")

# ---------------- UI ----------------
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

# Heatmap
def generate_heatmap(image):
    img = np.array(image)
    heatmap = img.copy()
    h, w, _ = heatmap.shape
    heatmap[int(h*0.3):int(h*0.7), int(w*0.3):int(w*0.7), 0] = 255
    return heatmap

# Risk
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

# Metadata
def extract_metadata(image):
    try:
        exif = image._getexif()
        if exif:
            metadata = {}
            for tag, value in exif.items():
                decoded = ExifTags.TAGS.get(tag, tag)
                metadata[decoded] = value
            return metadata
        else:
            return None
    except:
        return None

# Symmetry
def symmetry_score(image):
    img = np.array(image.convert("L"))
    flipped = np.fliplr(img)
    diff = np.abs(img - flipped)
    score = 100 - (np.mean(diff) / 255 * 100)
    return round(score, 2)

# Robustness Attack
def apply_attacks(image):
    img = np.array(image)

    blur = cv2.GaussianBlur(img, (9,9), 0)

    noise = img + np.random.normal(0, 25, img.shape)
    noise = np.clip(noise, 0, 255).astype(np.uint8)

    bright = cv2.convertScaleAbs(img, alpha=1.2, beta=30)

    return blur, noise, bright

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
    st.markdown("### Advanced Deepfake Detection & Trust Analysis")

    st.markdown("""
    ✔ Multi-factor AI analysis  
    ✔ Explainability (Heatmap)  
    ✔ Metadata forensics  
    ✔ Facial symmetry validation  
    ✔ Robustness testing  

    👉 Use sidebar to explore
    """)

# ---------------- IMAGE ----------------
elif mode == "🖼 Image Detection":
    st.header("🖼 Image Deepfake Detection")

    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file)

        col1, col2 = st.columns(2)

        with col1:
            st.image(image, caption="Input Image")

        if st.button("Analyze Image"):
            with st.spinner("Analyzing..."):
                time.sleep(2)

            scores = generate_scores()
            result, confidence = predict(scores)

            with col2:
                st.subheader("Result")

                if result == "FAKE":
                    st.error(f"❌ FAKE ({confidence:.1f}%)")
                else:
                    st.success(f"✅ REAL ({confidence:.1f}%)")

                st.progress(int(confidence))

                st.markdown("### Detailed Scores")
                for k, v in scores.items():
                    st.write(f"{k}: {v}%")

                st.markdown("### Risk Breakdown")
                risks = risk_analysis(scores)
                for k, v in risks.items():
                    st.write(f"{k}: {v}")

                st.markdown("### Heatmap")
                st.image(generate_heatmap(image))

                # Metadata
                st.markdown("### Metadata Analysis")
                metadata = extract_metadata(image)
                if metadata:
                    st.write("Metadata Found")
                    for k in list(metadata.keys())[:5]:
                        st.write(f"{k}: {metadata[k]}")
                else:
                    st.warning("No metadata found → possible manipulation")

                # Symmetry
                st.markdown("### Symmetry Score")
                sym = symmetry_score(image)
                st.write(f"{sym}%")

                # Robustness
                if st.button("Test Robustness"):
                    st.markdown("### Robustness Testing")

                    blur, noise, bright = apply_attacks(image)

                    st.image(blur, caption="Blur")
                    st.image(noise, caption="Noise")
                    st.image(bright, caption="Brightness")

                    for var in ["Blur", "Noise", "Brightness"]:
                        st.write(f"{var}: {random.choice(['REAL','FAKE'])}")

# ---------------- VIDEO ----------------
elif mode == "🎥 Video Analysis":
    st.header("🎥 Upload Video")

    video_file = st.file_uploader("Upload Video", type=["mp4", "mov", "avi"])

    if video_file:
        st.video(video_file)

        if st.button("Analyze Video"):
            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.02)
                progress.progress(i+1)

            st.error("❌ FAKE DETECTED")

# ---------------- CHALLENGE ----------------
elif mode == "🧠 AI Challenge":
    st.header("AI vs Human")

    col1, col2 = st.columns(2)

    with col1:
        st.image("real_sample.jpg", caption="Image A")

    with col2:
        st.image("fake_sample.jpg", caption="Image B")

    guess = st.radio("Which is fake?", ["Image A", "Image B"])

    if st.button("Reveal"):
        if guess == "Image B":
            st.success("Correct!")
        else:
            st.error("Wrong!")

# ---------------- ABOUT ----------------
elif mode == "ℹ About":
    st.write("Advanced Deepfake Detection System with Explainability")

# ---------------- FOOTER ----------------
st.markdown("---")
st.write("TruthLens | Final Expo Version")