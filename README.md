# Análise de Jogadores FIFA 26 

Este repositório contém o código-fonte e a documentação do **Projeto da Unidade III** da disciplina **IMD3003 - Aprendizado de Máquina Não-Supervisionado** (2025.2) Ministrada pelo professor **Silvan Ferreira**.

O projeto aplica técnicas de clusterização e análise exploratória para identificar perfis de jogadores e padrões ocultos, simulando cenários para o **FIFA 26**.



## Objetivos do Projeto
Conforme as diretrizes da disciplina, este trabalho abrange:

1.  **Pré-processamento:** Seleção de atributos relevantes, tratamento de dados faltantes e normalização.
2.  **Aprendizado Não-Supervisionado:** Aplicação e comparação de pelo menos dois algoritmos de clusterização.
3.  **Visualização:** Geração de gráficos e projeções (2D/3D) para interpretar os agrupamentos.
4.  **Entendimento dos Resultados:** Interpretação dos clusters no contexto de futebol (ex: "Jovens Promessas", "Veteranos de Elite").

## Estrutura do Repositório

Os arquivos estão organizados para refletir o fluxo de trabalho de Ciência de Dados exigido na avaliação:

| Arquivo/Pasta | Descrição |
| :--- | :--- |
| `data/` | Contém os datasets brutos e processados. |
| `plots/` | Visualizações geradas para o relatório e apresentação. |
| `data_cleaning.ipynb` | **Pré-processamento:** Limpeza, padronização e normalização dos dados. |
| `eda.ipynb` | **EDA:** Análise Exploratória para entender distribuições e correlações iniciais. |
| `model.ipynb` | **Modelagem (Principal):** Implementação de algoritmos de clusterização (ex: Gaussian Mixture Models). |
| `non_linear_model.ipynb` | **Modelagem (Comparativa):** Testes com abordagens não-lineares ou algoritmos alternativos. |
| `gmm_resumo_*.md` | **Resultados:** Resumos interpretativos dos clusters gerados (6 e 10 grupos). |
| `helpers.py` | Funções auxiliares e utilitários de código. |

## 🛠️ Metodologia e Tecnologias

Utilizamos **Python** e as bibliotecas padrão de Data Science (`pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`).

### Algoritmos Aplicados
1.  **Gaussian Mixture Models (GMM):** Utilizado para modelagem probabilística dos clusters.
2.  **[Inserir Nome do 2º Algoritmo]:** (Ex: K-Means, DBSCAN ou Hierarchical Clustering) utilizado para comparação.
3.  **[Opcional - Redução de Dimensionalidade]:** (Ex: PCA, t-SNE) utilizado para visualização dos grupos.

## 🚀 Instalação e Execução

Para reproduzir as análises localmente:

1.  Clone o repositório:
    ```bash
    git clone [https://github.com/enzoustk/fifa26-players-analysis.git](https://github.com/enzoustk/fifa26-players-analysis.git)
    cd fifa26-players-analysis
    ```

2.  Instale as dependências necessárias:
    ```bash
    pip install pandas numpy matplotlib seaborn scikit-learn jupyter
    ```

3.  Execute o Jupyter Notebook e abra os arquivos na ordem sugerida (Cleaning -> EDA -> Models):
    ```bash
    jupyter notebook
    ```
