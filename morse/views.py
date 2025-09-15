import numpy as np
import wave
import io
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render

MORSE_CODE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".",
    "F": "..-.", "G": "--.", "H": "....", "I": "..", "J": ".---",
    "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---",
    "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-",
    "U": "..-", "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--",
    "Z": "--..",
    "0": "-----", "1": ".----", "2": "..---", "3": "...--",
    "4": "....-", "5": ".....", "6": "-....", "7": "--...",
    "8": "---..", "9": "----."
}

FREQ = 800
DOT = 0.2
DASH = DOT * 3
GAP = DOT
LETTER_GAP = DOT * 3
WORD_GAP = DOT * 7
SAMPLE_RATE = 44100

def make_tone(duration):
    t = np.linspace(0, duration, int(SAMPLE_RATE*duration), False)
    return 0.5 * np.sin(FREQ * 2 * np.pi * t)

def make_silence(duration):
    return np.zeros(int(SAMPLE_RATE*duration))

def text_to_morse_wav(text):
    text = text.upper()
    audio = np.array([], dtype=np.float32)
    
    for char in text:
        if char == " ":
            audio = np.concatenate((audio, make_silence(WORD_GAP)))
        elif char in MORSE_CODE:
            for symbol in MORSE_CODE[char]:
                if symbol == ".":
                    audio = np.concatenate((audio, make_tone(DOT)))
                elif symbol == "-":
                    audio = np.concatenate((audio, make_tone(DASH)))
                audio = np.concatenate((audio, make_silence(GAP)))
            audio = np.concatenate((audio, make_silence(LETTER_GAP - GAP)))
    
    audio_int16 = (audio * 32767).astype(np.int16)
    buffer = io.BytesIO()
    with wave.open(buffer, "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SAMPLE_RATE)
        f.writeframes(audio_int16.tobytes())
    buffer.seek(0)
    return buffer

def text_to_morse_code(text):
    """Convert text to morse code string"""
    text = text.upper()
    morse_parts = []
    
    for char in text:
        if char == " ":
            morse_parts.append(" / ")  # Use / to separate words
        elif char in MORSE_CODE:
            morse_parts.append(MORSE_CODE[char])
    
    return " ".join(morse_parts)

class MorseController(View):
    template_name = "morse/home.html"
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        word = request.POST.get("word", "").strip()
        action = request.POST.get("action", "convert")  # Default action
        
        if not word:
            return render(request, self.template_name, {
                "error": "Please enter some text to convert."
            })
        
        # Convert to morse code
        morse = text_to_morse_code(word)
        
        if action == "download":
            # Generate and return WAV file
            try:
                wav_buffer = text_to_morse_wav(word)
                response = HttpResponse(wav_buffer.getvalue(), content_type="audio/wav")
                response["Content-Disposition"] = f'attachment; filename="{word.replace(" ", "_")}_morse.wav"'
                return response
            except Exception as e:
                return render(request, self.template_name, {
                    "word": word,
                    "morse": morse,
                    "error": f"Error generating audio: {str(e)}"
                })
        else:
            # Just show the morse code conversion
            return render(request, self.template_name, {
                "word": word,
                "morse": morse
            })