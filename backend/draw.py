import cv2


def draw_results(
    image,
    chiller_box,
    nestle_boxes,
    other_boxes,
    analytics
):

    output = image.copy()

    x1, y1, x2, y2 = chiller_box

    # -------------------------------------------------
    # Draw Chiller
    # -------------------------------------------------

    cv2.rectangle(
        output,
        (x1, y1),
        (x2, y2),
        (255, 0, 0),
        3,
    )

    cv2.putText(
        output,
        "Chiller",
        (x1, y1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 0, 0),
        2,
    )

    # -------------------------------------------------
    # Draw Nestle Boxes
    # -------------------------------------------------

    for box in nestle_boxes:

        bx1, by1, bx2, by2 = box

        bx1 += x1
        bx2 += x1
        by1 += y1
        by2 += y1

        cv2.rectangle(
            output,
            (bx1, by1),
            (bx2, by2),
            (0, 255, 0),
            2,
        )

        cv2.putText(
            output,
            "Nestle",
            (bx1, by1 - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2,
        )

    # -------------------------------------------------
    # Draw Other Boxes
    # -------------------------------------------------

    for box in other_boxes:

        bx1, by1, bx2, by2 = box

        bx1 += x1
        bx2 += x1
        by1 += y1
        by2 += y1

        cv2.rectangle(
            output,
            (bx1, by1),
            (bx2, by2),
            (0, 0, 255),
            2,
        )

        cv2.putText(
            output,
            "Other",
            (bx1, by1 - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 255),
            2,
        )

    # -------------------------------------------------
    # Analytics Panel
    # -------------------------------------------------

    panel_height = 140

    cv2.rectangle(
        output,
        (10, 10),
        (360, panel_height),
        (40, 40, 40),
        -1,
    )

    cv2.putText(
        output,
        "Retail Analytics",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2,
    )

    cv2.putText(
        output,
        f"Nestle : {analytics['nestle_count']}",
        (20, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0, 255, 0),
        2,
    )

    cv2.putText(
        output,
        f"Other : {analytics['other_count']}",
        (20, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0, 0, 255),
        2,
    )

    cv2.putText(
        output,
        f"Nestle Share : {analytics['nestle_percent']:.1f}%",
        (20, 115),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2,
    )

    cv2.putText(
        output,
        f"Other Share : {analytics['other_percent']:.1f}%",
        (20, 140),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2,
    )

    return output