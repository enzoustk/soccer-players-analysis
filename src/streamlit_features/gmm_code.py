import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px



umap_code = """
df = pd.read_pickle('data/df_cleaned.pkl')
numeric_df = df.select_dtypes(include=[np.number])
numeric_df = numeric_df.drop(['rank', 'ovr'], axis=1, errors='ignore')

# Scale
X = numeric_df.fillna(0)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Params chosen by trial and error
N_NEIGHBORS = 50
MIN_DIST = 0.15      

umap_3d = UMAP(
    n_components=3, 
    n_neighbors=N_NEIGHBORS,
    min_dist=MIN_DIST,
    metric='euclidean',
    n_jobs=-1
)

projection_3d = umap_3d.fit_transform(X_scaled)
"""

gmm_code = """# Cluster range to test
n_components_range = range(2, 21)
bic_scores = []
aic_scores = []

for n in n_components_range:
    gmm_test = GaussianMixture(n_components=n, n_init=5, random_state=42)
    gmm_test.fit(projection_3d)
    
    # Armazena as métricas (quanto menor, melhor)
    bic_scores.append(gmm_test.bic(projection_3d))
    aic_scores.append(gmm_test.aic(projection_3d))


# Training Model
N_COMPONENTS = 7
gmm = GaussianMixture(n_components=N_COMPONENTS, n_init=10, random_state=42)
cluster_labels = gmm.fit_predict(projection_3d)

# 3. Calcular a probabilidade de certeza
probs = gmm.predict_proba(projection_3d)
certainty = probs.max(axis=1)

df['cluster_gmm'] = cluster_labels.astype(str)
df_viz['cluster_conf'] = certainty
"""

gmm_report = """
* **Cluster 0 (Defensive Midfielder):** The midfield balance. `midfielder` (+165%) and `all_around` (+137%) players who prioritize marking (`interceptions` +35%) and safe ball distribution.

* **Cluster 1 (Striker):** The firepower. A unified group of finishers (`sector_forward` +460%) with a terminal focus on `finishing` (+41%) and `volleys` (+38%), ignoring defensive tasks.

* **Cluster 2 (Creative Midfielder):** The offensive engine. Midfielders and wingers (`offensive` +178%) defined by refined technique (`versatility` +74%, `skill_moves` +29%) and dribbling ability.

* **Cluster 3 (Left-Footed Defender):** The rare asset. Center-backs and left-backs (`sector_defense` +199%) isolated by their footedness (`preferred_foot` -100%), essential for the geometry of build-up play.

* **Cluster 4 (Goalkeeper):** The last line. Goalkeeping attributes ~800% above average. A geometrically isolated group.

* **Cluster 5 (Stopper):** The wall. Physical defenders (`defensive` +850%) who forgot `all_around` technique to focus purely on play disruption and physical strength.

* **Cluster 6 (Right-Footed Defender):** The modern defense. Right-backs and technical center-backs (`all_around` +134%) who combine strong marking with mobility and support play.
"""

def plot_umap():
    df = pd.read_parquet('data/df_umap.parquet')
    fig = px.scatter_3d(
        df,
        x='UMAP1', y='UMAP2', z='UMAP3',
        color='position',
        hover_name='name',
        hover_data={
            'position': True,
            'ovr': True,
            'age': True,
            'UMAP1': False,
            'UMAP2': False,
            'UMAP3': False
        },
        opacity=0.7,
        height=800,
        title="3d UMAP by Dominant Position"
    )

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        scene=dict(
            xaxis=dict(
                showbackground=False,
                gridcolor='rgba(255,255,255,0.25)'
            ),
            yaxis=dict(
                showbackground=False,
                gridcolor='rgba(255,255,255,0.25)'
            ),
            zaxis=dict(
                showbackground=False,
                gridcolor='rgba(255,255,255,0.25)'
            ),
        )
    )

    fig.update_traces(marker=dict(size=3))
    st.plotly_chart(fig, width= 'stretch')


def plot_gmm():
    df = pd.read_parquet('data/gmm_df.parquet')
    fig = px.scatter_3d(
        df,
        x='UMAP1', y='UMAP2', z='UMAP3',
        color='cluster_gmm',
        hover_name='name',
        hover_data=['position', 'cluster_conf', 'ovr'],
        title=f'Gaussian Model over 7-Component Clustering',
        opacity=0.75,
        height=650
    )

    # 🎨 Ajuste para modo noturno do Streamlit
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',   # fundo transparente
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            color='white',
            family='Arial',
            size=13
        ),
        scene=dict(
            xaxis=dict(
                title='UMAP 1',
                showgrid=True,
                gridcolor='rgba(255,255,255,0.15)',
                zeroline=False,
                color='white'
            ),
            yaxis=dict(
                title='UMAP 2',
                showgrid=True,
                gridcolor='rgba(255,255,255,0.15)',
                zeroline=False,
                color='white'
            ),
            zaxis=dict(
                title='UMAP 3',
                showgrid=True,
                gridcolor='rgba(255,255,255,0.15)',
                zeroline=False,
                color='white'
            ),
            aspectmode='data',
            bgcolor='rgba(0,0,0,0)'
        ),
        legend_title_text='Cluster',
        legend=dict(
            bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        ),
        margin=dict(l=0, r=0, b=0, t=50)
    )

    fig.update_traces(
        marker=dict(
            size=3,
            line=dict(width=0)
        )
    )

    st.plotly_chart(fig, width= 'stretch')
    return df


def top_gmm_players(df: pd.DataFrame):
    cols_show = ['name', 'position', 'ovr', 'pac', 'sho', 'pas', 'dri', 'def', 'phy', 'cluster_conf']
    df['cluster_sort'] = df['cluster_gmm'].astype(int)
    df_sorted = df.sort_values(by=['cluster_sort', 'ovr'], ascending=[True, False])


    df_top_examples = df_sorted.groupby('cluster_sort').head(5)[cols_show + ['cluster_gmm']].reset_index(drop=True)
    st.dataframe(df_top_examples)    

import plotly.express as px
import pandas as pd
import streamlit as st
import numpy as np

def cluster_feature_matrix(df: pd.DataFrame):

    # 1. Selecionar colunas numéricas
    atributos_disponiveis = (
        df.select_dtypes(include='number')
          .columns
          .drop('cluster_gmm', errors='ignore')
    )

    # 2. Cálculo
    cluster_means = df.groupby('cluster_gmm')[atributos_disponiveis].mean()
    global_means = df[atributos_disponiveis].mean()
    pct_diff_matrix = ((cluster_means - global_means) / global_means) * 100
    df_report = pct_diff_matrix.T.round(1)
    df_report.columns = df_report.columns.astype(int)
    df_report = df_report.sort_index(axis=1)


    # Lógica de Filtro

    if df_report.empty:
        st.warning("Nenhum atributo atende a esse critério. Diminua o filtro.")
        return

    # --- 3. HEATMAP ---
    # Altura dinâmica
    dynamic_height = max(400, len(df_report) * 35)

    # Nota: text_auto=False porque vamos desenhar o texto manualmente nas anotações
    fig = px.imshow(
        df_report,
        labels=dict(x='Cluster', y='Atributo', color='Diff (%)'),
        x=df_report.columns.astype(str),
        y=df_report.index,
        text_auto=False, 
        aspect='auto',
        color_continuous_scale='RdBu_r',
        color_continuous_midpoint=0,
        range_color=[-60, 60]
    )

    # --- LÓGICA DE COR DO TEXTO VIA ANOTAÇÕES ---
    # Esta é a única forma segura de ter cores de texto diferentes por célula no Heatmap
    annotations = []
    limit = 25
    
    # Iteramos sobre as linhas e colunas do dataframe filtrado
    for y in df_report.index:
        for x in df_report.columns:
            val = df_report.loc[y, x]
            
            # Define cor baseada no valor
            font_color = 'black' if abs(val) < limit else 'white'
            
            annotations.append(dict(
                x=str(x), 
                y=y,
                text=f"{val:.0f}%",
                showarrow=False,
                font=dict(color=font_color, size=12)
            ))

    # --- 4. ESTILO ---
    fig.update_layout(
        height=dynamic_height,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        annotations=annotations, # Adiciona as etiquetas manuais aqui
        font=dict(color='white', size=13),
        xaxis=dict(side='top', tickfont=dict(color='white')),
        yaxis=dict(tickfont=dict(color='white')),
        margin=dict(l=20, r=20, t=30, b=20),
        coloraxis_colorbar=dict(
            title=dict(text='Dif. (%)', font=dict(color='white')),
            tickfont=dict(color='white')
        )
    )

    st.plotly_chart(fig, width= 'stretch')
    