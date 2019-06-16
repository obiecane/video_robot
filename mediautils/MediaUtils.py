from mediautils import AudioMetaInfo
from mutagen.mp3 import MP3


# 获取指定音频文件的信息
# @param filename 文件名
# @return AudioMetaInfo
def get_audio_meta_info(filename: str) -> AudioMetaInfo.AudioMetaInfo:
    fmt = get_format(filename)
    if fmt != "mp3":
        raise Exception("暂时不支持%s格式文件" % fmt)
    music = MP3(filename)
    a_info = AudioMetaInfo.AudioMetaInfo()
    a_info.filename = filename
    a_info.duration = int(music.info.length * 1000)
    a_info.bitRate = music.info.bitrate
    a_info.sampleRate = music.info.sample_rate
    a_info.format = fmt
    return a_info


# 获取指定文件的文件格式名称
# @param filename 文件名
# @return str
def get_format(filename: str) -> str:
    split = filename.split(".")
    fmt = split[len(split) - 1]
    return fmt.lower()


if __name__ == "__main__":
    meta_info = get_audio_meta_info("F:/temp/imgvideo/6/gdqq.mp3")
    print(meta_info)
