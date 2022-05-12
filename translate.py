import cv2
import os
import numpy as np


def translate_plate() -> str:

    # 模版匹配
    # 准备模板(template[0-9]为数字模板；)
    template = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                '藏', '川', '鄂', '甘', '赣', '贵', '桂', '黑', '沪', '吉', '冀', '津', '晋', '京', '辽', '鲁', '蒙', '闽', '宁',
                '青', '琼', '陕', '苏', '皖', '湘', '新', '渝', '豫', '粤', '云', '浙']

    # 读取一个文件夹下的所有图片，输入参数是文件名，返回模板文件地址列表
    def read_directory(directory_name):
        referImg_list = []
        for filename in os.listdir(directory_name):
            referImg_list.append(directory_name + "/" + filename)
        return referImg_list

    # 获得中文模板列表（只匹配车牌的第一个字符）
    def get_chinese_words_list():
        chinese_words_list = []
        for i in range(34, 64):
            # 将模板存放在字典中
            c_word = read_directory('refer1/' + template[i])
            chinese_words_list.append(c_word)
        return chinese_words_list
    chinese_words_list = get_chinese_words_list()

    # 获得英文模板列表（只匹配车牌的第二个字符）

    def get_eng_words_list():
        eng_words_list = []
        for i in range(10, 34):
            e_word = read_directory('refer1/' + template[i])
            eng_words_list.append(e_word)
        return eng_words_list
    eng_words_list = get_eng_words_list()

    # 获得英文和数字模板列表（匹配车牌后面的字符）

    def get_eng_num_words_list():
        eng_num_words_list = []
        for i in range(0, 34):
            word = read_directory('refer1/' + template[i])
            eng_num_words_list.append(word)
        return eng_num_words_list
    eng_num_words_list = get_eng_num_words_list()

    # 读取一个模板地址与图片进行匹配，返回得分
    def template_score(template, images):
        # 将模板进行格式转换
        template_img = cv2.imdecode(np.fromfile(template, dtype=np.uint8), 1)
        template_img = cv2.cvtColor(template_img, cv2.COLOR_RGB2GRAY)
        # 模板图像阈值化处理——获得黑白图
        ret, template_img = cv2.threshold(
            template_img, 0, 255, cv2.THRESH_OTSU)
    #     height, width = template_img.shape
    #     image_ = image.copy()
    #     image_ = cv2.resize(image_, (width, height))
        image_ = images.copy()
        # 获得待检测图片的尺寸
        height, width = image_.shape
        # 将模板resize至与图像一样大小
        template_img = cv2.resize(template_img, (width, height))
        # 模板匹配，返回匹配得分
        result = cv2.matchTemplate(images, template_img, cv2.TM_CCOEFF_NORMED)
        return result[0][0]

    # 对分割得到的字符逐一匹配

    def template_matching():
        results = []
        for j in range(1, 8):
            path = "Split_Img/" + str(j) + '.jpg'
            # 1、得到模板
            img = cv2.imread("Split_Img/" + str(j) + '.jpg', 0)
            if j == 1:
                best_score = []
                for chinese_words in chinese_words_list:
                    score = []
                    for chinese_word in chinese_words:
                        result = template_score(chinese_word, img)
                        score.append(result)
                    best_score.append(max(score))
                i = best_score.index(max(best_score))
                print(i)
                r = template[34+i]
                results.append(r)
                continue
            if j == 2:
                best_score = []
                for eng_word_list in eng_words_list:
                    score = []
                    for eng_word in eng_word_list:
                        result = template_score(eng_word, img)
                        score.append(result)
                    best_score.append(max(score))
                i = best_score.index(max(best_score))
                # print(template[10+i])
                r = template[10+i]
                results.append(r)
                continue
            else:
                best_score = []
                for eng_num_word_list in eng_num_words_list:
                    score = []
                    for eng_num_word in eng_num_word_list:
                        result = template_score(eng_num_word, img)
                        score.append(result)
                    best_score.append(max(score))
                i = best_score.index(max(best_score))
                # print(template[i])
                r = template[i]
                results.append(r)
                continue
        return results

    # 调用函数获得结果
    result = template_matching()
    print(result)
    # "".join(result)函数将列表转换为拼接好的字符串，方便结果显示
    print("车牌号码是：")
    print("".join(result))
    return "".join(result)


if __name__ == '__main__':
    text = translate_plate()
    print(text)
