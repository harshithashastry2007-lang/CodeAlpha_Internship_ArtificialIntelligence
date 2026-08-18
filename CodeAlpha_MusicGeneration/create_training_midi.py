from music21 import stream, note, chord, tempo
import os

# Folder to save MIDI files
folder = "training_midi"
os.makedirs(folder, exist_ok=True)

# Notes for different training songs
songs = [
    ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"],
    ["C4", "E4", "G4", "C5", "G4", "E4", "C4"],
    ["G4", "A4", "B4", "C5", "D5", "C5", "B4", "A4"],
    ["E4", "F4", "G4", "A4", "G4", "F4", "E4", "D4"],
    ["C4", "G4", "A4", "F4", "E4", "D4", "C4"]
]

for i, song in enumerate(songs, start=1):

    music = stream.Stream()
    music.append(tempo.MetronomeMark(number=120))

    # Repeat notes to create more training data
    for _ in range(8):
        for n in song:
            music.append(note.Note(n, quarterLength=0.5))

    # Add a few chords
    music.append(chord.Chord(["C4", "E4", "G4"], quarterLength=1))
    music.append(chord.Chord(["F4", "A4", "C5"], quarterLength=1))
    music.append(chord.Chord(["G4", "B4", "D5"], quarterLength=1))

    filename = os.path.join(folder, f"training_song_{i}.mid")

    music.write("midi", fp=filename)

    print(f"Created: {filename}")

print("\n5 MIDI training files created successfully!")