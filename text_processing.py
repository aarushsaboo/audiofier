import random
import re

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
