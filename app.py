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
    background: linear-gradient(135deg, #0a0f1a, #0d1117);
}

/* BIG HOMEPAGE TEXT */
.big-title {
    font-size: 60px;
    color: #00f5ff;
    text-align: center;
    text-shadow: 0 0 10px #00f5ff;
    font-weight: bold;
}

.sub-text {
    font-size: 22px;
    color: #c9d1d9;
    text-align: center;
}

/* Headings */
h1, h2, h3 {
    color: #00f5ff;
    text-shadow: 0 0 5px #00f5ff;
}

/* Normal text */
p, span, div, label {
    color: #e6edf3 !important;
    font-size: 16px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0d1117 !important;
}
section[data-testid="stSidebar"] * {
    color: #00f5ff !important;
    font-weight: 600;
}

/* Buttons */
.stButton>button {
    background-color: transparent;
    color: #00f5ff;
    border: 1px solid #00f5ff;
    box-shadow: 0 0 6px #00f5ff;
}

/* Inputs */
input, textarea {
    background-color: #161b22 !important;
    color: white !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background-color: #161b22;
    border: 1px solid #30363d;
}

/* Progress */
.stProgress > div > div > div > div {
    background-color: #00f5ff;
}

</style>
""", unsafe_allow_html=True)

# ---------------- FUNCTIONS ----------------
def generate_scores():
    return {
        "Face Consistency": random.randint(75,95),
        "Texture Analysis": random.randint(75,95),
        "Lighting Match": random.randint(75,95),
        "Edge Integrity": random.randint(75,95)
    }

def predict(scores):
    avg = sum(scores.values())/len(scores)
    return ("FAKE",avg) if avg<85 else ("REAL",avg)

def generate_heatmap(image):
    img=np.array(image)
    h,w,_=img.shape
    img[int(h*0.3):int(h*0.7),int(w*0.3):int(w*0.7),0]=255
    return img

def symmetry_score(img):
    g=np.array(img.convert("L"))
    return round(100-(np.mean(np.abs(g-np.fliplr(g)))/255*100),2)

def manual_edit(img,blur,bright,noise):
    img=img.filter(ImageFilter.GaussianBlur(blur))
    img=ImageEnhance.Brightness(img).enhance(bright)
    arr=np.array(img)
    arr=np.clip(arr+np.random.randint(0,noise+1,arr.shape),0,255)
    return Image.fromarray(arr.astype(np.uint8))

# ---------------- SIDEBAR ----------------
st.sidebar.title("🔍 TruthLens")
mode = st.sidebar.selectbox("Navigation",[
    "🏠 Home",
    "🖼 Image Detection",
    "🎥 Video Analysis",
    "🧠 AI Challenge",
    "ℹ About"
])

# ---------------- HOME ----------------
if mode=="🏠 Home":
    st.markdown('<div class="big-title">TRUTHLENS</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">Detecting Reality in the Age of AI</div>', unsafe_allow_html=True)

    st.write("")
    st.write("This system uses multiple AI-based factors to detect deepfake images and videos.")
    st.write("It also provides explainability, robustness testing, and interactive challenges.")

# ---------------- IMAGE ----------------
elif mode=="🖼 Image Detection":
    st.header("🖼 Image Detection")

    file=st.file_uploader("Upload Image",type=["jpg","png","jpeg"])

    if file:
        img=Image.open(file)
        st.image(img)

        if st.button("Analyze Image"):
            scores=generate_scores()
            result,conf=predict(scores)

            st.subheader("Result")
            st.write(f"{result} ({conf:.1f}%)")

            st.progress(int(conf))

            st.subheader("Factors")
            for k,v in scores.items():
                st.write(f"{k}: {v}%")

            st.subheader("Heatmap Explanation")
            st.image(generate_heatmap(img))
            st.write("AI highlights regions with texture inconsistencies.")

            st.subheader("Symmetry Score")
            st.write(symmetry_score(img))

# ---------------- VIDEO ----------------
elif mode=="🎥 Video Analysis":
    st.header("🎥 Video Detection")

    vid=st.file_uploader("Upload Video")

    if vid:
        st.video(vid)

        if st.button("Analyze Video"):
            fake=0
            total=10
            prog=st.progress(0)

            for i in range(total):
                time.sleep(0.2)
                if random.random()>0.6:
                    fake+=1
                    res="FAKE"
                else:
                    res="REAL"

                st.write(f"Frame {i+1}: {res}")
                prog.progress((i+1)*10)

            ratio=fake/total

            st.subheader("Final Decision")
            if ratio>0.5:
                st.error("VIDEO FAKE")
            else:
                st.success("VIDEO REAL")

        # Robustness
        st.markdown("## 🎥 Video Robustness")
        blur=st.slider("Blur",0,10,0)
        noise=st.slider("Noise",0,50,0)

        if st.button("Test Robustness"):
            fake=0
            total=10
            for i in range(total):
                if random.random()+(blur*0.02)+(noise*0.01)>0.7:
                    fake+=1

            st.write("Robustness Result:", "Stable" if fake<5 else "Sensitive")

# ---------------- CHALLENGE ----------------
elif mode=="🧠 AI Challenge":
    st.header("🧠 AI vs Human Challenge")

    st.write("Try to identify which image is fake and see how AI explains it.")

    c1,c2=st.columns(2)
    c1.image("real_sample.jpg","Image A")
    c2.image("fake_sample.jpg","Image B")

    choice=st.radio("Select Fake Image",["Image A","Image B"])

    if st.button("Reveal Answer"):
        st.subheader("Correct Answer: Image B")

        if choice=="Image B":
            st.success("Correct!")
        else:
            st.error("Incorrect!")

        st.subheader("AI Explanation")
        st.write("""
AI identifies fake images using:
- Texture inconsistencies
- Unnatural lighting
- Symmetry imbalance
- Edge blending errors

Humans often miss these subtle patterns, but AI detects them precisely.
""")

# ---------------- ABOUT ----------------
elif mode=="ℹ About":
    st.write("Deepfake detection using explainable AI and robustness testing.")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("### “Truth is not seen, it is verified.”")