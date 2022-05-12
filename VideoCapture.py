import cv2


def capture():
    frameWidth = 640

    frameHeight = 480
    nPlatesCascade = cv2.CascadeClassifier(
        "Resources/haarcascade_licence_plate.xml")
    ######

    color = (255, 0, 255)
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
    cap.set(10, 200)
    minArea = 500
    count = 0

    #######

    while True:
        success, img = cap.read()
        imgRoi = img
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        numberPlates = nPlatesCascade.detectMultiScale(imgGray, 1.1, 4)
        for (x, y, w, h) in numberPlates:
            area = w*h
            if area > minArea:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
                cv2.putText(img, 'Car paste', (x, y-5),
                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)
                imgRoi = img[y:y+h, x:x+w]
                cv2.imshow('ROI', imgRoi)

        cv2.imshow("Result", img)

        if cv2.waitKey(1) & 0xFF == ord('s'):
            cv2.imwrite("Resources/Scan/NoPlate_"+str(count)+'.jpg', imgRoi)
            cv2.rectangle(img, (0, 200), (640, 300), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, "Save success", (150, 265), cv2.FONT_HERSHEY_DUPLEX,
                        2, (0, 0, 255), 2)
            cv2.waitKey(500)
            count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    capture()
