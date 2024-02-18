from itertools import product
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
from utils import get_time, color_print
from sklearn.metrics import mean_squared_error as mse_sklearn
from skimage.metrics import normalized_root_mse as nrmse_skimage
from skimage.metrics import structural_similarity as ssim_skimage
from skimage.metrics import peak_signal_noise_ratio as psnr_skimage
from sklearn.metrics import mean_absolute_error as mae_skimage
from skimage.metrics import normalized_mutual_information as nmi_skimage
from concurrent.futures import ThreadPoolExecutor

# ==================================================================================================================================
# |                                                              METRICS                                                           |
# ==================================================================================================================================

def pix2pix_np(image1: np.array, image2: np.array) -> bool:
    """
    Функция для сравнения двух изображений методом Pixel to Pixel.

    Вход:
    - image1 (ArrayLike): одномерный массив первого изображения
    - image2 (ArrayLike): одномерный массив второго изображения

    Вывод:
    - image_equal (boolean): True, если изображения идентичны, иначе False
    """

    are_equal = np.array_equal(image1, image2)

    return are_equal

class Metric:
    # def __init__(self, image_paths1: list, image_paths2: list):
    #     self.image_paths1 = image_paths1
    #     print("путь 1")
    #     self.image_paths2 = image_paths2
    #     print("путь 2")
    #     self.resized_images1 = [self.load_and_resize_image(path) for path in image_paths1]
    #     print("сжатые изображения 1")
    #     self.resized_images2 = [self.load_and_resize_image(path) for path in image_paths2]
    #     print("сжатые изображения 2")
    # def load_and_resize_image(self, image_path):
    #     with Image.open(image_path) as img:
    #         print(image_path)
    #         img_resized = img.resize((512, 512))
    #         img_array = np.array(img_resized)
    #     return img_array.flatten()
    def __init__(self, image_paths1: list, image_paths2: list):
        self.image_paths1 = image_paths1
        self.image_paths2 = image_paths2
        self.resized_images1 = self.load_and_resize_images(image_paths1)
        self.resized_images2 = self.load_and_resize_images(image_paths2)

    def load_and_resize_images(self, image_paths):
        with ThreadPoolExecutor() as executor:
            resized_images = list(executor.map(self.load_and_resize_image, image_paths))
            print (len(resized_images))
        return resized_images

    def load_and_resize_image(self, image_path):
        with Image.open(image_path) as img:
            img_resized = img.resize((512, 512))
            img_array = np.array(img_resized)
            print(image_path)
        return img_array.flatten()
    # def calculate_metric(self, metric_function):
    #     metric_values = []
    #     for img1 in self.resized_images1:
    #         row = []
    #         for img2 in self.resized_images2:
    #             row.append(metric_function(img1, img2))
    #         metric_values.append(row)
    #     return metric_values
    def calculate_metric(self, metric_function):
        metric_values = []
        k=0
        with ThreadPoolExecutor() as executor:
            for img1 in self.resized_images1:
                row = list(executor.map(lambda img2: metric_function(img1, img2), self.resized_images2))
                k+=1
                print(k)
                metric_values.append(row)
        return metric_values
    
    def pix2pix(self) -> list:
        return self.calculate_metric(pix2pix_np)
    
    def mae(self) -> list:
        return self.calculate_metric(mae_skimage)
    
    def mse(self) -> list:
        return self.calculate_metric(mse_sklearn)

    def nrmse(self) -> list:
        return self.calculate_metric(nrmse_skimage)

    def ssim(self) -> list:
        return self.calculate_metric(lambda x, y: ssim_skimage(x, y, win_size=3))

    def psnr(self) -> list:
        return self.calculate_metric(psnr_skimage)
    
    def nmi(self) -> list:
        return self.calculate_metric(nmi_skimage)
    def show(self, matrix):
        plt.imshow(matrix, cmap='viridis', interpolation='nearest')
        plt.colorbar()
        plt.show()

# ==================================================================================================================================

if __name__ == "__main__":
    #image_paths1 = ["test_images/PSNR-base.jpg", "test_images/PSNR-90.jpg", "test_images/PSNR-30.jpg", "test_images/PSNR-10.jpg"]
    #image_paths2 = ["test_images/PSNR-base.jpg", "test_images/PSNR-90.jpg", "test_images/PSNR-30.jpg", "test_images/PSNR-10.jpg"]
    from utils import scan_directory
    import os
    image_paths1 =  scan_directory('dataset')
    x2 =  list(map(lambda x: os.path.join(x[0], x[1]), image_paths1))
    print()

    metric = Metric(x2, x2)

    #pix2pix_values = metric.pix2pix()
    mae_values = metric.mae()
    # mse_values = metric.mse()
    # nrmse_values = metric.nrmse()
    # ssim_values = metric.ssim()
    # psnr_values = metric.psnr()
    # nmi_values = metric.nmi()

    #print(f"pix2pix values: {pix2pix_values}")
    print(f"mae values: {mae_values}")
    # print(f"MSE values: {mse_values}")
    # print(f"NRMSE values: {nrmse_values}")
    # print(f"SSIM values: {ssim_values}")
    # print(f"PSNR values: {psnr_values}")
    # print(f"NMI values: {nmi_values}")
    
    #metric.show(pix2pix_values)    
    metric.show(mae_values)    
    # metric.show(mse_values)    
    # metric.show(nrmse_values)    
    # metric.show(ssim_values)    
    # metric.show(psnr_values)    
    # metric.show(nmi_values)
