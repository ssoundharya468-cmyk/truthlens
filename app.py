if st.button("Reveal"):
    if guess == "Image B":
        st.success("✅ Correct! Image B is FAKE")
    else:
        st.error("❌ Wrong! Image B is FAKE")

    st.markdown("### 🧠 Explanation")

    st.info("""
AI identified Image B as fake due to:

• Slight facial asymmetry  
• Unnatural skin texture  
• Inconsistent lighting  

These patterns are difficult for humans to detect but are captured by AI models.
""")