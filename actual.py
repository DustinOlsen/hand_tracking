import cv2
from src.hand_tracker import HandTracker
from math import hypot
from pyautogui import press,hotkey

WINDOW = "Hand Tracking"
PALM_MODEL_PATH = "models/palm_detection_without_custom_op.tflite"
LANDMARK_MODEL_PATH = "models/hand_landmark.tflite"
ANCHORS_PATH = "models/anchors.csv"

num_frames = 0

cv2.namedWindow(WINDOW)
capture = cv2.VideoCapture(0)

if capture.isOpened():
    hasFrame, frame = capture.read()
else:
    hasFrame = False

#        8   12  16  20
#        |   |   |   |
#        7   11  15  19
#    4   |   |   |   |
#    |   6   10  14  18
#    3   |   |   |   |
#    |   5---9---13--17
#    2    \         /
#     \    \       /
#      1    \     /
#       \    \   /
#        ------0-

# connections = [
#     (0, 1), (1, 2), (2, 3), (3, 4),
#     (5, 6), (6, 7), (7, 8),
#     (9, 10), (10, 11), (11, 12),
#     (13, 14), (14, 15), (15, 16),
#     (17, 18), (18, 19), (19, 20),
#     (0, 5), (5, 9), (9, 13), (13, 17), (0, 17)
# ]

detector = HandTracker(
    PALM_MODEL_PATH,
    LANDMARK_MODEL_PATH,
    ANCHORS_PATH,
    box_shift=0.2,
    box_enlarge=1.3
)

while hasFrame:
    num_frames = num_frames + 1
    if num_frames % 24 == 0:
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        points, _ = detector(image)

        if type(points) != type(None):
            # print(points[5],points[8])
            # print(points[9],points[12])
            # print(points[13],points[16])
            p0 = points[0]
            p1 = points[9]
            # _,p2y = points[10]
            # _,p3y = points[11]
            p2 = points[12]
            # count = len(points)

            dist1 = hypot(p0[0]-p2[0],p0[1]-p2[1])
            dist2 = hypot(p0[0]-p1[0],p0[1]-p1[1])
            if dist1 > dist2:
                print("Open hand!!")
                # press("pgdn")
                press("playpause")
            else:
                print("Closed hand!!")
                # press("pgup")
                press("nexttrack")
            print("=================================")
    cv2.imshow(WINDOW, frame)
    hasFrame, frame = capture.read()
    key = cv2.waitKey(1)
    if key == 27:
        break

capture.release()
cv2.destroyAllWindows()
