from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
import pymorphy2
import os
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

stop_words = set(stopwords.words('russian'))
morph = pymorphy2.MorphAnalyzer()

def parse_web_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    soup = BeautifulSoup(content, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)
    return text

def extract_tokens(text):
    tokens = nltk.word_tokenize(text, language="russian")
    tokens = [token.lower() for token in tokens if token.isalpha() and token.lower() not in stop_words]
    return tokens

def lemmatize_words(tokens):
    lemmas = {}
    for token in tokens:
        p = morph.parse(token)[0]
        lemma = p.normal_form
        if lemma not in lemmas:
            lemmas[lemma] = set()
        lemmas[lemma].add(token)
    return lemmas

def process_web_documents(directory_path):
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.html'):
            file_path = os.path.join(directory_path, file_name)
            text = parse_web_content(file_path)
            tokens = extract_tokens(text)
            lemmas = lemmatize_words(tokens)

            page_name = os.path.splitext(file_name)[0]
            page_dir = os.path.join(directory_path, page_name)
            os.makedirs(page_dir, exist_ok=True)

            # Сохраняем токены
            with open(os.path.join(page_dir, "tokens_list.txt"), "w", encoding="utf-8") as tokens_file:
                for token in tokens:
                    tokens_file.write(f"{token}\n")

            # Сохраняем леммы
            with open(os.path.join(page_dir, "lemmatized_tokens_list.txt"), "w", encoding="utf-8") as lemmas_file:
                for lemma, tokens_set in lemmas.items():
                    lemmas_file.write(f"{lemma} {' '.join(tokens_set)}\n")

web_documents_directory = 'downloaded_texts'
if os.path.exists(web_documents_directory) and os.path.isdir(web_documents_directory):
    process_web_documents(web_documents_directory)
else:
    print("Папка 'downloaded_texts' не существует или не является директорией.")
