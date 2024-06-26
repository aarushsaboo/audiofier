import streamlit as st
import os
from pathlib import Path
import tempfile

from text_processing import *
from audio_processing import *

def display_audio_to_text_tab(stream):
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
            st.write("Sorry. We don't have microphone access")
        
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

def display_text_to_audio_tab():
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
            audio_file_path = text_to_speech(text, voice_settings)
            st.success("Conversion complete!")
            st.audio(audio_file_path, format='audio/mp3')
            st.download_button(
                label="Download Audio",
                data=open(audio_file_path, "rb"),
                file_name="lecture_audio.mp3",
                mime="audio/mp3"
            )
        os.remove(audio_file_path)  # Explicitly delete temporary audio file
        st.balloons()