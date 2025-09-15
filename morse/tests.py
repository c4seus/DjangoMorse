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
    
    def test_morse_conversion_post(self):
        """Test POST request for morse code conversion"""
        response = self.client.post(reverse("home"), {
            'word': 'HELLO',
            'action': 'convert'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, ".... . .-.. .-.. ---")
    
    def test_empty_word_post(self):
        """Test POST request with empty word"""
        response = self.client.post(reverse("home"), {
            'word': '',
            'action': 'convert'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter some text")
    
    def test_audio_download_post(self):
        """Test POST request for audio download"""
        response = self.client.post(reverse("home"), {
            'word': 'TEST',
            'action': 'download'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'audio/wav')
        self.assertIn('attachment', response['Content-Disposition'])