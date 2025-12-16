import ast
import pandas as pd
import streamlit as st
from streamlit_features.data import data_cleaning, eda

df = pd.read_pickle('data/df_cleaned.pkl')

st.title("FIFA 26 Player Analysis")



tabs = st.tabs(['Dataset', 'EDA', 'K-Means', 'GMM'])

with tabs[0]: 
    data_cleaning(df=df.copy())

with tabs[1]:
    eda(df=df.copy())

with tabs[2]:
    from streamlit_features.k_means_code import *

    
    # Plot K-Means
    kmeans_df = plot_kmeans()
    st.subheader('Results')
    
    kmeans_tabs = st.tabs([
        'Top 10 Players By Cluster',
        'Distribution of Ratings by Atribute',
        'Technical Report',
        'Code'
        ]
    )
    with kmeans_tabs[0]:
        cluster_df(df=kmeans_df)
    
    with kmeans_tabs[1]:
        plot_kde(df_viz=kmeans_df)

    with kmeans_tabs[2]:
        st.markdown(tech_report)

    with kmeans_tabs[3]:
        st.write("Step 1: Run Principal Component Analysis using 3 Principal Components to be able to make 3d plots")
        st.code(pca_code, language='python')
        st.write("Step 2: Run KMeans with K==4 (Elbow Method)")
        st.code(kmeans_code, language='python')


with tabs[3]:
    from streamlit_features.gmm_code import *
    
    umap_data = plot_umap()
    gmm_df = plot_gmm()
    
    gmm_tabs = st.tabs([
        'Cluster Report',
        'Cluster Feature Matrix',
        'Code'
    ])

    with gmm_tabs[0]:
        st.markdown(gmm_report)
        st.divider()
        st.subheader('Top 5 Players by Cluster')
        top_gmm_players(df=gmm_df)

    with gmm_tabs[1]:
        cluster_feature_matrix(df=gmm_df)

    
    with gmm_tabs[2]:
        st.code(umap_code, language='python')
        st.code(gmm_code, language='python')

st.divider()

cols = st.columns([2,8])
with cols[0]: st.write('About the dataset:')
with cols[1]:
    st.page_link(
        label='EAFC26 Mens Player Data Analysis Modeling (Click to view on Kaggle)',
        page='https://www.kaggle.com/code/devraai/eafc26-mens-player-data-analysis-modeling'
    )
