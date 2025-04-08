import os
import json
from collections import defaultdict

script_dir = os.path.dirname(os.path.abspath(__file__))
task2_dir = os.path.join(script_dir, '../task_2')
pages_dir = os.path.join(task2_dir, 'pages_tokens_lemmas')
output_file = os.path.join(script_dir, 'inverted_index.txt')

if not os.path.exists(pages_dir):
    raise FileNotFoundError(
        f"Директория не найдена: {pages_dir}"
    )

inverted_index = defaultdict(lambda: {"count": 0, "inverted_array": []})

for page_folder in sorted(os.listdir(pages_dir)):
    if not page_folder.startswith('page_'):
        continue
        
    page_path = os.path.join(pages_dir, page_folder)
    tokens_file = os.path.join(page_path, 'tokens_list.txt')
    lemmas_file = os.path.join(page_path, 'lemmatized_tokens_list.txt')
    
    try:
        page_num = int(page_folder.split('_')[1])
    except:
        print(f"Пропускаем папку с некорректным именем: {page_folder}")
        continue

    if not os.path.exists(tokens_file):
        print(f"Файл токенов отсутствует: {tokens_file}")
        continue
        
    with open(tokens_file, 'r', encoding='utf-8') as f:
        tokens = set(line.strip() for line in f if line.strip())

    for token in tokens:
        inverted_index[token]["count"] += 1
        inverted_index[token]["inverted_array"].append(page_num)
        inverted_index[token]["word"] = token  

print(f"Обработано {len(inverted_index)} уникальных токенов")

with open(output_file, 'w', encoding='utf-8') as f:
    for token_data in inverted_index.values():
        json.dump(token_data, f, ensure_ascii=False)
        f.write('\n')

print(f"Инвертированный индекс сохранён в {output_file}")