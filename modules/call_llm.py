from langchain_community.llms import HuggingFaceEndpoint
import os
from dotenv import load_dotenv

load_dotenv()

huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")

class Call_LLM:
    def __init__(self,):
        # super().__init__()
        self.setup_hf_llm()
        # self.setup_hf_llm_mcq()
        # self.call_openai()

    def setup_hf_llm(self,):
        # print("--setup_hf_llm--")
        try:
            self.llm = HuggingFaceEndpoint(
            # repo_id='mistralai/Mixtral-8x7B-Instruct-v0.1',
            repo_id='mistralai/Mistral-7B-Instruct-v0.3',
            task="text-generation",
            max_new_tokens=2000,
            do_sample=False,
            huggingfacehub_api_token=huggingfacehub_api_token
            )

        except Exception as error:
            print(error)





