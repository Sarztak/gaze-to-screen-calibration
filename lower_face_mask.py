import cv2
import numpy as np
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1)

def to_pixel_coords(landmarks, image_shape):
    h, w = image_shape[:2]
    return [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]

def create_lower_face_mask(image, landmarks, width, height):
    def to_pixel(index):
        return int(landmarks[index].x * width), int(landmarks[index].y * height)

    # Jaw + Mouth
    jaw_indices = [234, 93, 132, 58, 172, 136, 150, 149, 176, 148, 152, 377, 400, 378, 379, 365, 397, 288, 454]
    mouth_indices = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291]

    lower_face_points = [to_pixel(idx) for idx in jaw_indices + mouth_indices]

    # Top boundary (between eyes)
    eye_top_y = min(to_pixel(33)[1], to_pixel(263)[1]) + 10
    left_x = to_pixel(234)[0]
    right_x = to_pixel(454)[0]
    top_center = ((left_x + right_x) // 2, eye_top_y)
    lower_face_points.append(top_center)

    # Create mask
    mask = np.zeros((height, width), dtype=np.uint8)
    cv2.fillPoly(mask, [np.array(lower_face_points, dtype=np.int32)], 255)

    return mask

# Load image
image = cv2.imread("mediapipe_face_landmark_fullsize.png")
h, w = image.shape[:2]

# Detect face landmarks
results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

if results.multi_face_landmarks:
    face_landmarks = results.multi_face_landmarks[0].landmark
    mask = create_lower_face_mask(image, face_landmarks, w, h)

    # Apply mask
    masked = cv2.bitwise_and(image, image, mask=mask)

    # Optional overlay
    mask_colored = cv2.merge([mask, mask, mask])
    overlay = cv2.addWeighted(image, 0.7, mask_colored, 0.3, 0)

    cv2.imshow("Lower Face Overlay", overlay)
    cv2.imshow("Masked Image", masked)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No face detected.")
