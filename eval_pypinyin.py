from tkinter.ttk import Style
from wsgiref.validate import ErrorWrapper
import pypinyin 
import argparse

parser = argparse.ArgumentParser(description='Parse IO file names.')
parser.add_argument('--label', type=str, help='path to the file with labels')
parser.add_argument('--log', type=str, help='location to log conversion errors')

args = parser.parse_args()

read_file_name = args.label
write_file_name = args.log


total_word = 0
correct = 0
error = 0

error_words = {}
all_words = set()
with open(read_file_name, 'r') as file:
    for line in file:
        line = line.strip()
        if not line or line[0] == '\n' or line[0] == '#':
            continue
        
        l = line[:-1].split('|')
        filename, label, character = l
        label = label.replace('$', '%').split('%')
        label = [lab.strip() for lab in label]
        character = character.replace('$', '%').split('%')
        character = [c.strip() for c in character]

        pred = [pypinyin.pinyin(c, style=pypinyin.Style.TONE3, neutral_tone_with_five=True) for c in character]
        pred = [[' '.join(word) for word in phrase] for phrase in pred]
        pred = [' '.join(phrase) for phrase in pred]

        for c,p,l in zip(character,pred,label):
            all_words.add(c)
            total_word += 1
            if p == l:
                correct += 1
            else:
                error += 1
                error_words[c] = f'conversion={p}, label={l}'

with open(write_file_name,'w') as ef:
    for word in error_words:
        ef.write(f'{word}: {error_words[word]}\n')

print(f'total word count={total_word}, correct conversion={correct}, error={error}')
if total_word:
    print(f'correct rate={correct / total_word}, error rate={error / total_word}')

print(f'# of distinct words={len(all_words)}, # of distinct error words={len(error_words)}, error rate={len(error_words)/len(all_words)}')

