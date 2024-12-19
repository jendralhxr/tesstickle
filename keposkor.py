# usage: python -u keposkor.py <video-file> <start-framenumber> <seek-frame-interval> <target-string>
import cv2
import pytesseract
import sys

# Path to Tesseract OCR executable (modify this if necessary)
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# Input video file
video_path = sys.argv[1]

# Parameters
start_frame = int(sys.argv[2])  # Set the starting frame index
frame_interval = int(sys.argv[3])  # Set the frame sampling interval

# Open the video file
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Cannot open video file.")
    exit()

# Get total frame count of the video
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Start processing frames
frame_index = start_frame
ocr_detected = False
target_string= sys.argv[4]

while frame_index < total_frames:
    # Seek to the desired frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
    
    ret, frame = cap.read()
    if not ret:
        print(f"Error: Could not read frame at index {frame_index}.")
        break

    # Convert the frame to grayscale for better OCR performance
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Perform OCR on the frame
    ocr_result = pytesseract.image_to_string(gray_frame, lang="eng+ind")
    print(f"Frame {frame_index}: OCR Result:\n{ocr_result}")
    
    if target_string in ocr_result:
        print(f"Target string {target_string} found in frame {frame_index}.")
        ocr_detected = True
        break

    # Move to the next frame based on the interval
    frame_index += frame_interval

# Release the video capture object
cap.release()

if not ocr_detected:
    print(f"Target string {target_string} not found in the video.")
