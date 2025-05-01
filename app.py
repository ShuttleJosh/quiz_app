import streamlit as st
from quiz_data import quiz, results
from collections import Counter
import os

st.set_page_config(page_title="Which Ece Are You Today?", layout="wide")

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.answers = []

st.title("💖 Which Ece Are You Today?")
st.markdown("Choose the photo that best matches your mood each round.")

# Quiz in progress
if st.session_state.step < len(quiz):
    q = quiz[st.session_state.step]
    st.subheader(q["question"])

    cols = st.columns(len(q["options"]))

    for i, option in enumerate(q["options"]):
        with cols[i]:
            st.image(option["image"], use_container_width=True)
            filename = os.path.splitext(os.path.basename(option["image"]))[0]
            if st.button(filename, key=f"option_{i}_{st.session_state.step}"):
                st.session_state.answers.append(option["tag"])
                st.session_state.step += 1
                st.rerun()

# Quiz finished
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
