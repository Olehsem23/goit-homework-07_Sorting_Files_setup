from pathlib import Path
import shutil
import re
import sys

CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "yo", "zh", "z", "y", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "c", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "ye", 'i', "yi", "g")
print(len(CYRILLIC_SYMBOLS))
print(len(TRANSLATION))

TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

KN_EXT = set()
UN_EXT = set()

EXTENSIONS = {
    'images': ['JPEG', 'PNG', 'JPG', 'SVG'],
    'video': ['AVI', 'MP4', 'MOV', 'MKV'],
    'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLS', 'XLSX', 'PPTX'],
    'audio': ['MP3', 'OGG', 'WAV', 'AMR'],
    'archives': ['ZIP', 'GZ', 'TAR'],
    'unknown_extensions': []
}

ALL_FILES = {
    'images': [],
    'video': [],
    'documents': [],
    'audio': [],
    'archives': [],
    'unknown_extensions': []
}


def scan_folder(path_to_folder: Path) -> None:  # Функція сканує папку на наявність файлів і вкладених папок
    for element in path_to_folder.iterdir():
        if element.is_dir() and element in EXTENSIONS.keys():
            continue
        elif element.is_dir():
            if any(element.iterdir()):
                scan_folder(element)  # Рекурсивно проходимо по всіх вкладених папках
            else:
                element.rmdir()  # Видаляємо порожні папки
        else:
            sort_file(element)
            handle_file(element)
            if not any(element.parent.iterdir()): element.parent.rmdir()  # Роздаємо задачі іншим функціям


def unpack_archive(path_to_archive: Path, folder: str) -> None:  # Розпакування архівів
    new_folder = Path(path_to_folder) / folder
    if not new_folder.exists():
        new_folder.mkdir(exist_ok=True, parents=True)
    ALL_FILES[folder].append(normalize_name(path_to_archive))
    shutil.unpack_archive(path_to_archive, new_folder / normalize_name(path_to_archive).split('.')[0])
    Path.unlink(path_to_archive)  # Видалення архіву після розпакування


def normalize_name(path_to_file: Path) -> str:  # Транслітерація назв файлів
    name = path_to_file.name.split('.')
    name[0] = re.sub(r'\W', '_', name[0].translate(TRANS))
    new_name = '.'.join(name)
    return new_name


def handle_file(path_to_file: Path) -> None:  # Створення списків по групам файлів
    ext = path_to_file.suffix[1:].upper()
    for key, value in EXTENSIONS.items():
        if ext in value:
            ALL_FILES[key].append(normalize_name(path_to_file))
            return
    ALL_FILES['unknown_extensions'].append(normalize_name(path_to_file))


def sort_file(path_to_file: Path) -> list:  # Сортування файлів за розширенням та тип
    ext = path_to_file.suffix[1:].upper()
    for key, value in EXTENSIONS.items():
        if ext in value:
            KN_EXT.add(ext)
            if key == 'archives':
                unpack_archive(path_to_file, key)
                return
            else:
                move_file(path_to_file, key)
                return
    UN_EXT.add(ext)
    move_file(path_to_file, 'unknown_extensions')


def move_file(path_to_file: Path, folder: str) -> None:  # Переносимо файли у папки відповідного вмісту
    new_folder = Path(path_to_folder) / folder
    if not new_folder.exists():
        new_folder.mkdir(exist_ok=True, parents=True)
    try:
        shutil.copyfile(path_to_file, new_folder / Path(normalize_name(path_to_file)))
        Path.unlink(path_to_file)
    except:
        print(f'Can`t move this file: {normalize_name(path_to_file)}!')


if __name__ == '__main__':
    path_to_folder = sys.argv[1]
    
    scan_folder(Path(path_to_folder))

    print(f"Images: {' ** '.join(ALL_FILES['images'])}\n")
    print(f"Video: {' ** '.join(ALL_FILES['video'])}\n")
    print(f"Documents: {' ** '.join(ALL_FILES['documents'])}\n")
    print(f"Audio: {' ** '.join(ALL_FILES['audio'])}\n")
    print(f"Archives: {' ** '.join(ALL_FILES['archives'])}\n")
    print(f"Unknown_extensions: {' ** '.join(ALL_FILES['unknown_extensions'])}\n")
    print('*' * 60)
    print(f'\nUNKNOWN EXTENSIONS: {UN_EXT}\n')
    print(f'KNOWN EXTENSIONS: {KN_EXT}')
