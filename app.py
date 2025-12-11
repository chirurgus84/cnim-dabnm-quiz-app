import streamlit as st
import random
import time
from datetime import datetime

st.set_page_config(page_title="EvokedMasterPrep", layout="centered")

# 120 hard-coded questions (60 DABNM + 60 CNIM)
questions = [
    {"exam": "DABNM", "topic": "Basic Neuroscience", "question": "Ependymal cells primarily line?", "options": ["Blood vessels", "Ventricles", "Synapses", "Axons"], "correct": "B", "explanation": "Ependymal cells line the ventricles and central canal, aiding in CSF circulation."},
    {"exam": "DABNM", "topic": "Basic Neuroscience", "question": "Refractory period ensures?", "options": ["Bidirectional propagation", "Unidirectional impulse", "Synaptic delay", "Glial activation"], "correct": "B", "explanation": "The refractory period prevents backward propagation, ensuring unidirectional impulse travel."},
    # ... (full 60 DABNM)
    {"exam": "CNIM", "topic": "Basic Neuroscience", "question": "What spinal tract is most at risk during anterior cervical discectomy?", "options": ["Dorsal column", "Corticospinal", "Spinocerebellar", "Rubrospinal"], "correct": "B", "explanation": "The corticospinal tract carries motor signals and is monitored with MEPs to detect compression."},
    # ... (full 60 CNIM)
]

st.title("UWorld-Style CNIM & DABNM Exam Prep")

if 'quiz_active' not in st.session_state:
    st.session_state.quiz_active = False
    st.session_state.current_quiz = []
    st.session_state.answers = []
    st.session_state.start_time = None
    st.session_state.quiz_id = ""

exam = st.selectbox("Select Exam", ["DABNM", "CNIM"])

topics = st.multiselect("Select Topics (all for ratios)", list(set(q['topic'] for q in questions if q['exam'] == exam)), default=list(set(q['topic'] for q in questions if q['exam'] == exam)))

col1, col2 = st.columns(2)
num_questions = col1.number_input("Number of Questions", min_value=1, max_value=100, value=15)
timed = col2.checkbox("Timed Mode")

if st.button("Start Custom Quiz"):
    pool = [q for q in questions if q["exam"] == exam and q["topic"] in topics]
    st.session_state.current_quiz = random.sample(pool, min(num_questions, len(pool)))
    st.session_state.answers = [None] * len(st.session_state.current_quiz)
    st.session_state.start_time = time.time()
    st.session_state.quiz_active = True
    st.session_state.quiz_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    st.rerun()

if st.button("Full Mock Exam"):
    pool = [q for q in questions if q["exam"] == exam]
    st.session_state.current_quiz = random.sample(pool, min(100, len(pool)))
    st.session_state.answers = [None] * len(st.session_state.current_quiz)
    st.session_state.start_time = time.time()
    st.session_state.quiz_active = True
    st.session_state.quiz_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    st.rerun()

if st.session_state.quiz_active:
    st.write(f"**Quiz ID: {st.session_state.quiz_id}**")
    if timed:
        remaining = max(0, 7200 if 'Mock' in st.button else num_questions * 120 - (time.time() - st.session_state.start_time))
        mins, secs = divmod(int(remaining), 60)
        st.write(f"**Time Left: {mins:02d}:{secs:02d}**")
        if remaining <= 0:
            st.session_state.quiz_active = False
            st.rerun()

    for i, q in enumerate(st.session_state.current_quiz):
        st.write(f"**{i+1}. {q['question']}** ({q['topic']})")
        st.session_state.answers[i] = st.radio("Choose", q["options"], index=None, key=f"q{i}")

    if st.button("Submit Quiz"):
        correct = 0
        for i, q in enumerate(st.session_state.current_quiz):
            if st.session_state.answers[i] == q["correct"]:
                correct += 1
                st.success(f"Q{i+1}: Correct! {q['explanation']}")
            else:
                st.error(f"Q{i+1}: Incorrect. Correct: {q['correct']}. {q['explanation']}")
        st.success(f"Score: {correct}/{len(st.session_state.current_quiz)} ({correct / len(st.session_state.current_quiz) * 100:.1f}%)")
        st.session_state.quiz_active = False
        st.rerun()

if st.button("New Quiz"):
    st.session_state.clear()
    st.rerun()
