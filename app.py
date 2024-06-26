import gradio as gr
import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModel

# download internlm2 to the base_path directory using git tool
base_path = './HW4'
os.system(f'git clone https://code.openxlab.org.cn/amstrongzyf/HW4.git {base_path}')
model_path=base_path+'/final_model'

os.system(f'cd {model_path} && git lfs pull')

tokenizer = AutoTokenizer.from_pretrained(model_path,trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_path,trust_remote_code=True, torch_dtype=torch.float16).cuda()

def chat(message,history):
    for response,history in model.stream_chat(tokenizer,message,history,max_length=2048,top_p=0.7,temperature=1):
        yield response

gr.ChatInterface(chat,
                 title="InternLM2-1_8b_自我认知",
                description="""
这是一个不按标准输出的小助手哦.  
                 """,
                 ).queue(1).launch()

