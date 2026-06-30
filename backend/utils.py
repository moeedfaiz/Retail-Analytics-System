import cv2
import numpy as np


# ==========================================================
# IoU Calculation
# ==========================================================

def iou(box1, box2):
    """
    Calculate Intersection over Union
    box = [x1,y1,x2,y2]
    """

    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    inter = max(0, x2 - x1) * max(0, y2 - y1)

    if inter == 0:
        return 0.0

    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])

    return inter / (area1 + area2 - inter)


# ==========================================================
# Largest Chiller
# ==========================================================

def get_largest_box(boxes):
    """
    Returns largest bounding box
    """

    if len(boxes) == 0:
        return None

    return max(
        boxes,
        key=lambda b: (b[2] - b[0]) * (b[3] - b[1])
    )


# ==========================================================
# Crop Image
# ==========================================================

def crop_image(image, box):
    """
    Crop image using bounding box
    """

    x1, y1, x2, y2 = box

    return image[y1:y2, x1:x2]


# ==========================================================
# Shift Boxes
# ==========================================================

def shift_boxes(boxes, offset_x, offset_y):
    """
    Convert crop coordinates back
    to original image coordinates.
    """

    shifted = []

    for box in boxes:

        x1, y1, x2, y2 = box

        shifted.append([
            x1 + offset_x,
            y1 + offset_y,
            x2 + offset_x,
            y2 + offset_y
        ])

    return shifted


# ==========================================================
# Draw Boxes
# ==========================================================

def draw_boxes(image, boxes, color, label):
    """
    Draw bounding boxes on image.
    """

    img = image.copy()

    for box in boxes:

        x1, y1, x2, y2 = map(int, box)

        cv2.rectangle(
            img,
            (x1, y1),
            (x2, y2),
            color,
            2
        )

        cv2.putText(
            img,
            label,
            (x1, y1 - 6),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            color,
            2
        )

    return img


# ==========================================================
# Convert YOLO Results
# ==========================================================

def yolo_to_boxes(results):
    """
    Convert Ultralytics result
    into list of boxes.
    """

    boxes = []

    for r in results:

        for box in r.boxes:

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            boxes.append([x1, y1, x2, y2])

    return boxes


# ==========================================================
# Image Encoder
# ==========================================================

def encode_image(image):
    """
    Convert OpenCV image to bytes.
    Useful if needed later.
    """

    _, buffer = cv2.imencode(".jpg", image)

    return buffer.tobytes()


# ==========================================================
# Count Objects
# ==========================================================

def count_objects(boxes):
    return len(boxes)


# ==========================================================
# Image Size
# ==========================================================

def image_size(image):
    h, w = image.shape[:2]
    return w, h