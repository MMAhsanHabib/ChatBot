from newspaper import Article
import random
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings
warnings.filterwarnings('ignore')

nltk.download('punkt', quiet = True)

article = Article('https://www.mayoclinic.org/diseases-conditions/chronic-kidney-disease/symptoms-causes/syc-20354521')
article.download()
article.parse()
article.nlp()
corpus = article.text

#print(corpus)

#Tokenization
text = corpus
sentence_list = nltk.sent_tokenize(text)

#print(sentence_list)

# A function to return a random greeting response to a users greeting
def greeting_response(text):
    text = text.lower()
    
    #Bots greeting response
    bot_greetings = ['hi','hey','hello','howdy']
    
    #Users greeting response
    user_greetings = ['hi', 'hey', 'hello', 'wassup']
    
    for word in text.split():
        if word in user_greetings:
            return random.choice(bot_greetings)

        
def index_sort(list_var):
    length = len(list_var)
    list_index = list(range(0,length))
    
    x = list_var
    for i in range(length):
        for j in range(length):
            if x[list_index[i]]>x[list_index[j]]:
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp
                
    return list_index
        
        
# Create the bot response        
def bot_response(user_input):
    user_input = user_input.lower()
    sentence_list.append(user_input)
    bot_response = ''
    cm = CountVectorizer().fit_transform(sentence_list)
    similarity_score = cosine_similarity(cm[-1],cm)
    similarity_score_list = similarity_score.flatten()
    index = index_sort(similarity_score_list)
    index = index[1:]
    response_flag = 0
    
    j=0
    for i in range(len(index)):
        if similarity_score_list[index[i]]>0.0:
            bot_response = bot_response+'' +sentence_list[index[i]]
            response_flag = 1
            j = j+1
            if j>2:
                break
                
    if response_flag == 0:
        bot_response = bot_response+''+"I apologize, I don't understand"
        
    sentence_list.remove(user_input)
        
    return bot_response

# Start the chat
print('Bot: I am bot. I will answere you. Ask me your queries. If you want to exit type bye.')
exit_list = ['exit','see you later','bye','quit','break']

while(True):
    user_input = input()
    if user_input.lower() in exit_list:
        print('Bot: Chat with you later')
        break
    else:
        if greeting_response(user_input) != None:
            print('Bot: '+ greeting_response(user_input))
        else:
            print('Bot: '+ bot_response(user_input))
    
    
