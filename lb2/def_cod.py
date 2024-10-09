from heapq import heappop, heappush
# Импортируем функции heappop и heappush из модуля heapq для работы с кучей (heap).

# Шеннон-Фано кодирование
def shannon_fano_encode(symbols, prefix=""):
    # Определяем функцию для кодирования символов с помощью алгоритма Шеннона-Фано.
    
    if len(symbols) == 1:
        # Если остался только один символ,
        symbol, _ = symbols[0]  # Извлекаем символ и его частоту (не используется).
        return {symbol: prefix}  # Возвращаем символ с присвоенным ему префиксом.

    # Считаем общую частоту всех символов.
    total_weight = sum([weight for _, weight in symbols])
    cumulative_weight = 0  # Инициализируем переменную для накопления частоты.

    for i in range(len(symbols)):
        # Проходим по каждому символу и его частоте.
        cumulative_weight += symbols[i][1]  # Увеличиваем накопленную частоту.
        if cumulative_weight >= total_weight / 2:
            # Если накопленная частота превышает половину общей частоты,
            left_part = symbols[:i + 1]  # Разделяем символы на левую часть.
            right_part = symbols[i + 1:]  # И на правую часть.
            break  # Выходим из цикла.

    # Рекурсивно вызываем функцию для кодирования левой и правой частей с добавлением префиксов.
    left_codes = shannon_fano_encode(left_part, prefix + "0")
    right_codes = shannon_fano_encode(right_part, prefix + "1")

    # Объединяем коды левой и правой частей и возвращаем их.
    return {**left_codes, **right_codes}

def shannon_fano(symbol_freq):
    # Функция для подготовки данных и вызова функции шифрования Шеннона-Фано.
    sorted_symbols = sorted(symbol_freq.items(), key=lambda item: item[1], reverse=True)
    # Сортируем символы по их частоте в порядке убывания.
    return shannon_fano_encode(sorted_symbols)  # Возвращаем кодировку символов.

# Хаффман кодирование
class HuffmanNode:
    def __init__(self, symbol, freq):
        # Конструктор для узла Хаффмана.
        self.symbol = symbol  # Символ, связанный с узлом.
        self.freq = freq  # Частота символа.
        self.left = None  # Левый дочерний узел.
        self.right = None  # Правый дочерний узел.

    def __lt__(self, other):
        # Определяем порядок узлов по их частоте (для работы с кучей).
        return self.freq < other.freq

def huffman_tree(symbol_freq):
    # Функция для построения дерева Хаффмана.
    heap = [HuffmanNode(symbol, freq) for symbol, freq in symbol_freq.items()]
    # Создаем кучу из узлов Хаффмана для каждого символа и его частоты.
    heappush(heap, heap[0])  # Вставка для корректной работы (можно убрать, если куча не пуста).

    while len(heap) > 1:
        # Пока в куче больше одного узла,
        left = heappop(heap)  # Извлекаем узел с наименьшей частотой.
        right = heappop(heap)  # Извлекаем следующий узел с наименьшей частотой.
        # Создаем новый узел, который объединяет два извлеченных узла.
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left  # Устанавливаем левым дочерним узлом извлеченный узел left.
        merged.right = right  # Устанавливаем правым дочерним узлом извлеченный узел right.
        heappush(heap, merged)  # Вставляем объединенный узел обратно в кучу.

    return heap[0]  # Возвращаем корень дерева Хаффмана.

def huffman_codes(tree, prefix="", codebook=None):
    # Функция для получения кодов Хаффмана из дерева.
    if codebook is None:
        codebook = {}  # Инициализируем кодовую книгу, если она не была передана.

    if tree.symbol is not None:
        # Если узел является листом (содержит символ),
        codebook[tree.symbol] = prefix  # Сохраняем символ и его код в кодовой книге.
    else:
        # Если узел не является листом, рекурсивно обрабатываем левых и правых дочерних узлов.
        huffman_codes(tree.left, prefix + "0", codebook)  # Добавляем "0" к префиксу для левой ветви.
        huffman_codes(tree.right, prefix + "1", codebook)  # Добавляем "1" к префиксу для правой ветви.

    return codebook  # Возвращаем кодовую книгу.

# Шифрование текста
def encode_text(text, codes):
    # Функция для шифрования текста с использованием переданных кодов.
    return ''.join([codes[char] for char in text])  # Соединяем коды символов в одну строку.

# Расшифрование текста по дереву Хаффмана
def decode_huffman(encoded_text, tree):
    # Функция для расшифровки закодированного текста с использованием дерева Хаффмана.
    decoded_text = []  # Инициализируем список для хранения расшифрованного текста.
    node = tree  # Устанавливаем текущий узел на корень дерева.
    
    for bit in encoded_text:
        # Проходим по каждому биту закодированного текста.
        node = node.left if bit == '0' else node.right  # Переходим к левому или правому узлу в зависимости от бита.
        if node.symbol:
            # Если достигли листа (узел содержит символ),
            decoded_text.append(node.symbol)  # Добавляем символ в расшифрованный текст.
            node = tree  # Сбрасываем текущий узел на корень дерева.
    
    return ''.join(decoded_text)  # Возвращаем расшифрованный текст.

# Расшифровка Шеннона-Фано
def decode_shannon_fano(encoded_text, codes):
    # Функция для расшифровки закодированного текста, закодированного с помощью Шеннона-Фано.
    reversed_codes = {v: k for k, v in codes.items()}  # Создаем обратный словарь для поиска символов по коду.
    temp = ""  # Инициализируем временную строку для накопления битов.
    decoded_text = []  # Инициализируем список для хранения расшифрованного текста.

    for bit in encoded_text:
        # Проходим по каждому биту закодированного текста.
        temp += bit  # Добавляем бит к временной строке.
        if temp in reversed_codes:
            # Если временная строка соответствует коду в обратном словаре,
            decoded_text.append(reversed_codes[temp])  # Добавляем соответствующий символ в расшифрованный текст.
            temp = ""  # Сбрасываем временную строку.

    return ''.join(decoded_text)  # Возвращаем расшифрованный текст.
