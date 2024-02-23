import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact
from scipy import stats
from common.utils import color_print, scan_directory


# ==================================================================================================================================
# |                                                             SIFT TOOLS                                                         |
# ==================================================================================================================================


def load_image(image_path: str, echo: bool = False) -> np.ndarray:
    """
    Загружает изображение из файла и масштабирует его до ширины 512 пикселей, сохраняя пропорции.

    Parameters:
        - image_path (str): Путь к файлу изображения.
        - echo (str, optional): Управляет выводом сообщения о загрузке изображения. Если "on", то выводится сообщение.

    Returns:
        - numpy.ndarray: Загруженное и масштабированное изображение в формате RGB.
    """

    if echo == True:
        color_print("create", "create", f"Loading image {image_path}", True)

    # Загрузка изображения и преобразование его в формат RGB
    img = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)

    # Получение текущих размеров изображения
    height, width = img.shape[:2]

    # Вычисление новых размеров, сохраняя пропорции
    new_width = 512
    new_height = int(height * (new_width / width))

    # Масштабирование изображения до новых размеров
    resized_img = cv2.resize(img, (new_width, new_height))

    return resized_img


# ==================================================================================================================================


def get_descriptors(dataset_path: str, echo: bool = False):
    """
    Извлекает дескрипторы SIFT из изображений в указанной директории.

    Parameters:
        - images_dir (str): Путь к директории с изображениями.

    Returns:
        - numpy.ndarray: Массив дескрипторов SIFT.
        - numpy.ndarray: Массив меток изображений.
    """

    feature_extractor = cv2.SIFT_create()

    t = 0
    Xt = np.zeros((50000, 128))
    yt = np.zeros((50000,))

    image_paths = scan_directory(dataset_path)
    image_full_paths = list(map(lambda x: os.path.join(x[0], x[1]), image_paths))

    image_count = len(image_full_paths)

    print(image_full_paths) if echo else None

    for i in range(image_count):
        image = load_image(image_full_paths[i], echo)
        J = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        # SIFT extraction
        kp, desc = feature_extractor.detectAndCompute(J, None)
        ni = desc.shape[0]
        for j in range(ni):
            f = desc[j, :]
            Xt[t, :] = f / np.linalg.norm(f)
            yt[t] = i
            t = t + 1

        if echo:
            color_print("done", "done", f"{str(ni)} Дескрипторы были извлечены.")

    X = Xt[0:t, :]
    y = yt[0:t]

    if echo:
        color_print(
            "done",
            "done",
            f"Количество дескрипторов SIFT в {str(image_count)} images: {str(t)}",
            True,
        )

    return X, y


# ==================================================================================================================================


def find_similar_image(itest, X, y):
    """
    Находит наиболее похожее изображение на тестовом изображении с помощью дескрипторов SIFT.

    Parameters:
        itest (int): Индекс тестового изображения.
        X (numpy.ndarray): Массив дескрипторов SIFT.
        y (numpy.ndarray): Массив меток изображений.

    Returns:
        int: Индекс наиболее похожего изображения.
    """

    ik = itest
    ii = np.where(y == ik)[0]
    jj = np.where(y != ik)[0]

    Xi = X[ii, :]
    Xj = X[jj, :]
    yj = y[jj]

    Dt = np.dot(Xj, Xi.T)

    n = Xi.shape[0]

    z = np.zeros((n,))
    d = np.zeros((n,))

    for k in range(n):
        h = Dt[:, k]
        i = h.max()
        z[k] = i
        j = np.where(h == i)
        d[k] = yj[j]

    kk = np.where(z > 0.9)

    m = stats.mode(d[kk])
    ifound = int(m[0])

    return ifound


# ==================================================================================================================================


def visualize_similar_images(itest):
    """
    Визуализирует тестовое и наиболее похожее изображения.

    Parameters:
        itest (int): Индекс тестового изображения.
        images_fpath (list): Список путей к изображениям.
    """

    ifound = find_similar_image(itest, X, y)
    image = load_image(image_full_paths[itest], True)
    print("Тестовое изображение: " + str(itest))
    plt.imshow(image, cmap="gray")
    plt.axis("off")
    plt.show()
    print(" ")
    J = load_image(image_full_paths[ifound], True)
    print(
        "Для изображения "
        + str(itest)
        + ", наиболее похожее изображение: "
        + str(ifound)
        + "."
    )
    plt.imshow(J, cmap="gray")
    plt.axis("off")
    plt.show()
    print("--------------------------------------------------")


# Пример использования с ipywidgets interact
interact(visualize_similar_images, itest=(0, 2))

# ==================================================================================================================================

if __name__ == "__main__":
    print("gdgd")