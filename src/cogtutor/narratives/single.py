import json
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import argparse


def load_and_chat_from_json(base_model_path, input_file, output_file, system_role):
    # 加载基础模型和 tokenizer
    print("加载基础模型和 Tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(base_model_path, trust_remote_code=True)
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_path,
        trust_remote_code=True,
        device_map="auto",
        torch_dtype=torch.float16  # 使用 FP16 减少显存占用（需要支持 FP16 的硬件）
    )
    base_model.eval()  # 设置为推理模式
    print("模型加载完成！")

    # 定义基础模型对话函数
    def chat_with_base_model(messages, max_new_tokens=200, temperature=0.7):
        # 将消息模板转化为模型输入
        input_text = tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_tensors="pt",
            return_dict=True
        ).to(base_model.device)

        # 生成模型输出
        outputs = base_model.generate(
            **input_text,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=temperature
        )

        # 解码输出文本
        outputs = outputs[:, input_text["input_ids"].shape[1]:]
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response

    # 从输入文件加载问题
    print(f"从文件 {input_file} 加载问题...")
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    all_conversations = []
    # 遍历模块
    for module in data:
        module_code = module["code"]
        problems = module["problems"]

        print(f"\n正在处理模块: {module_code}")

        # 保存每个模块的对话记录
        conversation_log = {"code": module_code, "problems": []}

        for problem in problems:
            question = problem["problem"]
            print(f"问题: {question}")

            # 定义系统提示词和用户问题
            messages = [
                {"role": "system", "content": system_role},
                {"role": "user", "content": question}
            ]

            # 模型生成回答
            answer = chat_with_base_model(messages)
            print(f"回答: {answer}")

            # 记录问题和回答
            conversation_log["problems"].append({
                "problem": question,
                "response": answer
            })

        # 将当前模块记录添加到总记录中
        all_conversations.append(conversation_log)

    # 写入对话记录到输出文件
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_conversations, f, ensure_ascii=False, indent=4)
    print(f"所有对话记录已保存到 {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a script for question answering with a base model")
    parser.add_argument("--base_model_path", type=str, required=True, help="Path to the base model")
    parser.add_argument("--input_file", type=str, required=True, help="Path to the input JSON file")
    parser.add_argument("--output_file", type=str, required=True, help="Path to the output JSON file")
    parser.add_argument("--system_role", type=str, required=True, help="System role for the model")
    args = parser.parse_args()

    load_and_chat_from_json(
        base_model_path=args.base_model_path,
        input_file=args.input_file,
        output_file=args.output_file,
        system_role=args.system_role
    )
