import json

def conv(fro, to):
    with open(fro, 'r') as f:
        fro = f.readlines()
        fro = [word[:-1] for word in fro]

    with open(to, 'w', encoding='utf-8') as f:
        json.dump(fro, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    conv('all_words.txt', '../src/assets/json/playable-words.json')
    conv('wordlist.txt', '../src/assets/json/drawable-words.json')
