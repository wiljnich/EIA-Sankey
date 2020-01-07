import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv("flows.csv")

def genSankey(df,cat_cols=[],value_cols='',title='Sankey Diagram'):
        colorPalette = ['#0d9902','#0d9902','#0d9902','#0d9902','#0d9902','#0d9902','#0d9902','#0d9902']
        labelList = []
        colorNumList = []
        for catCol in cat_cols:
            labelListTemp =  list(set(df[catCol].values))
            colorNumList.append(len(labelListTemp))
            labelList = labelList + labelListTemp

        labelList = list(dict.fromkeys(labelList))

        colorList = []
        for idx, colorNum in enumerate(colorNumList):
            colorList = colorList + [colorPalette[idx]]*colorNum

        for i in range(len(cat_cols)-1):
            if i==0:
                sourceTargetDf = df[[cat_cols[i],cat_cols[i+1],value_cols]]
                sourceTargetDf.columns = ['source','target','count']
            else:
                tempDf = df[[cat_cols[i],cat_cols[i+1],value_cols]]
                tempDf.columns = ['source','target','count']
                sourceTargetDf = pd.concat([sourceTargetDf,tempDf])
            sourceTargetDf = sourceTargetDf.groupby(['source','target']).agg({'count':'sum'}).reset_index()

        sourceTargetDf['sourceID'] = sourceTargetDf['source'].apply(lambda x: labelList.index(x))
        sourceTargetDf['targetID'] = sourceTargetDf['target'].apply(lambda x: labelList.index(x))

        data = dict(
            type='sankey',
            node = dict(
              pad = 15,
              thickness = 20,
              line = dict(
                color = "black",
                width = 0.5
              ),
              label = labelList,
              color = colorList
            ),
            link = dict(
              source = sourceTargetDf['sourceID'],
              target = sourceTargetDf['targetID'],
              value = sourceTargetDf['count']
            )
          )

        layout =  dict(
            title = title,
            font = dict(
              size = 10
            )
        )

        fig = dict(data=[data], layout=layout)
        return fig
    
app = dash.Dash()
app.layout = html.Div([

    html.Div([
        dcc.Markdown('''
        ''')
    ], style={'width': '5%', 'display': 'inline-block'}),
    
    html.Div([
        dcc.Markdown('''
        ## US Energy Flows 2018
        Hover over each segment of the plot to see the annual flows in quadrillions of BTUs
        ''')
    ], style={'width': '55%', 'display': 'inline-block', 'font-family': 'Arial'}),
    
    html.Div([
        html.Img(src=app.get_asset_url("eia.jpg"), style={'height':'30%', 'width':'30%'})
                 ], style={'width': '20%', 'display': 'inline-block'}),
    
    html.Div([
        dcc.Graph(
            id='figure1',
            figure=genSankey(df,cat_cols=['lvl1','lvl2'],value_cols='count',title=''), style={"border":"2px black solid"}
        ),
    ], style={'width': '80%', 'display': 'inline-block'}),
    
    html.Div([
        dcc.Markdown('''
        ''')
    ], style={'width': '20%', 'display': 'inline-block'}),
    
    html.Div([
        dcc.Markdown('''
        ''')
    ], style={'width': '5%', 'display': 'inline-block'}),
    
    html.Div([
        dcc.Markdown('''
        This chart was modeled on Sankey diagrams issued by the Energy Information Administration with data from [this link](https://www.eia.gov/totalenergy/data/monthly/pdf/flow/total_energy.pdf). It is not an official product of the US Department of Energy.
        ''')
    ], style={'width': '55%', 'display': 'inline-block', 'font-family': 'Arial'}),
])

if __name__ == '__main__':
    app.run_server(debug=True)
    
