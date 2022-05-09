
import cv2
from matplotlib import pyplot as plt
import os
import numpy as np
#from hyperlpr import *
from aip import AipOcr
from cut_plate import *
from translate import *


def carplate(img_path):

    # 车牌识别系统主函
    def gray_guss(image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        image = cv2.GaussianBlur(gray_image, (5, 5), 0)
        canny = cv2.Canny(gray_image, 100, 255)
        return image

    def plt_show(img):
        plt.imshow(img, cmap='gray')
        plt.show()

    def lpr(filename):
        # 预处理，包括灰度处理，高斯滤波平滑处理，Sobel提取边界，图像二值化
        img = cv2.imread(filename)

        # 检查图片是否正常载入
        if img is None:
            print('Error opening image: ' + filename)
            return -1

        gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  # 灰度化处理
        # cv2.imshow('gray',gray_img)

        GaussianBlur_img = cv2.GaussianBlur(gray_img, (5, 5), 0)  # 高斯模糊
        # cv2.imshow('Gaussian',GaussianBlur_img)
        Sobel_img = cv2.Sobel(GaussianBlur_img, -1, 1, 0, ksize=3)  # 提取边界
        # cv2.imshow('Soble',Sobel_img)
        canny = cv2.Canny(GaussianBlur_img, 100, 255)  # 提取边界
        # cv2.imshow('Canny',canny)

        # 二值化处理
        ret, binary_img = cv2.threshold(canny, 127, 255, cv2.THRESH_BINARY)
        # cv2.imshow('Binary',binary_img)
        #
        #
        # 形态学运算
        kernel = np.ones((20, 20), np.uint8)
        # 先闭运算将车牌数字部分连接，再开运算将不是块状的或是较小的部分去掉
        close_img = cv2.morphologyEx(binary_img, cv2.MORPH_CLOSE, kernel)
        open_img = cv2.morphologyEx(close_img, cv2.MORPH_OPEN, kernel)
        kernel2 = np.ones((10, 10), np.uint8)
        open_img2 = cv2.morphologyEx(open_img, cv2.MORPH_OPEN, kernel2)
        #cv2.imshow('close', close_img)
        #cv2.imshow('open', open_img2)
    #     # 由于部分图像得到的轮廓边缘不整齐，因此再进行一次膨胀操作
        element = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        dilation_img = cv2.dilate(open_img, element, iterations=3)  # 膨胀操作
        # cv2.imshow('dilation',dilation_img)
    #
        # 获取轮廓
        contours, hierarchy = cv2.findContours(
            dilation_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # print(contours)
        # 测试边框识别结果
        # cv2.drawContours(img, contours, -1, (0, 0, 255), 3)
        # cv2.imshow("lpr", img)
    #
        # # 将轮廓规整为长方形
        rectangles = []
        mask = np.zeros(shape=img.shape, dtype=np.uint8)
        for c in contours:
            ## print (c)
            x = []
            y = []
            for point in c:
                y.append(point[0][0])
                x.append(point[0][1])
            r = [min(y), min(x), max(y), max(x)]
            rectangles.append(r)
            # print(rectangles)
            # cv2.rectangle(mask,pt1=(min(y),min(x)),pt2=(max(y),max(x)),color = (0,0,255),thickness=3)
            # cv2.rectangle(img, pt1=(min(y), min(x)), pt2=(max(y), max(x)), color=(0, 0, 255), thickness=3)
        #cv2.imshow('Mask', mask)
        #cv2.imshow('img', img)
    #
    #
        # 进一步细分筛选，排除干扰

        new_rectangles = []
        for i in rectangles:
            new_y = i[2]-i[0]
            new_x = i[3]-i[1]
            if new_y/new_x >= 2 and new_y:
                new_rectangles.append(i)

        print(new_rectangles)

        # 颜色识别车牌区域

        dist_r = []
        max_mean = 0
        mask2 = np.zeros(shape=img.shape, dtype=np.uint8)
        for r in new_rectangles:
            cv2.rectangle(mask2, pt1=(r[0], r[1]), pt2=(
                r[2], r[3]), color=(0, 0, 255), thickness=3)
            block = img[r[1]:r[3], r[0]:r[2]]
            hsv = cv2.cvtColor(block, cv2.COLOR_BGR2HSV)  # HSV
            low = np.array([100, 43, 46])
            up = np.array([124, 255, 255])
            result = cv2.inRange(hsv, low, up)
            # 用计算均值的方式找蓝色最多的区块
            mean = cv2.mean(result)
            if mean[0] > max_mean:
                max_mean = mean[0]
                dist_r = r

        mask3 = np.zeros(shape=img.shape, dtype=np.uint8)
        cv2.rectangle(mask3, (dist_r[0]+3, dist_r[1]),
                      (dist_r[2]-3, dist_r[3]), (0, 255, 0), 2)
        # cv2.imshow('Mask3',mask3)
        #
        # cv2.imshow('Mask2', mask2)
        cv2.rectangle(img, (dist_r[0]+3, dist_r[1]),
                      (dist_r[2]-3, dist_r[3]), (0, 255, 0), 2)
        cv2.putText(img, 'Car Plate', (dist_r[0]+3, dist_r[1]-5),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2)
        imgRoi = img[dist_r[1]:dist_r[3]-20, dist_r[0]:dist_r[2]]
        # cv2.imshow('key',imgRoi)
        count = 1
        cv2.imwrite("Resources/Scan/NoPlate_" +
                    str(count)+'.jpg', imgRoi)  # 将图片写入文件
        cv2.imshow("lpr", img)

        ReadPlate("Resources/Scan/NoPlate_"+str(count)+'.jpg')  # 将图片进行分割
        translate_plate()  # 将图片进行转译
        cv2.waitKey(0)
    #
    # ##FloodFill算法
    # # def floodfiii():
    # def get_file_content(filePath):
    #     with open(filePath,'rb') as fp:
    #         return fp.read()
    # 主程
    lpr(img_path)


if __name__ == '__main__':
    carplate()
