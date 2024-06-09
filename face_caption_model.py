import cv2

import os


imgs_folder = 'real_test_negative' #where images stored
faces_folder = 'real_test_captions_negative' #folder for captions

imgs = os.listdir(imgs_folder)
print(imgs)

for i in range(len(imgs)):
    img_path = imgs[i]
    id = img_path.split('.')[0]
    print(id)
    try:

        # read image
        image = cv2.imread(f"{imgs_folder}/{img_path}")

        # transform to BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # cascade for faces
        face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface_improved.xml')

        # detect faces
        faces = face_cascade.detectMultiScale(image, 1.3, minNeighbors=1)

        # faces check
        if len(faces) == 0:
          print(f"На изображении не найдено лиц {id}")


        else:

            # first face in cascade
            (x, y, w, h) = faces[0]

            # face caption
            roi = image[y-int(0.2*h):y+int(1.2*h), x-int(0.2*w):x+int(1.2*w)]

            # transform to RGB
            roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
            roi = cv2.resize(roi,(128,128))
            # img save
            cv2.imwrite(f"{faces_folder}/caption_{id}.jpg", roi)

    except:
        print(f'проблема с изображением {id}')

