import unittest
from src.tokenizer import word_tokenize, normalize_text, pos_tag, named_entity_recognition

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

class TestPOSTag(unittest.TestCase):

    def test_single_word(self):
        text = "పుస్తకం"
        expected = [("పుస్తకం", "NOUN")]
        self.assertEqual(pos_tag(text), expected)

    def test_simple_sentence(self):
        text = "నేను పుస్తకం చదువుతున్నాను."
        expected = [
            ("నేను", "X"),
            ("పుస్తకం", "NOUN"),
            ("చదువుతున్నాను", "VERB"),
            (".", "PUNCT")
        ]
        self.assertEqual(pos_tag(text), expected)

class TestNER(unittest.TestCase):

    def test_person_names(self):
        text = "రాముడు సీత హనుమంతుడు"
        expected = [
            ("రాముడు", "PERSON"),
            ("సీత", "PERSON"),
            ("హనుమంతుడు", "PERSON")
        ]
        self.assertEqual(named_entity_recognition(text), expected)


if __name__ == "__main__":
    unittest.main()