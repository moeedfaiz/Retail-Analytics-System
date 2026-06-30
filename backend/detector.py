import os
import uuid
import cv2
from ultralytics import YOLO

from config import (
    CHILLER_MODEL_PATH,
    GENERAL_MODEL_PATH,
    NESTLE_MODEL_PATH,
    OUTPUT_FOLDER,
    CONFIDENCE_THRESHOLD,
    IOU_THRESHOLD,
)

print("Loading AI Models...")

CHILLER_MODEL = YOLO(CHILLER_MODEL_PATH, task="detect")
GENERAL_MODEL = YOLO(GENERAL_MODEL_PATH, task="detect")
NESTLE_MODEL = YOLO(NESTLE_MODEL_PATH, task="detect")

print("Models Loaded Successfully!")


def box_iou(box1, box2):
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    inter_area = max(0, x2 - x1) * max(0, y2 - y1)

    if inter_area == 0:
        return 0.0

    area1 = max(0, box1[2] - box1[0]) * max(0, box1[3] - box1[1])
    area2 = max(0, box2[2] - box2[0]) * max(0, box2[3] - box2[1])

    return inter_area / (area1 + area2 - inter_area)


def extract_boxes(results):
    boxes = []

    for result in results:
        for box in result.boxes:
            xyxy = box.xyxy[0].cpu().numpy().astype(int).tolist()
            conf = float(box.conf[0])
            boxes.append(
                {
                    "box": xyxy,
                    "confidence": conf,
                }
            )

    return boxes


def clip_box(box, width, height):
    x1, y1, x2, y2 = box

    x1 = max(0, min(x1, width - 1))
    y1 = max(0, min(y1, height - 1))
    x2 = max(0, min(x2, width - 1))
    y2 = max(0, min(y2, height - 1))

    return [x1, y1, x2, y2]


def process_image(image_path):
    image = cv2.imread(image_path)

    if image is None:
        raise Exception("Unable to read uploaded image.")

    original = image.copy()
    img_h, img_w = image.shape[:2]

    # =====================================================
    # 1. Chiller Detection
    # =====================================================

    chiller_results = CHILLER_MODEL.predict(
        source=image,
        conf=CONFIDENCE_THRESHOLD,
        verbose=False,
    )

    chiller_detections = extract_boxes(chiller_results)

    if not chiller_detections:
        raise Exception("No chiller detected in the image.")

    largest_chiller = max(
        chiller_detections,
        key=lambda item: (item["box"][2] - item["box"][0]) * (item["box"][3] - item["box"][1]),
    )

    chiller_box = clip_box(largest_chiller["box"], img_w, img_h)
    chiller_confidence = round(largest_chiller["confidence"] * 100, 2)

    x1, y1, x2, y2 = chiller_box

    if x2 <= x1 or y2 <= y1:
        raise Exception("Invalid chiller crop detected.")

    chiller_crop = image[y1:y2, x1:x2]

    if chiller_crop.size == 0:
        raise Exception("Empty chiller crop generated.")

    # =====================================================
    # 2. General SKU Detection Inside Chiller
    # =====================================================

    general_results = GENERAL_MODEL.predict(
        source=chiller_crop,
        conf=CONFIDENCE_THRESHOLD,
        verbose=False,
    )

    general_detections = extract_boxes(general_results)
    general_boxes = [d["box"] for d in general_detections]

    # =====================================================
    # 3. Nestle SKU Detection Inside Chiller
    # =====================================================

    nestle_results = NESTLE_MODEL.predict(
        source=chiller_crop,
        conf=CONFIDENCE_THRESHOLD,
        verbose=False,
    )

    nestle_detections = extract_boxes(nestle_results)
    nestle_boxes = [d["box"] for d in nestle_detections]

    # =====================================================
    # 4. Other SKU = General SKU - Nestle SKU
    # =====================================================

    other_boxes = []

    for g_box in general_boxes:
        is_nestle = False

        for n_box in nestle_boxes:
            if box_iou(g_box, n_box) >= IOU_THRESHOLD:
                is_nestle = True
                break

        if not is_nestle:
            other_boxes.append(g_box)

    # =====================================================
    # 5. Draw Results On Original Image
    # =====================================================

    output = original.copy()

    cv2.rectangle(output, (x1, y1), (x2, y2), (255, 120, 0), 3)
    cv2.putText(
        output,
        f"Chiller {chiller_confidence:.1f}%",
        (x1, max(30, y1 - 10)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 120, 0),
        2,
    )

    # Nestle boxes - green
    for box in nestle_boxes:
        bx1, by1, bx2, by2 = box

        bx1 += x1
        bx2 += x1
        by1 += y1
        by2 += y1

        cv2.rectangle(output, (bx1, by1), (bx2, by2), (0, 255, 0), 2)
        cv2.putText(
            output,
            "Nestle",
            (bx1, max(20, by1 - 5)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 0),
            2,
        )

    # Other boxes - red
    for box in other_boxes:
        bx1, by1, bx2, by2 = box

        bx1 += x1
        bx2 += x1
        by1 += y1
        by2 += y1

        cv2.rectangle(output, (bx1, by1), (bx2, by2), (0, 0, 255), 2)
        cv2.putText(
            output,
            "Other",
            (bx1, max(20, by1 - 5)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 0, 255),
            2,
        )

    # =====================================================
    # 6. Analytics
    # =====================================================

    nestle_count = len(nestle_boxes)
    other_count = len(other_boxes)
    total = nestle_count + other_count

    if total > 0:
        nestle_percent = round((nestle_count / total) * 100, 2)
        other_percent = round((other_count / total) * 100, 2)
    else:
        nestle_percent = 0
        other_percent = 0

    # Small overlay panel
    cv2.rectangle(output, (20, 20), (390, 165), (20, 20, 20), -1)
    cv2.putText(output, "Retail Analytics", (35, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(output, f"Total SKUs: {total}", (35, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
    cv2.putText(output, f"Nestle: {nestle_count} ({nestle_percent}%)", (35, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
    cv2.putText(output, f"Other: {other_count} ({other_percent}%)", (35, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)

    # =====================================================
    # 7. Save Output
    # =====================================================

    output_filename = f"result_{uuid.uuid4().hex}.jpg"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    cv2.imwrite(output_path, output)

    return {
        "success": True,
        "total": total,
        "nestle_count": nestle_count,
        "other_count": other_count,
        "nestle_percent": nestle_percent,
        "other_percent": other_percent,
        "chiller_detected": True,
        "chiller_confidence": chiller_confidence,
        "output_image": output_filename,
    }