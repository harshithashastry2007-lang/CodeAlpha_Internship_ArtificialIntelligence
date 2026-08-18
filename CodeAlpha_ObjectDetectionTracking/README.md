# 🎯 AI Object Detection & Tracking

An AI-powered real-time **Object Detection and Tracking System** developed using **YOLO, OpenCV, Python, and Streamlit** as part of the **CodeAlpha Artificial Intelligence Internship**.

## 🚀 Features

- 🎯 Real-time object detection using YOLO
- 📹 Live webcam-based detection and tracking
- 🎬 Video file object detection
- 🔄 Multi-object tracking with unique tracking IDs
- 📦 Bounding boxes with object labels
- 📊 Confidence scores for detected objects
- ⚙️ Adjustable confidence threshold
- 💻 Interactive Streamlit interface

## 🛠️ Technologies Used

- Python
- YOLO (Ultralytics)
- OpenCV
- Streamlit
- Computer Vision
- Object Detection & Tracking

## 📦 Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## ▶️ How to Run

1. Clone or download this repository.

2. Open the project folder in VS Code.

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Run the Streamlit application:

```bash
python -m streamlit run app.py
```

5. Open the local URL displayed in the terminal, usually:

```text
http://localhost:8501
```

6. Select **Video File** or **Webcam** as the input source.

7. Adjust the confidence threshold if required.

8. Start detection and tracking.

## 🧠 How It Works

1. The application captures frames from the webcam or an uploaded video.
2. OpenCV processes the incoming video frames.
3. YOLO analyzes each frame and detects supported objects.
4. Bounding boxes, class labels, and confidence scores are displayed.
5. The tracking system assigns unique IDs to detected objects.
6. Objects are continuously tracked across consecutive frames.
7. The processed frames are displayed through the Streamlit interface in real time.

## 📂 Project Structure

```text
CodeAlpha_ObjectDetectionTracking/
│
├── app.py
├── requirements.txt
└── README.md
```

## 👩‍💻 Developer

**Harshitha M**  
B.E. Computer Science & Engineering  
**(Artificial Intelligence & Machine Learning)**

Developed as part of the **CodeAlpha Artificial Intelligence Internship Program**.