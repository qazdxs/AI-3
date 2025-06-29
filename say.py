def build_prompt(question : str, mainwindow):

    results = faiss_db.query(question, n_results=2)
    context = "\n".join(results["documents"]) if results["documents"] else ""
    logger.info(f"Retrived Context: {context}")
    # 如果没有相关上下文，直接将问题传递给大模型
    if not context.strip():
        choose(True, state='no_retrival', mainwindow = mainwindow)
        return False
    return f"""下面的"记忆"是你的记忆，请你根据你的记忆回答问题，不要反问我。
                记忆: {context}
                问题: {question}
            """

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
        elif state == 'no_retrival':
            mainwindow.model_bubble.setText("你所问的问题我当前不太清楚")
            pygame.mixer.music.load(config.AUDIO_NO_RETRIVAL_PATH)
        else:
            # 加载音频文件 (支持 .wav, .mp3, .ogg 等)
            mainwindow.model_bubble.setText("再见，欢迎您下次光临。")
            pygame.mixer.music.load(config.AUDIO_GOODBYE_PATH)
        # 播放音频
        pygame.mixer.music.play()
        # 等待播放完毕
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        if state == 'interupt'  or state == 'brain_short' or state == 'no_retrival':
            mainwindow.model_bubble.clear()
            logger.info("Say, Model bubble is cleared, state: %s", state)
            mainwindow.user_bubble.clear()
            logger.info("Say, User bubble is cleared, state: %s", state)
