import os
from dotenv import load_dotenv
from core import HistoryManager
from core import PreRetrieval, Retriever
from config import Config
from models import select_model

load_dotenv()


if __name__ == "__main__":
    config = Config("config/base.yaml")
    model = select_model(config)
    retriever = Retriever(config)
    # pre_retrieval.add_file("/home/zwj/workspace/ProjectAthena/src/data/file/鉴定工作报告、技术报告-0708.pdf")

    print(f"[{config.model_provider}:{config.get('model_name', 'default')}] Type 'exit' to quit")

    history_manager = HistoryManager()
    while True:
        query = input("\nUser: ")
        if query == "exit":
            break

        # 检索结果
        refs = retriever(query)
        # 重新构建用户的输入
        query = retriever.construct_query(query, refs)

        messages = history_manager.add_user(query)
        response = model.predict(messages, stream=config.stream)

        if config.stream:
            content = ""
            print(f"AI: ", end='', flush=True)
            for chunk in response:
                content += chunk.content
                print(f"{chunk.content}", end='', flush=True)
            print()
        else:
            content = response.content
            print(f"AI: {content}")

        history_manager.add_ai(content)
