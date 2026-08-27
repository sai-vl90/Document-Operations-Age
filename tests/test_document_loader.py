import docx

from tools.document_loader import DocumentLoader


def test_load_txt(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("Hello world.", encoding="utf-8")

    loader = DocumentLoader()
    text = loader.load(str(file_path))

    assert "Hello world." in text


def test_load_docx(tmp_path):
    file_path = tmp_path / "sample.docx"

    document = docx.Document()
    document.add_paragraph("This is a test paragraph.")
    document.save(str(file_path))

    loader = DocumentLoader()
    text = loader.load(str(file_path))

    assert "This is a test paragraph." in text


def test_unsupported_extension(tmp_path):
    file_path = tmp_path / "sample.xyz"
    file_path.write_text("data", encoding="utf-8")

    loader = DocumentLoader()

    try:
        loader.load(str(file_path))
        assert False, "Expected ValueError for unsupported extension"
    except ValueError:
        pass


def test_missing_file():
    loader = DocumentLoader()

    try:
        loader.load("does_not_exist.txt")
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError:
        pass
