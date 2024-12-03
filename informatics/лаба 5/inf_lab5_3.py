import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


data = pd.read_csv("D:\ИТМО\informatics\лаба 5\inf_lab5_3_csv.csv", sep=';')
data['date'] = pd.to_datetime(data['date'], format='%d.%m.%Y')

melted_data = pd.melt(
    data,
    id_vars=['date'],
    value_vars=['open', 'max', 'min', 'close'],
    var_name='тип',
    value_name='значение'
)

plt.figure(figsize=(12, 6))
ax = sns.boxplot(x='date', y='значение', hue='тип', data=melted_data)

plt.title("Диаграмма ящиков с усами", fontsize=16)
plt.xlabel("Дата", fontsize=12)
plt.ylabel("Цена", fontsize=12)
plt.xticks(rotation=30)
plt.legend(title="тип", loc="upper right")
plt.tight_layout()
plt.show()
