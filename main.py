import pickle
import nltk
import argparse
import os
import re
import tqdm
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import FreqDist
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import json
# create banned.txt file if it doesn't exist
if not os.path.exists("banned.txt"):
    open("banned.txt", 'w').close()

# create unicwords.txt file if it doesn't exist
if not os.path.exists("unicwords.txt"):
    open("unicwords.txt", 'w').close()

# create images, messages, and tables folders if they don't exist
os.makedirs("images", exist_ok=True)
os.makedirs("messages", exist_ok=True)
os.makedirs("tables", exist_ok=True)

# Ignore UserWarnings
warnings.filterwarnings('ignore', category=UserWarning)

# Set the font family for plots
plt.rcParams['font.family'] = 'DejaVu Sans'

# Parse command line arguments
parser = argparse.ArgumentParser(prog='Telegram_messages_parser and visualizer',
                                 description='Parse the messages from telegram group or chat and then visualize it')

# Define command line arguments
parser.add_argument('-u', '--unic_words', help='Shows only unicwords in unicwords.txt', action='store_true', dest='unic_words')
parser.add_argument('-l', '--len', type=int, help='Changes the minimal length of a word', default=3, action='store', dest='len')
parser.add_argument('--dpi', type=int, help='Changes DPI of the image', default=300, action='store', dest='dpi')
parser.add_argument('-m', '--max_words', type=int, help='Changes the maximum count of words for the image', action='store', dest='max_words')
parser.add_argument('-a', '--action',  help='Select the action to do', default='image', choices=['image', 'table', 'parse'], required=True)
parser.add_argument('-c', '--columns', type=int, help='Columns count for table', dest='columns',default=10)

args = parser.parse_args()


def read_data(file_name):
    with open(f"{file_name}", "r", encoding="utf-8") as f:
        return json.load(f)


def read_words_from_file(filename):
    """Reads words from a file and returns them as a list."""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        words = content.split(',')
        return [word.strip().replace(' ', '') for word in words]


def users(file_path):
    """Reads usernames from a file and returns them as a list."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return list(f.read().splitlines())


def parse():
    messages_by_name = {}

    for file_name in os.listdir("./messages"):
        if file_name.endswith(".json"):
            file_path = os.path.join("./messages", file_name)
            data = read_data(file_path)
            for i in data["messages"]:
                try:
                    name = i["from"]
                    text = i["text"]
                    if name not in messages_by_name:
                        messages_by_name[name] = []

                    if type(text) == str:
                        messages_by_name[name].append(text)

                except:
                    pass
    with open("messages.pkl", "wb") as f:
        pickle.dump(messages_by_name, f)
    with open("users.txt", "w", encoding="utf-8") as f:
        f.write('\n'.join(messages_by_name.keys()))
    for i in messages_by_name:
        messages = len(messages_by_name[i])
        print(f"{i} - {messages}")


def give_pic(jobs, file_name, dpi=300, max_words=None, min_chars=3):
    """"creates the words cloud"""
    # Tokenize the data
    text = ' '.join(jobs)
    tokens = word_tokenize(text)
    banned_words = read_words_from_file("banned.txt")
    # Remove stopwords and words less than 3 characters long
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word.lower() for word in tokens if word.lower() not in stop_words and len(word) >= min_chars and word.lower() not in banned_words]
    # Create a frequency distribution of the tokens
    freq_dist = nltk.FreqDist(filtered_tokens)
    # Generate a word cloud with closer together words
    if max_words is None:
        wordcloud = WordCloud(width=1920, height=1080, background_color='white', relative_scaling=0).generate_from_frequencies(freq_dist)
    else:
        wordcloud = WordCloud(width=1920, height=1080, background_color='white', max_words=max_words, relative_scaling=0).generate_from_frequencies(freq_dist)
    # Format the filename to remove invalid characters
    file_name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '', file_name)
    # Display the word cloud
    plt.figure(figsize=(12, 12), dpi=dpi)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    file_path = os.path.join("./images", file_name)
    plt.savefig(file_path, bbox_inches='tight')


def visualize_most_common_words(sentences, file_name, columns=10, unicwords=None, only_mat=False, min_chars=3):
    """"creates the table from most used words"""

    # Tokenize the sentences
    banned_words = read_words_from_file("banned.txt")
    if only_mat:
        tokens = [word.lower() for sentence in sentences for word in word_tokenize(sentence) if word.lower() in unicwords and word.lower() not in banned_words]
    else:
        tokens = [word.lower() for sentence in sentences for word in word_tokenize(sentence) if len(word.lower()) >= min_chars and word.lower() not in banned_words]

    # Compute the frequency distribution of the words
    freq_dist = FreqDist(tokens)

    # Check if freq_dist is empty
    if not freq_dist:
        return

    # Get the most common words, sorted by frequency
    most_common_words = sorted(freq_dist.items(), key=lambda x: x[1], reverse=True)[:columns]

    # Compute the average frequency of all words
    avg_frequency = sum([count for _, count in freq_dist.items()]) / len(freq_dist)

    # Create a bar plot of the most common words
    colors = sns.color_palette("flare", len(most_common_words), as_cmap=False)

    plt.figure(figsize=(12, 8))
    ax = plt.gca()
    for i, (word, frequency) in enumerate(most_common_words):
        ax.barh(word, frequency, align='center', height=0.7, color=colors[i])
        ax.text(frequency + (avg_frequency * 0.01), i, str(frequency), ha='left', va='center', fontsize=10)
    ax.set_xlabel('Frequency')
    ax.set_ylabel('Words')
    ax.set_title(file_name)

    plt.tight_layout()
    file_name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '', file_name)
    file_path = os.path.join('./tables', file_name)
    plt.savefig(file_path, bbox_inches='tight')


def main():
    if args.action == "parse":
        parse()
    elif args.action == "table":
        with open("messages.pkl", "rb") as f:
            soup_str = pickle.load(f)

            user_list = users("users.txt")
            u_words = read_words_from_file("unicwords.txt") if args.unic_words else None

            for i in tqdm.tqdm(user_list, desc="Generating tables"):
                messages = soup_str[i]
                visualize_most_common_words(messages, i, columns=args.columns, only_mat=args.unic_words, unicwords=u_words, min_chars=args.len)
    elif args.action == "image":
        with open("messages.pkl", "rb") as f:
            soup_str = pickle.load(f)

            user_list = users("users.txt")

            for i in tqdm.tqdm(user_list, desc="Generating images"):
                messages = soup_str[i]
                give_pic(messages, i, max_words=args.max_words, dpi=args.dpi, min_chars=args.len)


if __name__ == "__main__":
    main()
