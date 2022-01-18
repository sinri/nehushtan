from nehushtan.wave.Note import Note
from nehushtan.wave.SimpleComposer import SimpleComposer

if __name__ == '__main__':
    composer = SimpleComposer(r"/Users/leqee/code/nehushtan/debug/wave/test-1.wav")
    # composer.addSound(262, 4)
    # composer.addSound(294, 4)
    # composer.addSound(330, 4)
    # composer.addSound(349, 4)
    # composer.addSound(392, 4)

    composer.add_note(Note(name="E"))
    composer.add_note(Note(name="E"))
    composer.add_note(Note(name="F"))
    composer.add_note(Note(name="G"))
    composer.add_note(Note(name="G"))
    composer.add_note(Note(name="F"))
    composer.add_note(Note(name="E"))
    composer.add_note(Note(name="D"))
    composer.add_note(Note(name="C"))
    composer.add_note(Note(name="C"))
    composer.add_note(Note(name="D"))
    composer.add_note(Note(name="E"))
    composer.add_note(Note(name="E", beats=1.5))
    composer.add_note(Note(name="D", beats=0.5))
    composer.add_note(Note(name="D", beats=2))

    composer.close()
