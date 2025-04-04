# Задание 1:

### Методы:

```
download_page(url):
```
Этот метод загружает содержимое веб-страницы по указанному URL. Если запрос выполнен успешно (статус код 200), возвращает содержимое страницы в виде байтов. В случае ошибки при загрузке или запросе, выводит сообщение об ошибке и возвращает None.

```
save_html(content, filename):
```
Этот метод сохраняет содержимое веб-страницы в файл. Принимает содержимое страницы в виде байтов и имя файла для сохранения. Записывает содержимое в указанный файл в формате байтов.

```
crawler(url, output_dir, max_pages=100):
```
Основной метод, который выполняет сканирование (краулинг) страниц. Создает директорию для сохранения загруженных страниц, если она не существует. Ведет журнал в файле index.txt, содержащем информацию о загруженных страницах. Обходит страницы, начиная с указанного URL, и загружает их содержимое. Извлекает ссылки из загруженных страниц для дальнейшего обхода. Останавливается после загрузки указанного количества страниц или если больше нет новых страниц для обхода.

### Порядок действий:
Указали начальный URL start_url для начала сканирования. Указали директорию output_directory для сохранения загруженных текстовых страниц. Вызвали функцию crawler() с указанными параметрами, чтобы начать сканирование и загрузку страниц. Код обходит страницы, загружает их содержимое, сохраняет в файлы и создает индексный файл index.txt.

### Deployment Manual:
Установка зависимостей:

```
pip install requests
pip install beautifulsoup4
```

### Запуск скрипта:
```
python main.py
```
 
