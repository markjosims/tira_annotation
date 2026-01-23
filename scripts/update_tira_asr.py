"""
Script to update Tira ASR dataset with transcriptions and glosses
predicted by FST model. Takes as input a YAML file with the predicted
parses, greedily takes the most likely parse for each word, and updates
the transcription and gloss for each sentence accordingly.
"""

from argparse import ArgumentParser
from typing import Dict, Tuple, Any
from tqdm import tqdm
from datasets import load_from_disk
import yaml
import os

DATASETS_DIR = os.environ.get(
    'DATASETS', os.path.expanduser('~/datasets')
)
TIRA_ASR_DIR = os.path.join(DATASETS_DIR, 'tira_asr')

def get_transcription_and_gloss(sentence_obj: Dict[str, Any]) -> Tuple[str, str]:
    words = []
    glosses = []
    for word in sentence_obj['words']:
        chosen_parse = word.get('chosen_parse', 0)
        parse = word['parses'][chosen_parse]
        updated_str = parse[0]  # updated_str is at index 0
        gloss = parse[2]        # gloss is at index 2
        words.append(updated_str)
        glosses.append(gloss)
    transcription = ' '.join(words)
    gloss = ' '.join(glosses)
    return transcription, gloss

def main():
    args = get_args()
    with open(args.yaml, 'r') as f:
        data = yaml.safe_load(f)

    sentence2updated = {}
    for sentence_obj in tqdm(data, desc='Getting updated sentences...'):
        transcription, gloss = get_transcription_and_gloss(sentence_obj)
        sentence = sentence_obj['sentence']
        sentence2updated[sentence] = (transcription, gloss)
    
    update_sentence = lambda example: {
        'rewritten_transcript': sentence2updated[example['sentence']][0],
        'gloss': sentence2updated[example['sentence']][1],
    }

    ds = load_from_disk(args.dataset_dir)
    ds = ds.map(update_sentence, desc='Updating dataset...')
    ds.save_to_disk(args.dataset_dir+'_updated')

def get_args():
    parser = ArgumentParser(
        description="Update Tira ASR dataset with FST predicted transcriptions and glosses."
    )
    parser.add_argument(
        '--yaml', '-y', type=str, required=True,
        help="Path to the YAML file with predicted parses."
    )
    parser.add_argument(
        '--dataset-dir', '-d', type=str, default=TIRA_ASR_DIR,
        help="Path to the Tira ASR dataset directory. "\
        + f"Default: {TIRA_ASR_DIR}"
    )
    return parser.parse_args()

if __name__ == '__main__':
    main()