import face_recognition
import cv2
import os
import numpy as np

# Load the known faces and their names from the images directory
image_dir = "images"
known_faces = []
known_names = []
for name in os.listdir(image_dir):
    if name.endswith('.jpg') or name.endswith('.jpeg') or name.endswith('.png'):
        # Load the image and convert it to RGB format
        image = face_recognition.load_image_file(os.path.join(image_dir, name))
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Detect the face and encode it
        face_encoding = face_recognition.face_encodings(rgb)
        if len(face_encoding) > 0:
            face_encoding = face_encoding[0]

            # Add the face encoding and name to the known faces and names lists
            name = ''.join(filter(str.isalpha, name.split(".")[0]))
            known_faces.append(face_encoding)
            known_names.append(name)
        else:
            print(f"No face detected in {name}")

# Open the video capture device (change the number to use a different camera)
video_capture = cv2.VideoCapture(0)
# Initialize previous camera position
prev_pos = None
alpha = 0.5 # Smoothing parameter
# Loop through each frame in the video
while True:
    # Read a frame from the video capture device
    ret, frame = video_capture.read()

    if ret:
        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Get current camera position
        pos = cv2.mean(gray)

        # If this is the first frame, set prev_pos to current position
        if prev_pos is None:
            prev_pos = np.array(pos[:2])

        # Smooth camera position by averaging current and previous position
        smooth_pos = (prev_pos + np.array(pos[:2])) / 2

        # Set prev_pos to current position
        prev_pos = np.array(pos[:2])

        # Display frame with smoothed camera position
       # cv2.putText(frame, "Smoothed Camera Position: {:.2f}".format(smooth_pos[0]), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Camera", frame)

    # Convert the frame to RGB format for face detection and recognition
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces in the frame
    faces = face_recognition.face_locations(rgb, model="hog")

    # Recognize faces in the frame
    for (top, right, bottom, left) in faces:
        # Crop the face from the frame and resize it to 128x128 for better recognition
        face = frame[top:bottom, left:right]
        face = cv2.resize(face, (128, 128))

        # Encode the face for recognition
        face_encodings = face_recognition.face_encodings(face)
        if len(face_encodings) > 0:
            face_encoding = face_encodings[0]

            # Compare the face encoding to the known faces
            matches = face_recognition.compare_faces(known_faces, face_encoding)

            # Find the index of the first match in the list of matches
            match_index = matches.index(True) if True in matches else None
        
        # If a match is found, display the name of the person above the face in the video
        if match_index is not None:
            name = known_names[match_index]
        else:
            name = "Unknown"

        cv2.putText(frame, name, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)
    
    # Wait for a key press and check if the user wants to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture device and close the window
video_capture.release()
cv2.destroyAllWindows()

