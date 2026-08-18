import streamlit as st
import numpy as np
import tempfile
import os
import io

from music21 import converter, instrument, note, chord, stream
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Embedding
from tensorflow.keras.optimizers import Adam


# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------
st.set_page_config(
    page_title="AI Music Generator",
    page_icon="🎵",
    layout="centered"
)


# -------------------------------------------------
# CUSTOM STYLE
# -------------------------------------------------
st.markdown("""
<style>
.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 700;
}

.subtitle {
    text-align: center;
    color: gray;
    font-size: 17px;
    margin-bottom: 25px;
}

.footer {
    text-align: center;
    color: gray;
    font-size: 14px;
    margin-top: 30px;
}

div.stButton > button {
    border-radius: 10px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)


# -------------------------------------------------
# TITLE
# -------------------------------------------------
st.markdown(
    '<div class="main-title">🎵 AI Music Generator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Generate original music using Deep Learning and LSTM'
    '</div>',
    unsafe_allow_html=True
)


# -------------------------------------------------
# EXTRACT NOTES FROM MIDI
# -------------------------------------------------
def extract_notes(uploaded_files):

    notes = []

    for uploaded_file in uploaded_files:

        # Save uploaded MIDI temporarily
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mid"
        ) as temp_file:

            temp_file.write(uploaded_file.getvalue())
            temp_path = temp_file.name

        try:
            midi = converter.parse(temp_path)

            parts = instrument.partitionByInstrument(midi)

            if parts:
                elements = parts.parts[0].recurse()
            else:
                elements = midi.flat.notes

            for element in elements:

                if isinstance(element, note.Note):
                    notes.append(str(element.pitch))

                elif isinstance(element, chord.Chord):
                    notes.append(
                        ".".join(
                            str(n)
                            for n in element.normalOrder
                        )
                    )

        except Exception as e:
            st.warning(
                f"Could not process {uploaded_file.name}"
            )

        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    return notes


# -------------------------------------------------
# PREPARE TRAINING DATA
# -------------------------------------------------
def prepare_sequences(notes, sequence_length=20):

    unique_notes = sorted(set(notes))

    note_to_int = {
        note_name: number
        for number, note_name in enumerate(unique_notes)
    }

    network_input = []
    network_output = []

    for i in range(
        0,
        len(notes) - sequence_length
    ):

        sequence_in = notes[
            i:i + sequence_length
        ]

        sequence_out = notes[
            i + sequence_length
        ]

        network_input.append(
            [
                note_to_int[note_name]
                for note_name in sequence_in
            ]
        )

        network_output.append(
            note_to_int[sequence_out]
        )

    return (
        np.array(network_input),
        np.array(network_output),
        unique_notes
    )


# -------------------------------------------------
# BUILD LSTM MODEL
# -------------------------------------------------
def build_model(vocab_size, sequence_length):

    model = Sequential([
        Embedding(
            input_dim=vocab_size,
            output_dim=64,
            input_length=sequence_length
        ),

        LSTM(
            128,
            return_sequences=True
        ),

        Dropout(0.2),

        LSTM(128),

        Dropout(0.2),

        Dense(
            128,
            activation="relu"
        ),

        Dense(
            vocab_size,
            activation="softmax"
        )
    ])

    model.compile(
        loss="sparse_categorical_crossentropy",
        optimizer=Adam(
            learning_rate=0.001
        ),
        metrics=["accuracy"]
    )

    return model


# -------------------------------------------------
# GENERATE NOTES
# -------------------------------------------------
def generate_notes(
    model,
    network_input,
    unique_notes,
    number_of_notes
):

    int_to_note = {
        number: note_name
        for number, note_name
        in enumerate(unique_notes)
    }

    start = np.random.randint(
        0,
        len(network_input)
    )

    pattern = list(
        network_input[start]
    )

    generated_notes = []

    for _ in range(number_of_notes):

        prediction_input = np.array(
            [pattern]
        )

        prediction = model.predict(
            prediction_input,
            verbose=0
        )[0]

        index = np.random.choice(
            len(prediction),
            p=prediction
        )

        result = int_to_note[index]

        generated_notes.append(result)

        pattern.append(index)

        pattern = pattern[1:]

    return generated_notes


# -------------------------------------------------
# CREATE MIDI FILE
# -------------------------------------------------
def create_midi(
    generated_notes,
    tempo_value
):

    output_notes = []

    offset = 0

    for pattern in generated_notes:

        # Chord
        if "." in pattern:

            chord_notes = []

            for current_note in pattern.split("."):

                new_note = note.Note(
                    int(current_note)
                )

                new_note.storedInstrument = (
                    instrument.Piano()
                )

                chord_notes.append(new_note)

            new_chord = chord.Chord(
                chord_notes
            )

            new_chord.offset = offset

            output_notes.append(
                new_chord
            )

        # Single note
        else:

            new_note = note.Note(
                pattern
            )

            new_note.offset = offset

            new_note.storedInstrument = (
                instrument.Piano()
            )

            output_notes.append(
                new_note
            )

        offset += 0.5

    midi_stream = stream.Stream(
        output_notes
    )

    # Add tempo
    from music21 import tempo

    midi_stream.insert(
        0,
        tempo.MetronomeMark(
            number=tempo_value
        )
    )

    temp_output = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mid"
    )

    temp_output.close()

    midi_stream.write(
        "midi",
        fp=temp_output.name
    )

    with open(
        temp_output.name,
        "rb"
    ) as file:

        midi_bytes = file.read()

    os.remove(
        temp_output.name
    )

    return midi_bytes


# -------------------------------------------------
# USER INTERFACE
# -------------------------------------------------
st.subheader("📂 Upload Training Music")

uploaded_files = st.file_uploader(
    "Upload MIDI files",
    type=["mid", "midi"],
    accept_multiple_files=True
)

st.caption(
    "Upload multiple MIDI files for better AI-generated music."
)


# -------------------------------------------------
# SETTINGS
# -------------------------------------------------
st.subheader("⚙️ Music Generation Settings")

col1, col2 = st.columns(2)

with col1:

    epochs = st.slider(
        "Training Epochs",
        min_value=1,
        max_value=20,
        value=5
    )

with col2:

    generated_length = st.slider(
        "Number of Generated Notes",
        min_value=20,
        max_value=150,
        value=60
    )


tempo_value = st.slider(
    "🎼 Tempo (BPM)",
    min_value=60,
    max_value=180,
    value=120
)


# -------------------------------------------------
# GENERATE BUTTON
# -------------------------------------------------
if st.button(
    "🎵 Train AI & Generate Music",
    use_container_width=True,
    type="primary"
):

    if not uploaded_files:

        st.warning(
            "⚠️ Please upload at least one MIDI file."
        )

    else:

        with st.spinner(
            "Extracting musical notes..."
        ):

            notes = extract_notes(
                uploaded_files
            )


        if len(notes) < 50:

            st.error(
                "❌ Not enough musical notes found. "
                "Please upload larger or additional MIDI files."
            )

        else:

            st.success(
                f"✅ Extracted {len(notes)} musical notes."
            )


            sequence_length = min(
                20,
                max(
                    10,
                    len(notes) // 5
                )
            )


            network_input, network_output, unique_notes = (
                prepare_sequences(
                    notes,
                    sequence_length
                )
            )


            if len(network_input) == 0:

                st.error(
                    "Not enough data to create training sequences."
                )

            else:

                st.write(
                    f"🎹 Unique Notes/Chords: "
                    f"**{len(unique_notes)}**"
                )

                st.write(
                    f"🧠 Training Sequences: "
                    f"**{len(network_input)}**"
                )


                with st.spinner(
                    "Training LSTM neural network..."
                ):

                    model = build_model(
                        len(unique_notes),
                        sequence_length
                    )

                    history = model.fit(
                        network_input,
                        network_output,
                        epochs=epochs,
                        batch_size=32,
                        verbose=0
                    )


                st.success(
                    "✅ AI model training completed!"
                )


                final_accuracy = (
                    history.history["accuracy"][-1]
                    * 100
                )

                st.metric(
                    "Training Accuracy",
                    f"{final_accuracy:.2f}%"
                )


                with st.spinner(
                    "AI is composing new music..."
                ):

                    generated_notes = generate_notes(
                        model,
                        network_input,
                        unique_notes,
                        generated_length
                    )


                    midi_bytes = create_midi(
                        generated_notes,
                        tempo_value
                    )


                st.success(
                    "🎉 New AI music generated successfully!"
                )


                # -----------------------------------
                # DISPLAY GENERATED NOTES
                # -----------------------------------
                st.subheader(
                    "🎼 Generated Music Sequence"
                )

                st.write(
                    " → ".join(
                        generated_notes[:30]
                    )
                )

                if len(generated_notes) > 30:

                    st.caption(
                        "Showing first 30 generated notes."
                    )


                # -----------------------------------
                # DOWNLOAD MIDI
                # -----------------------------------
                st.download_button(
                    label="⬇️ Download Generated MIDI",
                    data=midi_bytes,
                    file_name="AI_Generated_Music.mid",
                    mime="audio/midi",
                    use_container_width=True
                )


# -------------------------------------------------
# INFORMATION
# -------------------------------------------------
st.divider()

with st.expander(
    "🧠 How does the AI Music Generator work?"
):

    st.write("""
    1. MIDI files are uploaded as training data.
    2. Musical notes and chords are extracted using music21.
    3. The notes are converted into numerical sequences.
    4. An LSTM neural network learns musical patterns.
    5. The trained AI model predicts new note sequences.
    6. The generated sequence is converted into a MIDI file.
    """)


# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.divider()

st.markdown(
    """
    <div class="footer">
    Developed by <b>Harshitha M</b><br>
    CodeAlpha Artificial Intelligence Internship<br>
    AI Music Generation Project
    </div>
    """,
    unsafe_allow_html=True
)