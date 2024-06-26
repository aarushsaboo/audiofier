import whisper
import wave
import pyttsx3
import pyaudio
import streamlit as st

# Audio parameters (unchanged)
FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

def transcribe_audio(audio_file):
    model = whisper.load_model("base")
    result = model.transcribe(audio_file, fp16=False)
    return result["text"]



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
    engine = pyttsx3.init()
    engine.setProperty('rate', voice_settings['rate'])
    engine.setProperty('volume', voice_settings['volume'])
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice_settings['voice_index']].id)
    
    file_name = 'output.mp3'
    engine.save_to_file(text, file_name)
    engine.runAndWait()
    return file_name