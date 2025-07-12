import cv2
import mediapipe as mp

# Init mediapipe
mp_face_mesh = mp.solutions.face_mesh

# Landmarks relevant to lips + jaw
selected_landmarks = [
    234, 93, 132, 58, 172, 136, 150, 149, 176, 148,
    152, 377, 400, 378, 379, 365, 397, 288, 454,
    116, 111, 117, 118, 119, 120, 121, 47, 126, 209, 
    64, 19, 278, 129, 277, 349, 348, 347, 346, 340, 345, 
    350, 355, 429, 455
]

# Load image
image_path = "mediapipe_face_landmark_fullsize.png"
image = cv2.imread(image_path)

with mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5
) as face_mesh:

    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_image)

    if results.multi_face_landmarks:
        annotated = image.copy()
        for face_landmarks in results.multi_face_landmarks:
            for idx in selected_landmarks:
                landmark = face_landmarks.landmark[idx]
                h, w, _ = image.shape
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                cv2.circle(annotated, (cx, cy), 10, (0, 0, 0), -1)
                # Optional: draw index number
                # cv2.putText(annotated, str(idx), (cx, cy - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 0), 1)
        cv2.imwrite("output_landmarks.jpg", annotated)
        # cv2.imshow("Selected Landmarks", annotated)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("No face detected.")
