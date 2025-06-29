# video.py
import os
from PySide6.QtCore import QObject, Signal, Qt
from PySide6.QtGui import QImage, QPainter, QColor, QPixmap
from config import logger

# 注意：此处使用了全局变量 WINDOW_SIZE，
# 建议在 main.py 中计算屏幕尺寸后赋值给该变量
WINDOW_SIZE = (1280, 800)  # 默认值，实际尺寸由 main.py 更新

class VideoStream(QObject):
    frame_loaded = Signal()

    def __init__(self, window_size : tuple[int, int]):
        super().__init__()
        self._running = True
        # 待机动画（2种，不包含呼吸动画）
        self.a_frames = []       # 待机动画1
        self.b_frames = []       # 待机动画2
        # 呼吸动画目录（等待唤醒状态）
        self.idle_frames_3 = []
        # 其它动画
        self.in_frames = []      # 进场（挥手动作）
        self.c_frames = []       # 说话动画
        self.farewell_frames = []  # 告别动画（再见）
        self.exit_frames = []      # 退场动画
        self.WINDOW_SIZE = window_size

    def load_frames(self, folder : str, target_list : list[QImage]):
        """加载指定文件夹中的图片到目标列表"""
        try:
            if not os.path.exists(folder):
                logger.info(f"Directory does not exist: {folder}")
                return
            file_list = sorted(
                [f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))],
                key=lambda x: int(''.join(filter(str.isdigit, x)) or 0)
            )
            for f in file_list:
                if not self._running:
                    break
                path = os.path.join(folder, f)
                img = QImage(path)
                if img.isNull():
                    logger.info(f"Cannot load image: {path}")
                    continue
                scaled_img = img.scaled(
                    int(self.WINDOW_SIZE[0]), int(self.WINDOW_SIZE[1]),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                final_img = QImage(self.WINDOW_SIZE[0], self.WINDOW_SIZE[1], QImage.Format_RGB32)
                painter = QPainter(final_img)
                offset_y = 0  # 根据需要调整
                painter.drawImage(
                    0,
                    0,
                    scaled_img
                )
                painter.end()
                target_list.append(final_img)
            self.frame_loaded.emit()
        except Exception as e:
            logger.exception(f"Frame loading error: {str(e)}")

    def stop(self):
        self._running = False
