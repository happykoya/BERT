import gensim
import matplotlib.pyplot as plt
import sys
import os
import numpy
from sklearn.decomposition import PCA

print("now loading...")
model = gensim.models.KeyedVectors.load_word2vec_format('model.vec', binary=False)

#print(model.most_similar(positive=['日本人']))
def draw_word_scatter(word, topn=30):
    
    words = [x[0] for x in sorted(model.most_similar(word, topn=topn))]

    vecs = []
    for word in words:
        vec = model[word]
        vecs.append(vec)
        
    # Scikit-learnのPCAによる次元削減とその可視化
    pca = PCA(n_components=2)
    coords = pca.fit_transform(vecs)
    print(coords)
    # matplotlibによる可視化
    fig, ax = plt.subplots()
    x = [v[0] for v in coords]
    y = [v[1] for v in coords]
    
    ax.scatter(x, y)
    
    for i, txt in enumerate(words):
        ax.annotate(txt, (coords[i][0], coords[i][1]))
    plt.show()


draw_word_scatter("love",topn=30)