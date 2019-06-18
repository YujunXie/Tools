import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import mpl_toolkits.mplot3d.axes3d as p3

def tsne():
	colors = ['k','r','yellow','b','c','m','chocolate','pink','lawngreen','indigo','aliceblue','burlywood','dimgray','sienna'
              'gold']

    X = np.load('X.npy')
    y = np.load('y.npy')

    print(X, y)
    print(X.shape, y.shape)

    if X.shape[0]:
        x_embedding = TSNE(n_components=3,n_iter=2000, metric='cosine').fit_transform(X)
        x_min, x_max = np.min(x_embedding, axis=0), np.max(x_embedding, axis=0)
        x_embedding = (x_embedding - x_min) / (x_max - x_min)
        fig = plt.figure(figsize=(8, 4))
        # ax = fig.add_subplot(1, 1, 1)
        ax2 = p3.Axes3D(fig)

        # ax2.scatter(x_embedding[:, 0], x_embedding[:, 1], x_embedding[:, 2],  c=y*20)
        for i in range(x_embedding.shape[0]):
            ax2.text(x_embedding[i, 0], x_embedding[i, 1], x_embedding[i, 2], str(y[i]), color=colors[y[i]],
                     fontdict={'weight': 'bold', 'size': 9})
        plt.show()