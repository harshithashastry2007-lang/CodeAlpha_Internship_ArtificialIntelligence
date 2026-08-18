import streamlit as st
import cv2
import tempfile
import os
from ultralytics import YOLO

st.set_page_config(
    page_title="AI Object Detection & Tracking",
    page_icon="🎯",
    layout="wide"
)

st.markdown(
    "<h1 style='text-align:center;'>🎯 AI Object Detection & Tracking</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;color:gray;'>Real-time object detection and tracking using YOLO</p>",
    unsafe_allow_html=True
)

@st.cache_resource
def load_model():
    return YOLO("yolo11n.pt")

model = load_model()

st.sidebar.header("⚙️ Settings")

source_type = st.sidebar.radio(
    "Choose Input Source",
    ["Video File", "Webcam"]
)

confidence = st.sidebar.slider(
    "Confidence Threshold",
    0.1,
    1.0,
    0.4,
    0.05
)

st.sidebar.info(
    "The system detects objects and tracks them using unique tracking IDs."
)

FRAME_WINDOW = st.image([])

if source_type == "Video File":

    uploaded_video = st.file_uploader(
        "📂 Upload a video",
        type=["mp4", "avi", "mov", "mkv"]
    )

    if uploaded_video is not None:

        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp4"
        )

        temp_file.write(uploaded_video.read())
        video_path = temp_file.name

        cap = cv2.VideoCapture(video_path)

        st.success("✅ Video uploaded successfully!")

        if st.button(
            "▶ Start Detection & Tracking",
            use_container_width=True
        ):

            while cap.isOpened():

                success, frame = cap.read()

                if not success:
                    break

                results = model.track(
                    frame,
                    persist=True,
                    conf=confidence,
                    verbose=False
                )

                annotated_frame = results[0].plot()

                annotated_frame = cv2.cvtColor(
                    annotated_frame,
                    cv2.COLOR_BGR2RGB
                )

                FRAME_WINDOW.image(
                    annotated_frame,
                    channels="RGB"
                )

            cap.release()

            st.success(
                "🎉 Object detection and tracking completed!"
            )

        if os.path.exists(video_path):
            os.remove(video_path)

else:

    st.warning(
        "Make sure your webcam is connected and permission is enabled."
    )

    start_camera = st.button(
        "📷 Start Webcam",
        use_container_width=True
    )

    if start_camera:

        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            st.error(
                "❌ Unable to access webcam."
            )

        else:

            stop_button = st.button(
                "⏹ Stop Webcam"
            )

            while cap.isOpened():

                success, frame = cap.read()

                if not success:
                    break

                results = model.track(
                    frame,
                    persist=True,
                    conf=confidence,
                    verbose=False
                )

                annotated_frame = results[0].plot()

                annotated_frame = cv2.cvtColor(
                    annotated_frame,
                    cv2.COLOR_BGR2RGB
                )

                FRAME_WINDOW.image(
                    annotated_frame,
                    channels="RGB"
                )

                if stop_button:
                    break

            cap.release()

st.divider()

with st.expander(
    "🧠 How does Object Detection & Tracking work?"
):

    st.write("""
    1. The video or webcam feed is captured using OpenCV.
    2. YOLO processes each frame and detects objects.
    3. Bounding boxes and class labels are drawn around detected objects.
    4. Tracking assigns unique IDs to objects across consecutive frames.
    5. The processed output is displayed in real time.
    """)

st.divider()

st.markdown(
    """
    <div style="text-align:center;color:gray;">
    Developed by <b>Harshitha M</b><br>
    CodeAlpha Artificial Intelligence Internship<br>
    AI Object Detection & Tracking Project
    </div>
    """,
    unsafe_allow_html=True
)