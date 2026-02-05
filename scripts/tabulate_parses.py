from argparse import ArgumentParser
import yaml
import pandas as pd
import os
from tqdm import tqdm

"""
Script to tabulate parse results from YAML files into a CSV format
where each row is a single parse for a word in a sentence.
The input YAML files contain a nested structure of sentences, words,
and their parses, so the resulting CSV has a length of
num(sentence) * num(word in sentence) * num(parse for word).
"""

PARSES_OUTPATH = os.path.expanduser("~/projects/tira_parser/data/sentences/parses.csv")
SENTENCE_YAML_PATH = "data/sentences.yaml"


def main():
    args = get_args()
    all_data = []
    for input_file in args.input_files:
        with open(input_file, 'r') as f:
            data = yaml.safe_load(f)
            all_data.extend(data)
    # data is nested list of dictionaries
    # sentence > words > parses
    rows = []
    for sentence in tqdm(all_data):
        word_data = sentence.pop('words')
        for word in word_data:
            parses = word.pop('parses')
            for parse in parses:
                row = {
                    **sentence,
                    **word,
                    **parse
                }
                rows.append(row)
    df = pd.DataFrame(rows)
    df.to_csv(args.output_file, index=False)

def get_args():
    parser = ArgumentParser(
        description="Tabulate parse results from YAML files."
    )
    parser.add_argument(
        "input_files",
        nargs="+",
        default=[SENTENCE_YAML_PATH],
        help="YAML files containing parse results."
    )
    parser.add_argument(
        "--output_file",
        default=PARSES_OUTPATH,
        help="File to write the tabulated results."
    )
    return parser.parse_args()

if __name__ == "__main__":
    main()