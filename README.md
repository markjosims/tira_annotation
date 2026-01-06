# tira_annotation

## Task description
This project concerns a dataset of linguistic annotations on Tira, a low-resource language from Sudan.
Data come from linguistic documentation 
The goal of this annotation task is to take existing hand-annotations for Tira sentences and normalize them to a consistent standard.
The primary engine for performing normalization is the FST-based morphological transducer stored in the `tira_parser` project and transformer-based transducers in `tira_lm`.
This project houses the predictions output by these transducers and provides an interface for users to choose the best prediction and update sentences with manual predictions when needed.

## Usage
`annotation.html` contains a lightweight offline webpage for parsing Tira sentences.
Sentences are stored in `.yaml` files in the data directory.
Each `.yaml` file contains a list of sentence objects, where each sentence has a field for the original hand-labeled string and the updated string produced by this annotation task.

```yaml
- sentence: àprí jɜ̀dí ðáŋàlà
  updated_sentence: àprí jàdí ðáŋàlà
  translation: boy held sheep
  split: train
  index: '0'
  checked_by_pi: false
  words:
    ...
```

Most of the action centers around the `words` field.

```yaml
    words:
    - original_str: àprí
      updated_str: ''
      updated_gloss: ''
      chosen_parse: '0'
      comment: ''
      parses:
        '0':
          - àpɾí
          - àpɾí
          - boy-nominative-singular
          - 0.05
        '1':
          - ápɾí
          - àpɾí
          - boy-nominative-left_h-singular
          - 0.1
        '2':
          - àpɔ́ŕ
          - àp-ɔ́-ŕ
          - carry-ventive-aɔ-1pl.incl.sbj-imperfective
          - 1.05
        '3':
          - àpɔ́ŕ
          - àp-ɔ́-ŕ
          - carry-ventive-aɔ-1pl.incl.obj-imperfective
          - 1.05
```


## Language resources
- [Interactive Kwaras corpus](https://tira.ucsd.edu/) which supports basic text search and displays various data fields including transcription, segmentation, translation and glossing *where applicable*.
    All data here are hand-produced and have not undergone normalization.
- `/data/lexicon/*.csv` in `tira_parser` project. These files are the sources the FST uses to build its parses, and therefore serve as 'ground truth' for this project. When in doubt on a words gloss or root form, defer to what is stored here.