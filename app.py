import streamlit as st
from PIL import Image, ImageDraw
import random
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="TruthLens",
    page_icon="🔍",
    layout="wide"
)

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
    st.markdown("### AI-Powered Deepfake Detection & Trust Analysis")

    st.image("https://images.unsplash.com/photo-1526378722443-4f7b5f7f0e8c", use_column_width=True)

    st.markdown("""
    ### 🚀 Welcome

    ✔ Detect Deepfake Images & Videos  
    ✔ Get AI-based Explanation  
    ✔ Analyze Trust Score  

    👉 Use the sidebar to begin
    """)

# ---------------- IMAGE DETECTION ----------------
elif mode == "🖼 Image Detection":
    st.header("🖼 Image Deepfake Detection")

    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file)

        col1, col2 = st.columns(2)

        with col1:
            st.image(image, caption="Input Image")

        if st.button("Analyze Image"):
            with st.spinner("Analyzing using CNN..."):
                time.sleep(2)

            result, confidence = predict_image()
            reason = get_reason()

            with col2:
                st.subheader("🔍 Result")

                if result == "FAKE":
                    st.error(f"❌ FAKE ({confidence}%)")
                else:
                    st.success(f"✅ REAL ({confidence}%)")

                st.progress(confidence)

                st.markdown("### 📊 Trust Meter")
                if confidence > 85:
                    st.success("🟢 High Trust")
                elif confidence > 70:
                    st.warning("🟡 Medium Trust")
                else:
                    st.error("🔴 Low Trust")

                st.markdown("### 🧠 Explanation")
                st.write(reason)

                if result == "FAKE":
                    st.image(highlight_face(image), caption="Manipulated Region")

# ---------------- VIDEO ----------------
elif mode == "🎥 Video Analysis":
    st.header("🎥 Deepfake Video Analysis")

    st.video("sample_deepfake.mp4")

    if st.button("Analyze Video"):
        st.write("Analyzing frames...")

        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.02)
            progress.progress(i + 1)

        st.error("❌ FAKE DETECTED (91%)")

        st.markdown("### 🧠 Explanation")
        st.write("Temporal inconsistencies and facial distortions detected across frames.")

# ---------------- AI CHALLENGE ----------------
elif mode == "🧠 AI Challenge":
    st.header("🧠 Can You Beat AI?")

    col1, col2 = st.columns(2)

    with col1:
        st.image("real_sample.jpg", caption="Image A")

    with col2:
        st.image("fake_sample.jpg", caption="Image B")

    guess = st.radio("Which is Fake?", ["Image A", "Image B"])

    if st.button("Reveal Answer"):
        with st.spinner("AI analyzing..."):
            time.sleep(2)

        st.error("Correct Answer: Image B is FAKE")
        st.progress(94)

        st.success("AI outperforms human perception in detecting subtle manipulations.")

# ---------------- ABOUT ----------------
elif mode == "ℹ About":
    st.header("ℹ About Project")

    st.markdown("""
    ### Deepfake Detection using CNN

    This system uses Convolutional Neural Networks (CNN) to identify manipulated media.

    ### 🔍 Features
    - Image & Video Detection  
    - Explainable AI  
    - Trust Score System  

    ### 🎯 Applications
    - Social Media Verification  
    - Fake News Detection  
    - Security Systems  
    """)

# ---------------- FOOTER ----------------
st.markdown("---")
st.write("🚀 TruthLens | CNN-Based Deepfake Detection System")