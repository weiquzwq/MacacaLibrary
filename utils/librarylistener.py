# -*- coding: utf-8 -*-
import re
import events as event
import os
from PIL import Image
import images2gif
from robot.libraries.BuiltIn import BuiltIn
import shutil


class LibraryListener(object):
    ROBOT_LISTENER_API_VERSION = 2

    def start_suite(self, name, attrs):
        event.dispatch('scope_start', attrs['longname'])

    def end_suite(self, name, attrs):
        event.dispatch('scope_end', attrs['longname'])

    def start_test(self, name, attrs):
        event.dispatch('scope_start', attrs['longname'])

    def end_test(self, name, attrs):
        my_variables = BuiltIn().get_variables()
        current_output_dir = os.path.abspath(my_variables['${OUTPUTDIR}'])
        fullname = my_variables['${SUITE_NAME}'] + '.' + my_variables['${TEST_NAME}'] + '-MOBILE'
        fullname = re.sub(r'\s+', '_', fullname)

        test_output_dir = os.path.join(current_output_dir, 'gif', fullname)
        gif_name = fullname + '.gif'
        gif_path = os.path.join(current_output_dir, gif_name)

        myPicList = self.GetDirImageList(os.path.abspath(my_variables['${OUTPUTDIR}']), False)
        # human sort png list eg: [1,11,2] -- > [1,2,11]
        myPicList = self.sort_nicely(myPicList)

        if myPicList:
            self.GetGifAnimationFromImages(gif_path, myPicList, 2)
            if os.path.isdir(test_output_dir):
                shutil.rmtree(test_output_dir)
            os.makedirs(test_output_dir)

        for item in os.listdir(current_output_dir):
            # if re.search(r'mobile-gif.*png|.*gif',item):
            if re.search(r'(^mobile-gif-.*png)|(.*MOBILE\.gif$)', item):
                shutil.move(os.path.join(current_output_dir, item), os.path.join(test_output_dir, item))

        event.dispatch('scope_end', attrs['longname'])

    # type 合成GIF分类
    # 0：图片缩放到最大宽度*最大高度（长方形）、并粘贴到最大宽度*最大高度（长方形）的白色背景图片中、居中后合成
    # 1：图片缩放到最大长度（正方形）、并粘贴到最大长度（正方形）的白色背景图片中、居中后合成
    # 2：图片不缩放、并粘贴到最大宽度*最大高度（长方形）的白色背景图片中、居中后合成
    # 3：图片不缩放、并粘贴到最大长度（正方形）的白色背景图片中、居中后合成
    # 4：原图直接合成(按宽度排序、不缩放也不粘贴到新的白色背景图片中)
    # 5：原图直接合成(按高度排序、不缩放也不粘贴到新的白色背景图片中)
    def GetGifAnimationFromImages(self, targetGifFilePath, srcImageFilePaths, type=0):
        # 用来合成的图片
        images = []
        # 取得所有图片中最大长度（宽度、高度）
        maxWidthAndHeight = 1
        # 最大宽度和高度
        maxWidth = 1
        maxHeight = 1
        # 取得图片按宽度从大到小排序的路径顺序
        widthAndFilePaths = []
        # 取得图片按高度从大到小排序的路径顺序
        heightAndFilePaths = []

        for imageFilePath in srcImageFilePaths:
            fp = open(imageFilePath, "rb")
            width, height = Image.open(fp).size
            widthAndFilePaths.append((width, imageFilePath))
            heightAndFilePaths.append((height, imageFilePath))
            maxWidth = max(maxWidth, width)
            maxHeight = max(maxHeight, height)
            fp.close()

        maxWidthAndHeight = max(maxWidthAndHeight, maxWidth, maxHeight)

        # 降序排列
        widthAndFilePaths.sort(key=lambda item: item[0], reverse=True)
        heightAndFilePaths.sort(key=lambda item: item[0], reverse=True)

        if type == 4 or type == 5:
            # 原图直接合成(按宽度排序)
            if type == 4:
                for widthAndFilePath in widthAndFilePaths:
                    img = Image.open(widthAndFilePath[1])
                    images.append(img)
            # 原图直接合成(按高度排序)
            if type == 5:
                for heightAndFilePath in heightAndFilePaths:
                    img = Image.open(heightAndFilePath[1])
                    images.append(img)
        else:
            for imageFilePath in srcImageFilePaths:
                fp = open(imageFilePath, "rb")
                img = Image.open(fp)
                width, height = img.size
                # 生成空的白色背景图片
                if type == 0 or type == 2:
                    # 长方形
                    imgResizeAndCenter = Image.new("RGB", [maxWidth, maxHeight], (255, 255, 255))
                elif type == 1 or type == 3:
                    # 正方形
                    imgResizeAndCenter = Image.new("RGB", [maxWidthAndHeight, maxWidthAndHeight], (255, 255, 255))

                if type == 0:
                    # 宽度/最大宽度>=高度/最大高度，使用小的缩放比例
                    if maxWidth / width >= maxHeight / height:
                        resizeImg = img.resize((width * maxHeight / height, maxHeight), Image.ANTIALIAS)
                        imgResizeAndCenter.paste(resizeImg, ((maxWidth - width * maxHeight / height) / 2, 0))
                    else:
                        resizeImg = img.resize((maxWidth, height * maxWidth / width), Image.ANTIALIAS)
                        imgResizeAndCenter.paste(resizeImg, (0, (maxHeight - height * maxWidth / width) / 2))
                if type == 1:
                    # 宽度>=高度，按宽度缩放到最大长度
                    if width >= height:
                        resizeImg = img.resize((maxWidthAndHeight, height * maxWidthAndHeight / width), Image.ANTIALIAS)
                        imgResizeAndCenter.paste(resizeImg,
                                                 (0, (maxWidthAndHeight - height * maxWidthAndHeight / width) / 2))
                    else:
                        resizeImg = img.resize((width * maxWidthAndHeight / height, maxWidthAndHeight), Image.ANTIALIAS)
                        imgResizeAndCenter.paste(resizeImg,
                                                 ((maxWidthAndHeight - width * maxWidthAndHeight / height) / 2, 0))
                elif type == 2:
                    imgResizeAndCenter.paste(img, ((maxWidth - width) / 2, (maxHeight - height) / 2))
                elif type == 3:
                    imgResizeAndCenter.paste(img, ((maxWidthAndHeight - width) / 2, (maxWidthAndHeight - height) / 2))

                images.append(imgResizeAndCenter)
                fp.close()

        images2gif.writeGif(targetGifFilePath, images, duration=1, nq=0.1)

    def GetDirImageList(self, dir_proc, recusive=True):
        resultList = []
        for file in os.listdir(dir_proc):
            if re.search(r'mobile-gif-.*png', file):  # <------ select specified picture type
                if os.path.isdir(os.path.join(dir_proc, file)):
                    if (recusive):
                        resultList.append(self.GetDirImageList(os.path.join(dir_proc, file), recusive))
                    continue
                resultList.append(os.path.join(dir_proc, file))

        # if run fail: append the last failure screenshot to gen-gif png list
        # disable this fx temporary
        """
        for file in os.listdir(dir_proc):
            if re.search(r'appium.*png',file):   # <------ select specified picture type
                if os.path.isdir(os.path.join(dir_proc, file)):
                    if (recusive):
                        resultList.append(self.GetDirImageList(os.path.join(dir_proc, file), recusive))
                    continue
                # rename appium-screenshot-x.png --> screenshot-x.png
                new_name = str(file).replace('appium-','Appium-')
                shutil.move(os.path.join(dir_proc,file),os.path.join(dir_proc,new_name))
                resultList.append(os.path.join(dir_proc, new_name))
        """
        return resultList

    # human sort
    def tryint(self, s):
        try:
            return int(s)
        except:
            return s

    def alphanum_key(self, s):
        return [self.tryint(c) for c in re.split('([0-9]+)', s)]

    def sort_nicely(self, l):
        l.sort(key=self.alphanum_key)
        return l
