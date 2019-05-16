# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.views.generic import TemplateView

# Create your views here.
'''class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)'''

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic  

from .forms import SumForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.tokenize import sent_tokenize
import math
import collections
import numpy
from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt
import re

'''class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
'''

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def preprocess(text):
	text=text.replace("\n", " ")
	text=re.sub(r"[-()#/@;:<>{}`+=~|!?,]", "", text.lower())
	text=re.sub(r'[^\x00-\x7F]+','', text)
	text=re.sub(' +', ' ',text)
	return text
def summarize(text):
    summ=""
    vectorizer = TfidfVectorizer(stop_words='english')
    data=preprocess(text)
    print type(data)
    sent_tokenize_list = sent_tokenize(data)
    print sent_tokenize_list
    sent_len=len(sent_tokenize_list)
    X = vectorizer.fit_transform(sent_tokenize_list)
    print(vectorizer.get_feature_names())
    print X.toarray()
    true_k = int(math.ceil(float(sent_len)/2))
    print true_k
    model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
    model.fit_transform(X)
    print model.labels_
    clustering = collections.defaultdict(list)
 
    for idx, label in enumerate(model.labels_):
        clustering[label].append(idx)
    print clustering
      
    for key,values in clustering.items():
    	max=0
        for ind in values:
			p=X[ind].toarray()
			v=numpy.sum(p)
			if v>max:
				max=v
				max_ind=ind
        print sent_tokenize_list[max_ind]
        summ=summ+sent_tokenize_list[max_ind]+" "
        print summ
    return summ

def word_cloud(text):
    comment_words = ''
    stopwords = set(STOPWORDS)
    tokens = text.split()
    for i in range(len(tokens)): 
        tokens[i] = tokens[i].lower()
    for words in tokens: 
    	comment_words = comment_words + words + ' '
    #print comment_words
    wordcloud = WordCloud(width = 800, height = 800, 
                background_color ='white', 
                stopwords = stopwords, 
                min_font_size = 10).generate(comment_words)
    # plot the WordCloud image                        
    plt.figure(figsize = (8, 8), facecolor = None) 
    plt.imshow(wordcloud) 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 
  
    plt.show()



def sumrz(request):
    if request.method == 'POST':
        form = SumForm(request.POST)
        if form.is_valid():
            text=form.cleaned_data["text"]
            print text
            summary=summarize(text)
	    return render(request, 'hom.html', {'form':form, 'text':summary})
    else:
        form = SumForm()
    return render(request, 'hom.html', {'form': form})

def wrd(request):
    if request.method == 'POST':
        form = SumForm(request.POST)
        if form.is_valid():
            text=form.cleaned_data["text"]
            print text
            word_cloud(text)
	    #return render(request, 'word.html', {'form':form, 'text':summary})
    else:
        form = SumForm()
    return render(request, 'word.html', {'form': form})


