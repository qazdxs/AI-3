# config.py
import os
import sys
from set_logger import setup_logging

def resource_path(relative_path : str) -> str: 
    """获取资源文件的绝对路径"""
    try:
        # 首先尝试获取 PyInstaller 的临时路径
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
            logger.info(f"Using PyInstaller temporary path: {base_path}")
        else:
            # 如果不是打包环境，使用当前目录
            base_path = os.path.dirname(os.path.abspath(__file__))
            # print(f"使用当前目录作为基础路径: {base_path}")
    except Exception as e:
        # 如果出现任何异常，使用当前目录
        base_path = os.path.dirname(os.path.abspath(__file__))
        logger.info(f"Use current directory as base path: {base_path}")
        logger.exception(f"Exception: {str(e)}")
    
    full_path = os.path.join(base_path, relative_path)
    if not os.path.exists(full_path):
        logger.warning(f"Warning: File does not exist: {full_path}")
        # 尝试在当前目录下查找
        current_dir_path = os.path.join(os.getcwd(), relative_path)
        if os.path.exists(current_dir_path):
            logger.info(f"File found in current directory: {current_dir_path}")
            return current_dir_path
    return full_path

logger = setup_logging()
# 基础路径
BASE_PATH = os.path.abspath(".")

# 模型相关路径
VOSK_MODEL_PATH = resource_path("models/vosk-model-cn-0.22")
    # print(f"VOSK_MODEL_PATH: {VOSK_MODEL_PATH}")
EMBEDDING_MODEL_PATH = resource_path("models/embedding/BAAI/bge-large-zh-v1___5")

# 数据库路径
# CHROMA_DB_PATH = resource_path("chroma_db")
FAISS_INDEX_PATH = resource_path("data/faiss_data/faiss_index.index")
JSONL_DATA_PATH = resource_path("data/faiss_data/faiss_data.json")
FAISS_KEYWORD_PATH = resource_path("data/faiss_data/my_keywords.json")

# 音频文件路径
AUDIO_HELLO_PATH = resource_path("audio/hello.mp3")
AUDIO_GOODBYE_PATH = resource_path("audio/goodbye.mp3")
AUDIO_INTERUPT_PATH = resource_path("audio/interupt.mp3")
AUDIO_NO_SPEAK_PATH = resource_path("audio/no_speak.mp3")
AUDIO_THINKING_PATH = resource_path("audio/thinking.mp3")
AUDIO_BRAIN_SHORT_PATH = resource_path("audio/brain_short.mp3")
AUDIO_NO_RETRIVAL_PATH = resource_path("audio/no_retrival.mp3")

# 动画帧路径
FRAME_DIR_IN = resource_path("process/begin/begin_treated")
FRAME_DIR_A = resource_path("process/wait/wait1_treated")
FRAME_DIR_B = resource_path("process/wait/wait2_treated")
FRAME_DIR_IDLE_C = resource_path("process/wait/wait3_treated")   # 呼吸动画目录（等待状态使用）
FRAME_DIR_C = resource_path("process/say/speak_treated")
FRAME_DIR_FAREWELL = resource_path("process/quit/thank_treated")
FRAME_DIR_EXIT = resource_path("process/quit/exit_treated")

# icon图标路径
ICON_CLOSE = resource_path("icon/close.png")
ICON_HEAR = resource_path("icon/hear.png")
ICON_NO_HEAR = resource_path("icon/no_hear.png")
ICON_INTERUPT = resource_path("icon/interupt.png")

# 背景图片路径
BACKGROUND_IMAGE = resource_path("icon/background(1).jpg")

# 本地模型名称
LOCAL_MODEL = "llama3.2"

# 讯飞语音识别API配置列表
# 每个配置项包含APPID、APIKey和APISecret
XF_API_CONFIGS = [
    {
        "APPID": "2f730ad3",
        "APIKey": "5d6076cdb8adfd96dc8ae481f07ce682",
        "APISecret": "Yjk1NjQzYjU4ZDczN2U1MjNjMDFlMmNm"
    },
    # 备用API配置1
    {
        "APPID": "3941158",
        "APIKey": "6a8b89a798df21ba598b0c225da49484",
        "APISecret": "M2M5YTFlNmRlYTZhMWRiM2YwZTBmNDRh"
    },
    # 备用API配置2
    {
        "APPID": " 2ddf381b",
        "APIKey": "ac150afaf51742aa2daf2e0b5612ae4b",
        "APISecret": "OTYyMDU4NDA5NGZlN2QyMzFlNGRiOTBi"
    }
]

# logging.config.fileConfig('logger.ini')
# logger = logging.getLogger('appLogger')
# 智谱API配置
ZHIPU_API_KEY = "aa95a87da85447b09343e4ecfc751c9b.nwuABmnOBiJBmXXW"  # 请替换为您的智谱API密钥
ZHIPU_MODEL = "glm-4-plus"  # 智谱模型名称

# 知识图谱
HTML_PATH = resource_path("heritage/heritage/templates/index.html")