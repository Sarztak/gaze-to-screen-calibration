import threading
import cv2
import pygame
import math
import random
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import mediapipe as mp

# Global variables to store gaze and stimulus data
gaze_data = []
stimulus_data = []

# Screen dimensions
WIDTH, HEIGHT = 1280, 720

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

# Set dynamic ball radius
dot_radius = int(min(WIDTH, HEIGHT) * 0.03)

# Set speed and movement characteristics
speed = min(WIDTH, HEIGHT) * 0.005
direction_angle = random.uniform(0, 2 * math.pi)

def gaze_tracking():
    """Function to track gaze using Mediapipe and OpenCV."""
    global gaze_data

    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

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

    while True:
        ret, frame = capture.read()
        if not ret:
            break
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        detection_result = detector.detect(mp_image)

        if detection_result and detection_result.face_landmarks:
            iris_landmarks = detection_result.face_landmarks[0].landmark[468:473]  # Approx. iris landmarks
            iris_x = np.mean([lm.x for lm in iris_landmarks]) * WIDTH
            iris_y = np.mean([lm.y for lm in iris_landmarks]) * HEIGHT
            gaze_data.append((iris_x, iris_y))  # Store gaze data

        annotated_image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        cv2.imshow("Gaze Tracking", annotated_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()

def stimulus_display():
    """Function to display a moving stimulus in Pygame."""
    global stimulus_data, direction_angle

    clock = pygame.time.Clock()
    running = True
    x, y = WIDTH // 2, HEIGHT // 2

    while running:
        screen.fill((50, 50, 50))  # Dark grey background

        # Move the ball in a smooth curve
        direction_angle += random.uniform(-0.08, 0.08)  
        x += speed * math.cos(direction_angle)
        y += speed * math.sin(direction_angle)

        # Keep the stimulus within screen boundaries
        if x - dot_radius <= 0 or x + dot_radius >= WIDTH:
            direction_angle += math.pi  
        if y - dot_radius <= 0 or y + dot_radius >= HEIGHT:
            direction_angle += math.pi  

        # Store stimulus position
        stimulus_data.append((x, y))

        # Draw the ball
        pygame.draw.circle(screen, (255, 0, 0), (int(x), int(y)), dot_radius)
        pygame.display.flip()
        clock.tick(60)  # Maintain 60 FPS

        # Handle exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                running = False

    pygame.quit()

# Start both gaze tracking and stimulus in separate threads
gaze_thread = threading.Thread(target=gaze_tracking)
stimulus_thread = threading.Thread(target=stimulus_display)

gaze_thread.start()
stimulus_thread.start()

gaze_thread.join()
stimulus_thread.join()

# Save collected data
np.save("gaze_data.npy", gaze_data)
np.save("stimulus_data.npy", stimulus_data)
