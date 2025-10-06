import json
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch
import argparse
from openai import OpenAI


def load_and_chat_auto(base_model_path, lora_weights_path, output_file, rounds, chatgpt_identity):

    # 限制对话轮数在20轮以内
    if rounds > 20:
        rounds = 20

    # 加载基础模型和tokenizer
    print("加载基础模型和Tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(base_model_path, trust_remote_code=True)
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_path,
        trust_remote_code=True,
        device_map="auto",  # 自动分配设备
        torch_dtype=torch.float16  # 使用FP16减少显存占用（需要支持FP16的硬件）
    )

    # 加载LoRA权重
    print("加载LoRA微调权重...")
    model = PeftModel.from_pretrained(base_model, lora_weights_path)
    model.eval()  # 设置为推理模式
    print("模型加载完成！")

    # 对话记录列表
    conversation_log = []

    # 定义 LoRA 模型对话函数
    def chat_with_lora_model(prompt, max_new_tokens=200, temperature=0.7):
        # 输入文本转为张量
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

        # 生成模型输出
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,  # 启用采样
            temperature=temperature  # 控制生成多样性
        )

        # 解码输出文本
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response

    # 定义 ChatGPT-3.5 对话函数
    def chat_with_gpt(prompt, identity):
        # 初始化 OpenAI 客户端
        client = OpenAI(
            base_url='https://api.pumpkinaigc.online/v1',
            api_key='sk-TT3RixAQWmVvW3qL5c3166A8A92d428cBfDb483cE3DdE85d'
        )

        # 调用 OpenAI 接口
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": identity},  # 定义ChatGPT身份
                {"role": "user", "content": prompt}
            ]
        )

        # 提取生成结果
        solution_description = response.choices[0].message.content
        return solution_description

    # 自动对话循环
    print("\n开始自动对话...")
    prompt = "你好！让我们来聊天吧。"  # 初始对话输入
    for i in range(rounds):
        print(f"\n第 {i + 1} 回合：")

        # LoRA 模型生成回复
        lora_response = chat_with_lora_model(prompt)
        print(f"Qwen (LoRA): {lora_response}")
        conversation_log.append({"speaker": "Qwen (LoRA)", "content": lora_response})

        # ChatGPT-3.5 生成回复
        gpt_response = chat_with_gpt(lora_response, chatgpt_identity)
        print(f"ChatGPT-3.5: {gpt_response}")
        conversation_log.append({"speaker": "ChatGPT-3.5", "content": gpt_response})

        # 更新下一个输入提示
        prompt = gpt_response

    # 将对话内容保存到JSON文件
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(conversation_log, f, ensure_ascii=False, indent=4)
    print(f"\n对话内容已保存到文件：{output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a chat script with LoRA and ChatGPT integration")
    parser.add_argument("--base_model_path", type=str, required=True, help="Path to the base model")
    parser.add_argument("--lora_weights_path", type=str, required=True, help="Path to the LoRA weights")
    parser.add_argument("--output_file", type=str, default="conversation_log.json", help="Path to save the output JSON file")
    parser.add_argument("--rounds", type=int, default=10, help="Number of conversation rounds (max 20)")
    parser.add_argument("--chatgpt_identity", type=str, required=True, help="System identity for ChatGPT, including background information")
    args = parser.parse_args()

    load_and_chat_auto(
        base_model_path=args.base_model_path,
        lora_weights_path=args.lora_weights_path,
        output_file=args.output_file,
        rounds=args.rounds,
        chatgpt_identity=args.chatgpt_identity
    )
