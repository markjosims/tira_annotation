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
          - boy-NOM-SG
          - 0.05
        '1':
          - ápɾí
          - àpɾí
          - boy-NOM-SG-left_h
          - 0.1
        '2':
          - àpɔ́ŕ
          - àp-ɔ́-ŕ
          - carry-VENT-IPFV-1PL.INCL.SBJ
          - 1.05
        '3':
          - àpɔ́ŕ
          - àp-ɔ́-ŕ
          - carry-VENT-IPFV-1PL.INCL.OBJ
          - 1.05
```

Here we can see several candidate hypotheses from the FST parser where each candidate is given as a list [candidate_string, segmented_string, gloss, weight].
'Weight' here is the weight on the path on the FST that generated the candidate parse, corresponding to the number of edits between the candidate (normalized) string and the query (unnormalized) string
A weight of 0 indicates that the candidate is identical to the query, a weight of 1 indicates a single insertion/substitution/deletion, etc.
Several edits are given a weight of less than 1 to reflect particularly frequent spelling deviations, e.g. substitutions of 'o' with 'u' or 'u' with 'ʊ' have a much smaller weight of 0.05.

For each word, select a candidate parse from the list or, if no candidate parse seems adequate, you can use the 'manual override' section to leave a comment and, if you so wish, input a normalized version + gloss of your own.
Even if you don't leave a normalized string or gloss, at the very least leave a comment describing what the error is, which may be as simple as 'the word "yam" is missing from the corpus' or may be more complicated like 'the verb is marked with first person singular subject but none of the parses mention first person singular'.
A sentence is fully annotated when parses have been selected for every word.

## Controls
When using the web interface, click on the 'Load YAML' file in the top right to load a datafile to be annotated.
This will populate the left sidebar with all of the sentences in the `.yaml` file.
The left and right arrow keys will cycle through the words of the currently selected sentence, and the up and down arrows will cycle through parser candidates for the current word.
Shift+left/right change the current sentence.

When in **manual override** mode, you need to hit 'Enter' or click 'Save word info' to persist the normalized string, gloss or comment for the given word.
When selecting parses, it is sufficient to **click** or **highlight** the parse with the arrow keys and the index will be saved.
To save, press **ctrl/cmnd+s**, equivalent to clicking on the 'Download YAML' button, which will open a screen for saving the updated YAML with your annotations to disk.

## Language resources
- [Interactive Kwaras corpus](https://tira.ucsd.edu/) which supports basic text search and displays various data fields including transcription, segmentation, translation and glossing *where applicable*.
    All data here are hand-produced and have not undergone normalization.
- `/data/lexicon/*.csv` in `tira_parser` project. These files are the sources the FST uses to build its parses, and therefore serve as 'ground truth' for this project. When in doubt on a words gloss or root form, defer to what is stored here.

## Abbreviations and glossary

### Noun features
#### Case
- Nominative (NOM): subject of the verb, also the default case in Tira. ŋɛ́n ŋ-ícə̀lò dog-NOM-SG good-CLŋ-left_h 'the dog is good'
- Accusative (ACC): object of the verb. íŋgá nɔ́nà ŋɛ́nɛ́ nd̪ɔ̀bà AUX-IPFV-1SG.SBJ see-IPFV-IT dog-ACC tomorrow 'I will see the dog tomorrow'

#### Number
- Singular (SG): marked by noun class prefix, different for each word. ŋɛ́n dog-NOM-SG
- Plural (PL): marked by noun class prefix, different for each word. ɲɛ́n dog-NOM-PL

### Person
Note: only inalienably possessed nouns are marked for person in Tira.
Inaleinably possessed nouns include \TODO

### Verb features
#### Tense/aspect/mood
- Imperfective (IPFV): an incomplete action. Often translated with a future tense in English, e.g. íŋgá nɔ́nà 'I will see': gloss see-AUX-IT-IPFV-1SG.SBJ
- Perfective (PFV): a completed action. Often translated with a past tense in English, e.g. làŋú 'they saw': gloss see-CLl-VENT-PFV
- Imperative (IMP): command form, àpá carry-VENT-IMP 'bring (it) here!'
- Dependent (DEP): subordinate form, typically used in context 'tell X to do Y' e.g. àɾt̪ɔ́l lə̀rdì t̪ɔ́wə̀nì say-IMP-IT-3PL.OBJ dance-DEP-3PL.SUBJ now 'tell them to dance now!'

#### Deixis (aka associated motion)
- Itive (IT): motion away from the speaker or, for static verbs, location nearby speaker. və́lɛ́ðɔ́ pull-IT-IMP 'pull it (away from me)!' t̪ɔ́ ŋávɛ̀ drink-IT-IMP water-ACC-SG-final_lowering 'drink water (near me)!'
- Ventive (VENT): motion towards the speaker or, for static verbs, location far away from speaker. və́lɛ́ðɔ́ pull-IT-IMP 'pull it (away from me)!' t̪ɔ̌ ŋávɛ̀ drink-VENT-IMP water-ACC-SG-final_lowering 'drink water (far from me)!'

#### Person marking
Following person values present in Tira:
- First person singular (1SG)
- Second person singular (2SG)
- Third person singular (3SG)
- First person dual inclusive (1DU.INCL), 'me and you'
- First person plural inclusive (1PL.INCL), 'me/us + you/you all'
- First person plural exclusive (1PL.EXCL), 'us-not-you'
- Second person plural (2PL)
- Third person plural (3PL)

Both subjects and objects can be marked on a verb, e.g. 1SG.SBJ or 1SG.OBJ.

#### Class
Abbreviated CL{prefix}. Indicates the noun class the verb shows agreement for, represented with a consonantal prefix.
E.g.
- ùɟí kə̀-və̀lɛ̀ð-ɔ́ person-NOM-SG pull-**CLg**-VENT-PFV 'person pulled'
- lìɟí lə̀-və̀lɛ̀ð-ɔ́ people-NOM-PL pull-**CLl**-VENT-PFV 'people pulled'  

Note, class 'g' has a prefix with [k] because [k] and [g] are the same thing in Tira.

### Adjective features
#### Class
Only adjective feature in Tira.
Same as verbs.

- ùɟí kícə̀lò person-NOM-SG good-CLg 'person is good'
- lìɟí lícə̀lò person-NOM-PL good-CLl 'person is good'

### Left-H
'Left-H' is an umbrella term for various processes in Tira that all have one effect: the leftmost syllable of a word gains a high (H) tone.
There are multiple instances where this can occur.
For instance, in some cases a word ending with a high tone will 'spread' it's high tone onto the first syllable of the previous word, a process called (appropriately enough) 'High-tone spreading.'
Note that the word *ðàŋàl-à* 'sheep (accusative)' normally has a low tone on the first syllable (1), but following the verb *kə̀-və̀lɛ̀ð-ɔ́*, which ends in a high tone, the first syllable of 'sheep' also takes a high tone (2).

(1) ùrnɔ̀            k-á     və́lɛ̀ð-à       ðàŋàl-à  
    CLg.grandfather CLg-Aux pull-IT.PFV   CLð.sheep-ACC  
'Grandfather pulled the sheep' (away from speaker)  

(2) ùrnɔ̀            kə̀-və̀lɛ̀ð-ɔ́          ðáŋàl-à  
    CLg.grandfather CLg-pull-VENT.PFV   CLð.sheep.LEFT_H-ACC  
'Grandfather pulled the sheep' (towards speaker)  

Another case is focus constructions with the particle *àn*.
Focus constructions single out one part of the sentence, e.g. the subject of the verb 'It is Kuku that ate soup (and not someone else who ate it)', object 'It is soup that Kuku ate (and not e.g. bread).'
As these sentences show, an 'It'-cleft ('It is X that...') can introduce focus constructions in English.
In Tira the dedicated focus particle *àn* does this job.
Like high tone spreading above, the focus particle *àn* causes a high tone to occur on the first syllable of the following word.
Notice in (3) that the word lion typically has a low tone in the first syllable, but following *àn* it has a high tone (4).

(3) t̪òlé  
    CLt̪-lion  
'The lion'  

(4) àn  t̪ólé  
    FOC CLt̪-lion-LEFT_H  
'It is the lion'  

Focus constructions are associated with another form of Left-H.
Specifically, the main verb in a focus construction gains a high tone.
Compare the verb 'watch' in (5) vs. (6).

(5) t̪òlé      t̪ə̀-nɔ̀n-ɔ́          ŋɛ́n-ɛ́         únɛ́ɾɛ́  
    CLt̪-lion  CLt̪-watch-IT.PFV  CLŋ.dog-ACC   yesterday-LEFT_H  
'The lion watched the dog yesterday.'  

(6) àn  ɔ́ndì              kə́-nɔ̀n-ɔ́                ŋɛ́n-ɛ́         únɛ́ɾɛ́  
    FOC CLg.what.LEFT_H   CLg.LEFT_H-watch-IT.PFV CLŋ.dog-ACC   yesterday-LEFT_H  
'What watched the dog yesterday?'  

As an aside, note that the word *ùnɛ́ɾɛ́* also has a Left-H, in this case due to high-tone spreading from the preceding noun *ŋɛ́n-ɛ́*.

The last instance where Left-H can occur is in relative clauses.
Like in focus constructions, the main verb of a relative clause obtains a high tone at the left edge.
Compare the verb 'chase' in a matrix clause (7) and in a relative clause (8).

(7) ŋɛ́n     ŋə̀-r̀lɛ̀ɲ-í         t̪ólè-ɲá  
    CLŋ.doɡ CLŋ-chase-VEN.PFV CLt̪.lion-ACC  
'The dog chased the lion'  

(8) t̪òlé      [t̪ə́-r̀lɛ̀ɲ-í                 ŋɛ́n-ɛ́]       t̪-ìcò  
    CLt̪.lion  [CLt̪.LEFT_H-chase-VEN.PFV  CLŋ.dog-ACC] CLt̪-bad  
'The lion [who chased the dog] is bad.  

## FAQ
- **What if I'm not sure if the gloss I chose is correct?** Answer: Leave a comment and I'll review when you upload it and/or during our next meeting.
- **Why do none of the candidate parses have a definition relevant to the sentence I'm glossing?** Answer: Not all words in the lexicon are supported by the parser yet, leave a note so I can add it.
- **Several candidates have the same Tira string but different glosses. Which should I choose?** Answer: Use these heuristics:
  - Rely on the translation: If the translation says 'We (incl)', the verb should include 1PL.INCL in its gloss. If the translation says 'dogs', then the gloss should be dog-NOM-PL or dog-ACC-PL.
  - Verbs in isolation are **typically imperative.** E.g. the sentence is just the word 'ápɔ́' and the glosses are carry-IPFV-VENT-left_h and carry-IMP-IT, prefer carry-IMP-IT because it's imperative (also conforms to the feature parsimony heuristic above).
  - Few features over many, e.g. prefer hit-PFV-IT rather than hit-IPFV-VENT-1SG.SBJ-left_h .
  - `left_h` should only occur **following a high-toned word** (H-tone spreading), following the **focus particle 'àn'**, or **at the beginning of a relative clause** (e.g. The boy **who saw the dog** left). Otherwise, if there's one candidate with 'left_h' and another without, prefer the one without.