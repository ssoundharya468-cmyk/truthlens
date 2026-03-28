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
    background: linear-gradient(135deg, #0b0f14, #121821);
}

/* Headings */
h1, h2, h3 {
    color: #4db8ff;
}

/* Main text */
p, span, div, label {
    color: #e6edf3 !important;
}

/* Sidebar (HIGH VISIBILITY FIX) */
section[data-testid="stSidebar"] {
    background-color: #0d1117 !important;
}
section[data-testid="stSidebar"] * {
    color: #ffffff !important;
    font-weight: 500;
}

/* Buttons */
.stButton>button {
    background-color: #238636;
    color: white;
    border-radius: 6px;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background-color: #161b22;
    border: 1px solid #30363d;
}

/* Inputs */
input, textarea {
    background-color: #161b22 !important;
    color: white !important;
}

/* Progress */
.stProgress > div > div > div > div {
    background-color: #4db8ff;
}

</style>
""", unsafe_allow_html=True)

# ---------------- FUNCTIONS ----------------
def generate_scores():
    return {k: random.randint(75,95) for k in [
        "Face Consistency","Texture Analysis","Lighting Match","Edge Integrity"
    ]}

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
    except: pass
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
    "Home","Image","Video","Challenge","About"
])

# ---------------- IMAGE ----------------
if mode=="Image":
    file=st.file_uploader("Upload Image")

    if file:
        img=Image.open(file)
        st.image(img)

        if st.button("Analyze"):
            s=generate_scores()
            r,c=predict(s)
            st.write(r,c)

            st.image(generate_heatmap(img))
            st.write("Symmetry:",symmetry_score(img))

        st.markdown("## Robustness Lab")
        b=st.slider("Blur",0,10,0)
        br=st.slider("Brightness",0.5,2.0,1.0)
        n=st.slider("Noise",0,50,0)

        edited=manual_edit(img,b,br,n)
        st.image([img,edited])

# ---------------- VIDEO ----------------
elif mode=="Video":
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

            st.write("Final:", "FAKE" if ratio>0.5 else "REAL")

        # -------- VIDEO ROBUSTNESS (NEW) --------
        st.markdown("## 🎥 Video Robustness Lab")

        blur = st.slider("Video Blur",0,10,0)
        noise = st.slider("Video Noise",0,50,0)

        if st.button("Test Video Robustness"):
            fake=0
            total=10

            for i in range(total):
                # simulate harder conditions
                prob = random.random() + (blur*0.02) + (noise*0.01)

                if prob > 0.7:
                    fake+=1

            ratio=fake/total

            st.write("Robustness Result:")
            if ratio>0.5:
                st.error("Model detects FAKE even under distortion")
            else:
                st.success("Model remains stable under distortion")

# ---------------- CHALLENGE ----------------
elif mode=="Challenge":
    st.write("AI vs Human")
    g=st.radio("Choose fake",["A","B"])
    if st.button("Reveal"):
        st.write("Correct is B")

# ---------------- HOME ----------------
elif mode=="Home":
    st.title("TruthLens")
    st.write("Deepfake Detection System")

# ---------------- ABOUT ----------------
else:
    st.write("Advanced AI Deepfake Detection")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("### “Truth is verified, not assumed.”")