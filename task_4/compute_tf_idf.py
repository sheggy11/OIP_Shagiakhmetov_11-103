import math
import os
import shutil
from collections import Counter, defaultdict


def load_tokens(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        tokens = f.read().split()
    return tokens


def count_documents_containing(token, all_documents):
    return sum(token in doc for doc in all_documents)


def clear_directory(directory):
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")


def process_files(html_dir, input_tokens_lemmas_dir, out_tokens_path, out_lemmas_path):
    clear_directory(out_tokens_path)
    clear_directory(out_lemmas_path)

    all_token_docs = []
    all_lemma_docs = []
    page_texts = {}

    for i in range(1, 101):
        page_name = f"page_{i}"
        token_file = os.path.join(input_tokens_lemmas_dir, page_name, "tokens_list.txt")
        lemma_file = os.path.join(input_tokens_lemmas_dir, page_name, "lemmatized_tokens_list.txt")

        if os.path.exists(token_file) and os.path.exists(lemma_file):
            tokens = load_tokens(token_file)
            lemmas = load_tokens(lemma_file)
            all_token_docs.append(tokens)
            all_lemma_docs.append(lemmas)
            page_texts[page_name] = {"tokens": tokens, "lemmas": lemmas}
        else:
            print(f"Missing files in {page_name}, skipping.")

    os.makedirs(out_tokens_path, exist_ok=True)
    os.makedirs(out_lemmas_path, exist_ok=True)

    total_docs = len(page_texts)

    for page_name, content in page_texts.items():
        token_counts = Counter(content["tokens"])
        lemma_counts = Counter(content["lemmas"])

        with open(os.path.join(out_tokens_path, f"{page_name}.txt"), "w", encoding="utf-8") as token_out:
            for token in set(content["tokens"]):
                tf = token_counts[token] / len(content["tokens"])
                idf = math.log(total_docs / (1 + count_documents_containing(token, all_token_docs)))
                tf_idf = tf * idf
                token_out.write(f"{token} {idf:.6f} {tf_idf:.6f}\n")

        with open(os.path.join(out_lemmas_path, f"{page_name}.txt"), "w", encoding="utf-8") as lemma_out:
            for lemma in set(content["lemmas"]):
                tf = lemma_counts[lemma] / len(content["lemmas"])
                idf = math.log(total_docs / (1 + count_documents_containing(lemma, all_lemma_docs)))
                tf_idf = tf * idf
                lemma_out.write(f"{lemma} {idf:.6f} {tf_idf:.6f}\n")


if __name__ == "__main__":
    process_files(
        html_dir="task1/archive",
        input_tokens_lemmas_dir="task_2/pages_tokens_lemmas",
        out_tokens_path="task_4/tokens_list_tf_idf",
        out_lemmas_path="task_4/lemmas_list_tf_idf"
    )
