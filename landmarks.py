from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import matplotlib.pyplot as plt
import cv2
import mediapipe as mp


def draw_landmarks_on_image(rgb_image, detection_result, draw_iris=True, draw_contours=True, draw_tesselation=True, landmark_indices=None):

    face_landmarks_list = detection_result.face_landmarks
    annotated_image = np.copy(rgb_image)

    # Loop through the detected faces to visualize.
    for idx in range(len(face_landmarks_list)):
        face_landmarks = face_landmarks_list[idx]

        # Draw specific landmarks or all
        if landmark_indices is not None:
            selected_landmarks = [face_landmarks[i] for i in landmark_indices]
        else:
            selected_landmarks = face_landmarks

        face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        face_landmarks_proto.landmark.extend(
            [
                landmark_pb2.NormalizedLandmark(
                    x=landmark.x, y=landmark.y, z=landmark.z
                )
                for landmark in selected_landmarks
            ]
        )

        if draw_tesselation:
            mp.solutions.drawing_utils.draw_landmarks(
                image=annotated_image,
                landmark_list=face_landmarks_proto,
                connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_tesselation_style(),
            )
        if draw_contours:
            mp.solutions.drawing_utils.draw_landmarks(
                image=annotated_image,
                landmark_list=face_landmarks_proto,
                connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_contours_style(),
            )
        if draw_iris:
            mp.solutions.drawing_utils.draw_landmarks(
                image=annotated_image,
                landmark_list=face_landmarks_proto,
                connections=mp.solutions.face_mesh.FACEMESH_IRISES,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_iris_connections_style(),
            )

    return annotated_image

def get_iris_landmarks(detection_result):

    iris_landmarks_list = []

    if detection_result.face_landmarks:
        for face_landmarks in detection_result.face_landmarks:
            left_iris_landmarks = [face_landmarks[i] for i in [474, 475, 477, 476]]
            right_iris_landmarks = [face_landmarks[i] for i in [469, 470, 471, 472]]

            left_iris_coords = [
                {"x": landmark.x, "y": landmark.y, "z": landmark.z}
                for landmark in left_iris_landmarks
            ]
            right_iris_coords = [
                {"x": landmark.x, "y": landmark.y, "z": landmark.z}
                for landmark in right_iris_landmarks
            ]

            iris_landmarks_list.append({
                "left_iris": left_iris_coords,
                "right_iris": right_iris_coords,
            })

    return iris_landmarks_list

def plot_face_blendshapes_bar_graph(face_blendshapes):
    # Extract the face blendshapes category names and scores.
    face_blendshapes_names = [
        face_blendshapes_category.category_name
        for face_blendshapes_category in face_blendshapes
    ]
    face_blendshapes_scores = [
        face_blendshapes_category.score
        for face_blendshapes_category in face_blendshapes
    ]
    # The blendshapes are ordered in decreasing score value.
    face_blendshapes_ranks = range(len(face_blendshapes_names))

    fig, ax = plt.subplots(figsize=(12, 12))
    bar = ax.barh(
        face_blendshapes_ranks,
        face_blendshapes_scores,
        label=[str(x) for x in face_blendshapes_ranks],
    )
    ax.set_yticks(face_blendshapes_ranks, face_blendshapes_names)
    ax.invert_yaxis()

    # Label each bar with values
    for score, patch in zip(face_blendshapes_scores, bar.patches):
        plt.text(
            patch.get_x() + patch.get_width(), patch.get_y(), f"{score:.4f}", va="top"
        )

    ax.set_xlabel("Score")
    ax.set_title("Face Blendshapes")
    plt.tight_layout()
    plt.show()


def get_landmarks(image):

    base_options = python.BaseOptions(model_asset_path="face_landmarker.task")
    options = vision.FaceLandmarkerOptions(
        base_options=base_options,
        num_faces=1,
        running_mode=vision.RunningMode.IMAGE,
        min_tracking_confidence=0.65,
        min_face_detection_confidence=0.8,
        min_face_presence_confidence=0.8,
        output_facial_transformation_matrixes=True,
        output_face_blendshapes=True,
    )

    detector = vision.FaceLandmarker.create_from_options(options)
    detection_result = detector.detect(image)
    return detection_result

def draw_landmarks_on_cv2_capture():
    capture = cv2.VideoCapture(0)
    width = 1280
    height = 720

    capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)  # Set width
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)  # Set height

    while True:

        ret, frame = capture.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=frame
        ) 

        detection_result = get_landmarks(mp_image)
        iris_lnd = get_iris_landmarks(detection_result)
        print(iris_lnd)
        annotated_image = draw_landmarks_on_image(mp_image.numpy_view(), detection_result, )

        annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)
        cv2.imshow("image", annotated_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()


def draw_landmark(img_path):
    image = mp.Image.create_from_file(img_path)
    detection_result = get_landmarks(image)
    annotated_image = draw_landmarks_on_image(image.numpy_view(), detection_result)

    annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)
    cv2.imshow("image", annotated_image)
    cv2.waitKey(0)

    plot_face_blendshapes_bar_graph(detection_result.face_blendshapes[0])
    print(detection_result.facial_transformation_matrixes)


if __name__ == '__main__':
    # draw_landmark('business-person.png')  
    draw_landmarks_on_cv2_capture()





































