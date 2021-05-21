import cv2
import numpy as np
from targeting import mark_center, drw_line, detect
import sys


# Load Yolo
net = cv2.dnn.readNet("yolov3_training_last.weights", "yolotest.cfg")

classes = ["Fire"]


vid = cv2.VideoCapture(0)

layer_names = net.getLayerNames()

output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

threshold = 0.2

while True:
    # reading from video  frame
    _, frame = vid.read()

    frame = cv2.resize(frame, None, fx=0.4, fy=0.4)
    # 640 * 420
    height, width, channels = frame.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)

    # ag dan bilgilerin alinmasi
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > threshold:
                # nesne algilandi
                print(class_id)
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # sinirlayicci bolge koordinatlari
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    print(indexes)
    print(confidences)
    font = cv2.FONT_HERSHEY_PLAIN
    # Todo reverse image shape for showing
    fr_x, fr_y, _ = frame.shape
    fr_center = (int(fr_y/2), int(fr_x/2))
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[class_ids[i]]
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 0)
            cv2.putText(frame, "ates", (x, y + 30), font, 1, color, 0)
            # algilanan atesler icin kare
            center_te = (int(x+(w/2)), int(y+(h/2)))
            print(center_te)
            radius = 4
            thickness = 2

            frame = cv2.circle(frame, center_te, radius=4, thickness=2, color=(0, 0, 255))
            drw_line(frame, center_te, fr_center)
    #frame = detect(frame)
    mark_center(frame, fr_center)
    foto_son = cv2.resize(frame, (1920, 1080), interpolation=cv2.INTER_AREA)

    cv2.imshow("Image", foto_son)
    # key = cv2.waitKey(0)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        # break out of the while loop
        break

cv2.destroyAllWindows()