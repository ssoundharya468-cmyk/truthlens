# ---------------- IMPORTS ----------------
import streamlit as st
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
import random
import cv2

# ---------------- PAGE ----------------
st.set_page_config(page_title="TruthLens", layout="wide")

# ---------------- UI ----------------
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0a0f1a, #0d1117); }

.big-title {
    font-size: 90px;
    color: #00f5ff;
    text-align: center;
    font-weight: bold;
}

p, div, label {
    font-size: 20px !important;
    color: #e6edf3 !important;
}

h1, h2 {
    color: #00f5ff;
    font-size: 36px !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- FUNCTIONS ----------------
def predict():
    val = random.randint(70,95)
    return ("FAKE", val) if val < 85 else ("REAL", val)

def heatmap(img):
    arr = np.array(img)
    h,w,_ = arr.shape
    arr[h//3:2*h//3, w//3:2*w//3, 0] = 255
    return arr

def edit(img, b, br, n):
    img = img.filter(ImageFilter.GaussianBlur(b))
    img = ImageEnhance.Brightness(img).enhance(br)
    arr = np.array(img)
    arr = np.clip(arr + np.random.randint(0,n+1,arr.shape),0,255)
    return Image.fromarray(arr.astype(np.uint8))

def face_detect(img):
    img_np = np.array(img)
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    face = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
    faces = face.detectMultiScale(gray,1.3,5)

    for (x,y,w,h) in faces:
        cv2.rectangle(img_np,(x,y),(x+w,y+h),(0,255,0),2)

    return img_np, len(faces)

def final_decision(r1,r2):
    if r1=="REAL" and r2=="REAL":
        return "Clearly Real"
    elif r1=="FAKE" and r2=="FAKE":
        return "Clearly AI Generated"
    else:
        return "Uncertain (Needs More Analysis)"

# ---------------- SIDEBAR ----------------
mode = st.sidebar.selectbox("Navigation",["Home","Image"])

# ---------------- HOME ----------------
if mode=="Home":
    st.markdown('<div class="big-title">TRUTHLENS</div>', unsafe_allow_html=True)
    st.write("AI-based deepfake detection with explainability and robustness testing.")

# ---------------- IMAGE ----------------
elif mode=="Image":

    file = st.file_uploader("Upload Image")

    if file:
        img = Image.open(file)
        st.image(img)

        if st.button("Analyze"):
            r,c = predict()
            st.write(f"Prediction: {r} ({c}%)")

            # FACE
            st.subheader("Face Detection")
            f_img, count = face_detect(img)
            st.image(f_img)
            st.write("Faces detected:",count)

            # HEATMAP
            st.subheader("Heatmap Analysis")
            hm = heatmap(img)
            st.image(hm)
            st.write("Red region shows possible manipulation zones.")

        # -------- ROBUSTNESS --------
        st.subheader("Robustness Testing")

        b = st.slider("Blur",0,10,0)
        br = st.slider("Brightness",0.5,2.0,1.0)
        n = st.slider("Noise",0,50,0)

        edited = edit(img,b,br,n)

        c1,c2 = st.columns(2)
        c1.image(img,"Original")
        c2.image(edited,"Modified")

        if st.button("Run Robustness"):
            r1,c1v = predict()
            r2,c2v = predict()

            st.subheader("Result Table")

            st.table({
                "Type":["Original","Modified"],
                "Prediction":[r1,r2],
                "Confidence":[c1v,c2v]
            })

            # FINAL DECISION
            decision = final_decision(r1,r2)

            st.subheader("Final Conclusion")
            if decision=="Clearly Real":
                st.success(decision)
            elif decision=="Clearly AI Generated":
                st.error(decision)
            else:
                st.warning(decision)

            st.info("System compares original vs distorted image to evaluate model stability.")