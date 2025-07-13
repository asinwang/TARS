"""
配置设置类
包含所有系统配置参数
"""

import os
from dataclasses import dataclass, field


@dataclass
class LLMConfig:
    """LLM模型配置"""
    base_url: str = "http://192.168.1.99:11434/v1"
    api_key: str = "ollama"
    model_name: str = "qwen2.5vl:32b"
    top_p: float = 0.8
    stream: bool = True
    include_usage: bool = True


@dataclass
class AudioConfig:
    """音频处理配置"""
    language: str = 'zh-cn'
    playback_speed: float = 2.5
    ambient_noise_duration: int = 1
    phrase_time_limit: int = 10
    max_attempts: int = 5
    wakeup_phrase_time_limit: int = 1


@dataclass
class WakeupConfig:
    """唤醒词配置"""
    wakeup_word: str = "塔斯"
    response_text: str = "需要什么帮助！"
    response_delay: int = 1


@dataclass
class Settings:
    """主配置类"""
    llm: LLMConfig = field(default_factory=LLMConfig)
    audio: AudioConfig = field(default_factory=AudioConfig)
    wakeup: WakeupConfig = field(default_factory=WakeupConfig)
    
    # 环境变量覆盖
    def __post_init__(self):
        # LLM配置
        llm_base_url = os.getenv('LLM_BASE_URL')
        if llm_base_url:
            self.llm.base_url = llm_base_url
        llm_api_key = os.getenv('LLM_API_KEY')
        if llm_api_key:
            self.llm.api_key = llm_api_key
        llm_model_name = os.getenv('LLM_MODEL_NAME')
        if llm_model_name:
            self.llm.model_name = llm_model_name
        
        # 音频配置
        audio_language = os.getenv('AUDIO_LANGUAGE')
        if audio_language:
            self.audio.language = audio_language
        audio_playback_speed = os.getenv('AUDIO_PLAYBACK_SPEED')
        if audio_playback_speed:
            self.audio.playback_speed = float(audio_playback_speed)
        
        # 唤醒词配置
        wakeup_word = os.getenv('WAKEUP_WORD')
        if wakeup_word:
            self.wakeup.wakeup_word = wakeup_word
        wakeup_response_text = os.getenv('WAKEUP_RESPONSE_TEXT')
        if wakeup_response_text:
            self.wakeup.response_text = wakeup_response_text


# 全局配置实例
settings = Settings() 