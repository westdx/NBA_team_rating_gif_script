import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from sklearn.preprocessing import MinMaxScaler
import imageio
import warnings
warnings.filterwarnings('ignore')

#load data and create image path
df = pd.read_excel('team_rating_data.xlsx', sheet_name='Sheet1', header = 1)
df['path'] = 'team_logo/' + df['Team_formated'] + '.png'

#create a copy of the data and remove unnecessary features
df1 = df.copy()
df1['Date'] = pd.to_datetime(df1["Date"]).dt.date
df1 = df1.drop(['Rk', 'Team', 'Conf', 'Div', 'W', 'L', 'W/L%', 'MOV', 'NRtg', 
                'MOV/A', 'ORtg/A', 'DRtg/A', 'NRtg/A'], axis = 1)


def getImage(path):
    return OffsetImage(plt.imread(path), zoom=.05, alpha = 1)

def runScatter(dataframe):
    fig, ax = plt.subplots(figsize=(10, 10), dpi = 300)
    ax.scatter(dataframe['ORtg'], dataframe['DRtg'], color = 'white')
    for _, row in dataframe.iterrows():
        a = AnnotationBbox(getImage(row['path']), (row['ORtg'], row['DRtg']), frameon = False)
        ax.add_artist(a)
    plt.xticks(np.arange(0, 1.1, step = 0.1))
    plt.yticks(np.arange(0, 1.1, step = 0.1))
    plt.hlines(dataframe['DRtg'].mean(), dataframe['ORtg'].min(), dataframe['ORtg'].max(), color = 'red')
    plt.vlines(dataframe['ORtg'].mean(), dataframe['DRtg'].min(), dataframe['DRtg'].max(), color = 'red')
    plt.xlabel('Offensive Rating')
    plt.ylabel('Defensive Rating')
    plt.title('NBA Team Offensive and Defensive Rating {}'.format(str(dataframe['Date'].max())))
    plt.savefig('{}.png'.format(str(dataframe['Date'].max())))
    fig_name = '{}.png'.format(str(dataframe['Date'].max()))
    plt.close()
    return fig_name


scaler = MinMaxScaler()
dates = sorted(set(df1['Date']))
charts = []
for i in dates:
    filter_df = df1.loc[(df1['Date'] == i)]
    filter_df[['ORtg', 'DRtg']] = scaler.fit_transform(filter_df[['ORtg', 'DRtg']])
    chart = runScatter(filter_df)       
    charts.append(chart)
    

with imageio.get_writer('nba_team_rating.gif', mode='I', duration = 0.3) as writer:
    for i in charts:
        image = imageio.imread(i)
        writer.append_data(image)
    


