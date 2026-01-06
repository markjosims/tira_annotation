import yaml
import os
from tqdm import tqdm
from random import choice

yaml_path = 'data/sentences.yaml'
outpath_template = 'data/{split}/{annotator}/sentences_{indices}.yaml'
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
        i = 0
        with tqdm(total=len(split_yaml), desc=f"Writing {split} chunks") as pbar:
            while i < len(split_yaml):
                chunk = split_yaml[i:i+chunk_size]
                # add 1 to indices to make them 1-based
                indices = f"{i+1}-{i+len(chunk)}"
                if split == 'train':
                    annotator = choice(annotators)
                else:
                    annotator = ''
                outpath = outpath_template.format(
                    split=split,
                    annotator=annotator,
                    indices=indices
                )
                outpath = outpath.replace('//', '/')
                os.makedirs(os.path.dirname(outpath), exist_ok=True)
                with open(outpath, 'w') as out_f:
                    yaml.dump(chunk, out_f, sort_keys=False, allow_unicode=True)
                i += chunk_size
                pbar.update(len(chunk))
    


if __name__ == "__main__":
    main()