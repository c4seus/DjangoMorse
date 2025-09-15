import numpy as np
import wave
import io
import re
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

# Reverse dictionary for morse to text conversion
MORSE_TO_TEXT = {morse: char for char, morse in MORSE_CODE.items()}

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

def morse_to_text_code(morse):
    """Convert morse code to text"""
    # Clean up the input: normalize spaces and handle word separators
    morse = morse.strip()
    
    # Handle different word separators (/, multiple spaces, etc.)
    # Replace common word separators with a standard delimiter
    morse = re.sub(r'\s*/\s*|\s{3,}', ' | ', morse)
    
    # Split into words
    words = morse.split(' | ')
    result_words = []
    
    for word in words:
        if not word.strip():
            continue
            
        # Split word into individual morse letters
        letters = word.split()
        decoded_letters = []
        
        for letter in letters:
            letter = letter.strip()
            if not letter:
                continue
                
            # Convert morse to letter
            if letter in MORSE_TO_TEXT:
                decoded_letters.append(MORSE_TO_TEXT[letter])
            else:
                # Unknown morse code - mark with ?
                decoded_letters.append('?')
        
        if decoded_letters:
            result_words.append(''.join(decoded_letters))
    
    return ' '.join(result_words)

def is_morse_code(text):
    """Check if the input looks like morse code"""
    # Remove spaces and check if it only contains dots, dashes, and /
    cleaned = re.sub(r'[\s/]', '', text)
    return bool(cleaned) and all(c in '.-' for c in cleaned)

class MorseController(View):
    template_name = "home.html"

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        input_text = request.POST.get("input_text", "").strip()
        action = request.POST.get("action", "convert")
        conversion_mode = request.POST.get("mode", "text_to_morse")
        
        if not input_text:
            return render(request, self.template_name, {
                "error": "Please enter some text or morse code to convert."
            })
        
        try:
            if conversion_mode == "morse_to_text":
                # Morse to text conversion
                if not is_morse_code(input_text):
                    return render(request, self.template_name, {
                        "input_text": input_text,
                        "mode": conversion_mode,
                        "error": "Input doesn't appear to be valid morse code. Use dots (.) and dashes (-) separated by spaces."
                    })
                
                converted_text = morse_to_text_code(input_text)
                
                if action == "download":
                    # Generate audio from the original morse input
                    try:
                        # For audio generation, we need to convert back to standard format
                        # and then generate audio from the decoded text
                        wav_buffer = text_to_morse_wav(converted_text)
                        response = HttpResponse(wav_buffer.getvalue(), content_type="audio/wav")
                        response["Content-Disposition"] = f'attachment; filename="{converted_text.replace(" ", "_")}_morse.wav"'
                        return response
                    except Exception as e:
                        return render(request, self.template_name, {
                            "input_text": input_text,
                            "converted_text": converted_text,
                            "mode": conversion_mode,
                            "error": f"Error generating audio: {str(e)}"
                        })
                else:
                    return render(request, self.template_name, {
                        "input_text": input_text,
                        "converted_text": converted_text,
                        "mode": conversion_mode
                    })
            
            else:  # text_to_morse (default)
                # Text to morse conversion
                morse_code = text_to_morse_code(input_text)
                
                if action == "download":
                    try:
                        wav_buffer = text_to_morse_wav(input_text)
                        response = HttpResponse(wav_buffer.getvalue(), content_type="audio/wav")
                        response["Content-Disposition"] = f'attachment; filename="{input_text.replace(" ", "_")}_morse.wav"'
                        return response
                    except Exception as e:
                        return render(request, self.template_name, {
                            "input_text": input_text,
                            "converted_text": morse_code,
                            "mode": conversion_mode,
                            "error": f"Error generating audio: {str(e)}"
                        })
                else:
                    return render(request, self.template_name, {
                        "input_text": input_text,
                        "converted_text": morse_code,
                        "mode": conversion_mode
                    })
                    
        except Exception as e:
            return render(request, self.template_name, {
                "input_text": input_text,
                "mode": conversion_mode,
                "error": f"Conversion error: {str(e)}"
            })