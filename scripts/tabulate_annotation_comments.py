from argparse import ArgumentParser
import yaml
import pandas as pd
import os

# YAML parses are a list of [updated_str, segmented_str, gloss, FST weight]
updated_str_index = 0
gloss_index = 2

def tabulate_rows(annotations):
    rows = []
    for sentence in annotations:
        row = {
            'sentence': sentence['sentence'],
            'update_sentence': sentence.get('update_sentence', ''),
            'translation': sentence.get('translation', ''),
        }
        for word in sentence['words']:
            comment = word.get('comment', '')
            if not comment:
                continue
            row = row.copy()
            row.update({
                'word': word['original_str'],
                'comment': comment,
            })
            chosen_parse = word.get('chosen_parse', None)
            if chosen_parse:
                parse = word['parses'][chosen_parse]
                updated_str = parse[updated_str_index]
                gloss = parse[gloss_index]
            else:
                gloss = word.get('updated_gloss', '')
                updated_str = word.get('updated_str', '')
            row.update({
                'updated_str': updated_str,
                'gloss': gloss,
            })
            rows.append(row)
    return rows

def load_yaml_and_tabulate(input_file):
    with open(input_file, 'r') as infile:
        annotations = yaml.safe_load(infile)
    return tabulate_rows(annotations)

def main(args):
    rows = []
    for input_file in args.input_file:
        rows.extend(load_yaml_and_tabulate(input_file))
            
    df = pd.DataFrame(rows)
    outpath = args.output_file or os.path.join(
        os.path.dirname(args.input_file[0]),
        'comments.csv'
    )
    df.to_csv(outpath, index=False)
    return 0

if __name__ == "__main__":
    parser = ArgumentParser(description="Tabulate annotation comments from a file.")
    parser.add_argument(
        "--input_file",
        '-i',
        type=str,
        help="Path to the input file containing annotations.",
        nargs='+',
        required=True
    )
    parser.add_argument(
        "--output_file",
        '-o',
        type=str,
        help="Path to the output file for tabulated comments."
    )
    
    args = parser.parse_args()
    main(args)