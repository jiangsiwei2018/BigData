# coding=utf-8
import time
import numpy as np
from PIL import Image


from data_common.image_common.config import *
from data_common.utils.file_util import file_util

class ImageProcess:

    @staticmethod
    def image_train_data_read(data_path):
        for label in os.listdir(data_path):  # 获取目录下的所有文件
            label_path = data_path + '/' + label
            for image_path in os.listdir(label_path):
                image = Image.open(label_path + '/' + image_path)
                yield image, label

    @staticmethod
    def image_data_read(data_path):
        for label in os.listdir(data_path):  # 获取目录下的所有文件
            image_path = data_path + '/' + label
            image = Image.open(image_path)
            yield image, label

    @staticmethod
    def image_data_save(image, image_path, label='', suffix=''):
        print(f'save image to path: {image_path}/{label}/{suffix}')
        if not file_util.exists(image_path):
            file_util.mk_dirs(image_path)
        if label and not file_util.exists(f'{image_path}/{label}'):
            file_util.mk_dirs(f'{image_path}/{label}')
        image.save(f'{image_path}/{label}/{suffix}')

    @staticmethod
    def feature_transfer(image):
        """
        生成二值转换后的特征矩阵
        计算每副图像的行和、列和，共image_width + image_height个特征
        :param image:图像list
        :return:
        """
        image = image.resize((image_width, image_height))  # 标准化图像格式

        feature = []  # 计算特征
        for x in range(image_width):  # 计算行特征
            feature_width = 0
            for y in range(image_height):
                if image.getpixel((x, y)) == 0:
                    feature_width += 1
            feature.append(feature_width)

        for y in range(image_height):  # 计算列特征
            feature_height = 0
            for x in range(image_width):
                if image.getpixel((x, y)) == 0:
                    feature_height += 1
            feature.append(feature_height)
        return feature

    @staticmethod
    def image_simple_transfer(image, mode='L'):
        """
        图像粗清理: 将图像转换为灰度图像，将像素值小于某个值的点改成白色
        加阈值后类似：image.point
        :param image:
        :param mode:
        :return:
        """
        image = image.convert(mode)  # 转换为灰度图像，即RGB通道从3变为1
        image_new = Image.new(mode, image.size, 255)
        for y in range(image.size[1]):  # 遍历所有像素，将灰度超过阈值的像素转变为255（白）
            for x in range(image.size[0]):
                pix = image.getpixel((x, y))
                if int(pix) > threshold_grey:  # 灰度阈值
                    image_new.putpixel((x, y), 255)
                else:
                    image_new.putpixel((x, y), pix)
        return image_new

    @staticmethod
    def image_detail_transfer(image):
        """
        图像细清理
        获取干净的二值化的图片。
        图像的预处理：
        1. 先转化为灰度
        2. 再二值化
        3. 然后清除噪点
        参考:http://python.jobbole.com/84625/
        image.point类似:
        for x in range(w):
            for y in range(h):
                pix = img.getpixel((x,y))
                img.putpixel((x,y), colors[pix[0]])
        """
        image_l = image.convert('L')  # 转化为灰度图
        threshold_table = ImageProcess.get_threshold_table()
        out = image_l.point(threshold_table, '1')  # 变成二值图片:0表示黑色,1表示白色

        noise_point_list = []  # 通过算法找出噪声点,第一步比较严格,可能会有些误删除的噪点
        for x in range(out.width):
            for y in range(out.height):
                res_9 = ImageProcess.sum_9_region(out, x, y)
                if (0 < res_9 < 3) and out.getpixel((x, y)) == 0:  # 找到孤立点
                    pos = (x, y)  #
                    noise_point_list.append(pos)
        ImageProcess.image_noise_pixel_process(out, noise_point_list)
        return out

    @staticmethod
    def get_threshold_table(threshold=140):
        """
        获取灰度转二值的映射table
        :param threshold:
        :return:
        """
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        return table

    @staticmethod
    def gene_grid_abs(x1=0, x2=0, y1=0, y2=0, x_step=1, y_step=1):
        """生成当前格点的前后左右相对坐标"""
        x_step = x_step if x2 > x1 else -x_step
        y_step = y_step if y2 > y1 else -y_step
        x2 = x2 + 1 if x_step > 0 else x2 - 1
        y2 = y2 + 1 if y_step > 0 else y2 - 1
        Y, X = np.mgrid[y1:y2:y_step, x1:x2:x_step]
        shape = int((x2 - x1) / x_step) * int((y2 - y1) / y_step)
        array_list = []
        for dos in zip(X.reshape(shape), Y.reshape(shape)):
            array_list.append(dos)
        # print(array_list)
        return array_list, shape

    @staticmethod
    def sum_9_region(img, x, y):
        """
        9邻域框,以当前点为中心的田字框,黑点个数,作为移除一些孤立的点的判断依据
        :param img:
        :param x:
        :param y:
        :return:
        """
        cur_pixel = img.getpixel((x, y))  # 当前像素点的值
        width = img.width
        height = img.height

        if cur_pixel == 1:  # 如果当前点为白色区域,则不统计邻域值
            return 0

        if y == 0:  # 第一行
            if x == 0:  # 左上顶点,4邻域
                grid = (0, 1, 0, 1)
            elif x == width - 1:  # 右上顶点
                grid = (0, -1, 0, 1)
            else:  # 最上非顶点,6邻域
                grid = (-1, 1, 0, 1)
        elif y == height - 1:  # 最下面一行
            if x == 0:  # 左下顶点
                grid = (0, 1, 0, -1)
            elif x == width - 1:  # 右下顶点
                grid = (0, -1, 0, -1)
            else:  # 最下非顶点,6邻域
                grid = (-1, 1, 0, -1)
        else:  # y不在边界
            if x == 0:  # 左边非顶点
                grid = (0, 1, -1, 1)
            elif x == width - 1:  # 右边非顶点
                # print('%s,%s' % (x, y))
                grid = (0, -1, -1, 1)
            else:  # 具备9领域条件的
                grid = (-1, 1, -1, 1)

        array_list, shape = ImageProcess.gene_grid_abs(*grid)
        items = []
        x_y = np.array([x, y])
        for array in array_list:
            item = tuple( x_y + np.array(array))
            item2 = eval(repr(item))
            try:
                items.append(img.getpixel(item2))
            except Exception as e:
                print(e)
                items.append(1)
        return shape - sum(items)

    # @staticmethod
    # def sum_9_region(img, x, y):
    #     """
    #     9邻域框,以当前点为中心的田字框,黑点个数,作为移除一些孤立的点的判断依据
    #     :param img: Image
    #     :param x:
    #     :param y:
    #     :return:
    #     """
    #     cur_pixel = img.getpixel((x, y))  # 当前像素点的值
    #     width = img.width
    #     height = img.height
    #
    #     if cur_pixel == 1:  # 如果当前点为白色区域,则不统计邻域值
    #         return 0
    #
    #     if y == 0:  # 第一行
    #         if x == 0:  # 左上顶点,4邻域
    #             # 中心点旁边3个点
    #             sum = cur_pixel \
    #                   + img.getpixel((x, y + 1)) \
    #                   + img.getpixel((x + 1, y)) \
    #                   + img.getpixel((x + 1, y + 1))
    #             return 4 - sum
    #         elif x == width - 1:  # 右上顶点
    #             sum = cur_pixel \
    #                   + img.getpixel((x, y + 1)) \
    #                   + img.getpixel((x - 1, y)) \
    #                   + img.getpixel((x - 1, y + 1))
    #
    #             return 4 - sum
    #         else:  # 最上非顶点,6邻域
    #             sum = img.getpixel((x - 1, y)) \
    #                   + img.getpixel((x - 1, y + 1)) \
    #                   + cur_pixel \
    #                   + img.getpixel((x, y + 1)) \
    #                   + img.getpixel((x + 1, y)) \
    #                   + img.getpixel((x + 1, y + 1))
    #             return 6 - sum
    #     elif y == height - 1:  # 最下面一行
    #         if x == 0:  # 左下顶点
    #             # 中心点旁边3个点
    #             sum = cur_pixel \
    #                   + img.getpixel((x + 1, y)) \
    #                   + img.getpixel((x + 1, y - 1)) \
    #                   + img.getpixel((x, y - 1))
    #             return 4 - sum
    #         elif x == width - 1:  # 右下顶点
    #             sum = cur_pixel \
    #                   + img.getpixel((x, y - 1)) \
    #                   + img.getpixel((x - 1, y)) \
    #                   + img.getpixel((x - 1, y - 1))
    #
    #             return 4 - sum
    #         else:  # 最下非顶点,6邻域
    #             sum = cur_pixel \
    #                   + img.getpixel((x - 1, y)) \
    #                   + img.getpixel((x + 1, y)) \
    #                   + img.getpixel((x, y - 1)) \
    #                   + img.getpixel((x - 1, y - 1)) \
    #                   + img.getpixel((x + 1, y - 1))
    #             return 6 - sum
    #     else:  # y不在边界
    #         if x == 0:  # 左边非顶点
    #             sum = img.getpixel((x, y - 1)) \
    #                   + cur_pixel \
    #                   + img.getpixel((x, y + 1)) \
    #                   + img.getpixel((x + 1, y - 1)) \
    #                   + img.getpixel((x + 1, y)) \
    #                   + img.getpixel((x + 1, y + 1))
    #
    #             return 6 - sum
    #         elif x == width - 1:  # 右边非顶点
    #             # print('%s,%s' % (x, y))
    #             sum = img.getpixel((x, y - 1)) \
    #                   + cur_pixel \
    #                   + img.getpixel((x, y + 1)) \
    #                   + img.getpixel((x - 1, y - 1)) \
    #                   + img.getpixel((x - 1, y)) \
    #                   + img.getpixel((x - 1, y + 1))
    #
    #             return 6 - sum
    #         else:  # 具备9领域条件的
    #             sum = img.getpixel((x - 1, y - 1)) \
    #                   + img.getpixel((x - 1, y)) \
    #                   + img.getpixel((x - 1, y + 1)) \
    #                   + img.getpixel((x, y - 1)) \
    #                   + cur_pixel \
    #                   + img.getpixel((x, y + 1)) \
    #                   + img.getpixel((x + 1, y - 1)) \
    #                   + img.getpixel((x + 1, y)) \
    #                   + img.getpixel((x + 1, y + 1))
    #             return 9 - sum

    @staticmethod
    def image_noise_pixel_process(img, noise_point_list):
        """
        根据噪点的位置信息，消除二值图片的黑点噪声
        :type img:Image
        :param img:
        :param noise_point_list:
        :return:
        """
        for item in noise_point_list:
            img.putpixel((item[0], item[1]), 1)

    @staticmethod
    def image_get_split_pos(image):
        """获取切割图片位点： x轴固定, 沿着y方向扫描时, 非灰即白"""
        start_pos = None
        end_pos = None
        letters = []
        for x in range(image.size[0]):
            # x轴固定, 沿着y方向扫描时, 非灰即白
            for y in range(image.size[1]):
                pix = image.getpixel((x, y))
                # x轴固定, 沿y方向扫描, 某一个点是黑点时 则停止扫描
                if pix == 0:
                    is_black_flag = True
                    break
            else:
                # x轴固定, 沿y方向扫描全是白点
                is_black_flag = False

            # 初始位置条件：黑点、start_pos=None、end_pos=None
            if is_black_flag == True and start_pos is None and end_pos is None:
                start_pos = x     # 初始横坐标

            # 结束位置条件：白点、start_pos、end_pos=None；
            # 一个切割位查找结束，然后重置初始位置和结束位置
            if is_black_flag == False and start_pos is not None and end_pos is None:
                end_pos = x       # 结束横坐标
                letters.append((start_pos, end_pos))
                # 重置初始位置和结束位置
                start_pos = None
                end_pos = None
        return letters

    @staticmethod
    def image_split(image):
        """
        图像切割
        :param image:单幅图像
        :return:单幅图像被切割后的图像list
        """
        #找出每个字母开始和结束的位置  0 为黑 1为白
        letters = ImageProcess.image_get_split_pos(image)
        # 因为切割出来的图像有可能是噪声点
        # 筛选可能切割出来的噪声点
        subtract_array = []
        for each in letters:
            subtract_array.append(each[1]-each[0])
        re_set = sorted(subtract_array, reverse=True)[0:image_character_num]
        letter_choice = []
        for each in letters:
            if int(each[1] - each[0]) in re_set:
                letter_choice.append(each)
        # print(letter_choice)
        #切割图片
        image_split_array = []
        for each in letter_choice:
            # (切割的起始横坐标，起始纵坐标，切割的宽度，切割的高度)
            im_split = image.crop((each[0], 0, each[1], image.size[1]))
            im_split = im_split.resize((image_width, image_height))
            image_split_array.append(im_split)
        return image_split_array

    @staticmethod
    def image_captcha_path(captcha_path=None, limit=1000, save=False, save_path=None):
        """
        将验证码文件：粗处理, 细处理, 图像切割
        :return:
        """
        image_data = ImageProcess.image_data_read(captcha_path) #读取验证码文件
        num = 1
        for image, image_name in image_data:
            if num >= limit:
                break
            num += 1
            image_clean = ImageProcess.image_simple_transfer(image) #验证码图像粗清理
            image_out = ImageProcess.image_detail_transfer(image_clean) #验证码图像细清理
            image_split_result = ImageProcess.image_split(image_out) #图像切割
            for index, image_split in enumerate(image_split_result):
                label = image_name[index]
                if save and save_path:
                    suffix = f"{image_name.split('.')}_{int(time.time() * 1000)}_{index}"
                    ImageProcess.image_data_save(image_split, save_path, label, suffix=suffix)
                print(f'process image {num}: {image_name}_{index}_{label}')
                yield image_name, label, image_split

def print_result(item):
    print(item)

if __name__ == '__main__':
    from data_common.utils.pool_util import PoolUtility
    PoolUtility.process_pool_iter(print_result, ImageProcess.image_captcha_path(captcha_path), 30)