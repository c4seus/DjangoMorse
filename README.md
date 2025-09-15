# DjangoMorse

A Django web application that converts text to Morse code and vice versa, with audio generation capabilities.

## Features

- **Bidirectional Conversion**: Convert text to Morse code AND Morse code back to text
- **Audio Generation**: Generate and download WAV audio files of Morse code signals
- **Web Interface**: Clean, responsive web interface with mode switching
- **Real-time Conversion**: Instant conversion display with visual feedback
- **Input Validation**: Automatic detection and validation of Morse code input
- **Error Handling**: Comprehensive error messages and graceful failure handling

## Technical Details

### Morse Code Implementation
- Uses standard International Morse Code mapping
- Supports letters A-Z and digits 0-9
- Bidirectional conversion with proper parsing
- Word separation handling with multiple formats (spaces, `/` separator)
- Unknown Morse sequences marked with `?`

### Timing Standards
- **Dot**: 0.2 seconds
- **Dash**: 0.6 seconds (3x dot length)
- **Gap between signals**: 0.2 seconds
- **Gap between letters**: 0.6 seconds
- **Gap between words**: 1.4 seconds

### Audio Generation
- **Frequency**: 800 Hz sine wave
- **Sample Rate**: 44.1 kHz
- **Format**: 16-bit mono WAV
- **Amplitude**: 50% to prevent distortion
- **Library**: NumPy for signal generation, wave module for file creation

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd DjangoMorse
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

6. Open your browser and navigate to `http://127.0.0.1:8000`

## Usage

### Text to Morse Code
1. Select "Text to Morse" mode (default)
2. Enter text in the input field
3. Click **"Convert"** to see the Morse code representation
4. Click **"Download Audio"** to generate and download a WAV file

### Morse Code to Text
1. Select "Morse to Text" mode
2. Enter Morse code using dots (.) and dashes (-)
3. Separate letters with spaces
4. Separate words with `/` or multiple spaces
5. Click **"Convert"** to see the decoded text
6. Click **"Download Audio"** to generate audio of the decoded text

### Morse Code Input Format
- Use `.` for dots and `-` for dashes
- Separate letters with single spaces: `.- -...`
- Separate words with `/` or multiple spaces: `.- / -...` or `.-   -...`
- Example: `.... . .-.. .-.. --- / .-- --- .-. .-.. -..` = "HELLO WORLD"

## Project Structure

```
DjangoMorse/
├── djangomorse/           # Main Django project
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── morse/                 # Morse code application
│   ├── views.py          # Main logic and audio generation
│   ├── urls.py           # URL routing
│   ├── tests.py          # Unit tests
│   └── templates/morse/
│       └── home.html      # Main UI
├── static/                # Static files (CSS, JS, images)
│   └── css/
│       └── style.css
├── manage.py
└── README.md
```

> **Note:** Static files are now served from `static/`, not `templates/static/`.  
> Use `{% load static %}` at the top of your template and `{% static 'css/style.css' %}` to reference your CSS files.

## API Reference

### Main View: `MorseController`
- **GET `/`**: Display the main interface
- **POST `/`**: Process form submissions with parameters:
  - `input_text`: Text or Morse code to convert
  - `mode`: Conversion mode (`text_to_morse` or `morse_to_text`)
  - `action`: Action to perform (`convert` or `download`)

### Core Functions

#### Conversion Functions
- `text_to_morse_code(text)`: Convert text to Morse code string with proper spacing
- `morse_to_text_code(morse)`: Convert Morse code string back to readable text
- `is_morse_code(text)`: Validate if input appears to be valid Morse code

#### Audio Generation Functions
- `text_to_morse_wav(text)`: Generate WAV audio buffer from text
- `make_tone(duration)`: Generate sine wave tone of specified duration
- `make_silence(duration)`: Generate silence of specified duration

### Response Formats

#### Successful Conversion
```python
{
    'input_text': 'original input',
    'converted_text': 'conversion result',
    'mode': 'conversion_mode'
}
```

#### Error Response
```python
{
    'input_text': 'original input',
    'mode': 'conversion_mode',
    'error': 'error message'
}
```

#### Audio Download
- Content-Type: `audio/wav`
- Content-Disposition: `attachment; filename="text_morse.wav"`

## Input Validation

### Text to Morse
- Automatically converts to uppercase
- Ignores unsupported characters
- Handles multiple spaces as word separators

### Morse to Text
- Validates input contains only dots, dashes, spaces, and `/`
- Normalizes different word separator formats
- Marks unknown Morse sequences with `?`
- Provides helpful error messages for invalid input

## Error Handling

The application handles various error scenarios:
- Empty input validation
- Invalid Morse code format detection
- Audio generation failures
- File download errors
- Unexpected conversion errors

## Testing

Run the test suite:
```bash
python manage.py test morse
```

Tests should cover:
- Homepage loading and template rendering
- Text to Morse conversion accuracy
- Morse to text conversion accuracy
- Input validation and error handling
- Audio file generation
- Mode switching functionality
- Edge cases and invalid inputs

## Dependencies

- **Django 5.2.6+**: Web framework
- **NumPy**: Numerical computing for audio generation
- **Python 3.8+**: Runtime environment
- **wave**: Built-in Python module for WAV file handling
- **io**: Built-in Python module for in-memory file operations
- **re**: Built-in Python module for regex pattern matching

## Configuration

### Audio Settings (in views.py)
```python
FREQ = 800          # Tone frequency in Hz
DOT = 0.2          # Dot duration in seconds
DASH = DOT * 3     # Dash duration (3x dot)
GAP = DOT          # Gap between dots/dashes
LETTER_GAP = DOT * 3  # Gap between letters
WORD_GAP = DOT * 7    # Gap between words
SAMPLE_RATE = 44100   # Audio sample rate
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`python manage.py test`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Submit a pull request



## License

This project is open source and available under the MIT License.

## Educational Purpose

This project demonstrates:
- Django class-based views and form handling
- Bidirectional data conversion and validation
- Template rendering with dynamic content
- Audio signal generation with NumPy
- File downloads via HTTP responses
- Input validation and error handling
- Unit testing in Django applications
- Clean code organization and documentation
- User experience design for web applications

## Morse Code Reference

### Letters
```
A .-    B -...  C -.-.  D -..   E .     F ..-.
G --.   H ....  I ..    J .---  K -.-   L .-..
M --    N -.    O ---   P .--.  Q --.-  R .-.
S ...   T -     U ..-   V ...-  W .--   X -..-
Y -.--  Z --..
```

### Numbers
```
0 -----  1 .----  2 ..---  3 ...--  4 ....-
5 .....  6 -....  7 --...  8 ---..  9 ----.
```