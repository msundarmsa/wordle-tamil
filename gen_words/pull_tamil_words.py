import requests
import re
from tamil import utf8
import concurrent.futures
from tqdm import tqdm
import os

# download all words beginning with a given letter
# and extract `word_len` letter words from the words
def download_and_process(i, word_len=4, dl_if_exists=False):
    if not os.path.exists(f'all_words/{i}.txt') or dl_if_exists:
        start_ch = utf8.tamil_letters[i] 
        url = f'https://dsal.uchicago.edu/cgi-bin/app/tamil_query.py?qs={start_ch}&searchhws=yes&matchtype=default'
        r = requests.get(url)

        with open(f'all_words/{i}.txt', 'w') as f:
            f.write(r.text)
        
        parse_text = r.text
    else:
        with open(f'all_words/{i}.txt', 'r') as f:
            parse_text = f.read()

    word_links = re.findall(' <a href=".*_query.py\?qs=.*">.*</a> ', parse_text)

    words = set() 
    for word_link in word_links:
        curr_word = word_link.split('>')[1].split('<')[0]
        num_letters = len(utf8.get_letters(curr_word))
        if num_letters == word_len:
            words.add(curr_word)

    return words

if __name__  == '__main__':
    all_words_by_letter = dict()
    num_letters = len(utf8.tamil_letters)
    with tqdm(total=num_letters) as pbar:
        # We can use a with statement to ensure threads are cleaned up promptly
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            # Start the load operations and mark each future with its URL
            futures = {executor.submit(download_and_process, i): i for i in range(num_letters)}
            for future in concurrent.futures.as_completed(futures):
                letter = futures[future]
                all_words_by_letter[letter] = future.result()
                pbar.update(1)

    all_words = []
    for letter in range(num_letters):
        all_words.extend(all_words_by_letter[letter])

    with open('all_words.txt', 'w') as f:
        for word in all_words:
            f.write(f'{word}\n')