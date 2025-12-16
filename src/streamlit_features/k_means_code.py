import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


pca_code = """
numeric_df = df.select_dtypes(include=[np.number])
numeric_df = numeric_df.drop(['rank', 'ovr'], axis=1, errors='ignore')

X = numeric_df.fillna(0)

# Run Scaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

pca_var = PCA(n_components=10)
pca_var.fit(X_scaled)

cum_var = np.cumsum(pca_var.explained_variance_ratio_) * 100
"""
kmeans_code = """
X_pca = pca.fit_transform(X_scaled) 

# Cálculo da Variância Total
var_total = sum(pca.explained_variance_ratio_) * 100
print(f'Variância Total Explicada: {var_total:.2f}%')

# 3. KMeans (Gerando os Grupos)
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
labels = kmeans.fit_predict(X_scaled)
"""

tech_report = """
## 1. Clusters 1 & 3: "Niche" Players (Specialists)
This group contains players who are highly specialized in specific areas of the game but may lack versatility in others. The algorithm grouped them into two main distinct "Niche" sub-types:

### Type A: The Explosive Attacker
* **Characteristics:** High stats in Passing, Finishing, and Dribbling. Extremely fast and explosive.
* **Key Attributes:** Pace, Dribbling, Shooting.
* **Example Player:** Vinícius Júnior.


### Type B: The Heavy Defender
* **Characteristics:** High Defensive stats, great Height, and Strength. Generally slower pace.
* **Key Attributes:** Defense, Physicality, Height.
* **Example Player:** Gabriel Magalhães.


---

## 2. Cluster 2: Complete Players (All-Rounders)
This cluster represents the elite "all-around" players. These athletes possess high ratings across almost all major categories, making them versatile and dominant in multiple areas of the pitch.

* **Characteristics:** All attributes are at a high level. They excel particularly in physical attributes such as strength, speed, and height, combined with technical skill.
* **Analysis:** Players like Bellingham often have 78+ in all main rating categories.
* **Example Player:** Jude Bellingham.


---

## 3. Cluster 4: Goalkeepers
The algorithm successfully isolated goalkeepers into their own distinct cluster due to their unique attribute set (Handling, Diving, Reflexes, etc.) which is drastically different from outfield players.

* **Characteristics:** Exclusive Goalkeeper attributes.
* **Key Attributes:** GK Diving, GK Handling, GK Reflexes.
* **Example Player:** Manuel Neuer.

"""


def plot_kmeans():

    df = pd.read_parquet('data/kmeans_df.parquet')


    # Plot
    fig = px.scatter_3d(
        df,
        x='PC1', y='PC2', z='PC3',
        color='Cluster',
        hover_name='name',
        hover_data={
            'position': True,
            'ovr': True,
            'PC1': False,
            'PC2': False,
            'PC3': False,
            'Cluster': False
        },
        color_discrete_map={
            'Cluster 1': '#AED6F1',
            'Cluster 2': '#F5B7B1',
            'Cluster 3': '#A9DFBF',
            'Cluster 4': '#D7BDE2'
        },
        title='K-Means Clustering',
        opacity=1,
        height=800
    )

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family="Arial",
            size=12
        ),
        title_font=dict(
            size=20
        ),
        legend=dict(
            font=dict(size=12)
        ),
        scene=dict(
            xaxis=dict(
                showbackground=False,
                gridcolor="rgba(255,255,255,0.3)",
                zerolinecolor="white",
                title='PC1'
            ),
            yaxis=dict(
                showbackground=False,
                gridcolor="rgba(255,255,255,0.3)",
                zerolinecolor="white",
                title='PC2'
            ),
            zaxis=dict(
                showbackground=False,
                gridcolor="rgba(255,255,255,0.3)",
                zerolinecolor="white",
                title='PC3'
            ),
        )
    )


    fig.update_traces(marker=dict(size=3, line=dict(width=0)))
    st.plotly_chart(fig, width= 'stretch')
    return df


def cluster_df(df: pd.DataFrame):
    cols_to_show = ['name', 'Cluster', 'ovr', 'pac', 'sho', 'pas', 'dri', 'def', 'phy']

    df_exemplos = df.sort_values(['Cluster', 'ovr'], ascending=[True, False]) \
                        .groupby('Cluster') \
                        .head(10)[cols_to_show]

    df_exemplos = df_exemplos.reset_index(drop=True)


    st.dataframe(data=df_exemplos)


def plot_kde(df_viz):

    attributes = ['pac', 'sho', 'pas', 'dri', 'def', 'phy']

    cluster_colors = {
        'Cluster 1': '#440154',
        'Cluster 2': '#21908d',
        'Cluster 3': '#fde725',
        'Cluster 4': '#5e3c99'
    }

    sns.set_theme(style="ticks")

    # 👇 4 linhas x 2 colunas + figura maior
    fig, axes = plt.subplots(4, 2, figsize=(20, 25))
    axes = axes.flatten()

    for i, attr in enumerate(attributes):
        if attr in df_viz.columns:

            sns.kdeplot(
                data=df_viz,
                x=attr,
                hue='Cluster',
                palette=cluster_colors,
                fill=True,
                alpha=0.7,
                linewidth=2.5,
                ax=axes[i],
                common_norm=False,
                warn_singular=False
            )

            axes[i].set_title(
                f'{attr.upper()} Density',
                fontsize=16,
                fontweight='bold',
                color='white'
            )

            axes[i].set_xlabel(attr.upper(), fontsize=14, color='white')
            axes[i].set_ylabel('', fontsize=14, color='white')

            axes[i].tick_params(colors='white', labelsize=12)
            axes[i].set_xlim(left=0)

            axes[i].grid(
                axis='y',
                linestyle='--',
                alpha=0.25,
                color='white'
            )

            axes[i].spines['top'].set_visible(False)
            axes[i].spines['right'].set_visible(False)
            axes[i].spines['left'].set_color('white')
            axes[i].spines['bottom'].set_color('white')

            axes[i].set_facecolor('none')

    # 👇 esconder subplots não usados (2 últimos)
    for j in range(len(attributes), len(axes)):
        axes[j].set_visible(False)

    fig.patch.set_alpha(0)
    plt.tight_layout(pad=3)

    st.pyplot(fig, width= 'stretch')
    plt.close(fig)
