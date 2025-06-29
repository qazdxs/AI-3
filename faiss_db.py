import json
import time
import faiss
from sentence_transformers import SentenceTransformer
import os
import jieba
from collections import Counter
from config import FAISS_KEYWORD_PATH, EMBEDDING_MODEL_PATH, FAISS_INDEX_PATH, JSONL_DATA_PATH, logger

class FaissDB:
    def __init__(self, model_path : str, index_path : str, jsonl_path : str):
        """
        初始化FAISS数据库
        :param model_path: 嵌入模型路径
        :param index_path: FAISS索引文件路径
        :param jsonl_path: JSONL数据文件路径
        """
        self.embedding_model = SentenceTransformer(model_path)
        self.index_path = index_path
        self.jsonl_path = jsonl_path
        
        # 加载或创建索引
        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)
        else:
            self._create_index()
            
        # 加载元数据
        self.documents = []
        self.metadatas = []
        self.ids = []
        self.KeyWord = dict()
        self._load_metadata()
        self._load_Keywords()

    def load_data(self, path):
        with open(path, mode='r', encoding='utf-8') as f:
            data = json.load(f)
            # print(data['太极拳（陈氏太极拳）'])
        return data
        
    def _create_index(self):
        """创建新的FAISS索引"""
        # 读取JSONL文件并创建索引
        documents = []
        with open(self.jsonl_path, 'r', encoding='utf-8') as file:
            for line in file:
                data = json.loads(line)
                key = data['input']
                value =  data['output']
                combined_text = f"Title: {key}\nContent: {value}"
                documents.append(combined_text)
                
        # 生成嵌入向量
        embeddings = self.embedding_model.encode(documents).astype('float32')
        
        # 创建FAISS索引
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)
        
        # 保存索引
        faiss.write_index(self.index, self.index_path)
        
    def _load_metadata(self):
        # """加载元数据, jsonl格式数据"""
        # with open(self.jsonl_path, 'r', encoding='utf-8') as file:
        #     for line in file:
        #         data = json.loads(line)
        #         key = data['input']
        #         value =  data['output']
        #         combined_text = f"Title: {key}\nContent: {value}"
        #         self.documents.append(combined_text)
        #         self.metadatas.append({
        #             "title": key,
        #             "content": value,
        #             "question": f"关于 {key} 的信息"
        #         })
        #         self.ids.append(f"doc_{hash(key)}")
        """加载元数据, json格式数据"""
        try:
            # 处理文档数据
            with open(self.jsonl_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # 处理文档数据
            for key, value in data.items():
                combined_text = f"标题:{key}\n内容:{value}"
                self.documents.append(combined_text)
                self.metadatas.append({
                    "标题": key,
                    "内容": value,
                    "问题": f"关于 {key} 的信息"
                })
                self.ids.append(f"doc_{hash(key)}")
                
            logger.info(f"成功加载 {len(self.documents)} 条文档数据")
            
        except Exception as e:
            logger.exception(f"Error loading FAISS data: {e}")
            raise
    
    def query(self, query_text : str, n_results : int = 1) -> dict:
        """
        查询FAISS数据库
        :param query_text: 查询文本
        :param n_results: 返回结果数量
        :return: 查询结果
        """
        # start_time = time.time()
        keyword_index = self.KeySearch(query_text)
        # print(keyword_index)
        # print('3333333333', time.time() - start_time)

        # 生成查询向量
        query_embedding = self.embedding_model.encode([query_text]).astype('float32')
        
        # 搜索索引
        distances, indices = self.index.search(query_embedding, n_results)
        # print(indices)

        # print('111111111111111', time.time() - start_time)
        # 获取结果
        results = {
            "documents": [],
            "metadatas": [],
            "distances": distances[0].tolist()
        }
        for i in range(n_results):
            if i < len(keyword_index):
                results["documents"].append(self.documents[keyword_index[i]])
            if indices[0][i] < len(self.documents):  # 确保索引有效
                # print(distances[0][i])
                if distances[0][i] < 0.8:
                    results["documents"].append(self.documents[indices[0][i]])
                    results["metadatas"].append(self.metadatas[indices[0][i]])
        return results
