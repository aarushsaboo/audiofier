import os
import streamlit as st
import tempfile
from pathlib import Path
import os
from ui_components import *

stream = None
# At the start of your script
if 'audio_available' not in st.session_state:
    try:
        p = pyaudio.PyAudio()
        # Just test if we can open a stream
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
        # st.warning("Live audio recording is not available in this environment. Please use the file upload option.")

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
    display_audio_to_text_tab(stream)

with tab2:
    display_text_to_audio_tab()

st.divider()
st.markdown("Made with ❤️ for students")