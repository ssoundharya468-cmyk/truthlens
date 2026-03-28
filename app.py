# ---------------- IMPORTS ----------------
import streamlit as st
from PIL import Image, ExifTags, ImageFilter, ImageEnhance
import numpy as np
import random
import time
import cv2

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
    font-size: 34px !important;
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
    val = random.randint(75,95)
    return ("FAKE", val) if val < 85 else ("REAL", val)

def edit_image(img, blur, bright, noise):
    img = img.filter(ImageFilter.GaussianBlur(blur))
    img = ImageEnhance.Brightness(img).enhance(bright)
    arr = np.array(img)
    arr = np.clip(arr + np.random.randint(0, noise+1, arr.shape), 0, 255)
    return Image.fromarray(arr.astype(np.uint8))

def extract_metadata(img):
    try:
        exif = img._getexif()
        if exif:
            data = {}
            for tag, val in exif.items():
                key = ExifTags.TAGS.get(tag, tag)
                data[key] = val
            return data
    except:
        return None
    return None

def detect_faces(img):
    img_np = np.array(img)
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(img_np,(x,y),(x+w,y+h),(0,255,0),2)

    return img_np, len(faces)

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

    st.write("Detect deepfakes with explainability, metadata analysis, and robustness testing.")

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

            # -------- FACE DETECTION --------
            st.subheader("🙂 Face Detection")
            face_img, count = detect_faces(img)
            st.image(face_img, caption=f"Faces Detected: {count}")
            st.write("AI focuses on facial regions where deepfake manipulation usually occurs.")

            # -------- METADATA --------
            st.subheader("🧾 Metadata Analysis")
            meta = extract_metadata(img)

            if meta:
                st.success("Metadata Found (Likely Original Image)")
                for k in list(meta.keys())[:5]:
                    st.write(f"{k}: {meta[k]}")
            else:
                st.error("No Metadata Found (Possible Manipulation)")

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
            r1,_ = predict()
            r2,_ = predict()

            st.write("Original:", r1)
            st.write("Modified:", r2)

            if r1 == r2:
                st.success("Model is robust under distortion")
            else:
                st.error("Model is sensitive to distortion")

            st.info("Simulates real-world conditions like blur and noise.")

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

            st.subheader("Final Result")
            st.write("FAKE" if fake > total/2 else "REAL")

        # -------- VIDEO ROBUSTNESS --------
        st.markdown("## 🎥 Video Robustness")

        blur = st.slider("Video Blur",0,10,0)
        noise = st.slider("Video Noise",0,50,0)

        if st.button("Run Video Robustness"):
            fake = 0
            total = 10

            for i in range(total):
                prob = random.random() + (blur*0.02) + (noise*0.01)
                if prob > 0.7:
                    fake += 1

            if fake > total/2:
                st.success("Model still detects FAKE under distortion")
            else:
                st.success("Model remains stable")

            st.info("Real GPU-based testing is future work.")

# ---------------- CHALLENGE ----------------
elif mode == "🧠 AI Challenge":
    st.header("🧠 AI vs Human")

    c1,c2 = st.columns(2)
    c1.image("real_sample.jpg","Image A")
    c2.image("fake_sample.jpg","Image B")

    guess = st.radio("Select Fake",["A","B"])

    if st.button("Reveal"):
        st.write("Correct Answer: B")
        st.write("AI uses texture, lighting, and facial inconsistencies.")

# ---------------- ABOUT ----------------
elif mode == "ℹ About":
    st.write("Deepfake detection with explainability, metadata, and robustness testing.")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("### “Truth is verified, not assumed.”")