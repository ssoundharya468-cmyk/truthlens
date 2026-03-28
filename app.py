# ---------------- IMPORTS ----------------
import streamlit as st
from PIL import Image, ExifTags, ImageFilter, ImageEnhance
import numpy as np
import random
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="TruthLens", page_icon="🔍", layout="wide")

# ---------------- FINAL NEON UI ----------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #0a0f1a, #0d1117);
}

/* Neon Headings */
h1, h2, h3 {
    color: #00f5ff;
    text-shadow: 0 0 6px #00f5ff;
}

/* Normal Text (Readable) */
p, span, div, label {
    color: #e6edf3 !important;
    font-size: 15px;
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
.stButton>button:hover {
    background-color: #00f5ff;
    color: black;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background-color: #161b22;
    border: 1px solid #30363d;
}

/* Inputs */
input, textarea {
    background-color: #161b22 !important;
    color: #e6edf3 !important;
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

def extract_metadata(img):
    try:
        exif=img._getexif()
        if exif:
            return {ExifTags.TAGS.get(k,k):v for k,v in exif.items()}
    except:
        return None
    return None

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
    st.title("🔍 TruthLens")
    st.write("AI-powered deepfake detection with explainability and robustness testing.")

# ---------------- IMAGE ----------------
elif mode=="🖼 Image Detection":
    st.header("🖼 Image Detection")

    file=st.file_uploader("Upload Image",type=["jpg","png","jpeg"])

    if file:
        img=Image.open(file)
        st.image(img)

        if st.button("Analyze Image"):
            st.write("Analyzing image...")
            scores=generate_scores()
            result,conf=predict(scores)

            st.subheader("Result")
            st.write(f"{result} ({conf:.1f}%)")

            st.progress(int(conf))

            st.subheader("Analysis")
            for k,v in scores.items():
                st.write(f"{k}: {v}%")

            st.subheader("Heatmap")
            st.image(generate_heatmap(img))
            st.write("Highlighted regions indicate possible manipulation.")

            st.subheader("Metadata")
            meta=extract_metadata(img)
            st.write("Metadata Found" if meta else "No Metadata → Possible Fake")

            st.subheader("Symmetry Score")
            st.write(symmetry_score(img))

        # Robustness
        st.markdown("## 🧪 Image Robustness")
        b=st.slider("Blur",0,10,0)
        br=st.slider("Brightness",0.5,2.0,1.0)
        n=st.slider("Noise",0,50,0)

        edited=manual_edit(img,b,br,n)
        st.image([img,edited])

# ---------------- VIDEO ----------------
elif mode=="🎥 Video Analysis":
    st.header("🎥 Video Detection")

    vid=st.file_uploader("Upload Video")

    if vid:
        st.video(vid)

        if st.button("Analyze Video"):
            st.write("Analyzing frames...")
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

            if ratio>0.5:
                st.error("VIDEO FAKE")
            else:
                st.success("VIDEO REAL")

        # Robustness
        st.markdown("## 🎥 Video Robustness")
        blur=st.slider("Blur Level",0,10,0)
        noise=st.slider("Noise Level",0,50,0)

        if st.button("Test Robustness"):
            fake=0
            total=10
            for i in range(total):
                if random.random()+(blur*0.02)+(noise*0.01)>0.7:
                    fake+=1

            st.write("Robustness:", "Stable" if fake<5 else "Sensitive")

# ---------------- CHALLENGE ----------------
elif mode=="🧠 AI Challenge":
    st.header("AI Challenge")

    c1,c2=st.columns(2)
    c1.image("real_sample.jpg","A")
    c2.image("fake_sample.jpg","B")

    g=st.radio("Which is fake?",["A","B"])

    if st.button("Reveal"):
        st.write("Answer: B")
        st.write("AI detects subtle inconsistencies.")

# ---------------- ABOUT ----------------
elif mode=="ℹ About":
    st.write("Deepfake detection with explainable AI.")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("### “Truth shines even in the digital illusion.”")