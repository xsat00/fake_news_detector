import streamlit as st
from downloader import downloads
from frame_ext import extract_frames
from hash_comp import generate_hashes, detect_duplicates
from Cap_anal import analyze_caption
import os
from PIL import Image
import cv2

st.set_page_config(page_title="🧠 Fake News Video Detector", layout="centered")

st.title("🧠 Fake News Video Detector")
st.markdown("Paste a YouTube video link below to analyze.")

url = st.text_input("📹 YouTube video link")

if st.button("Analyze"):
    if url:
        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        st.info("⏳ Downloading video...")
        video_path, title = downloads(url)

        if video_path:
            st.success(f"✅ Downloaded: {title}")

            # Show video thumbnail
            cap = cv2.VideoCapture(video_path)
            success, frame = cap.read()
            cap.release()
            if success:
                frame_path = "thumbnail.jpg"
                cv2.imwrite(frame_path, frame)
                st.image(Image.open(frame_path), caption="🔍 Video Thumbnail", use_column_width=True)

            # Extract frames
            with st.spinner("🎞️ Extracting frames..."):
                frame_count = extract_frames(video_path)
            st.write(f"🧩 Extracted **{frame_count}** frames.")

            # Analyze for duplicate frames
            with st.spinner("🔍 Detecting duplicate frames..."):
                frames_folder = r"C:\Users\Sathwik\myprojects\frames"
                if os.path.exists(frames_folder):
                    hashes = generate_hashes(frames_folder)
                    dups = detect_duplicates(hashes)
                    if dups:
                        st.warning(f"⚠️ Detected **{len(dups)}** duplicate frame matches.")
                        first_few = dups[:5]
                        st.write("Example duplicates:")
                        st.code(f"{first_few[0]}")
                    else:
                        st.success("✅ No duplicate frames found.")
                else:
                    st.error(f"❌ Frame folder not found: {frames_folder}")

            # Caption analysis (supports other languages)
            with st.spinner("🧠 Analyzing caption..."):
                result = analyze_caption(title)
                st.markdown("### 📝 Caption Analysis Results")

                if result.get("clickbait_words"):
                    st.error(f"🚨 Clickbait detected: {', '.join(result['clickbait_words'])}")
                else:
                    st.success("✅ No clickbait words detected.")

                if result.get("emotive_words"):
                    st.warning(f"⚡ Emotive words: {', '.join(result['emotive_words'])}")
                else:
                    st.info("No strong emotive words found.")

                if result.get("named_entities"):
                    st.markdown("📌 Named Entities Found:")
                    for ne in result["named_entities"]:
                        st.markdown(f"- **{ne[0]}** (*{ne[1]}*)")

                if result.get("flagged"):
                    st.error("⚠️ This caption may contain misleading or fake information.")
                else:
                    st.success("🟢 Caption seems clear of misinformation.")
        else:
            st.error("❌ Download failed. Please check the link.")
    else:
        st.warning("⚠️ Please enter a YouTube video link.")
