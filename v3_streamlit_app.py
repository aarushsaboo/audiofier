import os
import whisper
from gtts import gTTS
import streamlit as st
import tempfile
import pyaudio
import wave
from pathlib import Path
import re
import random
import pyttsx3
import os
import platform
from pydub import AudioSegment
# st.set_option('server.maxUploadSize', 1024)

# install_command = 'pip install imageio-ffmpeg'

# Execute the installation command
# os.system(install_command)
# version_output = os.popen('ffmpeg --version').read()
# print(version_output)

#the unique names of temp files are unique only within the scope of the process that created them. If you create two files with the same name in different processes, they will still have the same name, which can cause issues.
#In your example, create_mp3_file and create_txt_file are two separate functions that create temporary files. If you call these functions in different processes or threads, they will create files with the same name, which can cause issues.
#ensure that the file names are unique across all processes and threads. You can do this by including a unique identifier in the file name, such as a timestamp or a random number.


# st.info # st.markdown # st.write_stream # st.balloons # st.html  # pyttsx3  # st.header # st.divider # st.tabs or st.expanders 

# Session state
if 'recording' not in st.session_state:
    st.session_state['recording'] = False

# Audio parameters (unchanged)
FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

if 'audio_available' not in st.session_state:
    try:
    # Open an audio stream (unchanged)
        p = pyaudio.PyAudio()
        stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=FRAMES_PER_BUFFER
        )
        stream.close()
        st.session_state['audio_available'] = True
    except OSError:
        st.session_state['audio_available'] = False
        st.write("audio recording Not available")

def transcribe_audio(audio_file):
    model = whisper.load_model("base")
    result = model.transcribe(audio_file, fp16=False)
    return result["text"]

def format_text(text):
    sentences = re.split('(?<=[.!?]) +', text)
    formatted_text = ""
    
    colors = ["red", "green", "blue", "orange", "purple", "teal"]

    for i, sentence in enumerate(sentences):
        words = sentence.split()
        
        if i >= 0 and len(words) < 7:
            color = random.choice(colors)
            formatted_text += f'<h3 style="color:{color};">{sentence}</h3>'
        elif any(keyword in sentence.lower() for keyword in ["important", "crucial", "significant"]):
            formatted_text += f'<p><u>{sentence}</u></p>'
        elif len(words) > 15 and len(words) < 30:
            rainbow_sentence = ""
            for j, word in enumerate(words):
                color = colors[j % len(colors)]
                rainbow_sentence += f'<span style="color:{color};text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">{word}</span> '
            formatted_text += f'<p>{rainbow_sentence}</p>'
        elif len(words) > 30:
            formatted_text += f'''
            <p style="animation: pulse 2s infinite;">
                <strong>{sentence}</strong>
            </p>
            '''
        else:
            formatted_text += f'''<p style="background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
                      -webkit-background-clip: text;
                      -webkit-text-fill-color: transparent;
                      font-size: 1.2em;">{sentence}</p>'''
    return formatted_text


# Existing functions (unchanged)
def start_recording():
    st.session_state['recording'] = True
    st.session_state['frames'] = []

def stop_recording():
    st.session_state['recording'] = False
    save_audio()

def save_audio():
    wf = wave.open("recorded_audio.wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(st.session_state['frames']))
    wf.close()

def text_to_speech(text, voice_settings):
    if platform.system() == "Windows":
        engine = pyttsx3.init(driverName = 'sapi5')
    else:
        engine = pyttsx3.init(driverName='espeak')
    engine.setProperty('rate', voice_settings['rate'])
    engine.setProperty('volume', voice_settings['volume'])
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice_settings['voice_index']].id)
    
    file_name = 'output.mp3'
    engine.save_to_file(text, file_name)
    engine.runAndWait()
    # Read the file using pydub
    audio = AudioSegment.from_mp3(file_name)
    
    # Convert to in-memory file
    buffer = io.BytesIO()
    audio.export(buffer, format="mp3")
    buffer.seek(0)
    
    # Remove the temporary file
    os.remove(file_name)
    
    return buffer

# def save_text_as_audio(text, lang='en'):
#     tts = gTTS(text=text, lang=lang)
#     temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
#     tts.save(temp_file.name)
#     return temp_file.name

# def save_audio_as_text(audio_file_path): 
#     model = whisper.load_model("base")
#     result = model.transcribe(audio_file_path, fp16=False)
#     text = result["text"]
#     temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
#     with open(temp_file.name, 'w') as f:
#         f.write(text)
#     return temp_file.name

# Streamlit app
st.markdown("# 🎓 Student Lecture Assistant")
st.info("Welcome! This tool helps you transcribe lectures and create voice recordings from text.")

tab1, tab2 = st.tabs(["Audio to Text", "Text to Audio"])

with tab1:
    st.header("📝 Transcribe Your Lecture")
    st.markdown("Upload an audio file or record directly to get a text transcript.")
    
    audio_source = st.radio("Select audio source:", ('Audio input', 'Audio file'))

    if audio_source == 'Audio input':
        if st.session_state['audio_available']:
            col1, col2 = st.columns(2)
            col1.button('Start Recording', on_click=start_recording)
            col2.button('Stop Recording', on_click=stop_recording)

            if st.session_state['recording']:
                st.write("Recording... (Click 'Stop Recording' when finished)")
                while st.session_state['recording']:
                    data = stream.read(FRAMES_PER_BUFFER)
                    st.session_state['frames'].append(data)
                    st.experimental_rerun()

            if Path('recorded_audio.wav').is_file():
                st.audio('recorded_audio.wav', format='audio/wav')
                st.download_button(
                    label="Download recorded audio",
                    data=open('recorded_audio.wav', 'rb'),
                    file_name='recorded_audio.wav',
                    mime='audio/wav')
                audio = 'recorded_audio.wav'
        else:
            st.write("Not available rn")
        
    elif audio_source == 'Audio file':
        uploaded_file = st.file_uploader("Choose an audio file...", type=["mp3", "wav", "m4a"])
        if uploaded_file is not None:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[-1])
            with open(temp_file.name, 'wb') as f:
                f.write(uploaded_file.read())
            audio = temp_file.name
            st.audio(audio, format=f'audio/{os.path.splitext(uploaded_file.name)[-1][1:]}')

    if st.button("Convert to Text") and 'audio' in locals():
        with st.spinner("Processing..."):
            try:
                # Transcribe
                transcription = transcribe_audio(audio)
                
                # Format
                formatted_text = format_text(transcription)
                
                # Display
                st.markdown(formatted_text, unsafe_allow_html=True)
                
                # Provide download option for plain text
                st.download_button(
                    label="Download Formatted Text",
                    data=formatted_text,
                    file_name="lecture_transcript.docx",
                    mime="text/plain"
                )
                st.success("Conversion complete!")
                st.balloons()
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

with tab2:
    st.header("🔊 Create Voice Recording")
    st.markdown("Enter text or upload a file to convert to audio.")
    
    text_source = st.radio("Select text source:", ('Text Input', 'Text File'))

    text = ""
    if text_source == 'Text Input':
        text = st.text_area("Enter your text here:")
    elif text_source == 'Text File':
        uploaded_file = st.file_uploader("Choose a text file...", type="txt")
        if uploaded_file is not None:
            text = uploaded_file.read().decode('utf-8')

    voice_options = {
    "Cheerful Princess": {"rate": 180, "volume": 1.0, "voice_index": 1},  # Faster, female voice
    "Grumpy Dwarf": {"rate": 120, "volume": 0.8, "voice_index": 0},  # Slower, male voice, lower volume
    "Wise Fairy": {"rate": 150, "volume": 0.9, "voice_index": 1},  # Moderate speed, female voice
    "Villainous Sorcerer": {"rate": 140, "volume": 1.0, "voice_index": 0},  # Slightly slow, male voice
    "Adventurous Hero": {"rate": 170, "volume": 1.0, "voice_index": 0},  # Fast, male voice
}

    voice_option = st.selectbox('Choose a voice', list(voice_options.keys()))

    if st.button("Convert to Speech") and text:
        with st.spinner("Converting text to audio..."):
            voice_settings = voice_options[voice_option]
            audio_buffer = text_to_speech(text, voice_settings)
            st.success("Conversion complete!")
            st.audio(audio_buffer, format='audio/mp3')
            st.download_button(
                label="Download Audio",
                data=audio_buffer,
                file_name="lecture_audio.mp3",
                mime="audio/mp3"
            )
        st.balloons()

st.divider()
st.markdown("Made with ❤️ for students")