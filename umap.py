import umap
import pandas as pd
import json

with open('graph.json') as f:
    data = f.read()

data = json.loads(data)

df = pd.DataFrame(data['links'])
df = df[~df.duplicated()]
df = df.pivot(index='source', columns='target', values='val')
df = df.fillna(0)

reducer = umap.UMAP()
embedding = reducer.fit_transform(df)
embedding = embedding.astype(float)

df[['x', 'y']] = embedding

for node in data['nodes']:
    row = df.loc[df['source'] == node['id']]
    if row.shape[0] > 0:
        node['x'] = float(row.iloc[0]['x'])
        node['y'] = float(row.iloc[0]['y'])

with open('out.js', 'w') as f:
    f.write(json.dumps(data))

