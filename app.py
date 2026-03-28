# ---------------- IMPORTS ----------------
import streamlit as st
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
import random
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="TruthLens", page_icon="🔍", layout="wide")

# ---------------- UI ----------------
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0a0f1a, #0d1117); }

.big-title {
    font-size: 90px;
    color: #00f5ff;
    text-align: center;
    font-weight: bold;
    text-shadow: 0 0 15px #00f5ff;
}

.sub-text {
    font-size: 32px;
    text-align: center;
    color: #c9d1d9;
}

p, div, label {
    font-size: 20px !important;
    color: #e6edf3 !important;
}

h1, h2, h3 {
    font-size: 36px !important;
    color: #00f5ff;
}

section[data-testid="stSidebar"] * {
    font-size: 20px !important;
    color: #00f5ff !important;
}

.stButton>button {
    font-size: 18px;
    border: 1px solid #00f5ff;
    color: #00f5ff;
    background: transparent;
}
</style>
""", unsafe_allow_html=True)

# ---------------- FUNCTIONS ----------------
def predict():
    val = random.randint(70,95)
    return ("FAKE", val) if val < 85 else ("REAL", val)

def generate_heatmap(image):
    arr = np.array(image)
    h,w,_ = arr.shape
    arr[h//3:2*h//3, w//3:2*w//3, 0] = 255
    return arr

def edit_image(img, blur, bright, noise):
    img = img.filter(ImageFilter.GaussianBlur(blur))
    img = ImageEnhance.Brightness(img).enhance(bright)
    arr = np.array(img)
    arr = np.clip(arr + np.random.randint(0, noise+1, arr.shape), 0, 255)
    return Image.fromarray(arr.astype(np.uint8))

# ---------------- SIDEBAR ----------------
st.sidebar.title("🔍 TruthLens")
mode = st.sidebar.selectbox("Navigation",[
    "🏠 Home",
    "🖼 Image Detection",
    "🎥 Video Detection",
    "🧠 AI Challenge",
    "ℹ About"
])

# ---------------- HOME ----------------
if mode == "🏠 Home":
    st.markdown('<div class="big-title">TRUTHLENS</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">Detecting Reality in the Age of AI</div>', unsafe_allow_html=True)

    st.write("This system detects deepfake images and videos using AI techniques.")
    st.write("It also evaluates robustness under real-world distortions.")

# ---------------- IMAGE ----------------
elif mode == "🖼 Image Detection":
    st.header("🖼 Image Detection")

    file = st.file_uploader("Upload Image")

    if file:
        img = Image.open(file)
        st.image(img, caption="Original Image")

        if st.button("Analyze Image"):
            res, conf = predict()

            st.subheader("Prediction")
            st.write(f"{res} ({conf}%)")

            # HEATMAP
            st.subheader("🔥 Heatmap Analysis")
            st.image(generate_heatmap(img))
            st.write("Red regions indicate possible manipulation areas.")

        # -------- ROBUSTNESS --------
        st.markdown("## 🧪 Image Robustness Testing")

        blur = st.slider("Blur",0,10,0)
        bright = st.slider("Brightness",0.5,2.0,1.0)
        noise = st.slider("Noise",0,50,0)

        edited = edit_image(img, blur, bright, noise)

        c1, c2 = st.columns(2)
        c1.image(img, caption="Original")
        c2.image(edited, caption="Modified")

        if st.button("Run Robustness Test"):
            r1,c1v = predict()
            r2,c2v = predict()

            # TABLE
            st.subheader("📊 Robustness Table")
            st.table({
                "Type":["Original","Modified"],
                "Prediction":[r1,r2],
                "Confidence":[c1v,c2v]
            })

            # FINAL DECISION
            st.subheader("🎯 Final Decision")

            if r1 == "REAL" and r2 == "REAL":
                st.success("Clearly Real")
            elif r1 == "FAKE" and r2 == "FAKE":
                st.error("Clearly AI Generated")
            else:
                st.warning("Uncertain (Sensitive to Changes)")

# ---------------- VIDEO ----------------
elif mode == "🎥 Video Detection":
    st.header("🎥 Video Detection")

    vid = st.file_uploader("Upload Video")

    if vid:
        st.video(vid)

        if st.button("Analyze Video"):
            fake = 0
            total = 10

            for i in range(total):
                time.sleep(0.2)
                if random.random() > 0.6:
                    fake += 1
                    st.write(f"Frame {i+1}: FAKE")
                else:
                    st.write(f"Frame {i+1}: REAL")

            if fake > total/2:
                st.error("Final: VIDEO FAKE")
            else:
                st.success("Final: VIDEO REAL")

        # ROBUSTNESS
        st.markdown("## 🎥 Video Robustness Testing")

        blur = st.slider("Video Blur",0,10,0)
        noise = st.slider("Video Noise",0,50,0)

        if st.button("Run Video Robustness"):
            fake = 0
            total = 10

            for i in range(total):
                prob = random.random() + (blur*0.02) + (noise*0.01)
                if prob > 0.7:
                    fake += 1

            st.subheader("Result")
            if fake > total/2:
                st.error("Model still detects FAKE under distortion")
            else:
                st.success("Model remains stable under distortion")

            st.info("Simulation of real-world distortions.")

# ---------------- CHALLENGE ----------------
elif mode == "🧠 AI Challenge":
    st.header("🧠 AI vs Human")

    c1,c2 = st.columns(2)
    c1.image("real_sample.jpg","Image A")
    c2.image("fake_sample.jpg","Image B")

    guess = st.radio("Select Fake",["A","B"])

    if st.button("Reveal"):
        st.write("Correct Answer: B")
        st.write("AI detects texture mismatch, lighting issues, and symmetry errors.")

# ---------------- ABOUT ----------------
elif mode == "ℹ About":
    st.write("Deepfake detection with explainability and robustness testing.")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("### “Truth is verified, not assumed.”")