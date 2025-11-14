# import yaml
# with open('conf.yaml', 'r', encoding='utf-8') as f:
#     content = yaml.load(f, Loader=yaml.FullLoader)
# print (content)


import argparse
import sys
import yaml
from easydict import EasyDict as edict
from pathlib import Path
def parse_args():
    """
    解析命令行参数和配置文件，返回包含所有参数的命名空间对象。
    """
    parser = argparse.ArgumentParser(description="Generate Synthetic Text Data")
    parser.add_argument('--cfg',
                        help='Path of config file',
                        required=False,
                        type=str,
                        default='configs/config.yaml')
    args = parser.parse_args()

    # 加载配置文件
    try:
        with open(args.cfg, 'r', encoding='utf-8') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        config = edict(config)
    except Exception as e:
        sys.exit(f"[Error] Failed to load YAML config: {e}")

    # 将配置文件中的参数更新到args对象
    # 假定配置文件的结构类似:
    #   SECTION:
    #     key: value
    for section in config:
        for key in config[section]:
            setattr(args, f"{key.lower()}", config[section][key])
    return args

def load_corpus(corpus_file_path):
    """
    加载语料库文件，返回行列表。
    """
    p = Path(corpus_file_path)
    if not p.exists():
        sys.exit(f"[Error] Corpus file not found: {corpus_file_path}")
        # 使用 with 语句打开文件 p，以只读模式 'r' 打开，并指定编码为 "utf-8-sig"，这意味着文件可以包含 BOM（字节顺序标记）。
        # 同时，设置 errors='ignore' 参数来忽略任何解码错误。
    with open(p, 'r', encoding="utf-8-sig", errors='ignore') as file:
        # line.strip()：去除行首和行尾的空白字符（包括换行符 \n）
        words_list = [line.strip() for line in file if line.strip()]
    return words_list

def main():
    # 1. 解析参数
    args = parse_args()

    # 2. 加载语料库
    corpus_list = load_corpus(args.corpus)
    num_texts = len(corpus_list)
    print(f"Loaded corpus with {num_texts} lines")