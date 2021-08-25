#データの読み込み
import pandas as pd

m_store = pd.read_csv('./data/m_store.csv')
m_store

#データ件数だけ確認
len(m_store)

#データの最初の5件のみ確認
m_store.head()

#他のデータを読み込む(地域マスタ)
m_area = pd.read_csv('./data/m_area.csv')
m_area

#ピザチェーンの4月分データ
tbl_order_4 = pd.read_csv('./data/tbl_order_202004.csv')
tbl_order_4

#5月分のデータ
tbl_order_5 = pd.read_csv('./data/tbl_order_202005.csv')
tbl_order_5

# 4月分と5月分のデータをユニオン(結合)する
order_all = pd.concat([tbl_order_4, tbl_order_5], ignore_index=True)
order_all

#ユニオンした件数の検証
len(order_all) == len(tbl_order_4) + len(tbl_order_5)


#フォルダ内のファイル名を一覧化する
#カレントディレクトリの表示
import os
current_dir = os.getcwd()
current_dir

#カレントディレクトリの内容を一覧表示
os.listdir(current_dir)

#カレントディレクトリの検索キーを設定
tbl_order_file = os.path.join(current_dir, 'data/tbl_order_*.csv')
tbl_order_file

#カレントディレクトリの注文データを一覧表示
import glob
tbl_order_files = glob.glob(tbl_order_file)
tbl_order_files


#複数データをユニオン(結合)する
#リストの1個目のファイルを指定した処理
order_all = pd.DataFrame()
file = tbl_order_files[0]
order_data = pd.read_csv(file)
print(f'{file}:{len(order_data)}')
order_all = pd.concat([order_all, order_data], ignore_index=True)
order_all

#繰り返し処理を実行
order_all = pd.DataFrame()
for file in tbl_order_files:
    prder_data = pd.read_csv(file)
    print(f'{file}:{len(order_data)}')
    order_all = pd.concat([order_all, order_data], ignore_index=True)
#ユニオン結果を出力
order_all

#まとめたデータの欠損値を確認
order_all.isnull().sum()

#注文データの統計量
order_all.describe()

#total_amountの統計量を取り出す(注文金額)
order_all['total_amount'].describe()

#データの期間
print(order_all["order_accept_date"].min())
print(order_all["order_accept_date"].max())
print(order_all["delivered_date"].min())
print(order_all["delivered_data"].max())

#不要なデータを除外
order_data = order_all.loc[order_all['store_id'] != 999]
order_data

#マスタデータを結合(ジョイン)
order_data = pd.merge(order_data, m_store, on='store_id', how='left')
order_data

#order_dataにエリアマスタをジョインする
order_data = pd.merge(order_data, m_area, on='area_cd', how='left')
order_data














