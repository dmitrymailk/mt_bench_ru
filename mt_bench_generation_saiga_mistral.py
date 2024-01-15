import os

# os.environ["CUDA_VISIBLE_DEVICES"] = "1"
import torch
from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
from datasets import load_dataset
import json
import shortuuid
import time
import tqdm

MODEL_NAME = "IlyaGusev/saiga_mistral_7b_lora"
DEFAULT_MESSAGE_TEMPLATE = "<s>{role}\n{content}</s>"
DEFAULT_RESPONSE_TEMPLATE = "<s>bot\n"
DEFAULT_SYSTEM_PROMPT = "Ты — Сайга, русскоязычный автоматический ассистент. Ты разговариваешь с людьми и помогаешь им."


class Conversation:
    def __init__(
        self,
        message_template=DEFAULT_MESSAGE_TEMPLATE,
        system_prompt=DEFAULT_SYSTEM_PROMPT,
        response_template=DEFAULT_RESPONSE_TEMPLATE,
    ):
        self.message_template = message_template
        self.response_template = response_template
        self.messages = [{"role": "system", "content": system_prompt}]

    def add_user_message(self, message):
        self.messages.append({"role": "user", "content": message})

    def add_bot_message(self, message):
        self.messages.append({"role": "bot", "content": message})

    def get_prompt(self, tokenizer):
        final_text = ""
        for message in self.messages:
            message_text = self.message_template.format(**message)
            final_text += message_text
        final_text += DEFAULT_RESPONSE_TEMPLATE
        return final_text.strip()


def generate(model, tokenizer, prompt, generation_config):
    data = tokenizer(prompt, return_tensors="pt", add_special_tokens=False)
    data = {k: v.to(model.device) for k, v in data.items()}
    output_ids = model.generate(**data, generation_config=generation_config)[0]
    output_ids = output_ids[len(data["input_ids"][0]) :]
    output = tokenizer.decode(output_ids, skip_special_tokens=True)
    return output.strip()


if __name__ == "__main__":
    config = PeftConfig.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(
        config.base_model_name_or_path,
        # load_in_8bit=True,
        torch_dtype=torch.float16,
        device_map={"": 0},
    )
    model = PeftModel.from_pretrained(
        model,
        MODEL_NAME,
    )
    model.eval()

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=False)
    generation_config = GenerationConfig.from_pretrained(MODEL_NAME)
    print(generation_config)
    generation_config.max_new_tokens = 4000

    inputs = [
        "Почему трава зеленая?",
    ]
    for inp in inputs:
        conversation = Conversation()
        conversation.add_user_message(inp)
        prompt = conversation.get_prompt(tokenizer)

        output = generate(model, tokenizer, prompt, generation_config)
        print(inp)
        print(output)
        print()
        print("==============================")
        print()

    dataset = load_dataset("dim/mt_bench_ru")

    dataset = dataset["train"].to_list()

    new_dataset = []
    model_id = "saiga_mistral_7b_lora-test"
    base_save_path = f"llm_judge/data/mt_bench/model_answer/{model_id}.jsonl"

    for item in tqdm.tqdm(dataset):
        replies = []
        conversation = Conversation()
        for turn in item["turns_ru"]:
            print(turn)
            conversation.add_user_message(turn)
            prompt = conversation.get_prompt(tokenizer)

            output = generate(model, tokenizer, prompt, generation_config)
            replies.append(output)
            print(output)
            conversation.add_bot_message(output)

            print("=" * 10)
            print("=" * 10)

        new_dataset.append(
            {
                "question_id": item["question_id"],
                "answer_id": shortuuid.uuid(),
                "model_id": model_id,
                "choices": [
                    {
                        "index": 0,
                        "turns": replies,
                    }
                ],
                "tstamp": time.time(),
            }
        )
        with open(base_save_path, "a") as f:
            json.dump(new_dataset[-1], f, ensure_ascii=False)
            f.write("\n")
        # break
