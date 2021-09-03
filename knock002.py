#order_data.csv
#データを読み込んで不要なものを除外する
#order_dataの読み込み結果
import pandas as pd
order_data = pd.read_csv('./output_data/order_data.csv')
print(len(order_data))
order_data.head()

#必要の無いデータを除外する
#絞り込み結果
order_data = order_data.loc[(order_data['status'] == 1)|(order_data['status'] == 2)]
print(len(order_data))
order_data.columns

#不要な項目を除外
analyze_data = order_data[['store_id', 'customer_id', 'coupon_cd', 'order_accept_date', 'delivered_date', 'total_amount', 'store_name', 'wide_area', 'narrow_area', 'takeout_name', 'status_name']]
print(analyze_data.shape)
analyze_data.head()

#分析用データの統計量
analyze_data.describe()

#テータ型を確認
analyze_data.dtypes

#分析用のデータ型を文字列型に変更する
analyze_data[['store_id', 'coupon_cd']] = analyze_data[['store_id', 'coupon_cd']].astype(str)
analyze_data.dtypes

#表示された警告を回避するコード
import warnings
warnings.filterwarnings('ignore')

#月別の売上集計(order_accept_date)
#日時のデータ項目2つを、月別の売上集計に利用するために、object型となっているので、
#日時型に変換して、さらに年月項目を作成する。
analyze_data['order_accept_date'] = pd.to_datetime(analyze_data['order_accept_date'])
analyze_data['order_accept_month'] = analyze_data['order_accept_date'].dt.strftime('%Y%m')
analyze_data[['order_accept_date', 'order_accept_month']].head()

#月別の売上集計(delivered_date)
#日時のデータ項目2つを、月別の売上集計に利用するために、object型となっているので、
#日時型に変換して、さらに年月項目を作成する
analyze_data['delivered_date'] = pd.to_datetime(analyze_data['delivered_date'])
analyze_data['delivered_month'] = analyze_data['delivered_date'].dt.strftime('%Y%m')
analyze_data[['delivered_date', 'delivered_month']].head()

#日時のデータ型確認
analyze_data.dtypes

#それぞれの日時がdatetime64[ns]に変更され、日時項目として利用できるようになったので、
#月別の統計データを確認する
month_data = analyze_data.groupby('order_accept_month')
month_data.describe()

#合計金額を確認
month_data.sum()

#月別の推移を可視化する
#月別の売上合計推移
import matplotlib.pyplot as plt
%matplotlib inline
month_data.sum().plot()

#売上の平均額を可視化
month_data.mean().plot()

#売上からヒストグラムを作成
plt.hist(analyze_data['total_amount'])

#ヒストグラムのピン(横軸)を変更
plt.hist(analyze_data['total_amount'], bins=21)

#都道府県別の売上を集計して可視化する
#ピボットテーブルを使ったクロス集計
#都道府県別の売上
pre_data = pd.pivot_table(analyze_data, index='order_accept_month', columns='narrow_area', values='total_amount', aggfunc='mean')
pre_data

#都道府県別の売上をグラフで可視化
import japanize_matplotlib
plt.plot(list(pre_data.index), pre_data['東京'], label='東京')
plt.plot(list(pre_data.index), pre_data['神奈川'], label='神奈川')
plt.plot(list(pre_data.index), pre_data['埼玉'], label='埼玉')
plt.plot(list(pre_data.index), pre_data['千葉'], label='千葉')
plt.plot(list(pre_data.index), pre_data['茨城'], label='茨城')
plt.plot(list(pre_data.index), pre_data['栃木'], label='栃木')
plt.plot(list(pre_data.index), pre_data['群馬'], label='群馬')
plt.legend()

#クラスタリングに向けてデータを加工する
#注文データを店舗毎に集計し、クラスタリングに使用できる状態にする
#店舗別の統計量
store_clustering = analyze_data.groupby('store_id').agg(['size', 'mean', 'median', 'max', 'min'])['total_amount']
store_clustering.reset_index(inplace = True, drop = True)
print(len(store_clustering))
store_clustering.head()

#各店舗の状況を可視化する
import seaborn as sns
hexbin = sns.jointplot(x='mean', y='size', data=store_clustering, kind='hex')

#K-means法でのクラスタリング
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

sc = StandardScaler()
store_clustering_sc = sc.fit_transform(store_clustering)

kmeans = KMeans(n_clusters=4, random_state=0)
clusters = kmeans.fit(store_clustering_sc)
store_clustering['cluster'] = clusters.labels_
print(store_clustering['cluster'].unique())
store_clustering.head()

#4つのグループの傾向を分析する
#グループ毎の件数を確認する
store_clustering.columns = ['月内件数', '月内平均値', '月内中央値', '月内最大値', '月内最小値', 'cluster']
store_clustering.groupby('cluster').count()

#グループ毎の金額の内訳
store_clustering.groupby('cluster').mean()

#クラスタリングの結果をt-SNEで可視化する
from sklearn.manifold import TSNE

tsne = TSNE(n_components=2, random_state=0)
x = tsne.fit_transform(store_clustering_sc)
tsne_df = pd.DataFrame(x)
tsne_df['cluster'] = store_clustering['cluster']
tsne_df.columns = ['axis_0', 'axis_1', 'cluster']
tsne_df.head()

#t-SNEでの可視化結果
tsne_graph = sns.scatterplot(x='axis_0', y='axis_1', hue='cluster', data=tsne_df)
















