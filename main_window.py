class RotatingButtonsWidget(QWidget):
    def __init__(self, mainwindow, parent=None, radius_x=200, radius_y=350, num_buttons=8, button_radius=30):
        self.mainwindow = mainwindow
        # 计算宽高，确保按钮不被裁剪
        width = radius_x * 2 + button_radius * 2
        height = radius_y * 2 + button_radius * 2
        super().__init__(parent)
        self.setFixedSize(width, height)

        # 默认中心在组件中心
        self.center_x = width / 2
        self.center_y = height / 2
        self.radius_x = radius_x
        self.radius_y = radius_y
        self.button_radius = button_radius
        self.num_buttons = num_buttons
        self.buttons = []
        self.angles = []
        self.paused = False

        # 创建按钮并安装事件过滤器
        for i in range(self.num_buttons):
            angle = (2 * math.pi * i) / self.num_buttons
            x = self.center_x + self.radius_x * math.cos(angle)
            y = self.center_y + self.radius_y * math.sin(angle)
            btn = QPushButton(str(i+1), self)
            btn.setGeometry(int(x - self.button_radius), int(y - self.button_radius),
                            self.button_radius * 2, self.button_radius * 2)
            btn.setStyleSheet(
                f"""
                QPushButton {{ background-color: rgb(166, 27, 41); color: white; border-radius: {self.button_radius}px; font-size: 20px; }}
                QPushButton:hover {{ background-color: rgb(130, 17, 31); }}
                QPushButton:pressed {{ background-color: rgb(75, 30, 47); }}
                """
            )
            # 设置工具提示
            category = self.mainwindow.Class[i+1]
            items = self.mainwindow.Class_List[category][:6]
            tooltip_text = f"{category}\n\n其中部分非遗文化如下\n\n" + "\n".join([item for item in items if item])
            btn.setToolTip(tooltip_text)
            btn.clicked.connect(lambda checked, num=i+1: self.button_clicked(num))
            btn.installEventFilter(self)
            self.buttons.append(btn)
            self.angles.append(angle)

        # 定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate_buttons)
        self.timer.start(50)

    def rotate_buttons(self):
        if self.paused:
            return
        speed = 0.01
        for i, btn in enumerate(self.buttons):
            angle = self.angles[i] + speed
            self.angles[i] = angle
            x = self.center_x + self.radius_x * math.cos(angle)
            y = self.center_y + self.radius_y * math.sin(angle)
            btn.move(int(x - self.button_radius), int(y - self.button_radius))

    def button_clicked(self, num):
        # 或者更精确的方式（推荐）：
        for i in reversed(range(self.mainwindow.text_layout.count())):
            widget = self.mainwindow.text_layout.itemAt(i).widget()
            if isinstance(widget, QLabel):
                widget.deleteLater()

        # 然后重新设置滚动区域（确保 UI 更新）
        self.mainwindow.text_scroll_area.update()
        # print(self.mainwindow.front_button)
        if self.mainwindow.front_button != num:
            text = f"按钮 {num} 被点击了！"
            # 计算尺寸
            label_width = int(self.mainwindow.rotating_width * 0.5)
            label_height = int(self.mainwindow.rotating_height * 0.05)
            # 添加标签
            nums = self.mainwindow.Class[num]
            titles = self.mainwindow.Class_List[nums]

            for title in set(titles):
                if title == '':
                    continue
                label = QLabel()
                label.setStyleSheet("""
                                    QLabel {
                                        background: rgba(30, 30, 30, 0.7);
                                        color: white;
                                        font-size: 24px;
                                        font-weight: bold;
                                        border-radius: 10px;
                                        padding: 10px 10px;
                                    }
                                    QLabel:hover {
                                        background: rgba(50, 50, 50, 0.8);
                                        background-color: rgb(130, 17, 31);
                                    }
                                    """)
                label.setText(title)
                label.setAlignment(Qt.AlignLeft)
                label.setFixedSize(label_width, label_height)
                # 添加悬停提示
                label.setToolTip(f"{summary[title]}")
                # 安装事件过滤器以处理鼠标悬停事件
                label.installEventFilter(self)
                self.mainwindow.text_layout.addWidget(label)
        else:
            label_width, label_height = int(self.mainwindow.rotating_width * 0.5), int(self.mainwindow.rotating_height * 0.6)
            label = QLabel(self.mainwindow.text_overlay_container)
            label.setStyleSheet("""
                                QLabel {
                                    background: rgba(30, 30, 30, 0.7);
                                    color: white;
                                    font-size: 24px;
                                    font-weight: bold;
                                    border-radius: 10px;
                                    padding: 5px 5px;
                                }
                                QLabel:hover {
                                    background: rgba(50, 50, 50, 0.8);
                                }
                                """)
            label.setText('\n\n'.join([f'{i}: {value}' for i, value in (self.mainwindow.Class.items())]))
            label.setAlignment(Qt.AlignLeft)
            label.setFixedSize(label_width, label_height)
            # 添加悬停提示
            label.setToolTip("点击任意类别查看详细信息")
            # 安装事件过滤器以处理鼠标悬停事件
            label.installEventFilter(self)
            self.mainwindow.text_layout.addWidget(label)

        self.mainwindow.front_button = num

    def eventFilter(self, watched, event):
        if watched in self.buttons:
            if event.type() == QEvent.Enter:
                self.paused = True
            elif event.type() == QEvent.Leave:
                self.paused = False
        elif isinstance(watched, QLabel):
            if event.type() == QEvent.Enter:
                # 当鼠标进入标签时，可以添加额外的视觉效果
                watched.setStyleSheet(watched.styleSheet().replace("rgba(30, 30, 30, 0.7)", "rgba(50, 50, 50, 0.8)"))
            elif event.type() == QEvent.Leave:
                # 当鼠标离开标签时，恢复原始样式
                watched.setStyleSheet(watched.styleSheet().replace("rgba(50, 50, 50, 0.8)", "rgba(30, 30, 30, 0.7)"))
        return super().eventFilter(watched, event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 0))
