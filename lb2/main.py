from collections import Counter
from def_cod import shannon_fano, encode_text, decode_shannon_fano, huffman_tree, huffman_codes, decode_huffman

# Основная программа
if __name__ == "__main__":
    text = str(input("Введите текст для кодирования: "))

    # Подсчёт частоты символов
    symbol_freq = Counter(text)
    
    # Шеннон-Фано кодирование
    shannon_fano_codes = shannon_fano(symbol_freq)
    print("Шеннон-Фано коды:", shannon_fano_codes)
    encoded_shannon_fano = encode_text(text, shannon_fano_codes)
    print("Закодированный текст (Шеннон-Фано):", encoded_shannon_fano)
    decoded_shannon_fano = decode_shannon_fano(encoded_shannon_fano, shannon_fano_codes)
    print("Раскодированный текст (Шеннон-Фано):", decoded_shannon_fano)
    
    # Хаффман кодирование
    huffman_tree_root = huffman_tree(symbol_freq)
    huffman_codes = huffman_codes(huffman_tree_root)
    print("Хаффман коды:", huffman_codes)
    encoded_huffman = encode_text(text, huffman_codes)
    print("Закодированный текст (Хаффман):", encoded_huffman)
    decoded_huffman = decode_huffman(encoded_huffman, huffman_tree_root)
    print("Раскодированный текст (Хаффман):", decoded_huffman)
