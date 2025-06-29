# 牡丹智能对话系统

## 项目资源下载
- 模型文件：[百度网盘链接](通过网盘分享的文件：models.zip 链接: https://pan.baidu.com/s/15ZyH0jYMjHNLNI5aHrFuNQ 提取码: 41mp)
- data数据文件(keywords和faiss_data以及index)：[百度网盘链接](通过网盘分享的文件：data.zip 链接: https://pan.baidu.com/s/1ccoQmU1BSTbK_wJVYe5hCw 提取码: y3ke)
- 音频文件：[百度网盘链接](通过网盘分享的文件：audio.zip 链接: https://pan.baidu.com/s/1TVteiziRqByfiQcEVKt1sw 提取码: k8au)
- icon图标文件：[百度网盘链接](通过网盘分享的文件：icon.zip 链接: https://pan.baidu.com/s/1E69fO_b9Gp7ohXYnUOKzCQ 提取码: saz2)
- utils工具包文件：[百度网盘链接](通过网盘分享的文件：utils.zip 链接: https://pan.baidu.com/s/1pRgEfW88VZ_UVfZ-DQU3jQ 提取码: 7b9k)


## 项目架构
```
panda_mudan/
├── main.py            # 主程序入口，必需
├── main_window.py     # 主窗口界面实现，必需
├── config.py          # 配置文件，必需
├── requirements.txt   # 项目依赖，必需
├── logger.ini         # 日志配置，必需
├── set_logger.py      # 日志设置模块，必需
├── say.py             # 对话核心模块，必需
├── say_say.py         # 对话扩展模块，必需
├── faiss_db.py        # 向量数据库模块，必需
├── video.py           # 视频处理模块，必需
│
├── web_front/         # 前端界面，非必需
│   ├── index.html     # 主页面
│   ├── css/           # 样式文件
│   ├── js/            # JavaScript文件
│   ├── img/           # 图片资源
│   └── font/          # 字体文件
│
├── data/              # 数据存储目录，必需
├── logs/              # 日志文件目录，必需
├── models/            # 模型文件目录，必需
├── utils/             # 工具函数目录，非必需
├── process/           # 数据处理目录，必需
├── audio/             # 音频文件目录，必需
├── icon/              # 图标资源目录，必需
└── heritage/          # 历史数据目录，非必需
```

## 项目说明
牡丹智能对话系统是一个基于Python开发的智能对话应用，集成了语音识别、自然语言处理、语音合成等功能。

### 主要功能
1. 智能对话：支持自然语言交互
2. 语音识别：支持语音输入
3. 语音合成：支持语音输出
4. Web界面：提供友好的用户界面
5. 向量检索：支持语义相似度搜索

### 技术特点
- 使用FAISS进行高效的向量检索
- 采用模块化设计，便于扩展
- 完善的日志系统
- 响应式Web界面

### 环境要求
- Python 3.11+
- 详见requirements.txt

### 安装说明
1. 克隆项目代码
2. 安装依赖：`pip install -r requirements.txt`
3. 下载预训练模型并放置在models目录
4. 运行主程序：`python main.py`
-- web_front 下是前端界面
--heritage 下是neo4j的知识图谱界面，需要打开neo4j数据库

### 使用说明
1. 启动程序后，可以通过Web界面或桌面应用进行交互
2. 支持文本输入和语音输入两种方式
3. 系统会自动记录对话历史
4. 可以通过配置文件调整系统参数

### 注意事项
- 首次运行需要下载预训练模型
- 确保有足够的磁盘空间存储数据
- 建议使用虚拟环境运行项目

### 更新日志
- 2025-05-20：初始版本发布

### 联系方式
如有问题或建议，请通过以下方式联系：
- 邮箱：18037486834@163.com
- GitHub Issues

### 许可证
本项目采用 MIT 许可证
