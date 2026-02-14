from RSTProcesser import RSTProcessor
from nltk import word_tokenize
from tqdm import tqdm
import fire
import os
import json

from pathlib import Path

def ensure_path_exits(path):
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)

def merge_node(node, leaf_len):
    if not node['is_leaf']:
    #     return node['node_text'], len(word_tokenize(node['node_text']))
    # else:
        l, ll = merge_node(node['left_child'], leaf_len)
        r, rl = merge_node(node['right_child'], leaf_len)
        if l is None or r is None:
            return None, None

        if ll + rl <= leaf_len:
            node['node_text'] = f"{l} {r}"
            node['left_child'] = None
            node['right_child'] = None
            node['is_leaf'] = True
        else:
            return None, None
    
    return node['node_text'], len(word_tokenize(node['node_text']))

def merge_leaf(path, save_path, leaf_len):
    files = os.listdir(path)
    ensure_path_exits(save_path)
    for file in tqdm(files):
        with open(os.path.join(path, file), 'r', encoding='utf-8') as f:
            data = json.load(f)
        tree = data['full_tree']
        merge_node(tree, leaf_len)
        data['full_tree'] = tree

        with open(os.path.join(save_path, file), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


def leaf_num(node):
    if node['is_leaf']:
        node['leaf_num'] = 1
    else:
        node['leaf_num'] = leaf_num(node['left_child']) + leaf_num(node['right_child'])
    
    return node['leaf_num']

def get_text(node):
    if node['is_leaf']:
        return node['node_text']
    else:
        return f"{get_text(node['left_child'])} {get_text(node['right_child'])}"

def merge_by_leaf_num(node):
    if node['is_leaf']:
        pass
    elif node['leaf_num'] <= 3:
        node['node_text'] = get_text(node)
        node['is_leaf'] = True
        node['left_child'] = None
        node['right_child'] = None
    else:
        node['left_child'] = merge_by_leaf_num(node['left_child'])
        node['right_child'] = merge_by_leaf_num(node['right_child'])
    
    return node

def merge_leaf_num(path, save_path):
    files = os.listdir(path)
    for file in tqdm(files):
        with open(os.path.join(path, file), 'r', encoding='utf-8') as f:
            data = json.load(f)
        tree = data['full_tree']
        leaf_num(tree)
        merge_by_leaf_num(tree)
        data['full_tree'] = tree

        with open(os.path.join(save_path, file), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)



if __name__ == "__main__":
    fire.Fire(merge_leaf)