import pandas as pd
from glob import glob
import matplotlib as mpl
import matplotlib.pyplot as plt

# ggplot, seaborn, fivethirtyeight
mpl.style.use('seaborn') 

files = glob("*.xlsx")

df = pd.read_excel(files[0])
# print(df.head())

# print(df['Tipo'].unique())
# print(df['Tipo'].value_counts())

# values = df['Tipo'].value_counts().to_list()
# types = list(df['Tipo'].unique())
# # df['Tipo'].value_counts().plot(kind='barh')
# plt.figure(figsize=(12, 8))
# plt.barh(types, values)
# # plt.grid(alpha=0.5, which='major', axis='both')
# # plt.yticks(fontsize=17)
# for x, y in zip(values, range(len(values))):
#     plt.text(x, y, values[y], fontsize=17)

# # orientation : {'landscape', 'portrait'}
# plt.savefig('type-of-credits.png', orientation='landscape')

# print(df['Colaborador'].value_counts())
print(df[df['Colaborador'] == ' '])

def plot_by_column_agg(column_name, plot_type='seaborn'):
    mpl.style.use(plot_type) 
    values = df[column_name].value_counts().to_list()
    types = list(df[column_name].unique())
    # df['Tipo'].value_counts().plot(kind='barh')
    # plt.figure(figsize=(12, 8))
    plt.barh(types, values)
    # plt.grid(alpha=0.5, which='major', axis='both')
    # plt.yticks(fontsize=17)
    for x, y in zip(values, range(len(values))):
        plt.text(x, y, values[y], fontsize=12)
    
    plt.savefig(f'{column_name}.png', orientation='landscape')

plot_by_column_agg('Estado', 'ggplot')

















































