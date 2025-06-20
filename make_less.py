import os

def create_mini_version(input_file, output_file, max_size_mb=5):
    """
    Создает уменьшенную версию большого файла
    
    :param input_file: путь к исходному файлу
    :param output_file: путь для сохранения уменьшенного файла
    :param max_size_mb: максимальный размер нового файла в МБ (по умолчанию 5MB)
    """
    max_size = max_size_mb * 1024 * 1024  # Конвертируем в байты
    
    # Проверяем размер исходного файла
    input_size = os.path.getsize(input_file)
    if input_size <= max_size:
        print(f"Исходный файл уже меньше {max_size_mb}MB, копирование не требуется")
        return
    
    print(f"Создание уменьшенной версии {input_file} ({input_size/1024/1024:.2f} MB)")
    print(f"Новый размер: не более {max_size_mb} MB")
    
    # Читаем только часть исходного файла
    with open(input_file, 'r', encoding='utf-8') as f_in:
        with open(output_file, 'w', encoding='utf-8') as f_out:
            # Читаем первые N символов (примерно 5MB текста)
            chunk = f_in.read(max_size)
            f_out.write(chunk)
    
    output_size = os.path.getsize(output_file)
    print(f"Файл {output_file} успешно создан ({output_size/1024/1024:.2f} MB)")

if __name__ == "__main__":
    input_file = "collect.txt"  # Ваш исходный большой файл
    output_file = "collect_mini.txt"  # Уменьшенная версия
    
    # Создаем уменьшенную версию (5MB)
    create_mini_version(input_file, output_file, max_size_mb=1)