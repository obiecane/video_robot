# -*- coding: UTF-8 -*-
from PIL import Image, ImageDraw, ImageFont
import os
import subprocess
import re
import ZakTimeUtils
'''
    Auth: zak
    Note: Please install [pillow] library before run this script.
'''

base_dir = "F:/temp/imgvideo/6/"

def draw_image(new_img, text: str):
    text.replace(r" ", "")
    text.replace(r",", "，")
    text = "   " + text
    draw = ImageDraw.Draw(new_img)
    img_size = new_img.size
    # 画线
    # draw.line((0, 0) + img_size, fill=128)
    # draw.line((0, img_size[1], img_size[0], 0), fill=128)

    font_size = 45
    text_list = []
    while True:
        font_size -= 5
        # msyh.ttf  微软雅黑
        fnt = ImageFont.truetype("msyh.ttf", font_size)
        width = img_size[0] * 0.7

        while True:
            text_size = fnt.getsize(text)
            if not text_size[0] > width:
                text_list.append(text)
                break

            tmp_len = int(width / font_size) - 1
            while True:
                tmp_len += 1
                tmp = text[:tmp_len]
                tmp_size = fnt.getsize(tmp)
                if tmp_size[0] > width:
                    break

            while True:
                tmp_len -= 1
                tmp = text[:tmp_len]
                tmp_size = fnt.getsize(tmp)
                if not tmp_size[0] > width:
                    text = text[tmp_len:]
                    text_list.append(tmp)
                    break

        text_size = fnt.getsize(text_list[0])
        if text_size[0] < img_size[0] and text_size[1] < img_size[1]:
            break

    # single_len = img_size[0] * 0.7 / font_size
    # text_list = []
    # while len(text) > single_len:

    x = (img_size[0] - text_size[0]) / 2
    y = (img_size[1] - text_size[1] * len(text_list)) / 2
    for i, t in enumerate(text_list):
        draw.text((x, y + text_size[1] * i), t, font=fnt, fill=(255, 0, 0))
    del draw


def new_image(width, height, text: str, filename: str, color=(0, 0, 0, 255), show_image=False) -> str:
    new_img = Image.new('RGBA', (int(width), int(height)), color)
    draw_image(new_img, text)
    if show_image:
        new_img.show()

    img_name = '%s_%s_%s.png' % (width, height, text) if filename is None else '%s.png' % filename
    new_img.save(img_name)
    del new_img
    return img_name


def new_image_with_file(fn):
    with open(fn, encoding='utf-8') as f:
        for l in f:
            l = l.strip()
            if l:
                ls = l.split(',')
                if '#' == l[0] or len(ls) < 2:
                    continue

                new_image(*ls)


def gen_ffmpeg_conf_file(img_list: list) -> str:

    string = ''
    for t in img_list:
        string += "file " + t + "\n" + "duration 3\n"
    string += "file " + img_list[len(img_list) - 1] + "\n"

    fn = base_dir + "in.txt"
    with open(fn, "w") as tmp:
        tmp.write(string)
    return fn

if __name__ == "__main__":
    text1 = "学校门口的公交站叫十里店，大家都戏称自己是十里店大学的，2.75环。大四了，考研失败，下午投了简历刚被拒。。。好吧，三月，春风十里，好不想毕业，虽然一直吐槽自己学校，临走了还是不舍。室友喜欢带自家酿的葡萄酒，很好喝，春风十里宜人，这些都如你一样，那么好，我都舍不得";
    text = "愿漂泊的人都有酒喝 愿孤独的人都会唱歌。 愿相爱的人都有未来，愿等待的人都有回答。 愿孤单的人不必永远逞强，愿逞强的人身边永远都有个肩膀。 愿肩膀可以接住你的欢喜忧伤，愿有情人永生执手相望。 愿你如阳光，明媚不忧伤；愿你如月光，明亮不清冷。 愿你最爱的人，也最爱你。"
    text2 = "5年前结婚时，我家那位唱着这首歌，在烟火光影里款款走来。"
    str_list = []
    img_list = []
    str_list.append(text)
    str_list.append(text1)
    str_list.append(text2)

    for i, t in enumerate(str_list):
        img_name = new_image(1920, 1080, t, base_dir + "img%d" % i, show_image=False)
        img_list.append(img_name)

    fn = gen_ffmpeg_conf_file(img_list)
    fn = fn.replace(r"/", "\\")
    (status, output) = subprocess.getstatusoutput("ffmpeg -y -f concat -safe 0 -i \"%s\" -pix_fmt yuv420p %s" % (fn, base_dir + "output.mp4"))
    print(output)
    findall = re.findall(r'time=\d{,3}:\d{,3}:\d{,3}.\d{,3}', output)
    print(findall[len(findall) - 1].split("=")[1])
    # 提取视频时长
    # 拼接音频, 使得音频时长大于等于视频时长
    # ffmpeg -f concat -i list.txt -c copy out.mp3
    #     file 'love.mp3'
    #     file 'love2.mp3'
    # 截取音频, 使得音频时长和视频时长相等
    #  ffmpeg -i out.mp3 -ss 00:00:00.0 -t 00:06:38 -acodec copy love3.mp3
    # 混合视频和音频
    # ffmpeg -i no-audio.mp4 -i audio.mp3 -c copy /path/to/output.mp4
