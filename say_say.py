def choose(response : bool, state : str, mainwindow):
    if response:
        pygame.mixer.init()
        if state=='hello':
            # 加载音频文件 (支持 .wav, .mp3, .ogg 等)
            mainwindow.model_bubble.setText("牡丹盛绽映春辉，国粹非遗共翠微，我是牡丹，欢迎来到河南非遗世界")
            pygame.mixer.music.load(config.AUDIO_HELLO_PATH)
        elif state == 'interupt':
            # 加载音频文件 (支持 .wav, .mp3, .ogg 等)
            mainwindow.model_bubble.setText("已打断")
            pygame.mixer.music.load(config.AUDIO_INTERUPT_PATH)
        elif state == 'no_speak':
            mainwindow.model_bubble.setText("当前我没有说话")
            pygame.mixer.music.load(config.AUDIO_NO_SPEAK_PATH)
        elif state == 'brain_short':
            mainwindow.model_bubble.setText("不好意思，刚刚思绪有点乱，请您重新提问")
            pygame.mixer.music.load(config.AUDIO_BRAIN_SHORT_PATH)
        elif state == 'thinking':
            mainwindow.model_bubble.setText("请让我思考一下")
            pygame.mixer.music.load(config.AUDIO_THINKING_PATH)
        else:
            # 加载音频文件 (支持 .wav, .mp3, .ogg 等)
            mainwindow.model_bubble.setText("再见，欢迎您下次光临。")
            pygame.mixer.music.load(config.AUDIO_GOODBYE_PATH)
        # 播放音频
        pygame.mixer.music.play()
        # 等待播放完毕
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        if state == 'interupt' or state == 'brain_short':
            mainwindow.model_bubble.clear()
            logger.info("Say,Model bubble is cleared, state: %s", state)
            mainwindow.user_bubble.clear()
            logger.info("User bubble is cleared, state: %s", state)
    else:
        if state == 'hello':
            speaking('你好, 你有什么问题呢？')
        elif state == 'interupt':
            speaking('已打断')
        elif state == 'no_speak':
            speaking('当前我没有说话')
        elif state == 'brain_short':
            speaking('不好意思，刚刚大脑短路了,请你再问一遍吧')
        elif state == 'thinking':
            speaking('让我转动我的脑子思考一下')
        else:
            speaking('再见，欢迎您下次光临。')
