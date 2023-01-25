import os
import sys
import random
import orjson
import pathlib
import re
import twokenize

TWEETS = '../usa_extracted/'
DATA = '../dataset'

def get_whitelist(path='../whitelist'):
    sources = []
    with open(path) as wlst:
        for line in wlst:
            sources.append(line.rstrip('\n'))
    return sources

WHITELIST = get_whitelist()

def get_queue():
    return sorted([str(i) for i in pathlib.Path('./../').glob(f'usa_extracted/*')])

def meets_whitelist(tweet):
    return tweet['source'] in WHITELIST

def starts_with_rt(tweet):
    # rt string then a non alnum character (some twitter clients use rt"..." or the other double quote utf character)
    if len(tweet['text']) > 3:
        if tweet['text'][:2].lower() == 'rt':
            if not tweet['text'][2].isalnum():
                return True
    return False

def includes_rt(tweet):
    if len(tweet['text']) > 3:
        toks = [w.lower() for w in twokenize.tokenizeRawTweetText(tweet['text'])]
        return 'rt' in toks
    return False

def includes_bad(tweet):
    if len(tweet['text']) > 3:
        toks = [w.lower() for w in twokenize.tokenizeRawTweetText(tweet['text'])]
        return 'rt' in toks or 'follow' in toks or 'mention' in toks
    return False

def hashtags_check(tweet, max_tags=2):
    return len(tweet['entities']['hashtags']) <= max_tags

def followers_check(tweet, max_followers=9999):
    return tweet['user']['followers_count'] <= max_followers

def urls_check(tweet, max_urls=4):
    return len(tweet['entities']['urls']) <= max_urls

def mentions_check(tweet, max_ments=4):
    return len(tweet['entities']['user_mentions']) <= max_ments

def reservoir(filter_func, tag='', size=500):
    sample = []
    queue = get_queue()
    i = 0
    j = 0
    for day_file in queue:
        print(f'Filter {tag}: {day_file}')
        with open(day_file, encoding='utf-8') as day:
            for line in day:
                obj = orjson.loads(line)
                if filter_func(obj):
                    i += 1
                    if len(sample) < size:
                        sample.append(line)
                    else:
                        if random.random() < size/i:
                            index = random.randint(0,size-1)
                            sample[index] = line
            j += 1
        if j > 0 and j % 100 == 0:
            with open(f'./intermediates/sample{j//100}_{tag}', 'w+', encoding='utf-8') as sample_out:
                for line in sample:
                    sample_out.write(line)
    with open(f'./sample_{tag}', 'w+', encoding='utf-8') as sample_out:
        for line in sample:
            sample_out.write(line)

# Filter 0: Whitelist + Starting with RT
def filter_alpha(tweet):
    return meets_whitelist(tweet) and not starts_with_rt(tweet)

# Filter 1: Whitelist + Starting with RT + 10,000 Followers
def filter_beta(tweet):
    return filter_alpha(tweet) and followers_check(tweet)

# Filter 2: Whitelist + Starting with RT + 3 Hashtags
def filter_gamma(tweet):
    return filter_alpha(tweet) and hashtags_check(tweet)

# Filter 3: Whitelist + Starting with RT + 10,000 Followers + 3 Hashtags
def filter_epsilon(tweet):
    return filter_beta(tweet) and hashtags_check(tweet)

# Filter 4: Whitelist + Starting with RT + 10,000 Followers + 3 Hashtags + 5 Mentions
def filter_phi(tweet):
    return filter_epsilon(tweet) and mentions_check(tweet)

# Filter 5: Whitelist + Includes RT
def filter_pi(tweet):
    return meets_whitelist(tweet) and not includes_rt(tweet)

# Filter 6: Whitelist + Includes RT + 10,000 Followers + 3 Hashtags
def filter_omega(tweet):
    return filter_pi(tweet) and followers_check(tweet) and hashtags_check(tweet)

# Filter 7: Whitelist + Includes RT + 10,000 Followers + 3 Hashtags + 5 Mentions
def filter_mu(tweet):
    return filter_omega(tweet) and mentions_check(tweet)

# Filter 8: Whitelist + Includes RT/follow/mention + 10,000 Followers + 3 Hashtags
def filter_psi(tweet):
    return meets_whitelist(tweet) and not includes_bad(tweet) and followers_check(tweet) and hashtags_check(tweet)

# Filter 9: Whitelist + Includes RT/follow/mention + 5,000 Followers + 3 Hashtags
def filter_delta(tweet):
    return meets_whitelist(tweet) and not includes_bad(tweet) and followers_check(tweet, max_followers=4999) and hashtags_check(tweet)


def dataset(day_file, filter_func):
    filter_name = f'data{day_file.split("usa")[-1]}'
    filter_file = f'{DATA}/{filter_name}'
    with open(filter_file, 'w+', encoding='utf-8') as ff:
        with open(day_file, encoding='utf-8') as day:
            for line in day:
                obj = orjson.loads(line)
                if filter_func(obj):
                    ff.write(line)

if __name__ == '__main__':
    if sys.argv[1] == "0":
        reservoir(filter_alpha, 'a')
    elif sys.argv[1] == "1":
        reservoir(filter_beta, 'b')
    elif sys.argv[1] == "2":
        reservoir(filter_gamma, 'c')
    elif sys.argv[1] == "3":
        reservoir(filter_epsilon, 'd')
    elif sys.argv[1] == "4":
        reservoir(filter_phi, 'e')
    elif sys.argv[1] == "5":
        reservoir(filter_pi, 'f')
    elif sys.argv[1] == "6":
        reservoir(filter_omega, 'g')
    elif sys.argv[1] == "7":
        reservoir(filter_mu, 'h')
    elif sys.argv[1] == "8":
        reservoir(filter_psi, 'i')
    elif sys.argv[1] == "9":
        reservoir(filter_delta, 'j')
    elif sys.argv[1] == 'dataset':
        mode = filter_delta
        worker = int(sys.argv[2])
        threads = int(sys.argv[3])
        queue = get_queue()
        splits = [i for i in range(0,len(queue),len(queue)//threads)]
        partitions = [queue[splits[i-1]:splits[i]] for i in range(len(splits))] + [queue[splits[-1]:]]
        for day_file in partitions[worker]:
            dataset(day_file, mode)
    elif sys.argv[1] == 'fix':
        mode = filter_delta
        quarter = int(sys.argv[2])
        queue = get_queue()
        for day_file in [queue[-1]]: 
            filter_name = f'data{day_file.split("usa")[-1]}'
            filter_file = f'{DATA}/{filter_name}'
            if not os.path.exists(filter_file):
                dataset(day_file, mode)
