import streamlit as st
from PIL import Image, ExifTags
from quiz_data import quiz, results
from collections import Counter
import os

def correct_image_rotation(image_path):
    """Correct the image rotation based on EXIF data."""
    try:
        img = Image.open(image_path)
        # Check if the image has EXIF data (e.g., orientation)
        for orientation_tag in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation_tag]=='Orientation':
                break
        
        # Get EXIF data and rotate the image accordingly
        exif = img._getexif()
        if exif is not None:
            orientation = dict(exif).get(orientation_tag)
            if orientation == 3:
                img = img.rotate(180, expand=True)
            elif orientation == 6:
                img = img.rotate(270, expand=True)
            elif orientation == 8:
                img = img.rotate(90, expand=True)
        return img
    except (AttributeError, KeyError, IndexError):
        # If no EXIF data, return the image as is
        return Image.open(image_path)

st.set_page_config(page_title="Which Ece Are You Today?", layout="wide")

if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.answers = []

st.title("💖 Which Ece Are You Today?")
st.markdown("Choose the photo that best matches your mood each round.")

if st.session_state.step < len(quiz):
    q = quiz[st.session_state.step]
    st.subheader(q["question"])

    cols = st.columns(len(q["options"]))

    for i, option in enumerate(q["options"]):
        with cols[i]:
            # Correct rotation for each image before displaying it
            corrected_image = correct_image_rotation(option["image"])
            st.image(corrected_image, use_container_width=True)
            
            filename = os.path.splitext(os.path.basename(option["image"]))[0]
            if st.button(filename, key=f"option_{i}_{st.session_state.step}"):
                st.session_state.answers.append(option["tag"])
                st.session_state.step += 1
                st.rerun()
else:
    st.subheader("Your result is...")

    if st.session_state.answers:
        most_common = Counter(st.session_state.answers).most_common(1)[0][0]
        st.markdown(f"### 🎉 {results[most_common]}")
        st.image(f"images/{most_common}.JPG", use_container_width=True)
    else:
        st.warning("No answers recorded. Please restart the quiz.")

    if st.button("Play again"):
        st.session_state.step = 0
        st.session_state.answers = []
        st.rerun()
