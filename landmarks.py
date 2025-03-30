import cv2
import mediapipe as mp 


def initialize_face_mesh(min_tracking_conf=0.65, min_detection_conf=0.8):
    face_mesh = mp.solutions.face_mesh.FaceMesh(
        min_detection_confidence=min_detection_conf,
        min_tracking_confidence=min_tracking_conf,
    )

    return face_mesh


