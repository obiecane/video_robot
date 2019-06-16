# -*- coding: UTF-8 -*-
from PIL import Image, ImageDraw, ImageFont
import subprocess
import re
import TimeUtils
from mediautils import VideoMetaInfo
from mediautils import MediaUtils
from mediautils import AudioMetaInfo
########################################################################################################################
#    Author: zak                                                                                                       #
#    Note: Please install [ffmpeg] application and [pillow, mutagen] library before run this script.                   #
########################################################################################################################

base_dir = "F:/temp/imgvideo/6/"
video_width = 1920
video_height = 1080


def format_text(text: str) -> dict:
    ret = dict()
    font_size = 55
    text = text.replace(r" ", "")
    text = text.replace(r",", "，")
    text = "田田" + text

    width = video_width * 0.7
    height = video_height * 0.8

    while True:
        text_list = []
        op_text = text
        fnt = ImageFont.truetype("./MSYH.ttf", font_size)
        while True:
            text_size = fnt.getsize(op_text)

            if not text_size[0] > width:
                text_list.append(op_text)
                break

            tmp_len = int(width / font_size) - 1
            while True:
                tmp_len += 1
                tmp = op_text[:tmp_len]
                tmp_size = fnt.getsize(tmp)
                if tmp_size[0] > width:
                    break

            while True:
                tmp_len -= 1
                tmp = op_text[:tmp_len]
                tmp_size = fnt.getsize(tmp)
                if not tmp_size[0] > width:
                    op_text = op_text[tmp_len:]
                    text_list.append(tmp)
                    break
        example_size = fnt.getsize("田")
        first_line_size = fnt.getsize(text_list[0])
        if not (len(text_list) + 2.618) * first_line_size[1] > height:
            ret["fnt"] = fnt
            ret["text_list"] = text_list
            ret["example_size"] = example_size
            ret["first_line_size"] = first_line_size
            break
        else:
            font_size -= 1

    return ret


def draw_image(new_img, text: str, title: str):
    title = "《%s》" % title
    draw = ImageDraw.Draw(new_img)
    img_size = new_img.size
    # 画线
    # draw.line((0, 0) + img_size, fill=128)
    # draw.line((0, img_size[1], img_size[0], 0), fill=128)

    dic = format_text(text)

    first_line_size = dic["first_line_size"]
    example_size = dic["example_size"]
    text_list = dic["text_list"]
    fnt = dic["fnt"]

    x = (img_size[0] - first_line_size[0]) / 2
    y = (img_size[1] - first_line_size[1] * (len(text_list) + 2.618)) / 2
    for i, t in enumerate(text_list):
        tmp = x + example_size[0] * 2 if i == 0 and len(text_list) > 1 else x
        t = t[2:] if i == 0 else t
        draw.text((tmp, y + first_line_size[1] * i), t, font=fnt, fill=(255, 255, 255))

    title_size = fnt.getsize(title)
    draw.text((video_width - video_width * 0.15 - title_size[0], first_line_size[1] * len(text_list) + example_size[1] * 1.618 + y), title, font=fnt, fill=(255, 255, 255))
    del draw


def new_image(width, height, text: str, filename: str, color=(0, 0, 0, 255), show_image=False) -> str:
    new_img = Image.new('RGBA', (int(width), int(height)), color)
    draw_image(new_img, text, "ss")
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


def gen_ffmpeg_conf_file(img_list: list, text_list: list) -> str:
    string = ''
    for i in range(len(img_list)):
        text = text_list[i]
        img_name = img_list[i]
        dur = len(text) / 5
        string += "file %s\nduration %d\n" % (img_name, dur)
    # string += "file " + img_list[len(img_list) - 1] + "\n"

    fn = base_dir + "in.txt"
    open(fn, "w").write(string)
    fn = fn.replace(r"/", "\\")
    return fn


# 通过图片生成视频
def gen_video_by_images(img_list: list, text_list: list) -> VideoMetaInfo.VideoMetaInfo:
    cnf_file = gen_ffmpeg_conf_file(img_list, text_list)
    video_name = "%s%s.mp4" % (base_dir, TimeUtils.get_curr_datetime_ms_str())
    (status, output) = subprocess.getstatusoutput(
        "ffmpeg -y -f concat -safe 0 -i \"%s\" -pix_fmt yuv420p %s" % (cnf_file, video_name))
    findall = re.findall(r'time=\d{,3}:\d{,3}:\d{,3}.\d{,3}', output)
    clock = findall[len(findall) - 1].split("=")[1]

    v_info = VideoMetaInfo.VideoMetaInfo()
    v_info.filename = video_name
    v_info.duration = TimeUtils.convert_clock_2_times(clock)
    print(v_info.filename)
    return v_info
    pass


if __name__ == "__main__":
    text1 = "学校门口的公交站叫十里店，大家都戏称自己是十里店大学的，2.75环。大四了，考研失败，下午投了简历刚被拒。。。好吧，三月，春风十里，好不想毕业，虽然一直吐槽自己学校，临走了还是不舍。室友喜欢带自家酿的葡萄酒，很好喝，春风十里宜人，这些都如你一样，那么好，我都舍不得"
    text = "愿漂泊的人都有酒喝 愿孤独的人都会唱歌。 愿相爱的人都有未来，愿等待的人都有回答。 愿孤单的人不必永远逞强，愿逞强的人身边永远都有个肩膀。 愿肩膀可以接住你的欢喜忧伤，愿有情人永生执手相望。 愿你如阳光，明媚不忧伤；愿你如月光，明亮不清冷。 愿你最爱的人，也最爱你。"
    text2 = "5年前结婚时，我家那位唱着这首歌，在烟火光影里款款走来。"
    str_list = []
    img_list = []
    str_list.append(text)
    str_list.append(text1)
    str_list.append(text2)

    for i, t in enumerate(str_list):
        img_name = new_image(video_width, video_height, t, base_dir + "img%d" % i, show_image=False)
        img_list.append(img_name)

    # 提取视频时长
    v_info = gen_video_by_images(img_list, str_list)
    print(v_info)
    # 拼接音频, 使得音频时长大于等于视频时长
    a_info = MediaUtils.get_audio_meta_info("F:/temp/imgvideo/6/gdqq.mp3")

    # ffmpeg -f concat -i list.txt -c copy out.mp3
    #     file 'love.mp3'
    #     file 'love2.mp3'
    # 截取音频, 使得音频时长和视频时长相等
    #  ffmpeg -i out.mp3 -ss 00:00:00.0 -t 00:06:38 -acodec copy love3.mp3
    # 混合视频和音频
    # ffmpeg -i no-audio.mp4 -i audio.mp3 -c copy /path/to/output.mp4
