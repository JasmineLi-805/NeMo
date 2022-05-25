"""
Creates the NeMo style manifest files where the text labels are in pinyin instead of characters.
"""
import json
import pypinyin
import argparse

parser = argparse.ArgumentParser(description='Parse IO file names.')
parser.add_argument('--input', type=str, help='path to the file with labels')
parser.add_argument('--output', type=str, help='path to the output file')

args = parser.parse_args()

read_file_name = args.input
write_file_name = args.output

with open(read_file_name, 'r') as file:
    with open(write_file_name, 'w') as out_file:
        for line in file:
            if not line:
                continue
            line = json.loads(line)
            
            path = line['audio_filepath'].replace('/NeMo','')
            line['audio_filepath'] = path
            
            pred = pypinyin.pinyin(line['text'], style=pypinyin.Style.NORMAL, neutral_tone_with_five=True)
            pred = [p[0] for p in pred]
            pred = ' '.join(pred)
            line['text'] = pred
            
            out_file.write(json.dumps(line) + '\n')
