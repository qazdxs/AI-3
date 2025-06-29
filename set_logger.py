import os
import logging
import logging.config
from datetime import datetime
import time
def setup_logging():
    # 确保logs目录存在
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    log_filename = time.strftime('logs/mudan_%Y-%m-%d_%H-%M-%S.log')
    # 加载日志配置
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logger.ini')
    logging.config.fileConfig(config_path, defaults={'log_filename': log_filename})
    logger = logging.getLogger('appLogger')
    
    # 添加会话开始标记
    logger.info('-'*80)
    logger.info(f'开始时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    logger.info('-'*80)
    
    return logger

def get_logger():
    return logging.getLogger('appLogger')

# 当目录文件数超过以前的，删除以前的文件
def delete_old_log_files(directory):
    if os.path.exists(directory):
        files = os.listdir(directory)
        files.sort()
        if len(files) > 10:
            for file in files[:-10]:
                os.remove(os.path.join(directory, file))
