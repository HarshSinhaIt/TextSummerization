import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from nltk.corpus import stopwords
from heapq import nlargest


text = """The Mughal Empire, founded by Babur in 1526, was one of the largest and most powerful empires in the Indian subcontinent, lasting until the mid-19th century. It was known for its centralized administrative structure, military prowess, and cultural contributions that significantly shaped the history of India. Babur, a descendant of Timur and Genghis Khan, defeated the Delhi Sultanate and established Mughal rule, which reached its zenith under Akbar the Great. Akbar's policies of religious tolerance, efficient governance, and cultural integration helped solidify the empire’s dominance over a vast territory, extending from Afghanistan to Bengal and from the Himalayas to the Deccan plateau. Akbar’s successors, Jahangir, Shah Jahan, and Aurangzeb, continued to expand and consolidate the empire. Shah Jahan, in particular, is renowned for his architectural achievements, including the construction of the Taj Mahal, one of the world’s most famous monuments. The Mughal Empire became a melting pot of Persian, Indian, and Islamic art and culture, which gave rise to remarkable contributions in architecture, painting, literature, and cuisine. However, despite its golden age, the empire faced challenges, particularly under Aurangzeb, whose religious conservatism and military overreach led to internal dissent and weakening of the central authority. By the early 18th century, the empire began to decline, facing invasions, revolts, and the rise of regional powers such as the Marathas and Sikhs. The British East India Company’s growing influence further eroded Mughal control, and after the Indian Rebellion of 1857, the British formally ended the Mughal Empire, exiling the last emperor, Bahadur Shah II. Despite its eventual collapse, the Mughal Empire left a lasting legacy on Indian history, particularly in its contributions to culture, architecture, and administration."""
def summarizer(rawdoc):
    stopwords= list(STOP_WORDS)
    # print(STOP_WORDS)

    nlp= spacy.load('en_core_web_sm')
    doc= nlp(rawdoc)
    # print(doc)

    tokens = [token.text for token in doc]
    # print(tokens)

    word_freq= {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1
    # print(word_freq)

    max_freq = max(word_freq.values())
    # print(max_freq)

    for word in word_freq.keys():
        word_freq[word]= word_freq[word]/max_freq
    # print(word_freq)

    sentance_tokens= [sent for sent in doc.sents]
    # print(sentance_tokens)

    sent_scores= {}
    for sent in sentance_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]
    # print(sent_scores)

    select_len = int(len(sentance_tokens) * 0.3)
    # print(select_len)

    summary= nlargest(select_len, sent_scores, key= sent_scores.get)
    # print(summary)

    final_summary = [word.text for word in summary]
    summary= ' '.join(final_summary)
    # print("org_text=",text)
    # print("summary_text",summary)

    # print("Length of original text", len(text.split(' ')))
    # print("Length of summary text", len(summary.split(' ')))

    return summary, doc, len(rawdoc.split(' ')), len(summary.split(' '))
