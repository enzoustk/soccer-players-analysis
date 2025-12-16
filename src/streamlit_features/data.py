import ast
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

def data_cleaning(df: pd.DataFrame):

    st.subheader('Data Cleaning, Transformation and Feature Engineering')

    with st.echo():
        df = pd.read_csv('data/EAFC26-Men_raw.csv')
        df.head(10)
    st.dataframe(data=df.head(10))

    st.code('df.columns', language='python')
    st.text(df.columns)

    with st.echo():
        # Checking Missing Counts
        missing_counts = df.isnull().sum()
        print('Missing Values:')
        print(missing_counts[missing_counts > 0])
    st.write('Missing Values:')
    st.text(missing_counts[missing_counts > 0])

    with st.echo():
        # Drop Useless Columns
        df = df.drop(
            columns=[
                "ID", "card", "url",
                "GENDER", "play style"
            ])
        
    with st.echo():
        gk_cols = [
            "GK Diving", "GK Handling", "GK Kicking",
            "GK Positioning", "GK Reflexes"
            ]

    with st.echo():
        df[gk_cols] = df[gk_cols].fillna(0)

    with st.echo():
        
        # Mapeamento manual das posições
        sector_map = {
            'GK': 'goalie',

            'CB': 'defense',
            'LB': 'defense',
            'RB': 'defense',
            
            'CDM': 'midfielder',
            'CM': 'midfielder',
            'CAM': 'midfielder',
            'RM': 'midfielder',
            'LM': 'midfielder',

            'ST': 'forward',
            'LW': 'forward',
            'RW': 'forward'
        }

    with st.echo():
        df['sector'] = df['Position'].map(sector_map)

    with st.echo():
        def count_positions(value):
            if isinstance(value, str):
                try:
                    # str -> list
                    positions = ast.literal_eval(value)
                    return len(positions)
                except:
                    return 0
            else:
                return 0

    with st.echo():
        df['versatility'] = df['Alternative positions'].apply(count_positions)

    with st.echo():
        df['Height'] = df['Height'].str.extract(r'(\d+)\s*cm').astype(int)
        df['Weight'] = df['Weight'].str.extract(r'(\d+)\s*kg').astype(int)

        df = df.rename(columns={'Height': 'Height(cm)', 'Weight': 'Weight(kg)'})

    with st.echo():
        df['Preferred foot'] = (df['Preferred foot'] == "Right").astype(int)

    with st.echo():
        import re
        import unicodedata
        
        def clean_column(col):
            col = str(col)
            col = unicodedata.normalize('NFKD', col).encode('ASCII', 'ignore').decode('utf-8')
            col = col.lower()
            col = col.replace(" ", "_")
            col = re.sub(r'[^a-z0-9_]', '', col)

            return col

    with st.echo():
        df.columns = [clean_column(c) for c in df.columns]

    with st.echo():
        df = pd.get_dummies(
            data=df,
            columns=['sector'],
            dtype=int
        )

    with st.echo():
        nao_goleiro = df['sector_goalie'] != 1

        # Offensive Player Flag
        df['offensive'] = (
            ((df['sho'] > df['def'] * 1.2) | (df['dri'] > df['def'] * 1.2)) & nao_goleiro
        ).astype(int)

        # Defensive Player Flag
        df['defensive'] = (
            (df['def'] > df['sho'] * 1.2) & (df['def'] > df['dri'] * 1.2) & nao_goleiro
        ).astype(int)

        # All Around Player Flag
        df['all_around'] = (
            (df['offensive'] == 0) & (df['defensive'] == 0) & nao_goleiro
        ).astype(int)

    with st.echo():
        df.head()
    st.dataframe(data=df.head(5))

    with st.echo():
        # PKL para salvar os dados
        df.to_pickle('data/df_cleaned.pkl')

        # CSV para quem quiser ler rapidamente
        df.to_csv('data/df_cleaned.csv', index=False)

def eda(df: pd.DataFrame):
    try:
        plt.style.use('seaborn-v0_8-darkgrid')
    except:
        try:
            plt.style.use('seaborn-darkgrid')
        except:
            plt.style.use('default')


    sns.set_palette(['#1f77b4'])

    plt.rcParams['figure.figsize'] = (12, 6)
    plt.rcParams['font.size'] = 10
    pd.set_option('display.max_columns', None)
    
    bg_color = '#0E1117'
    text_color = '#FAFAFA'
    bar_color = '#AED6F1'
    edge_color = '#FAFAFA' 
    grid_color = '#404040'

    with st.echo():
        print(f"Total players: {df.shape[0]:,}")
        print(f"Total features: {df.shape[1]:,}")
    

    st.text(f"Total players: {df.shape[0]:,}")
    st.text(f"Total features: {df.shape[1]:,}")

    with st.echo():
        # Entender Features Principais
        main_attributes = [
            'ovr', 'pac', 'sho',
            'pas', 'dri', 'def',
            'phy', 'age',
            'heightcm', 'weightkg',
            'weak_foot', 'skill_moves'
        ]
    
    with st.echo():
        df[main_attributes].describe()
   
    st.dataframe(df[main_attributes].describe())

    st.divider()
    st.subheader('Start Plotting')
    
    # Distribution of Features
    with st.echo():
        fig, axes = plt.subplots(6, 2, figsize=(10, 20), facecolor=bg_color)
        axes = axes.ravel()

        for idx, attr in enumerate(main_attributes):
            if idx >= len(axes): 
                break
            
            axes[idx].set_facecolor(bg_color)

            axes[idx].hist(
                df[attr].dropna(), bins=30,
                color=bar_color, 
                edgecolor=bg_color, 
                linewidth=1.2
            )
            
            axes[idx].set_title(f'{attr.title()} Distribution', fontsize=12, fontweight='bold', color=text_color)
            axes[idx].set_xlabel(attr, fontsize=10, fontweight='bold', color=text_color)
            axes[idx].set_ylabel('Frequência', fontsize=10, fontweight='bold', color=text_color)
            
            axes[idx].spines['bottom'].set_linewidth(2)
            axes[idx].spines['bottom'].set_color(text_color)
            axes[idx].spines['left'].set_linewidth(2)
            axes[idx].spines['left'].set_color(text_color)
            axes[idx].spines['top'].set_visible(False)
            axes[idx].spines['right'].set_visible(False)
            
            axes[idx].tick_params(axis='both', colors=text_color, width=2)
            axes[idx].grid(True, linestyle='--', alpha=0.3, color=text_color)

        for i in range(len(main_attributes), len(axes)):
            axes[i].set_facecolor(bg_color) 
            axes[i].axis('off')

        plt.tight_layout()
        
        st.pyplot(fig, transparent=True)
    
    with st.echo():
        corr_matrix = df[main_attributes].corr()

        fig, ax = plt.subplots(figsize=(10, 8))
        
        fig.patch.set_facecolor('none')
        ax.patch.set_facecolor('none')
        
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

        sns.heatmap(
            corr_matrix, 
            mask=mask, 
            annot=True, 
            fmt='.2f', 
            cmap='coolwarm', 
            center=0, 
            square=True, 
            linewidths=1, 
            linecolor='#0e1117',
            cbar_kws={"shrink": 0.8},
            ax=ax 
        )

        ax.set_title(
            'Feature Matrix', 
            fontsize=14, fontweight='bold', pad=20, color='white'
        )
        
        plt.xticks(color='white', fontsize=10)
        plt.yticks(color='white', fontsize=10)

        cbar = ax.collections[0].colorbar
        cbar.ax.yaxis.set_tick_params(color='white')
        plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white') 

        plt.tight_layout()
        
        st.pyplot(fig)
    
    with st.echo():
        all_numeric = df.select_dtypes(include=[np.number]).columns
        
        corr_with_ovr = (
            df[all_numeric]
            .corrwith(df['ovr'])
            .abs()
            .sort_values(ascending=False)
            .drop(['ovr', 'rank'], errors='ignore') 
        )

        fig, ax = plt.subplots(figsize=(10, 6), facecolor=bg_color)
        ax.set_facecolor(bg_color)

        ax.bar(corr_with_ovr.index, corr_with_ovr.values, 
                color=bar_color,
                edgecolor=bg_color,
                linewidth=1.5,
                width=0.7)

        ax.set_title("OVR Feature Correlation", fontsize=16, fontweight='bold', color=text_color)
        ax.set_ylabel("Correlation", fontsize=12, fontweight='bold', color=text_color)

        ax.spines['bottom'].set_linewidth(2)
        ax.spines['bottom'].set_color(text_color)
        ax.spines['left'].set_linewidth(2)
        ax.spines['left'].set_color(text_color)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        ax.tick_params(width=2, colors=text_color)
        ax.set_xticklabels(corr_with_ovr.index, rotation=45, ha='right', fontsize=10, fontweight='bold', color=text_color)
        
        ax.grid(axis='x', color=grid_color, linestyle='-', linewidth=0.8, alpha=0.5)
        
        ax.grid(axis='y', color=grid_color, linestyle='--', alpha=0.3)

        ax.set_axisbelow(True) 

        plt.tight_layout()
        st.pyplot(fig, transparent=False)

    with st.echo():
        position_counts = df['position'].value_counts()

        fig, ax = plt.subplots(figsize=(10, 8), facecolor=bg_color)
        ax.set_facecolor(bg_color)

        ax.barh(
            position_counts.index, position_counts.values, 
            color=bar_color,
            edgecolor=bg_color,
            linewidth=1.5, 
            height=0.7
        )

        ax.set_title('Position Distribution', fontsize=16, fontweight='bold', color=text_color)
        ax.set_xlabel('Total Players', fontsize=12, fontweight='bold', color=text_color)
        ax.set_ylabel('Position', fontsize=12, fontweight='bold', color=text_color)

        ax.invert_yaxis()

        ax.spines['bottom'].set_linewidth(2)
        ax.spines['bottom'].set_color(text_color)
        ax.spines['left'].set_linewidth(2)
        ax.spines['left'].set_color(text_color)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        ax.tick_params(width=2, colors=text_color)

        ax.grid(axis='x', color=grid_color, linestyle='--', linewidth=0.8, alpha=0.5)
        
        ax.grid(axis='y', visible=False)

        ax.set_axisbelow(True)

        plt.tight_layout()
        st.pyplot(fig, transparent=False)

    with st.echo():
        counts = df['versatility'].value_counts() 

        fig, ax = plt.subplots(figsize=(10, 6), facecolor=bg_color)
        ax.set_facecolor(bg_color)

        bars = ax.bar(counts.index, counts.values, 
                    color=bar_color,
                    edgecolor=bg_color, 
                    linewidth=1.5,
                    width=0.7)

        ax.set_title('Versatility Distribution', fontsize=16, fontweight='bold', color=text_color)
        ax.set_xlabel('Versatility', fontsize=12, fontweight='bold', color=text_color)
        ax.set_ylabel('Players', fontsize=12, fontweight='bold', color=text_color)

        ax.spines['bottom'].set_linewidth(2)
        ax.spines['bottom'].set_color(text_color)
        ax.spines['left'].set_linewidth(2)
        ax.spines['left'].set_color(text_color)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        ax.tick_params(width=2, colors=text_color)
        ax.grid(axis='y', linestyle='--', alpha=0.3, color=grid_color)
        ax.grid(axis='x', visible=False)
        ax.set_axisbelow(True)

        plt.tight_layout()
        st.pyplot(fig, transparent=False)

    st.subheader('Run Linear Regression')
    with st.echo():
        # Regressão Linear Simples
        numeric_df = df.select_dtypes(include=[np.number])

        X = numeric_df.drop(['ovr', 'rank'], axis=1, errors='ignore')
        y = numeric_df['ovr']

        X = X.fillna(0)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = LinearRegression()
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)

        print(f"R²: {r2:.4f}")
        print(f"MSE: {mse:.4f}")
    
    st.text(f"R²: {r2:.4f}")
    st.text(f"MSE: {mse:.4f}")

    with st.echo():
        dot_color = '#AED6F1'
        line_color = '#E74C3C'

        fig, ax = plt.subplots(figsize=(10, 6), facecolor=bg_color)
        ax.set_facecolor(bg_color)

        ax.scatter(
            y_test, y_pred, 
            color=dot_color, 
            edgecolor=bg_color,
            s=60,
            alpha=0.8, 
            linewidth=0.8,
            zorder=3
        ) 


        min_val = min(y_test.min(), y_pred.min())
        max_val = max(y_test.max(), y_pred.max())
        
        ax.plot([min_val, max_val], [min_val, max_val], 
                color=line_color, 
                linestyle='--', 
                linewidth=2.5, 
                label='Perfect Prediction',
                zorder=2
            )

        ax.set_title(f'Real OVR vs Forecast', fontsize=16, fontweight='bold', color=text_color)
        ax.set_xlabel(f'Real', fontsize=12, fontweight='bold', color=text_color)
        ax.set_ylabel(f'Forecast', fontsize=12, fontweight='bold', color=text_color)
        
        legend = ax.legend(frameon=False, labelcolor=text_color)
        
        ax.spines['bottom'].set_linewidth(2)
        ax.spines['bottom'].set_color(text_color)
        ax.spines['left'].set_linewidth(2)
        ax.spines['left'].set_color(text_color)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        ax.tick_params(width=2, colors=text_color)

        ax.grid(axis='both', linestyle='--', alpha=0.3, color=grid_color)
        
        ax.set_axisbelow(True)

        plt.tight_layout()
        st.pyplot(fig, transparent=False)