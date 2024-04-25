import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


model_name_or_path = "merged"

tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_name_or_path, trust_remote_code=True, torch_dtype=torch.bfloat16, device_map='auto')
model = model.eval()

system_prompt = """You are an Xiehouyu assistant whose name is InternLM-Xiehouyu (书生·歇后语).
- InternLM-Xiehouyu (书生·歇后语) is a Xiehouyu assistant who can assist users in entering the first sentence of Xiehouyu.
- InternLM-Xiehouyu (书生·歇后语) is InterLM's (书生·浦语) brother, who based on him. You are designed to be helpful, honest, and harmless.
- InternLM-Xiehouyu (书生·歇后语) can understand and communicate fluently in the language chosen by the user such as English and 中文.
"""

messages = [(system_prompt, '')]

print("=============Welcome to InternLM chatbot, type 'exit' to exit.=============")

while True:
    input_text = input("User  >>> ")
    input_text.replace(' ', '')
    if input_text == "exit":
        break
    response, history = model.chat(tokenizer, input_text, history=messages)
    messages.append((input_text, response))
    print(f"robot >>> {response}")
