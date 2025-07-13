"""
音频处理类
负责语音识别和语音合成功能
"""

import io
import string
import time
from typing import Optional, Callable
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr

from config.settings import settings
from utils.logger import logger


class AudioHandler:
    """音频处理类"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self._setup_microphone()
    
    def _setup_microphone(self) -> None:
        """设置麦克风"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(
                    source, 
                    duration=settings.audio.ambient_noise_duration
                )
        except Exception as e:
            logger.error(f"麦克风设置失败: {e}")
    
    def is_valid_text(self, text: str) -> bool:
        """检查文本是否包含有效的单词"""
        return any(char not in string.punctuation and not char.isspace() for char in text)
    
    def speak_text_gtts(self, text: str, lang: Optional[str] = None) -> None:
        """使用gTTS进行语音合成"""
        if not self.is_valid_text(text):
            logger.warning(f"Warning: Invalid text received: '{text}'")
            return
        
        try:
            # 使用配置的语言，如果没有指定的话
            if lang is None:
                lang = settings.audio.language
            
            tts = gTTS(text=text, lang=lang, slow=False)
            mp3_fp = io.BytesIO()
            
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            
            # 将 MP3 数据加载到 AudioSegment 对象中
            audio_segment = AudioSegment.from_file(
                io.BytesIO(mp3_fp.read()), 
                format="mp3"
            )

            # 根据配置调整语速
            if settings.audio.playback_speed != 1.0:
                audio_segment = audio_segment.speedup(
                    playback_speed=settings.audio.playback_speed
                )
            
            play(audio_segment)
            
        except Exception as e:
            logger.error(f"语音合成失败: {e}")
    
    def get_voice_input(self, source, max_attempts: Optional[int] = None) -> Optional[str]:
        """获取语音输入"""
        if max_attempts is None:
            max_attempts = settings.audio.max_attempts
        
        attempts = 0
        while attempts < max_attempts:
            logger.info("麦克风监听...")
            
            try:
                # 增加环境噪音适应时间
                self.recognizer.adjust_for_ambient_noise(
                    source, 
                    duration=settings.audio.ambient_noise_duration
                )
                
                # 监听音频
                audio = self.recognizer.listen(
                    source, 
                    phrase_time_limit=settings.audio.phrase_time_limit
                )
                
                # 识别音频
                text = self.recognizer.recognize_google(
                    audio, 
                    language='zh-CN'
                )
                logger.info(f"麦克风监听的是: {text}")
                return text
                
            except sr.UnknownValueError:
                logger.warning("get_voice_input无法理解音频")
            except sr.RequestError as e:
                logger.error(f"get_voice_input请求错误; {e}")
            except Exception as e:
                logger.error(f"get_voice_input发生未知错误: {e}")
            
            attempts += 1
            logger.info(f"麦克风监听尝试次数: {attempts}/{max_attempts}")
        
        logger.warning("麦克风监听多次尝试后仍无法理解音频")
        return None
    
    def listen_for_wakeup(self, source) -> Optional[str]:
        """监听唤醒词"""
        try:
            # 持续监听麦克风
            audio = self.recognizer.listen(
                source, 
                phrase_time_limit=settings.audio.wakeup_phrase_time_limit
            )
            
            # 识别音频
            text = self.recognizer.recognize_google(
                audio, 
                language='zh-CN'
            ).lower()
            
            logger.info(f"唤醒监听到: {text}")
            return text
            
        except sr.UnknownValueError:
            logger.warning("无法理解音频")
        except sr.RequestError as e:
            logger.error(f"请求错误; {e}")
        except Exception as e:
            logger.error(f"发生未知错误: {e}")
        
        return None
    
    def is_wakeup_word_detected(self, text: str) -> bool:
        """检测是否包含唤醒词"""
        return settings.wakeup.wakeup_word in text
    
    def speak_wakeup_response(self) -> None:
        """播放唤醒响应"""
        self.speak_text_gtts(settings.wakeup.response_text)
        time.sleep(settings.wakeup.response_delay)  # 延迟确保语音提示播放完毕 