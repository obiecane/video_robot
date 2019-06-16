from typing import Any

from mediautils import MetaInfo


class VideoMetaInfo(MetaInfo.MetaInfo):

    def __init__(self):
        super().__init__()
        # 视频（帧）宽度 ，单位为px
        self.width = None
        # 视频（帧）高度 ，单位为px
        self.height = None
        # 音频时长, 单位：毫秒
        self.duration = None
        # 比特率，单位：Kb / s    指视频每秒传送（包含）的比特数
        self.bitRate = None
        # 编码器
        self.encoder = None
        # 帧率，单位：FPS（Frame Per Second）  指视频每秒包含的帧数
        self.frameRate = None
        # 视频旋转角度
        self.rotate = None
        # 视频中包含的音频信息
        self.musicMetaInfo = None

    def __str__(self):
        return "VideoMetaInfo(filename=%s, duration=%s)" % (self.filename, self.duration)

