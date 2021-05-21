
def mark_center(frame, center_te):
    import cv2 as cv
    x, y, z = frame.shape
    # ToDo reverse image size
    print("koordinatlar ", x, y, "\n")
    font = cv.FONT_HERSHEY_PLAIN
    # center = int(y/2),int(x/2)
    # print("center = ",center)
    # center_te = int(y/2),int(x/2)+10
    color = (255, 0, 255)
    frame = cv.putText(frame, "hedef", center_te, font, 1, color, 0)

    frame = cv.circle(frame, center_te, radius=4, thickness=1, color=(0, 0, 255))
    return frame


def drw_line(frame, obj_center, center):
    import cv2 as cv
    color = (255, 0, 0)
    image = cv.line(frame, center, obj_center, color, 1)
    return image


def detect(frame):
    import cv2
    HOGCV = cv2.HOGDescriptor()
    HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    bounding_box_cordinates, weights = HOGCV.detectMultiScale(frame, winStride=(4, 4), padding=(8, 8), scale=1.03)

    person = 1
    for x, y, w, h in bounding_box_cordinates:
        print("insan koordinat ", x, " ", y)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, f'person {person}', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
        person += 1
    size_x , size_y,_ = frame.shape
    color = (255, 0, 255)
    frame = cv2.putText(frame,f'Total Persons : {person - 1}', (10,10), cv2.FONT_HERSHEY_DUPLEX, 0.5, color, 2)
    #cv2.putText(frame, f'Total Persons : {person - 1}', (10, 10), cv2.FONT_HERSHEY_DUPLEX, 0.2, (0, 255, 0), 1)
    return frame
