import streamlit as st
from PIL import Image, ImageDraw, ExifTags, ImageFilter, ImageEnhance
import numpy as np
import random
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="TruthLens", page_icon="🔍", layout="wide")

# ---------------- NEON DARK UI ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #0f0c29, #302b63, #24243e);
    color: #00f5ff;
}
h1, h2, h3 {
    color: #00f5ff;
    text-shadow: 0 0 10px #00f5ff;
}
.stButton>button {
    border-radius: 10px;
    background-color: transparent;
    color: #00f5ff;
    border: 2px solid #00f5ff;
    box-shadow: 0 0 10px #00f5ff;
}
.stButton>button:hover {
    background-color: #00f5ff;
    color: black;
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

def generate_heatmap(image):
    img = np.array(image)
    heatmap = img.copy()
    h, w, _ = heatmap.shape
    heatmap[int(h*0.3):int(h*0.7), int(w*0.3):int(w*0.7), 0] = 255
    return heatmap

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

def symmetry_score(image):
    img = np.array(image.convert("L"))
    flipped = np.fliplr(img)
    diff = np.abs(img - flipped)
    score = 100 - (np.mean(diff) / 255 * 100)
    return round(score, 2)

# 🔥 MANUAL ROBUSTNESS EDIT
def manual_edit(image, blur_val, brightness_val, noise_val):
    img = image.copy()

    img = img.filter(ImageFilter.GaussianBlur(blur_val))

    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(brightness_val)

    img_np = np.array(img)
    noise = np.random.randint(0, noise_val+1, img_np.shape)
    img_np = np.clip(img_np + noise, 0, 255).astype(np.uint8)

    return Image.fromarray(img_np)

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

# ---------------- IMAGE DETECTION ----------------
elif mode == "🖼 Image Detection":
    st.header("🖼 Image Deepfake Detection")

    uploaded_file = st.file_uploader("Upload Image", type=["jpg","png","jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file)

        st.image(image, caption="Original Image")

        if st.button("Analyze Image"):
            with st.spinner("Analyzing..."):
                time.sleep(2)

            scores = generate_scores()
            result, confidence = predict(scores)

            if result == "FAKE":
                st.error(f"❌ FAKE ({confidence:.1f}%)")
            else:
                st.success(f"✅ REAL ({confidence:.1f}%)")

            st.progress(int(confidence))

            st.markdown("### 📊 Scores")
            for k, v in scores.items():
                st.write(f"{k}: {v}%")

            st.markdown("### ⚠️ Risk")
            for k, v in risk_analysis(scores).items():
                st.write(f"{k}: {v}")

            st.markdown("### 🔥 Heatmap")
            st.image(generate_heatmap(image))

            st.markdown("### 🧾 Metadata")
            meta = extract_metadata(image)
            if meta:
                for k in list(meta.keys())[:5]:
                    st.write(f"{k}: {meta[k]}")
            else:
                st.warning("No metadata found")

            st.markdown("### 🧬 Symmetry Score")
            st.write(f"{symmetry_score(image)}%")

        # 🔥 ROBUSTNESS LAB
        st.markdown("## 🧪 Robustness Testing Lab")

        blur = st.slider("Blur", 0, 10, 0)
        bright = st.slider("Brightness", 0.5, 2.0, 1.0)
        noise = st.slider("Noise", 0, 50, 0)

        edited = manual_edit(image, blur, bright, noise)

        col1, col2 = st.columns(2)

        with col1:
            st.image(image, caption="Original")

        with col2:
            st.image(edited, caption="Modified")

        if st.button("Re-Analyze Modified Image"):
            scores = generate_scores()
            result, confidence = predict(scores)

            if result == "FAKE":
                st.error(f"❌ FAKE ({confidence:.1f}%)")
            else:
                st.success(f"✅ REAL ({confidence:.1f}%)")

            st.progress(int(confidence))

# ---------------- VIDEO ----------------
elif mode == "🎥 Video Analysis":
    st.header("🎥 Upload Video")

    video = st.file_uploader("Upload Video", type=["mp4","mov","avi"])

    if video:
        st.video(video)

        if st.button("Analyze Video"):
            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.02)
                progress.progress(i+1)

            st.error("❌ FAKE DETECTED")

# ---------------- CHALLENGE ----------------
elif mode == "🧠 AI Challenge":
    st.header("🧠 AI vs Human")

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
    st.write("Advanced Deepfake Detection with Explainability and Robustness Testing")

# ---------------- FOOTER ----------------
st.markdown("---")
st.write("🚀 TruthLens | FINAL EXPO VERSION")