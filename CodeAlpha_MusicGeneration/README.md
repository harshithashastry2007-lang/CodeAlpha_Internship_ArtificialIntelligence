# 🎵 AI Music Generator

An AI-powered Music Generation application developed as part of the **CodeAlpha Artificial Intelligence Internship**.

This project uses **Deep Learning with LSTM neural networks** to learn musical patterns from MIDI files and generate new music sequences automatically.

## ✨ Features

- 🎼 Upload multiple MIDI files as training data
- 🎹 Extract musical notes and chords using `music21`
- 🧠 Train an LSTM-based deep learning model
- 🎵 Generate new AI-created music sequences
- ⚙️ Adjustable training epochs
- 🎶 Adjustable number of generated notes
- ⏱️ Tempo control in BPM
- 📊 Training accuracy display
- ⬇️ Download generated music as a MIDI file
- 🎨 Interactive Streamlit interface

## 🧠 How It Works

1. MIDI files are uploaded as training data.
2. Notes and chords are extracted using `music21`.
3. Musical notes are converted into numerical sequences.
4. An LSTM neural network is trained on those sequences.
5. The trained model predicts and generates new note patterns.
6. The generated sequence is converted back into a MIDI file.
7. The generated MIDI file can be downloaded and played.

## 🛠️ Technologies Used

- Python
- Streamlit
- TensorFlow
- Keras
- LSTM Neural Networks
- NumPy
- music21
- MIDI Processing

## 🚀 How to Run

1. Clone this repository.

2. Install the required packages:

   ```bash
   pip install -r requirements.txt



## 👩‍💻 Developer

**Harshitha M**  
B.E. Computer Science & Engineering 
(Artificial Intelligence & Machine Learning)

Developed as part of the **CodeAlpha Artificial Intelligence Internship Program**.