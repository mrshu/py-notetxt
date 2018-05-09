import os
from pathlib import Path
import sys
sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import notetxt  # noqa


def test_basic_load_from_dir():
    notes = notetxt.load_from_dir('./tests/test-notedir/')
    assert len(notes) > 0
    assert len(notes[0].tags) > 0
    assert notes[0].title == 'Test note'
    assert notes[0].tags == {'another-tag', 'some-tag'}


def test_note_title_very_long():
    filepath = './tests/test-notedir/notes/test-note-very-long.md'
    dirpath = './tests/test-notedir/'
    note = notetxt.note_from_path(Path(filepath), Path(dirpath))
    assert note is None


def test_note_wrong_filetype():
    filepath = './tests/test-notedir/notes/otherfile.pdf'
    dirpath = './tests/test-notedir/'
    note = notetxt.note_from_path(Path(filepath), Path(dirpath))
    assert note is None


def test_note_wrong_filetype_again():
    filepath = './tests/test-notedir/notes/otherfile.tex'
    dirpath = './tests/test-notedir/'
    note = notetxt.note_from_path(Path(filepath), Path(dirpath))
    assert note is None


def test_note_add_tag():
    notes = notetxt.load_from_dir('./tests/test-notedir/')
    assert notes[0].tags == {'another-tag', 'some-tag'}

    notes[0].add_tag('special-tag')
    notes[0].save_tags()
    assert notes[0].tags == {'another-tag', 'some-tag', 'special-tag'}
    assert Path('./tests/test-notedir/special-tag/').is_dir()

    notes[0].remove_tag('special-tag')
    notes[0].save_tags()
    assert notes[0].tags == {'another-tag', 'some-tag'}
    assert not Path('./tests/test-notedir/special-tag/test-note.md').exists()


def test_note_add_deep_tag():
    notes = notetxt.load_from_dir('./tests/test-notedir/')
    assert notes[0].tags == {'another-tag', 'some-tag'}

    notes[0].add_tag('deep/tag')
    notes[0].save_tags()
    assert notes[0].tags == {'another-tag', 'some-tag', 'deep/tag'}
    assert Path('./tests/test-notedir/deep/tag/').is_dir()

    notes[0].remove_tag('deep/tag')
    notes[0].save_tags()
    assert notes[0].tags == {'another-tag', 'some-tag'}
    assert not Path('./tests/test-notedir/deep/tag/test-note.md').exists()
