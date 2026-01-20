# AVISOS!
# Este código exibirá as primeiras 20 linhas dos DataFrames apenas para fins de entendimento do usuário, e continuará sendo rodado à medida que o usuário clicar no botão 'OK'.
# O DataFrame final será exportado com as informações completas

# Importando as bibliotecas utilizadas
import pandas as pd
import datetime as dt
import tkinter as tk
from tkinter import ttk, messagebox

# Função para exibir DataFrame em janela
def show_dataframe(df, title="DataFrame", step=""):
    root = tk.Tk()
    root.title(f"📊 Etapa: {step} - {title}" if step else title)
    root.geometry("1200x800")
    root.configure(bg='#f0f0f0')
    
    # Configurar tema moderno
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('Modern.Treeview', background='white', foreground='black', 
                   fieldbackground='white', borderwidth=1, relief='solid')
    style.configure('Modern.Treeview.Heading', background='#4a90e2', foreground='white',
                   font=('Arial', 10, 'bold'))
    
    # Frame principal com bordas arredondadas
    main_frame = tk.Frame(root, bg='#f0f0f0')
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Título da etapa
    title_label = tk.Label(main_frame, text=f"📈 {step}" if step else "📊 Visualização", 
                          font=('Arial', 14, 'bold'), bg='#f0f0f0', fg='#2c3e50')
    title_label.pack(pady=(0, 10))
    
    # Frame para a tabela
    table_frame = tk.Frame(main_frame, bg='white', relief='raised', bd=2)
    table_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
    
    # Criar Treeview com scrollbars
    tree = ttk.Treeview(table_frame, style='Modern.Treeview')
    
    # Scrollbars estilizadas
    v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
    
    # Grid layout
    tree.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    v_scrollbar.grid(row=0, column=1, sticky="ns", pady=10)
    h_scrollbar.grid(row=1, column=0, sticky="ew", padx=10)
    
    table_frame.grid_rowconfigure(0, weight=1)
    table_frame.grid_columnconfigure(0, weight=1)
    
    # Configurar colunas
    tree["columns"] = list(df.columns)
    tree["show"] = "headings"
    
    for col in df.columns:
        tree.heading(col, text=col, anchor="center")
        max_width = max(len(str(col)), df[col].astype(str).str.len().max()) * 8 + 30
        tree.column(col, width=min(max_width, 180), anchor="center")
    
    # Inserir dados com cores alternadas
    for i, (index, row) in enumerate(df.head(20).iterrows()):
        tag = 'evenrow' if i % 2 == 0 else 'oddrow'
        tree.insert("", "end", values=[str(val) for val in row], tags=(tag,))
    
    # Configurar cores das linhas
    tree.tag_configure('evenrow', background='#f8f9fa')
    tree.tag_configure('oddrow', background='white')
    
    # Frame para botões
    button_frame = tk.Frame(main_frame, bg='#f0f0f0')
    button_frame.pack(pady=10)
    
    # Botão OK moderno
    ok_button = tk.Button(button_frame, text="✓ Continuar", command=root.destroy,
                         bg='#27ae60', fg='white', font=('Arial', 11, 'bold'),
                         relief='flat', padx=30, pady=8, cursor='hand2')
    ok_button.pack()
    
    # Info label
    info_label = tk.Label(main_frame, text=f"Exibindo primeiras 20 linhas de {len(df)} registros",
                         font=('Arial', 9), bg='#f0f0f0', fg='#7f8c8d')
    info_label.pack()
    
    root.mainloop()

# Definindo e exibindo o DataFrame inicial que será usado para a análise (Lembrar de deixar o arquivo .csv no mesmo diretório deste script)
df = pd.read_csv('vendas2018_2023.csv')
show_dataframe(df, "DataFrame Inicial - Vendas 2018-2023", "1 - Carregamento dos Dados")
# Exibindo informações gerais sobre o DataFrame (Colunas, Valores Nulos, Tipos)
df.info()

# Vamos criar um novo Data Frame apenas com as colunas necessárias para nossa análise RFM
df_analise_vendas = df [['data_venda', 'cliente', 'quantidade', 'valor_venda' ]]
show_dataframe(df_analise_vendas, "DataFrame Análise Vendas", "2 - Seleção de Colunas")
# Exibindo as informações gerais do novo DataFrame df_analise_vendas
df_analise_vendas.info()

# Perceba que, a coluna data_venda está como object, vamos convertela para datetime
df_analise_vendas['data_venda'] = pd.to_datetime(df_analise_vendas['data_venda'])
# Exibindo novamente as informações do df_analise_vendas, vemos agora que a coluna está no formato correto
df_analise_vendas.info()

# Para realizar a análise RFM, vamos agrupar os dados por cliente, calcular os valores para cada um dos indicadores e criar um novo DataFrame com esses valores.
# Antes disso, definiremos um valor de referência para calcularmos há quantos dias o cliente fez a última compra (Recência = data_referencia - última_compra_cliente)
data_referencia = (df_analise_vendas['data_venda'].max() + dt.timedelta(days=1)).date() # Perceba que a função .date() já transforma a variável data_referencia no formato datetime. Esse formato será importante, pois nos cálculos mais adiante os dados terão que estar no mesmo formato
data_referencia 

# Agora vamos criar um DataFrame onde agruparemos os clientes por quantidade de produtos comprada, valor total da venda e a data da venda
df_agregado_cliente = df_analise_vendas.groupby('cliente').agg({
    'quantidade': 'sum', 
    'valor_venda': 'sum', 
    'data_venda': ['count', lambda x: (data_referencia - x.max().date()).days]
})
# Achatando as colunas multi-nível
df_agregado_cliente.columns = ['total_produtos_comprados', 'monetario', 'frequencia', 'recencia']
# Resetando o índice para transformar 'cliente' em coluna
df_agregado_cliente = df_agregado_cliente.reset_index()
# Reordenando as colunas para ficar mais organizado
df_agregado_cliente = df_agregado_cliente[['cliente', 'recencia', 'frequencia', 'monetario', 'total_produtos_comprados']]
# Exibindo o novo DataFrame
show_dataframe(df_agregado_cliente, "DataFrame Agregado por Cliente", "3 - Agregação por Cliente")

# Com esse novo DataFrame, vamos agora fazer os agrupamentos por Recência, Frequência e Monetário
# Recência
r_groups = pd.qcut(df_agregado_cliente['recencia'], q=5, labels=range(1,6))
r_groups.value_counts()
df_agregado_cliente['R'] = r_groups # Vamos adicionar a coluna 'R', 'F' e 'M' ao nosso df
#Frequência
f_groups = pd.qcut(df_agregado_cliente['frequencia'], q=5, labels=range(1,6))
f_groups.value_counts()
df_agregado_cliente['F'] = f_groups
# Monetário (Para definirmos o range deste grupo, vamos ver a distribuição do df_agregado_cliente)
print(df_agregado_cliente['monetario'].describe())
m_groups = pd.cut(df_agregado_cliente['monetario'], bins=[0, 25000, 35000, 42000, 55000, 151164], labels=[1, 2, 3, 4, 5])
m_groups.value_counts()
df_agregado_cliente['M'] = m_groups
# Veja como ele ficou!
show_dataframe(df_agregado_cliente, "DataFrame com Grupos RFM", "4 - Criação dos Grupos RFM")

# Podemos ver usando o info() as informações gerais do df_agregado_cliente e vemos que as colunas R, F, M estão no formato category, então iremos converter em int
df_agregado_cliente ['R'] = df_agregado_cliente['R'].astype(int)
df_agregado_cliente ['F'] = df_agregado_cliente['F'].astype(int)
df_agregado_cliente ['M'] = df_agregado_cliente['M'].astype(int)

# Agora vamos para a análise propriamente dita. 
# O primeiro passo é definirmos o score e a segmentação do cliente. 
df_agregado_cliente['RFM_Score'] = df_agregado_cliente['R'] + df_agregado_cliente['F'] + df_agregado_cliente['M'] # O score é a soma dos valores de RFM
df_agregado_cliente['RFM_Segment'] = df_agregado_cliente['R'].astype(str) + df_agregado_cliente['F'].astype(str) + df_agregado_cliente['M'].astype(str) # A segmentação é a junção dos valores RFM
# Interpretação prática da segmentação: 5XX: Clientes recentes ativos; X5X: Clientes frequentes; XX5: Clientes de alto valor

# Vamos agora criar uma função para categorizar os clientes de acordo com o seu score RFM
def classify_by_score(score):
    if score >= 11:
        return 'Alto Valor'
    elif score >= 7:
        return 'Médio Valor'
    else:
        return 'Baixo Valor'
# Faremos o mesmo para categorizar os clientes agora pela segmentação 
def classify_by_segment(segment):
    r, f, m = int(segment[0]), int(segment[1]), int(segment[2])
    if r >= 4 and f >= 4 and m >= 4:
        return 'Campeões'
    elif r >= 3 and f >= 3 and m >= 3:
        return 'Clientes Fiéis'
    elif r >= 3 and f >= 1 and m >= 3:
        return 'Clientes Potenciais'
    elif r >= 3 and f >= 1 and m >= 1:
        return 'Novos Clientes'
    elif r >= 1 and f >= 1 and m >= 1:
        return 'Clientes em Risco'
    else:
        return 'Perdidos'
    
# De acordo com as funções acima, vamos classificar os clientes de pelo score e pela segmentação 
df_agregado_cliente['Classe_Score'] = df_agregado_cliente['RFM_Score'].apply(classify_by_score)
df_agregado_cliente['Classe_Segmento'] = df_agregado_cliente['RFM_Segment'].apply(classify_by_segment)
# Perceba que transformamos os números das colunas Classe_Score e Classe_Segmento em String. Então nosso DataFrame fica assim:
show_dataframe(df_agregado_cliente, "DataFrame com Classificações", "5 - Classificação dos Clientes")

# Exibindo as distribuições por classificação
print("Distribuição por Classe Score:")
print(df_agregado_cliente['Classe_Score'].value_counts())
print("\nDistribuição por Classe Segmento:")
print(df_agregado_cliente['Classe_Segmento'].value_counts())

# Pausar para mostrar as distribuições
messagebox.showinfo("Distribuições", "Verifique o console para ver as distribuições por classe. Clique OK para continuar.")

# Como parte da análise, para cada classe de cliente temos uma tomada de decisão, então definiremos uma função que determina a decisão baseada na segmentação
def acao_por_segmento(classe):
    if classe == 'Campeões':
        return 'Priorizar: Oferecer benefícios exclusivos e programas VIP para maximizar retenção e valor.'
    elif classe == 'Clientes Fiéis':
        return 'Manter: Enviar comunicações regulares e ofertas de upsell para fortalecer o relacionamento.'
    elif classe == 'Clientes Potenciais':
        return 'Converter: Incentivar compras mais frequentes com promoções personalizadas e cross-sell.'
    elif classe == 'Novos Clientes':
        return 'Integrar: Bem-vindo e orientações para construir lealdade desde o início.'
    elif classe == 'Clientes em Risco':
        return 'Reativar: Campanhas de win-back com descontos e lembretes para recuperar interesse.'
    else:
        return 'Avaliar: Considerar se vale a pena investir em reativação ou focar em segmentos mais promissores.'
# Vamos incluir a coluna 'Ação' no nosso DataFrame
df_agregado_cliente['Acao'] = df_agregado_cliente['Classe_Segmento'].apply(acao_por_segmento)

# Por fim, podemos exportar o DataFrame para um arquivo CSV para utilizar em relatórios ou apresentações
df_agregado_cliente.to_csv('df_agregado_cliente.csv', index=False)

# Exibindo o DataFrame final
show_dataframe(df_agregado_cliente, "DataFrame Final com Ações", "6 - Resultado Final")

# Fim do código!!
messagebox.showinfo("Concluído", "Análise RFM finalizada! Arquivo CSV exportado com sucesso.")
print("Análise RFM concluída!")
