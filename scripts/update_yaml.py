import yaml
from tqdm import tqdm
import re
from glob import glob

yaml_path = 'data/sentences.yaml'

train_path_rgx = r'data/train/([A-Za-z]+)/sentences_(\d+)-(\d+).yaml'
test_val_path_rgx = r'data/(validation|test)/sentences_(\d+)-(\d+).yaml'

splits = ['train', 'validation', 'test']
annotators = ['Hudson', 'James', 'Gordon']
chunk_size = 100

def main():
    print(f"Loading YAML from {yaml_path}")
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
    for split in splits:
        print(f"Processing split: {split}")
        split_yaml = [
            sentence for sentence in data if sentence['split'] == split
        ]
        if split == 'train':
            path_pattern = 'data/train/*/sentences_*.yaml'
            path_rgx = train_path_rgx
        else:
            path_pattern = f'data/{split}/sentences_*.yaml'
            path_rgx = test_val_path_rgx
        existing_files = glob(path_pattern)

        for filepath in tqdm(existing_files):
            match = re.match(path_rgx, filepath)
            assert match, filepath
            start_idx = int(match.group(2))
            end_idx = int(match.group(3))
            segment = [
                sentence for sentence in split_yaml
                if start_idx <= int(sentence['index']) <= end_idx
            ]
            with open(filepath, 'w') as out_f:
                yaml.dump(segment, out_f, sort_keys=False, allow_unicode=True)
            print(f"Updated {filepath} with {len(segment)} sentences.")
        
    


if __name__ == "__main__":
    main()