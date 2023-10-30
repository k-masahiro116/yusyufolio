import pyaudio
import numpy as np
import math

class Stream:
    AUDIO = pyaudio.PyAudio()
    FORMAT = pyaudio.paInt16
    CHANNELS = 1  # モノラル
    RATE = 44100  # サンプルレート
    CHUNK = 2 ** 11  # データ点数
    RECORD_SECONDS = 5  # 録音する時間の長さ
    def __init__(self, input_index=0, output_index=1):
        self.stream = self.AUDIO.open(format=self.FORMAT,
                            channels=self.CHANNELS,
                            rate=self.RATE,
                            input=True,
                            output=True,
                            input_device_index=input_index,#←適したインデックスに変更してください.
                            output_device_index=output_index,#←適したインデックスに変更してください.
                            frames_per_buffer=self.CHUNK)
        self.stream.stop_stream()

def surveillance(stream):
    frames = []
    for i in range(0, int(Stream.RATE / Stream.CHUNK * Stream.RECORD_SECONDS)):
        buf = stream.read(Stream.CHUNK)
        data = np.frombuffer(buf, dtype="int16")
        frames.append(max(data))
    stream.stop_stream()
    return calculation(frames)

def calculation(frames):
    rms = (max(frames))
    db = 20 * math.log10(rms) if rms > 0.0 else -math.inf
    return db
    
def index_search():
    p = pyaudio.PyAudio()
    for index in range(0, p.get_device_count()):
        print(p. get_device_info_by_index(index))
