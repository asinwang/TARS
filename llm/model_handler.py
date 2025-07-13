"""
LLM模型处理类
负责与大型语言模型的交互
"""

import nltk
import ssl
import json
import base64
from typing import Generator, List, Dict, Any, Optional, Iterator
from openai import OpenAI

from config.settings import settings
from utils.logger import logger


class LLMModelHandler:
    """LLM模型处理类"""
    
    def __init__(self):
        self.client = OpenAI(
            base_url=settings.llm.base_url,
            api_key=settings.llm.api_key,
        )
        self._setup_ssl()
        self._setup_nltk()
    
    def _setup_ssl(self) -> None:
        """设置SSL配置"""
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context
    
    def _setup_nltk(self) -> None:
        """设置NLTK分句器"""
        try:
            nltk.download('punkt_tab')
        except Exception as e:
            logger.warning(f"NLTK下载失败: {e}")
    
    def encode_image(self, image_path: str) -> str:
        """编码图片为base64字符串"""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
        except Exception as e:
            logger.error(f"图片编码失败: {e}")
            return ""
    
    def get_response(self, input_text: str, images: Optional[List[str]] = None) -> Iterator[str]:
        """获取模型响应"""
        try:
            # 构建消息内容
            content: List[Dict[str, Any]] = [{"type": "text", "text": input_text}]
            
            # 如果有图片，添加图片内容
            if images:
                for image_path in images:
                    encoded_image = self.encode_image(image_path)
                    if encoded_image:
                        content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encoded_image}"
                            }
                        })
            
            # 创建聊天完成请求
            completion = self.client.chat.completions.create(
                model=settings.llm.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": content,
                    }
                ],
                top_p=settings.llm.top_p,
                stream=settings.llm.stream,
                stream_options={"include_usage": settings.llm.include_usage},
            )
            
            # 返回流式响应
            return (chunk.model_dump_json() for chunk in completion)
            
        except Exception as e:
            logger.error(f"获取模型响应失败: {e}")
            return iter([])
    
    def process_streaming_response_and_speak(self, stream_data: Iterator[str], 
                                          speak_callback=None) -> str:
        """处理流式响应并调用语音合成"""
        accumulated_text = ""
        spoken_sentences = set()  # 用于存储已经朗读过的句子
        
        try:
            for chunk in stream_data:
                # 解析JSON数据
                response_chunk = json.loads(chunk)
                
                # 检查是否有内容字段
                if 'choices' in response_chunk and len(response_chunk['choices']) > 0:
                    delta = response_chunk['choices'][0].get('delta', {})
                    content = delta.get('content')
                    
                    if content:
                        # 累积文本内容
                        accumulated_text += content
                        
                        # 使用nltk进行句子分割
                        sentences = nltk.sent_tokenize(accumulated_text)
                        
                        if sentences:
                            for sentence in sentences:
                                # 判断句子是否完整且尚未朗读过
                                if (sentence.endswith((',', '.', '!', '?', '，', '。', '！', '？' ,'#','-')) 
                                    and sentence not in spoken_sentences):
                                    # 提取完整的句子
                                    complete_sentence = sentence
                                    logger.info(f"Accumulated content: {complete_sentence}")
                                    
                                    # 调用语音合成回调
                                    if speak_callback:
                                        speak_callback(complete_sentence)
                                    
                                    spoken_sentences.add(complete_sentence)  # 标记为已朗读
                                    accumulated_text = accumulated_text.replace(complete_sentence, '', 1)  # 从累积文本中移除
                    else:
                        logger.warning("Warning: No content found in the current chunk.")
                else:
                    logger.warning("Warning: No choices found in the current chunk.")
                    
        except Exception as e:
            logger.error(f"处理流式响应失败: {e}")
        
        return accumulated_text 