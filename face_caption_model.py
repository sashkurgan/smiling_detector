import cv2
import matplotlib.pyplot as plt
import os


imgs_folder = 'synthetic_images'
faces_folder = 'real_test_captions_negative'

imgs = os.listdir(imgs_folder)
print(imgs)

for i in range(len(imgs)):
    img_path = imgs[i]
    id = img_path.split('.')[0]
    print(id)
    try:

        # Загрузить изображение
        image = cv2.imread(f"{imgs_folder}/{img_path}")

        # Преобразовать изображение в формат RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Определить каскад классификатора лиц
        face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface_improved.xml')

        # Обнаружить лица на изображении
        faces = face_cascade.detectMultiScale(image, 1.5, minNeighbors=3)

        # Проверить, есть ли лица на изображении
        if len(faces) == 0:
          print(f"На изображении не найдено лиц {id}")


        else:

            # Выбрать первое обнаруженное лицо
            (x, y, w, h) = faces[0]

            # Вырезать захваченное лицо
            roi = image[y:y+h, x:x+w]

            # Преобразовать изображение в формат BGR
            roi = cv2.cvtColor(roi, cv2.COLOR_RGB2BGR)
            roi = cv2.resize(roi,(64,64))
            # Сохранить захваченное лицо
            cv2.imwrite(f"{faces_folder}/caption_{id}.png", roi)

    except:
        print(f'проблема с изображением {id}')
