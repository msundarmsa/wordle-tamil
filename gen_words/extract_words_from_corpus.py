import csv
from tamil import utf8
from tqdm import tqdm
import string

def strip_punc(s):
    return s.translate(str.maketrans('', '', string.punctuation))

uyirmei_table = set(['க', 'கா', 'கி', 'கீ', 'கு', 'கூ', 'கெ', 'கே', 'கை', 'கொ', 'கோ', 'கௌ', 'க்'
                 'ங', 'ஙா', 'ஙி', 'ஙீ', 'ஙு', 'ஙூ', 'ஙெ', 'ஙே', 'ஙை', 'ஙொ', 'ஙோ', 'ஙௌ', 'ங்',
                 'ச', 'சா', 'சி', 'சீ', 'சு', 'சூ', 'செ', 'சே', 'சை', 'சொ', 'சோ', 'சௌ', 'ச்',
                 'ஞ', 'ஞா', 'ஞி', 'ஞீ', 'ஞு', 'ஞூ', 'ஞெ', 'ஞே', 'ஞை', 'ஞொ', 'ஞோ', 'ஞௌ', 'ஞ்',
                 'ட', 'டா', 'டி', 'டீ', 'டு', 'டூ', 'டெ', 'டே', 'டை', 'டொ', 'டோ', 'டௌ', 'ட்',
                 'ண', 'ணா', 'ணி', 'ணீ', 'ணு', 'ணூ', 'ணெ', 'ணே', 'ணை', 'ணொ', 'ணோ', 'ணௌ', 'ண்',
                 'த', 'தா', 'தி', 'தீ', 'து', 'தூ', 'தெ', 'தே', 'தை', 'தொ', 'தோ', 'தௌ', 'த்',
                 'ந', 'நா', 'நி', 'நீ', 'நு', 'நூ', 'நெ', 'நே', 'நை', 'நொ', 'நோ', 'நௌ', 'ந்',
                 'ப', 'பா', 'பி', 'பீ', 'பு', 'பூ', 'பெ', 'பே', 'பை', 'பொ', 'போ', 'பௌ', 'ப்',
                 'ம', 'மா', 'மி', 'மீ', 'மு', 'மூ', 'மெ', 'மே', 'மை', 'மொ', 'மோ', 'மௌ', 'ம்',
                 'ய', 'யா', 'யி', 'யீ', 'யு', 'யூ', 'யெ', 'யே', 'யை', 'யொ', 'யோ', 'யௌ', 'ய்',
                 'ர', 'ரா', 'ரி', 'ரீ', 'ரு', 'ரூ', 'ரெ', 'ரே', 'ரை', 'ரொ', 'ரோ', 'ரௌ', 'ர்',
                 'ல', 'லா', 'லி', 'லீ', 'லு', 'லூ', 'லெ', 'லே', 'லை', 'லொ', 'லோ', 'லௌ', 'ல்',
                 'வ', 'வா', 'வி', 'வீ', 'வு', 'வூ', 'வெ', 'வே', 'வை', 'வொ', 'வோ', 'வௌ', 'வ்',
                 'ழ', 'ழா', 'ழி', 'ழீ', 'ழு', 'ழூ', 'ழெ', 'ழே', 'ழை', 'ழொ', 'ழோ', 'ழௌ', 'ழ்',
                 'ள', 'ளா', 'ளி', 'ளீ', 'ளு', 'ளூ', 'ளெ', 'ளே', 'ளை', 'ளொ', 'ளோ', 'ளௌ', 'ள்',
                 'ற', 'றா', 'றி', 'றீ', 'று', 'றூ', 'றெ', 'றே', 'றை', 'றொ', 'றோ', 'றௌ', 'ற்',
                 'ன', 'னா', 'னி', 'னீ', 'னு', 'னூ', 'னெ', 'னே', 'னை', 'னொ', 'னோ', 'னௌ', 'ன்',
                 'அ', 'ஆ', 'இ', 'ஈ', 'உ', 'ஊ', 'எ', 'ஏ', 'ஐ', 'ஒ', 'ஓ', 'ஔ'])

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
                    curr_letters = utf8.get_letters(curr_word)
                    num_letters = len(curr_letters)
                    curr_letters = set(curr_letters)
                    num_other_letters = len(list(set.difference(curr_letters, uyirmei_table)))
                    if num_letters == word_len and curr_word in valid_words and num_other_letters == 0:
                        all_words.add(curr_word)

                pbar.update(1)
    
    with open('wordlist.txt', 'w') as f:
        for word in all_words:
            f.write(f'{word}\n')