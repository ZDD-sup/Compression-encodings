import chardet
import os

ENCODINGS = {
    "1": "cp866",
    "2": "cp1251",
    "3": "koi8-r",
    "4": "iso-8859-5"
}

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        if encoding is None:
            raise ValueError("Не удалось определить кодировку файла.")
        return encoding

def convert_file_encoding(input_file, output_file, target_encoding):
    source_encoding = detect_encoding(input_file)
    print(f"Исходная кодировка: {source_encoding}")

    with open(input_file, 'r', encoding=source_encoding) as file:
        file_content = file.read()

    with open(output_file, 'w', encoding=target_encoding) as file:
        file.write(file_content)

    print(f"Файл успешно преобразован в кодировку {target_encoding} и сохранён как {output_file}")

input_file = str(input("Напишите название исходного файла (например, input.txt): "))

if not os.path.exists(input_file):
    print(f"Файл {input_file} не найден. Убедитесь, что он существует в текущей директории.")
else:
    print("Все доступные кодировки:")
    print("1) CP866")
    print("2) CP1251")
    print("3) СЗ10007")
    print("4) ISO-8859-5")

    encoding_choice = input("Укажите номер кодировки: ")

    if encoding_choice in ENCODINGS:
        target_encoding = ENCODINGS[encoding_choice]
        output_file = "output_" + input_file

        try:
            convert_file_encoding(input_file, output_file, target_encoding)
        except ValueError as e:
            print(f"Ошибка: {e}")
    else:
        print("Некорректный выбор кодировки.")