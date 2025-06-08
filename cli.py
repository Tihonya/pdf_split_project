import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description="PDF Book Splitter: розбиває PDF за рівнем закладок"
    )
    parser.add_argument("input_pdf", help="шлях до вхідного PDF-файла")
    parser.add_argument("-o", "--output-dir", default="output", help="папка для збереження частин")
    parser.add_argument("-c", "--config", help="шлях до YAML-конфігурації (необов’язково)")
    parser.add_argument("-l", "--level", type=int, help="рівень закладок для розбиття (перевизначає конфіг)")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    print(vars(args))