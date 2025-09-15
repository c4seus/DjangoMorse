# DjangoMorse

A Django web application that converts text to Morse code and generates audio files of the Morse code signals.

## Features

- **Text to Morse Code Conversion**: Convert any text input into standard International Morse Code
- **Audio Generation**: Generate and download WAV audio files of Morse code signals
- **Web Interface**: Clean, responsive web interface for easy interaction
- **Real-time Conversion**: Instant conversion display with visual feedback

## Technical Details

### Morse Code Implementation
- Uses standard International Morse Code mapping
- Supports letters A-Z and digits 0-9
- Proper timing ratios:
  - Dot: 0.2 seconds
  - Dash: 0.6 seconds (3x dot length)
  - Gap between signals: 0.2 seconds
  - Gap between letters: 0.6 seconds
  - Gap between words: 1.4 seconds

### Audio Generation
- **Frequency**: 800 Hz sine wave
- **Sample Rate**: 44.1 kHz
- **Format**: 16-bit mono WAV
- **Library**: NumPy for signal generation

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
pip install django numpy
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

1. Enter text in the input field
2. Click **"Convert to Morse"** to see the Morse code representation
3. Click **"Download Audio"** to generate and download a WAV file of the Morse code

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
│   └── templates/
│       └── morse/
│           └── home.html # Main interface
├── manage.py
└── README.md
```

## API Reference

### Main View: `MorseController`
- **GET `/`**: Display the main interface
- **POST `/`**: Process form submissions
  - `action=convert`: Convert text to Morse code
  - `action=download`: Generate and download audio file

### Core Functions
- `text_to_morse_code(text)`: Convert text to Morse code string
- `text_to_morse_wav(text)`: Generate WAV audio buffer
- `make_tone(duration)`: Generate sine wave tone
- `make_silence(duration)`: Generate silence

## Testing

Run the test suite:
```bash
python manage.py test morse
```

Tests cover:
- Homepage loading
- Content verification
- Morse code conversion
- Audio file generation
- Error handling

## Dependencies

- **Django 5.2.6**: Web framework
- **NumPy**: Numerical computing for audio generation
- **Python 3.13+**: Runtime environment

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is open source and available under the MIT License.

## Educational Purpose

This project demonstrates:
- Django class-based views
- Template rendering and form handling
- Audio signal generation with NumPy
- File downloads via HTTP responses
- Unit testing in Django
- Proper project structure and documentation