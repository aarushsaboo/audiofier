import os
import whisper
from gtts import gTTS
import streamlit as st
import tempfile

os.system("pip install whisper") # due to difficulty in loading whisper

def save_text_as_audio(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    tts.save(temp_audio_file.name)
    return temp_audio_file.name

def save_audio_as_text(audio_file_path):
    try:
        model = whisper.load_model("base") # Load the model here lazily
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None
    result = model.transcribe(audio_file_path, fp16=False)
    text = result["text"]
    temp_text_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
    with open(temp_text_file.name, 'w') as f:
        f.write(text)
    return temp_text_file.name

# Streamlit app for text to audio
st.title("Text to Audio Converter")
text_source = st.radio("Select text source:", ('Text Input', 'Text File'))

text = ""
if text_source == 'Text Input':
    text = st.text_area("Enter your text here:")
elif text_source == 'Text File':
    uploaded_file = st.file_uploader("Choose a text file...", type="txt")
    if uploaded_file is not None:
        text = uploaded_file.read().decode('utf-8')

if st.button("Convert to Audio") and text:
    with st.spinner("Converting text to audio..."):
        audio_file_path = save_text_as_audio(text)
        st.success("Conversion complete!")
        st.audio(audio_file_path, format='audio/mp3')
        st.download_button(
            label="Download Audio",
            data=open(audio_file_path, "rb"),
            file_name="output.mp3",
            mime="audio/mp3"
        )
    os.remove(audio_file_path)  # Explicitly delete temporary audio file

# Streamlit app for audio to text
st.title('Audio to Text Converter')
audio_source = st.radio("Select audio source:", ('Audio file',))

audio = None
if audio_source == 'Audio file':
    uploaded_file = st.file_uploader("Choose an audio file...", type=["mp3", "wav", "m4a"])
    if uploaded_file is not None:
        temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[-1])
        with open(temp_audio_file.name, 'wb') as f:
            f.write(uploaded_file.read())
        audio = temp_audio_file.name

if st.button("Convert to Text") and audio:
    with st.spinner("Converting audio to text..."):
        text_file_path = save_audio_as_text(audio)
        st.success("Conversion complete!")
        with open(text_file_path, 'r') as f:
            st.text(f.read())
        st.download_button(
            label="Download Text",
            data=open(text_file_path, "rb"),
            file_name="output.txt",
            mime="text/plain"
        )
    os.remove(text_file_path)  # Explicitly delete temporary text file

