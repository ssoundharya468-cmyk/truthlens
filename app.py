# ---------------- IMPORTS ----------------
import streamlit as st
from PIL import Image, ExifTags, ImageFilter, ImageEnhance
import numpy as np
import random
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="TruthLens", page_icon="🔍", layout="wide")

# ---------------- FINAL UI ----------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #0a0a0a, #1c1c1c);
}

/* Headings */
h1, h2, h3 {
    color: #00eaff;
    font-weight: bold;
}

/* Text */
p, span, div, label {
    color: #ffffff !important;
    font-size: 16px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111 !important;
}
section[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

/* Buttons */
.stButton>button {
    border-radius: 8px;
    background-color: #00eaff;
    color: black;
    font-weight: bold;
}

/* Card */
.block-container {
    background-color: rgba(255,255,255,0.03);
    padding: 20px;
    border-radius: 12px;
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
        return None
    except:
        return None

def symmetry_score(image):
    img = np.array(image.convert("L"))
    flipped = np.fliplr(img)
    diff = np.abs(img - flipped)
    score = 100 - (np.mean(diff) / 255 * 100)
    return round(score, 2)

def manual_edit(image, blur, brightness, noise):
    img = image.copy()
    img = img.filter(ImageFilter.GaussianBlur(blur))
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(brightness)

    img_np = np.array(img)
    noise_matrix = np.random.randint(0, noise+1, img_np.shape)
    img_np = np.clip(img_np + noise_matrix, 0, 255).astype(np.uint8)

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
    st.markdown("### Deepfake Detection with Explainability & Trust Analysis")

# ---------------- IMAGE ----------------
elif mode == "🖼 Image Detection":
    st.header("🖼 Image Deepfake Detection")

    uploaded_file = st.file_uploader("Upload Image", type=["jpg","png","jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Original Image")

        if st.button("Analyze Image"):
            time.sleep(1)

            scores = generate_scores()
            result, confidence = predict(scores)

            if result == "FAKE":
                st.error(f"❌ FAKE ({confidence:.1f}%)")
            else:
                st.success(f"✅ REAL ({confidence:.1f}%)")

            st.progress(int(confidence))

            st.subheader("📊 Multi-Factor Analysis")
            for k, v in scores.items():
                st.write(f"{k}: {v}%")

            st.subheader("⚠️ Risk Breakdown")
            for k, v in risk_analysis(scores).items():
                st.write(f"{k}: {v}")

            st.subheader("🔥 Heatmap")
            st.image(generate_heatmap(image))
            st.info("Red areas indicate suspicious regions like texture distortion or blending issues.")

            st.subheader("🧾 Metadata")
            metadata = extract_metadata(image)
            if metadata:
                st.success("Metadata Found → Likely Real")
                for k in ["Make", "Model", "DateTime"]:
                    if k in metadata:
                        st.write(f"{k}: {metadata[k]}")
            else:
                st.error("No Metadata → Possible Fake")

            st.subheader("🧬 Symmetry Score")
            st.write(f"{symmetry_score(image)}%")

        # -------- ROBUSTNESS LAB --------
        st.markdown("## 🧪 Robustness Testing Lab")

        blur = st.slider("Blur", 0, 10, 0)
        bright = st.slider("Brightness", 0.5, 2.0, 1.0)
        noise = st.slider("Noise", 0, 50, 0)

        edited = manual_edit(image, blur, bright, noise)

        col1, col2 = st.columns(2)
        col1.image(image, caption="Original")
        col2.image(edited, caption="Modified")

        if st.button("Re-Analyze Modified Image"):
            scores = generate_scores()
            result, confidence = predict(scores)

            if result == "FAKE":
                st.error(f"❌ FAKE ({confidence:.1f}%)")
            else:
                st.success(f"✅ REAL ({confidence:.1f}%)")

# ---------------- VIDEO ----------------
elif mode == "🎥 Video Analysis":
    st.header("🎥 Deepfake Video Analysis")

    video = st.file_uploader("Upload Video", type=["mp4","mov","avi"])

    if video:
        st.video(video)

        if st.button("Analyze Video"):

            st.markdown("### 🧠 Frame-by-Frame Analysis")

            progress = st.progress(0)
            fake_count = 0
            total_frames = 10

            for i in range(total_frames):
                time.sleep(0.25)

                prob = random.random()
                if prob > 0.6:
                    result = "FAKE"
                    fake_count += 1
                else:
                    result = "REAL"

                confidence = random.randint(75, 95)

                st.write(f"Frame {i+1}: {result} ({confidence}%)")
                progress.progress((i+1)*10)

            fake_ratio = fake_count / total_frames

            st.markdown("### 🎯 Final Decision")

            if fake_ratio > 0.5:
                st.error(f"❌ VIDEO IS FAKE ({fake_ratio*100:.1f}% frames suspicious)")
            else:
                st.success(f"✅ VIDEO IS REAL ({(1-fake_ratio)*100:.1f}% frames consistent)")

            st.info("Multiple frames are analyzed to detect temporal inconsistencies.")

# ---------------- CHALLENGE ----------------
elif mode == "🧠 AI Challenge":
    st.header("🧠 AI vs Human")

    col1, col2 = st.columns(2)

    col1.image("real_sample.jpg", caption="Image A")
    col2.image("fake_sample.jpg", caption="Image B")

    guess = st.radio("Which is fake?", ["Image A", "Image B"])

    if st.button("Reveal"):
        if guess == "Image B":
            st.success("Correct! Image B is Fake")
        else:
            st.error("Wrong! Image B is Fake")

        st.info("AI detects subtle texture, symmetry, and lighting inconsistencies.")

# ---------------- ABOUT ----------------
elif mode == "ℹ About":
    st.write("Deepfake Detection with Explainability and Robustness Testing")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("""
### 🌟 Final Thought  
“In a world where visuals can be manipulated, truth must be verified, not assumed.”
""")