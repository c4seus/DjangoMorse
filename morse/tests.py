from django.test import TestCase
from django.urls import reverse

class MorseViewTest(TestCase):
    def test_homepage_status_code(self):
        """Test that the homepage loads successfully"""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
    
    def test_homepage_contains_expected_content(self):
        """Test that the homepage contains expected content"""
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Morse Code Application")
        self.assertContains(response, "Enter text here...")
    
    def test_text_to_morse_conversion(self):
        """Test POST request for text to morse conversion"""
        response = self.client.post(reverse("home"), {
            'input_text': 'HELLO',
            'action': 'convert',
            'mode': 'text_to_morse'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, ".... . .-.. .-.. ---")
    
    def test_morse_to_text_conversion(self):
        """Test POST request for morse to text conversion"""
        response = self.client.post(reverse("home"), {
            'input_text': '.... . .-.. .-.. ---',
            'action': 'convert',
            'mode': 'morse_to_text'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "HELLO")
    
    def test_empty_input_post(self):
        """Test POST request with empty input"""
        response = self.client.post(reverse("home"), {
            'input_text': '',
            'action': 'convert'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter some text")
    
    def test_invalid_morse_input(self):
        """Test POST request with invalid morse code"""
        response = self.client.post(reverse("home"), {
            'input_text': 'invalid morse',
            'action': 'convert',
            'mode': 'morse_to_text'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "doesn't appear to be valid morse code")
    
    def test_text_audio_download(self):
        """Test POST request for audio download from text"""
        response = self.client.post(reverse("home"), {
            'input_text': 'TEST',
            'action': 'download',
            'mode': 'text_to_morse'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'audio/wav')
        self.assertIn('attachment', response['Content-Disposition'])
    
    def test_morse_audio_download(self):
        """Test POST request for audio download from morse"""
        response = self.client.post(reverse("home"), {
            'input_text': '- . ... -',
            'action': 'download',
            'mode': 'morse_to_text'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'audio/wav')
        self.assertIn('attachment', response['Content-Disposition'])
    
    def test_morse_with_word_separators(self):
        """Test morse code with different word separators"""
        response = self.client.post(reverse("home"), {
            'input_text': '.... . .-.. .-.. --- / .-- --- .-. .-.. -..',
            'action': 'convert',
            'mode': 'morse_to_text'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "HELLO WORLD")