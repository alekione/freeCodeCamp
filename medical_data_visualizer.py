import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1: Import data
df = pd.read_csv('medical_examination.csv')

# 2: Add 'overweight' column (BMI = weight (kg) / height (m)^2)
df['overweight'] = ((df.weight / ((df.height / 100) ** 2)) > 25).astype(int)

# 3: Normalize data by making 0 always good and 1 always bad for cholesterol and gluc
# Normalize cholesterol (if cholesterol is 1, set to 0; if cholesterol is greater than 1, set to 1)
df.loc[df['cholesterol'] == 1, 'cholesterol'] = 0
df.loc[df['cholesterol'] > 1, 'cholesterol'] = 1

# Normalize glucose (if gluc is 1, set to 0; if gluc is greater than 1, set to 1)
df.loc[df['gluc'] == 1, 'gluc'] = 0
df.loc[df['gluc'] > 1, 'gluc'] = 1

# 4: Draw Categorical Plot
def draw_cat_plot():
    # 5: Create DataFrame for the cat plot using pd.melt with values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'
    df_cat = df.melt(id_vars=['cardio'], value_vars=['cholesterol', 'gluc', 'alco', 'active', 'overweight', 'smoke'])

    # 6: Group and reformat the data to split it by 'cardio' and show the counts of each feature
    df_cat = df_cat.groupby(['cardio', 'variable', 'value'], as_index=False).size().rename(columns={"size": "total"})

    # 7: Draw the categorical plot with sns.catplot
    g = sns.catplot(x="variable", y="total", hue="value", col="cardio", data=df_cat, kind="bar")
    fig = g.fig

    # 8: Save the figure
    fig.savefig('catplot.png')

    return fig

# 10: Draw Heat Map
def draw_heat_map():
    # 11: Clean the data by filtering out incorrect patient segments
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) &
                 (df['height'] >= df['height'].quantile(0.025)) &
                 (df['height'] <= df['height'].quantile(0.975)) &
                 (df['weight'] >= df['weight'].quantile(0.025)) &
                 (df['weight'] <= df['weight'].quantile(0.975))]

    # 12: Calculate the correlation matrix
    corr = df_heat.corr()

    # 13: Generate a mask for the upper triangle of the correlation matrix
    mask = np.triu(np.ones_like(corr))

    # 14: Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(12, 8))

    # 15: Draw the heatmap with sns.heatmap
    sns.heatmap(corr, mask=mask, annot=True, fmt='.1f', cmap='coolwarm', vmin=-0.16, vmax=0.32, center=0, square=True, linewidths=.5, ax=ax)

    # 16: Save the figure
    fig.savefig('heatmap.png')

    return fig
