from tools.text_stats import compute_text_stats


def test_compute_text_stats_basic():
    text = "Hello world. This is a test. Testing stats."

    stats = compute_text_stats(text)

    assert stats["characters"] == len(text)
    assert stats["sentences"] == 3
    assert stats["words"] > 0
    assert stats["unique_words"] > 0
    assert stats["average_word_length"] > 0


def test_compute_text_stats_empty():
    stats = compute_text_stats("")

    assert stats["characters"] == 0
    assert stats["words"] == 0
    assert stats["sentences"] == 0
    assert stats["average_word_length"] == 0.0
