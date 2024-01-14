import json

from datasets import load_dataset
from tqdm import tqdm

from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
import torch


from datasets import load_dataset


def generate_orca_ru(
    tokenizer,
    model,
    generation_config,
    instructions,
):
    system = "Вы помощник ИИ, который помогает людям находить информацию."
    prompt = [
        {
            "role": "system",
            "content": system,
        },
        *[
            {"role": "user" if i % 2 == 0 else "assistant", "content": instruction}
            for i, instruction in enumerate(instructions)
        ],
    ]
    prompt = tokenizer.apply_chat_template(
        prompt,
        tokenize=False,
        add_generation_prompt=True,
    )

    def generate(model, tokenizer, prompt, generation_config):
        data = tokenizer(prompt, return_tensors="pt", add_special_tokens=True)
        data = data.to(model.device)
        output_ids = model.generate(**data, generation_config=generation_config)[0]
        output_ids = output_ids[len(data["input_ids"][0]) :]

        output = tokenizer.decode(output_ids, skip_special_tokens=True)
        return output.strip()

    return generate(
        model=model,
        tokenizer=tokenizer,
        prompt=prompt,
        generation_config=generation_config,
    )


def evaluate_mt_bench_ru(
    weights_path,
    output_save_path,
):
    dataset = load_dataset("dim/mt_bench_ru")
    dataset = dataset["train"]
    dataset = dataset.to_list()

    tokenizer = AutoTokenizer.from_pretrained(weights_path)
    model = AutoModelForCausalLM.from_pretrained(
        weights_path,
        torch_dtype=torch.bfloat16,
        device_map={"": 0},
    )
    generation_config = GenerationConfig(
        bos_token_id=1,
        eos_token_id=32000,
        pad_token_id=32000,
        max_new_tokens=4000,
        repetition_penalty=1.0,
    )
    model.eval()
    # Test generation
    print(
        generate_orca_ru(
            model=model,
            tokenizer=tokenizer,
            generation_config=generation_config,
            instructions=["Почему трава зеленая?"],
        )
    )

    for i in tqdm(range(len(dataset))):
        item = dataset[i]
        conversation = []
        dataset[i]["replies"] = []
        for turn in item["turns_ru"]:
            conversation.append(turn)
            print("USER: ", turn)
            bot_output = generate_orca_ru(
                model=model,
                tokenizer=tokenizer,
                generation_config=generation_config,
                instructions=conversation,
            )
            print("BOT: ", bot_output)
            conversation.append(bot_output)
            dataset[i]["replies"].append(bot_output)
            print()
            print("==============================")
            print()
        #     break
        # break
    with open(
        output_save_path,
        "w",
        encoding="utf-8",
    ) as outfile:
        json.dump(
            dataset,
            outfile,
            ensure_ascii=False,
        )


if __name__ == "__main__":
    weights_path = "dim/mistral-open-orca-ru-4600-step"
    model_name = "EXAMPLE_MODEL.json"
    output_save_path = f"llm_judge/data/mt_bench/model_answer/{model_name}"
    evaluate_mt_bench_ru(
        weights_path=weights_path,
        output_save_path=output_save_path,
    )
