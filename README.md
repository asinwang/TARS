# TARS 语音助手

一个基于大语言模型的智能语音助手，支持语音唤醒、语音识别和语音合成功能。

## 项目结构

```
TARS/
├── llm/                    # 大语言模型处理模块
│   ├── __init__.py
│   └── model_handler.py    # LLM模型处理类
├── audio/                  # 音频处理模块
│   ├── __init__.py
│   └── audio_handler.py    # 音频处理类
├── utils/                  # 工具模块
│   ├── __init__.py
│   └── logger.py          # 日志处理类
├── config/                 # 配置模块
│   ├── __init__.py
│   └── settings.py        # 配置设置类
├── main.py                # 主程序
├── requirements.txt       # 依赖包列表
└── README.md             # 项目说明
```

## 功能特性

- 🎤 **语音唤醒**: 支持自定义唤醒词
- 🗣️ **语音识别**: 实时语音转文字
- 🤖 **智能对话**: 基于大语言模型的智能回复
- 🔊 **语音合成**: 文字转语音播放
- ⚙️ **配置管理**: 灵活的配置系统
- 📝 **日志记录**: 完整的日志记录功能

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置说明

### 环境变量配置

可以通过环境变量覆盖默认配置：

```bash
# LLM配置
export LLM_BASE_URL="http://192.168.1.99:11434/v1"
export LLM_API_KEY="ollama"
export LLM_MODEL_NAME="qwen2.5vl:32b"

# 音频配置
export AUDIO_LANGUAGE="zh-cn"
export AUDIO_PLAYBACK_SPEED="1.5"

# 唤醒词配置
export WAKEUP_WORD="塔斯"
export WAKEUP_RESPONSE_TEXT="需要什么帮助！"
```

### 默认配置

- **唤醒词**: "塔斯"
- **响应文本**: "需要什么帮助！"
- **语言**: 中文 (zh-cn)
- **播放速度**: 2.5倍速

## 使用方法

### 运行程序

```bash
python main.py
```

### 使用流程

1. 启动程序后，系统开始监听唤醒词
2. 说出唤醒词（默认："塔斯"）
3. 系统响应后，说出您的问题或指令
4. 系统将智能回复并语音播放

### 退出程序

按 `Ctrl+C` 退出程序。

## 模块说明

### LLM模块 (`llm/`)

负责与大语言模型的交互，包括：
- 模型连接和配置
- 文本生成和流式响应处理
- 图片编码（支持多模态）

### 音频模块 (`audio/`)

负责音频处理，包括：
- 语音识别（Speech-to-Text）
- 语音合成（Text-to-Speech）
- 麦克风管理和音频播放
- 唤醒词检测

### 工具模块 (`utils/`)

提供通用工具功能：
- 日志记录和管理
- 时间戳格式化
- 错误处理

### 配置模块 (`config/`)

管理系统配置：
- 环境变量支持
- 默认配置管理
- 配置验证

## 开发说明

### 添加新功能

1. 在相应模块中添加新的类或方法
2. 更新配置文件（如需要）
3. 在主程序中集成新功能
4. 更新文档

### 扩展配置

在 `config/settings.py` 中添加新的配置类：

```python
@dataclass
class NewConfig:
    """新功能配置"""
    param1: str = "default_value"
    param2: int = 100
```

### 自定义唤醒词

修改环境变量或直接修改 `config/settings.py` 中的 `WakeupConfig` 类。

## 故障排除

### 常见问题

1. **麦克风无法识别**
   - 检查麦克风权限
   - 确保网络连接正常（语音识别需要网络）

2. **语音合成失败**
   - 检查网络连接
   - 确认gTTS服务可用

3. **模型连接失败**
   - 检查Ollama服务是否运行
   - 确认模型名称正确

### 日志查看

程序运行时会输出详细的日志信息，包括：
- 时间戳
- 操作类型
- 错误信息

## 许可证

本项目采用 MIT 许可证。
