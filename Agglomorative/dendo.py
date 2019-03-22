import plotly.plotly as py
import plotly.figure_factory as ff
import pickle
import numpy as np
from scipy.cluster.hierarchy import linkage

pkl_file=open("../pkl_files/dist.pkl","rb")
dist=pickle.load(pkl_file)
pkl_file.close()

figure = ff.create_dendrogram(
    dist, orientation='bottom', labels=id_label_list,
    linkagefun=lambda x: linkage(dist, 'ward', metric='euclidean')
)
py.iplot(dendro, filename='simple_dendrogram_with_color_threshold')