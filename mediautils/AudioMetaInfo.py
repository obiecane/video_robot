from mediautils import MetaInfo


class AudioMetaInfo(MetaInfo.MetaInfo):
    def __init__(self):
        super().__init__()
        # 音频时长, 单位：毫秒
        self.duration = None
        # 比特率，单位：Kb / s  指音频每秒传送（包含）的比特数
        self.bitRate = None
        # 采样频率，单位：Hz  指一秒钟内对声音信号的采样次数
        self.sampleRate = None
