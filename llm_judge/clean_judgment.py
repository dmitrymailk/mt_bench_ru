"""
Clean model judgment files.
"""
import pandas as pd
import json

selected_models = [
    "mt_bench_ru_chatgpt",
    "Mistral-7B-OpenOrca",
    "mistral-open-orca-ru-4600-step",
    "saiga_mistral_7b_lora",
    "verbalist_v10_1650",
    "verbalist_7b_v9_800",
    "mt_bench_ru_saiga2_13b",
    "mt_bench_ru_saiga2_7b",
    "mt_bench_ru_gigachat",
    "mt_bench_ru_xglm_4.5B_lora_our_dataset",
    "saiga_7b_v1_ru",
    "mt_bench_ru_gigasaiga_13b",
]


if __name__ == "__main__":
    infile = "/code/llm_judge/data/mt_bench/model_judgment/gpt-4_single.jsonl"
    dataset = pd.read_json(infile, lines=True)
    dataset = dataset.to_dict("records")
    outfile = infile.replace(".jsonl", "_clean.jsonl")

    raw_lines = open(infile).readlines()
    rets = []
    for line in dataset:
        if line["model"] in selected_models:
            rets.append(line)

    with open(outfile, "w") as fout:
        for x in rets:
            fout.write(json.dumps(x) + "\n")
