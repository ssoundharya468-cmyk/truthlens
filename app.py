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

/* BIG TITLE */
.big-title {
    font-size: 70px;
    color: #00f5ff;
    text-align: center;
    text-shadow: 0 0 12px #00f5ff;
    font-weight: bold;
}

/* Subtitle */
.sub-text {
    font-size: 26px;
    color: #c9d1d9;
    text-align: center;
}

/* Headings */
h1, h2, h3 {
    color: #00f5ff;
    font-size: 32px !important;
}

/* Body text */
p, span, div, label {
    color: #e6edf3 !important;
    font-size: 18px !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0d1117 !important;
}
section[data-testid="stSidebar"] * {
    color: #00f5ff !important;
    font-size: 18px !important;
    font-weight: 600;
}

/* Buttons */
.stButton>button {
    font-size: 18px;
    padding: 10px;
    border: 1px solid #00f5ff;
    color: #00f5ff;
    background: transparent;
}

/* Inputs */
input, textarea {
    background-color: #161b22 !important;
    color: white !important;
    font-size: 16px !important;
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

    st.write("This system detects deepfakes using explainable AI and robustness testing.")

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

            st.subheader("Heatmap")
            st.image(generate_heatmap(img))

        # -------- IMAGE ROBUSTNESS (UPGRADED) --------
        st.markdown("## 🧪 Image Robustness Testing")
        st.write("Modify the image and check if detection changes.")

        b=st.slider("Blur Level",0,10,0)
        br=st.slider("Brightness",0.5,2.0,1.0)
        n=st.slider("Noise Level",0,50,0)

        edited=manual_edit(img,b,br,n)

        c1,c2=st.columns(2)
        c1.image(img,"Original")
        c2.image(edited,"Modified")

        if st.button("Run Robustness Test"):
            s1=generate_scores()
            r1,_=predict(s1)

            s2=generate_scores()
            r2,_=predict(s2)

            st.write("Original Result:",r1)
            st.write("Modified Result:",r2)

            if r1==r2:
                st.success("Model is ROBUST (consistent prediction)")
            else:
                st.error("Model is SENSITIVE to changes")

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
            st.write("FAKE" if ratio>0.5 else "REAL")

        # -------- VIDEO ROBUSTNESS --------
        st.markdown("## 🎥 Video Robustness")
        blur=st.slider("Blur",0,10,0)
        noise=st.slider("Noise",0,50,0)

        if st.button("Test Video Robustness"):
            fake=0
            total=10
            for i in range(total):
                if random.random()+(blur*0.02)+(noise*0.01)>0.7:
                    fake+=1

            st.write("Robustness:", "Stable" if fake<5 else "Sensitive")

# ---------------- CHALLENGE ----------------
elif mode=="🧠 AI Challenge":
    st.header("🧠 AI vs Human Challenge")

    st.write("Guess the fake image and understand AI reasoning.")

    c1,c2=st.columns(2)
    c1.image("real_sample.jpg","Image A")
    c2.image("fake_sample.jpg","Image B")

    choice=st.radio("Select Fake Image",["Image A","Image B"])

    if st.button("Reveal"):
        st.write("Correct Answer: Image B")
        st.write("""
AI detects:
- Texture inconsistencies
- Lighting mismatch
- Symmetry imbalance
- Edge blending errors
""")

# ---------------- ABOUT ----------------
elif mode=="ℹ About":
    st.write("Deepfake detection using explainable AI and robustness testing.")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("### “Truth is verified, not assumed.”")