# MT_BENCH_RU

Перевод оригинального [mt_bench](https://huggingface.co/datasets/dim/mt_bench_en) на русский язык. 
Переведенный датасет можно найти здесь: [dim/mt_bench_ru](https://huggingface.co/datasets/dim/mt_bench_ru)

## MT_BENCH_RU Leaderboard
Ссылка на google sheets [link](https://docs.google.com/spreadsheets/d/1aRZiYCjtHSjl_aw8fukKAcjpoNvknL9HwlmNveWeQ0E/edit?usp=sharing)

|model_name                          |mt_bench_ru_turn_1|mt_bench_ru_turn_2|mt_bench_ru_avg|score_date|
|------------------------------------|------------------|------------------|---------------|----------|
|gpt-3.5-turbo                       |8.7               |7.45              |8.075          |31.08.2023|
|Open-Orca/Mistral-7B-OpenOrca       |6.85              |5.95              |6.4            |15.12.2023|
|mistral-open-orca-ru-4600-step      |7.1625            |5.46              |6.31125        |15.12.2023|
|IlyaGusev/saiga_mistral_7b_lora     |6.567901          |5.3375            |5.9527005      |15.12.2023|
|verbalist_v10_1650                  |5.6125            |5                 |5.30625        |15.12.2023|
|verbalist_7b_v9_800                 |6.175             |4.375             |5.275          |15.12.2023|
|IlyaGusev/saiga2_13b_lora           |5.96              |4.12              |5.04           |31.08.2023|
|IlyaGusev/saiga2_7b_lora            |4.76              |3.62              |4.19           |31.08.2023|
|GigaChat(v1.13.0) когда только вышел|4.53              |3.53              |4.03           |31.08.2023|
|IlyaGusev/saiga_7b_lora             |4.23              |3.06              |3.645          |31.08.2023|
|ruGPT-3.5 13B saiga dataset         |3.71              |1.96              |2.835          |31.08.2023|
|dim/xglm-4.5b_dolly_oasst1_chip2    |2.28              |2.08              |2.18           |31.08.2023|


## Как пользоваться?
1. Создать 2 файла в корне проекта. 
- gpt_token - переменная среды OPENAI_API_KEY
- openai_base_url - переменная среды OPENAI_BASE_URL (необходима для обхода блокировки по IP)

2. Запустить оценку файла который лежит в `llm_judge/data/mt_bench/model_answer` с именем `EXAMPLE_MODEL.json` в режиме когда оценивается только одна модель. Необходимо поменять на ваш файл.

```bash
python -m llm_judge.gen_judgment --model-list EXAMPLE_MODEL --mode single --judge-file llm_judge/data/judge_prompts_ru.jsonl --question-file question_ru
```
3. Показываем результат оценок в консоли для каждого turn
```bash
python -m llm_judge.show_result
```
```console
Mode: single
Input file: llm_judge/data/mt_bench/model_judgment/gpt-4_single.jsonl

########## First turn ##########
                                                  score
model                                    turn          
mt_bench_ru_chatgpt                      1     8.700000
mistral-open-orca-ru-4600-step           1     7.162500
Mistral-7B-OpenOrca                      1     6.850000
saiga_mistral_7b_lora                    1     6.567901
verbalist_7b_v9_800                      1     6.175000
mt_bench_ru_saiga2_13b                   1     5.962500
verbalist_v10_1650                       1     5.612500
saiga_7b_v2                              1     5.587500
saiga_7b_v1                              1     5.234568
mt_bench_ru_saiga2_7b                    1     4.762500
mt_bench_ru_gigachat                     1     4.537500
mt_bench_ru_saiga2_13b_our_dataset       1     4.300000
mt_bench_ru_yandexgpt                    1     4.275000
saiga_7b_v1_ru                           1     4.237500
mt_bench_ru_saiga2_7b_our_dataset        1     4.062500
mt_bench_ru_gigasaiga_13b                1     3.712500
mt_bench_en_gigachat                     1     3.581250
saiga_7b_v2_ru                           1     3.500000
mt_bench_ru_xglm_4.5B_lora_saiga_dataset 1     2.737500
xglm_4.5b_v10_epoch_6_step_41141         1     2.637500
mt_bench_ru_rugpt_13B_our_dataset        1     2.612500
mt_bench_en_xglm_4.5B_lora_our_dataset   1     2.531250
xglm_4.5b_v10_epoch_6_step_41141_ru      1     2.325000
mt_bench_ru_xglm_4.5B_lora_our_dataset   1     2.287500

########## Second turn ##########
                                                  score
model                                    turn          
mt_bench_ru_chatgpt                      2     7.450000
Mistral-7B-OpenOrca                      2     5.950000
mistral-open-orca-ru-4600-step           2     5.462500
saiga_mistral_7b_lora                    2     5.337500
verbalist_v10_1650                       2     5.000000
mt_bench_ru_yandexgpt                    2     4.650000
saiga_7b_v1                              2     4.432099
verbalist_7b_v9_800                      2     4.375000
saiga_7b_v2                              2     4.150000
mt_bench_ru_saiga2_13b                   2     4.125000
mt_bench_ru_saiga2_7b                    2     3.625000
mt_bench_ru_gigachat                     2     3.537500
mt_bench_en_gigachat                     2     3.262500
saiga_7b_v1_ru                           2     3.062500
mt_bench_ru_saiga2_13b_our_dataset       2     2.987500
mt_bench_ru_saiga2_7b_our_dataset        2     2.975000
saiga_7b_v2_ru                           2     2.912500
mt_bench_ru_gigasaiga_13b                2     2.750000
mt_bench_en_xglm_4.5B_lora_our_dataset   2     2.200000
xglm_4.5b_v10_epoch_6_step_41141         2     2.137500
mt_bench_ru_xglm_4.5B_lora_our_dataset   2     2.087500
xglm_4.5b_v10_epoch_6_step_41141_ru      2     1.975000
mt_bench_ru_xglm_4.5B_lora_saiga_dataset 2     1.962500
mt_bench_ru_rugpt_13B_our_dataset        2     1.750000

########## Average ##########
                                             score
model                                             
mt_bench_ru_chatgpt                       8.075000
Mistral-7B-OpenOrca                       6.400000
mistral-open-orca-ru-4600-step            6.312500
saiga_mistral_7b_lora                     5.956522
verbalist_v10_1650                        5.306250
verbalist_7b_v9_800                       5.275000
mt_bench_ru_saiga2_13b                    5.043750
saiga_7b_v2                               4.868750
saiga_7b_v1                               4.833333
mt_bench_ru_yandexgpt                     4.462500
mt_bench_ru_saiga2_7b                     4.193750
mt_bench_ru_gigachat                      4.037500
saiga_7b_v1_ru                            3.650000
mt_bench_ru_saiga2_13b_our_dataset        3.643750
mt_bench_ru_saiga2_7b_our_dataset         3.518750
mt_bench_en_gigachat                      3.421875
mt_bench_ru_gigasaiga_13b                 3.231250
saiga_7b_v2_ru                            3.206250
xglm_4.5b_v10_epoch_6_step_41141          2.387500
mt_bench_en_xglm_4.5B_lora_our_dataset    2.365625
mt_bench_ru_xglm_4.5B_lora_saiga_dataset  2.350000
mt_bench_ru_xglm_4.5B_lora_our_dataset    2.187500
mt_bench_ru_rugpt_13B_our_dataset         2.181250
xglm_4.5b_v10_epoch_6_step_41141_ru       2.150000
```

4. Открываем просмотр в браузере отдельных ответов. Есть 2 режима. Single и side by side.
```bash
python -m llm_judge.qa_browser  --share --question-file question_ru
```

### Single 
![](./example_3.jpg)
### Side by side
![](./example.jpg)
![](./example_2.jpg)