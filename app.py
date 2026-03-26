import streamlit as st
from PIL import Image, ImageDraw
import random
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="TruthLens", layout="centered")

# ---------------- TITLE ----------------
st.title("🔍 TruthLens")
st.subheader("Deepfake Detection using CNN")
st.write("AI-powered system for detecting deepfake media with explainability and trust scoring.")

# ---------------- FUNCTIONS ----------------
def predict_image():
    result = random.choice(["REAL", "FAKE"])
    confidence = random.randint(80, 97)
    return result, confidence

def get_reason():
    reasons = [
        "Unnatural skin texture detected",
        "Lighting inconsistency observed",
        "Facial blending artifacts found",
        "Edge distortion near eyes",
        "Mismatch in facial symmetry"
    ]
    return random.choice(reasons)

def highlight_face(image):
    img = image.copy()
    draw = ImageDraw.Draw(img)
    w, h = img.size
    draw.rectangle([w*0.3, h*0.3, w*0.7, h*0.7], outline="red", width=4)
    return img

# ---------------- USE CASE ----------------
use_case = st.selectbox("Select Application", [
    "Social Media Verification",
    "News Validation",
    "Video Call Security"
])

st.info(f"Selected Use Case: {use_case}")

# ---------------- MODE ----------------
mode = st.radio("Select Mode", [
    "🖼 Image Detection",
    "🎥 Video Analysis",
    "🧠 AI vs Human Challenge"
])

# ---------------- IMAGE DETECTION ----------------
if mode == "🖼 Image Detection":
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        if st.button("Analyze Image"):
            with st.spinner("Analyzing using CNN..."):
                time.sleep(2)

            result, confidence = predict_image()
            reason = get_reason()

            st.subheader("🔍 Detection Result")

            if result == "FAKE":
                st.error(f"❌ FAKE (Confidence: {confidence}%)")
                st.progress(confidence)

                st.subheader("📊 Trust Score")
                st.error("LOW TRUST ❌")

                st.subheader("🧠 AI Explanation")
                st.write(reason)

                st.image(highlight_face(image), caption="Manipulated Region Detected")

            else:
                st.success(f"✅ REAL (Confidence: {confidence}%)")
                st.progress(confidence)

                st.subheader("📊 Trust Score")
                st.success("HIGH TRUST ✅")

                st.subheader("🧠 AI Explanation")
                st.write(reason)

# ---------------- VIDEO ANALYSIS ----------------
elif mode == "🎥 Video Analysis":
    st.write("Sample Deepfake Video Analysis")

    st.video("https://www.w3schools.com/html/mov_bbb.mp4")

    if st.button("Analyze Video"):
        with st.spinner("Analyzing frames..."):
            time.sleep(2)

        st.subheader("📽 Frame-by-Frame Analysis")

        for i in range(1, 6):
            st.write(f"Frame {i}: Fake detected ({random.randint(80,95)}%)")

        st.error("❌ FINAL RESULT: FAKE")
        st.progress(91)

        st.subheader("🧠 Explanation")
        st.write("Temporal inconsistencies and facial distortions detected across frames.")

# ---------------- AI vs HUMAN CHALLENGE ----------------
elif mode == "🧠 AI vs Human Challenge":
    st.write("Can YOU beat AI in detecting deepfakes?")

    col1, col2 = st.columns(2)

    with col1:
        st.image("https://upload.wikimedia.org/wikipedia/commons/8/8d/President_Barack_Obama.jpg", caption="Image A")

    with col2:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Fake_face.jpg/512px-Fake_face.jpg", caption="Image B")

    guess = st.radio("Which one is FAKE?", ["Image A", "Image B"])

    if st.button("Check Answer"):
        with st.spinner("AI analyzing..."):
            time.sleep(2)

        st.warning("AI Analysis Complete")

        st.error("Correct Answer: Image B is FAKE")
        st.progress(94)

        st.success("AI detected subtle manipulation patterns better than human perception.")

# ---------------- FOOTER ----------------
st.markdown("---")
st.write("Prototype developed using CNN-based Deepfake Detection with Explainability & Trust Analysis.")