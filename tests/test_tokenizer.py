import unittest
from src.tokenizer import word_tokenize, normalize_text

class TestWordTokenizer(unittest.TestCase):

    def test_basic_tokenization(self):
        text = "నేను బిట్స్ కాలేజీలో చదువుతున్నాను."
        expected = ["నేను", "బిట్స్", "కాలేజీలో", "చదువుతున్నాను", "."]
        self.assertEqual(word_tokenize(text), expected)

    def test_with_punctuation(self):
        text = "నేను అన్నం, రసం మరియు సాంబారుతో భోజనం చేస్తున్నాను! "
        expected = ["నేను", "అన్నం", ",", "రసం", "మరియు", "సాంబారుతో", "భోజనం", "చేస్తున్నాను", "!"]
        self.assertEqual(word_tokenize(text), expected)

    def test_empty_string(self):
        text = ""
        expected = []
        self.assertEqual(word_tokenize(text), expected)

    def test_only_punctuation(self):
        text = "!?.,"
        expected = ["!", "?", ".", ","]
        self.assertEqual(word_tokenize(text), expected)

class TestTextNormalization(unittest.TestCase):

    def test_remove_extra_spaces(self):
        text = "  నేను   బిట్స్  కాలేజీలో   చదువుతున్నాను.  "
        expected = "నేను బిట్స్ కాలేజీలో చదువుతున్నాను."
        self.assertEqual(normalize_text(text), expected)

    def test_empty_string(self):
        text = ""
        expected = ""
        self.assertEqual(normalize_text(text), expected)

    def test_no_changes_needed(self):
        text = "నేను బిట్స్ కాలేజీలో చదువుతున్నాను."
        expected = "నేను బిట్స్ కాలేజీలో చదువుతున్నాను."
        self.assertEqual(normalize_text(text), expected)

if __name__ == "__main__":
    unittest.main()