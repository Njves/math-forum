import requests
import shutil
import hashlib
import random
import uuid

URL = "https://latex.codecogs.com/png.latex?\dpi{110}&space;\large&space;"
IMG_PATH = 'app/static/img/'


class MathTextConverter:
    # Берет сырое мат.выражение прокидывает на сайт и получает картинку
    # отформатированного изображения
    @staticmethod
    def getImage(expression):
        # Запрос картинки мат.выражения
        image_url = requests.get(URL + expression, stream=True)

        if image_url.status_code != 200:
            return None
        # Генерация имени картинки
        img_name = str(uuid.uuid1()).split('-')[0] + ".png"
        # берем байтики и засовываем их в файл
        with open(IMG_PATH + img_name, 'wb') as f:
            image_url.raw.decode_content = True
            shutil.copyfileobj(image_url.raw, f)
            return IMG_PATH + img_name

