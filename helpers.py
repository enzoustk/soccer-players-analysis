import re
import ast
import unicodedata

def count_positions(value):
    if isinstance(value, str):
        try:
            # Converte string para lista real
            positions = ast.literal_eval(value)
            return len(positions)
        except:
            return 0
    else:
        return 0

def clean_column(col):
    # transformar em string (por segurança)
    col = str(col)

    # remover acentos
    col = unicodedata.normalize('NFKD', col).encode('ASCII', 'ignore').decode('utf-8')

    # minúsculas
    col = col.lower()

    # substituir espaços por _
    col = col.replace(" ", "_")

    # remover qualquer caractere que não seja letra, número ou _
    col = re.sub(r'[^a-z0-9_]', '', col)

    return col
