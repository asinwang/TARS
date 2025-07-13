"""
TARS 语音助手主程序
整合LLM模型处理、音频处理和配置管理
"""

from llm.model_handler import LLMModelHandler
from audio.audio_handler import AudioHandler
from utils.logger import logger


class TARSVoiceAssistant:
    """TARS语音助手主类"""
    
    def __init__(self):
        """初始化语音助手"""
        self.llm_handler = LLMModelHandler()
        self.audio_handler = AudioHandler()
        logger.info("TARS语音助手初始化完成")
    
    def process_user_input(self, user_input: str) -> None:
        """处理用户输入"""
        if not user_input:
            logger.warning("没有检测到有效的用户输入")
            return
        
        logger.info(f"用户输入: {user_input}")
        
        try:
            # 获取流式响应
            stream_data = self.llm_handler.get_response(user_input)
            
            # 处理流式响应并读出内容
            self.llm_handler.process_streaming_response_and_speak(
                stream_data, 
                speak_callback=self.audio_handler.speak_text_gtts
            )
            
        except Exception as e:
            logger.error(f"处理用户输入失败: {e}")
    
    def run(self) -> None:
        """运行语音助手"""
        # 使用默认麦克风作为源
        with self.audio_handler.microphone as source:
            self.audio_handler.recognizer.adjust_for_ambient_noise(
                source, 
                duration=5
            )  # 增加环境噪音适应时间
            logger.info("开始唤醒监听...")

            while True:
                logger.info("唤醒监听...")
                try:
                    # 监听唤醒词
                    text = self.audio_handler.listen_for_wakeup(source)
                    
                    if text and self.audio_handler.is_wakeup_word_detected(text):
                        logger.info("唤醒词已检测到...")
                        
                        # 播放唤醒响应
                        self.audio_handler.speak_wakeup_response()
                        
                        # 获取用户输入
                        user_input = self.audio_handler.get_voice_input(source)
                        
                        # 处理用户输入
                        if user_input:
                            logger.info(f"用户输入: {user_input}")  # 增加调试信息
                            self.process_user_input(user_input)
                        else:
                            logger.warning("没有检测到有效的用户输入")  # 增加调试信息
                            
                except KeyboardInterrupt:
                    logger.info("用户中断程序")
                    break
                except Exception as e:
                    logger.error(f"运行过程中发生错误: {e}")


def main():
    """主函数"""
    try:
        assistant = TARSVoiceAssistant()
        assistant.run()
    except Exception as e:
        logger.error(f"程序启动失败: {e}")


if __name__ == "__main__":
    main() 