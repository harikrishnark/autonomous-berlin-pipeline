import cv2
import numpy as np
from pathlib import Path


OUTPUT_PATH = Path(__file__).resolve().parent.parent / 'artifacts' / 'street_drive_simulation.mp4'
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)


def build_frame(frame_idx: int, width: int = 640, height: int = 480) -> np.ndarray:
    img = np.zeros((height, width, 3), dtype=np.uint8)
    img[:] = (90, 160, 80)

    # Road and lane markings.
    cv2.rectangle(img, (0, 200), (width, 330), (40, 40, 40), thickness=-1)
    cv2.line(img, (0, 265), (width, 265), (255, 255, 255), 4)
    for x in range(0, width + 80, 80):
        pos = (x - (frame_idx * 8) % 160) % 160 - 80
        cv2.rectangle(img, (pos, 248), (pos + 40, 282), (255, 255, 255), thickness=-1)

    # Horizon and buildings.
    cv2.rectangle(img, (0, 0), (width, 180), (30, 80, 130), thickness=-1)
    for x in range(40, width, 120):
        cv2.rectangle(img, (x, 80), (x + 40, 160), (20, 50, 90), thickness=-1)

    # Moving car.
    car_x = 120 + (frame_idx * 6) % 320
    car_y = 200
    cv2.rectangle(img, (car_x, car_y), (car_x + 90, car_y + 45), (255, 80, 0), thickness=-1)
    cv2.rectangle(img, (car_x + 15, car_y - 20), (car_x + 75, car_y), (255, 80, 0), thickness=-1)
    cv2.circle(img, (car_x + 20, car_y + 45), 12, (0, 0, 0), thickness=-1)
    cv2.circle(img, (car_x + 70, car_y + 45), 12, (0, 0, 0), thickness=-1)

    # Overlay text.
    cv2.putText(img, 'Street drive simulation', (70, 48), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(img, f'frame {frame_idx}', (430, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (220, 220, 220), 1)
    return img


def main() -> None:
    fps = 15
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(str(OUTPUT_PATH), fourcc, fps, (640, 480))
    if not writer.isOpened():
        raise RuntimeError(f'Unable to create video writer for {OUTPUT_PATH}')

    try:
        for frame_idx in range(120):
            frame = build_frame(frame_idx)
            writer.write(frame)
    finally:
        writer.release()

    print(f'Wrote video to {OUTPUT_PATH}')


if __name__ == '__main__':
    main()
