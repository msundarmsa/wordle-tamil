import csv
from tamil import utf8
from tqdm import tqdm
import string

def strip_punc(s):
    return s.translate(str.maketrans('', '', string.punctuation))

if __name__ == '__main__':
    all_words = set() 
    word_len = 4

    with open('all_words.txt', 'r') as f:
        valid_words = f.readlines()
        valid_words = set([word[:-1] for word in valid_words])

    num_lines = 126746
    with tqdm(total=num_lines) as pbar:
        with open('Tamilmurasu_dataset_06_Jan_2011_06_Jan_2020.csv') as f:
            reader = csv.DictReader(f)
            for row in reader:
                curr_words = strip_punc(row['news_title']).split(' ')
                curr_words.append(strip_punc(row['news_category']))
                curr_words.extend(strip_punc(row['news_article']).split(' '))

                for curr_word in curr_words:
                    num_letters = len(utf8.get_letters(curr_word))
                    if num_letters == word_len and curr_word in valid_words:
                        all_words.add(curr_word)

                pbar.update(1)
    
    with open('wordlist.txt', 'w') as f:
        for word in all_words:
            f.write(f'{word}\n')