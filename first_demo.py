# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3

import plotly.express as px
import plotly.graph_objects as go

dbname = 'RbfnRain.db'
tbClusterName = 'ResultCluster'
tbMeshName = 'RbfnMesh'
tbRainName = 'RainSeries'

conn = sqlite3.connect(dbname)
cur = conn.cursor()
    

def matrix_rain_plot(cno, df, select='災害の発生', title='超過・非超過散布図'):
    strSql = 'SELECT ResultCluster.*, (Cluster'+ str(cno) +'.地域 || Cluster'+ str(cno) +'.市町村等) AS 地域 FROM ' + tbClusterName
    strSql = strSql + ' INNER JOIN ' + 'Cluster'+ str(cno) + ' ON (ResultCluster.Mesh3Code=' + 'Cluster'+ str(cno) +'.地域メッシュコード )'
    strSql = strSql + ' WHERE ClusterNo='+ str(cno) +' ORDER BY ClusterNo'
    df = pd.read_sql(strSql, conn) 
    
    col = ['土壌雨量指数','60分間積算雨量', '半減期1時間', '半減期1時間30分', '地域', '災害の発生']
    #df_plot = df[['半減期1時間','半減期1時間30分', '地域', '災害の発生']] 
    #df_plot = df[['土壌雨量指数','60分間積算雨量', '半減期1時間', '半減期1時間30分', '地域', '災害の発生']]
    df_plot = df[col]
    #df_plot = df_plot.dropna()
    #df_plot
    
    title = title + '(クラスター:' + str(cno) +')'
    fig = px.scatter_matrix(df_plot, color=select, title=title)
    fig.update_layout(
        width=1000,
        height=1000,
    ) 
    
    st.markdown('## クラスター番号：' + str(cno))
    # streatlimで表示するために
    st.plotly_chart(fig, use_container_width=True)
   

def matrix_basic_plot(cno, select='災害の発生', title='超過・非超過散布図'):
    strSql = 'SELECT ResultCluster.*, (Cluster'+ str(cno) +'.地域 || Cluster'+ str(cno) +'.市町村等) AS 地域 FROM ' + tbClusterName
    strSql = strSql + ' INNER JOIN ' + 'Cluster'+ str(cno) + ' ON (ResultCluster.Mesh3Code=' + 'Cluster'+ str(cno) +'.地域メッシュコード )'
    strSql = strSql + ' WHERE ClusterNo='+ str(cno) +' ORDER BY ClusterNo'
    df = pd.read_sql(strSql, conn)  
    df_plot = df[['土壌雨量指数','60分間積算雨量', '地域', '災害の発生']]
    df_plot = df_plot.dropna()
    title = title + '(クラスター:' + str(cno) +')'
    fig = px.scatter_matrix(df_plot, color=select, title=title)
    fig.update_layout(
        width=1000,
        height=1000,
    ) 
    
    st.markdown('## クラスター番号：' + str(cno))
    # streatlimで表示するために
    st.plotly_chart(fig, use_container_width=True)
    
    
def cluster_plot(cno, select='災害の発生', title='超過・非超過散布図', hover_name='地域', hover_data=['土壌雨量指数', '60分間積算雨量','地域']):
    strSql = 'SELECT ResultCluster.*, (Cluster'+ str(cno) +'.地域 || Cluster'+ str(cno) +'.市町村等) AS 地域 FROM ' + tbClusterName
    #strSql = 'SELECT ResultCluster.*, ' + 'Cluster'+ str(cno) +'.地域,' + 'Cluster'+ str(cno) +'.市町村等 FROM ' + tbClusterName
    strSql = strSql + ' INNER JOIN ' + 'Cluster'+ str(cno) + ' ON (ResultCluster.Mesh3Code=' + 'Cluster'+ str(cno) +'.地域メッシュコード )'
    strSql = strSql + ' WHERE ClusterNo='+ str(cno) +' ORDER BY ClusterNo'
    #strSql
    df = pd.read_sql(strSql, conn)
    
    df_plot = df[['土壌雨量指数','60分間積算雨量', '半減期1時間',
       '半減期1時間30分', '半減期2時間', '半減期3時間', '半減期4時間',
       '半減期6時間', '半減期8時間', '半減期10時間', '半減期12時間',
       '半減期24時間', '半減期48時間', '半減期72時間', '半減期96時間',
       '半減期120時間', '半減期144時間', '半減期240時間', '半減期500時間',
       '半減期1000時間', '半減期1500時間', '災害の発生', 'Mesh3Code', '地域']]
    df_plot = df_plot.dropna()

    title = title + '(クラスター:' + str(cno) +')'
    fig = px.scatter(df_plot, x='土壌雨量指数', y='60分間積算雨量', color=select, title=title, hover_name=hover_name, hover_data=hover_data)
    fig.update_layout(
        width=640,
        height=640,
    )
    
    st.markdown('## クラスター番号：' + str(cno))
    # streatlimで表示するために
    st.plotly_chart(fig, use_container_width=True)


def db_mesh_read(cno):
    strSql = 'SELECT 地域メッシュコード, 注意報基準, 警報基準 FROM Cluster'+ str(cno)
    df = pd.read_sql(strSql, conn)
    st.sidebar.write('地域メッシュと基準値')
    st.sidebar.dataframe(df)

def db_cluster_read(cno):
    strSql = 'SELECT ResultCluster.*, (Cluster'+ str(cno) +'.地域 || Cluster'+ str(cno) +'.市町村等) AS 地域 FROM ' + tbClusterName
    #strSql = 'SELECT ResultCluster.*, ' + 'Cluster'+ str(cno) +'.地域,' + 'Cluster'+ str(cno) +'.市町村等 FROM ' + tbClusterName
    strSql = strSql + ' INNER JOIN ' + 'Cluster'+ str(cno) + ' ON (ResultCluster.Mesh3Code=' + 'Cluster'+ str(cno) +'.地域メッシュコード )'
    strSql = strSql + ' WHERE ClusterNo='+ str(cno) +' ORDER BY ClusterNo'
    #strSql
    df = pd.read_sql(strSql, conn)
    
    df_plot = df[['土壌雨量指数','60分間積算雨量', '半減期1時間',
        '半減期1時間30分', '半減期2時間', '半減期3時間', '半減期4時間',
        '半減期6時間', '半減期8時間', '半減期10時間', '半減期12時間',
        '半減期24時間', '半減期48時間', '半減期72時間', '半減期96時間',
        '半減期120時間', '半減期144時間', '半減期240時間', '半減期500時間',
        '半減期1000時間', '半減期1500時間', '災害の発生', 'Mesh3Code', '地域']]
    df_plot = df_plot.dropna()
    return df_plot


def xy_plot(cno, x='土壌雨量指数', y='60分間積算雨量', select='災害の発生', title='超過・非超過散布図', hover_name='地域', hover_data=['土壌雨量指数', '60分間積算雨量','地域']):
    strSql = 'SELECT ResultCluster.*, (Cluster'+ str(cno) +'.地域 || Cluster'+ str(cno) +'.市町村等) AS 地域 FROM ' + tbClusterName
    #strSql = 'SELECT ResultCluster.*, ' + 'Cluster'+ str(cno) +'.地域,' + 'Cluster'+ str(cno) +'.市町村等 FROM ' + tbClusterName
    strSql = strSql + ' INNER JOIN ' + 'Cluster'+ str(cno) + ' ON (ResultCluster.Mesh3Code=' + 'Cluster'+ str(cno) +'.地域メッシュコード )'
    strSql = strSql + ' WHERE ClusterNo='+ str(cno) +' ORDER BY ClusterNo'
    #strSql
    df = pd.read_sql(strSql, conn)
    
    df_plot = df[['土壌雨量指数','60分間積算雨量', '半減期1時間',
       '半減期1時間30分', '半減期2時間', '半減期3時間', '半減期4時間',
       '半減期6時間', '半減期8時間', '半減期10時間', '半減期12時間',
       '半減期24時間', '半減期48時間', '半減期72時間', '半減期96時間',
       '半減期120時間', '半減期144時間', '半減期240時間', '半減期500時間',
       '半減期1000時間', '半減期1500時間', '災害の発生', 'Mesh3Code', '地域']]
    df_plot = df_plot.dropna()

    title = title + '(クラスター:' + str(cno) +')'
    fig = px.scatter(df_plot, x=x, y=y, color=select, title=title, hover_name=hover_name, hover_data=hover_data)
    fig.update_layout(
        width=640,
        height=640,
    )
    
    st.markdown('## クラスター番号：' + str(cno))
    # streatlimで表示するために
    st.plotly_chart(fig, use_container_width=True)
    
def main():

    st.set_page_config(layout="wide")
    st.markdown('# 土砂災害危険度予測結果クラスター別表示')
    # dbをクラスター番号を抽出する。
    strSql ='SELECT DISTINCT ClusterNo as クラスター番号, count(降雨番号) as データ数 FROM ' + tbClusterName + ' GROUP by ClusterNo ORDER BY ClusterNo'
    df_cluster = pd.read_sql(strSql, conn)
    clusterNo = df_cluster['クラスター番号'].to_list()
    
    # プルダウンサイドバーに表示させる
    cno = 0
    cno = st.sidebar.selectbox(
        '表示するクラスター番号を選択して下さい。',
        clusterNo)
    
    st.markdown('## クラスター番号：' + str(cno)) 
    
    st.sidebar.markdown('## クラスター番号：' + str(cno)) 
    
    db_mesh_read(cno)
    
    df_plot = db_cluster_read(cno)
    
    st.dataframe(df_plot)
    
    xcols = ['土壌雨量指数','60分間積算雨量', '半減期1時間',
       '半減期1時間30分', '半減期2時間', '半減期3時間', '半減期4時間',
       '半減期6時間', '半減期8時間', '半減期10時間', '半減期12時間',
       '半減期24時間', '半減期48時間', '半減期72時間', '半減期96時間',
       '半減期120時間', '半減期144時間', '半減期240時間', '半減期500時間',
       '半減期1000時間', '半減期1500時間']
    
    ycols = ['土壌雨量指数','60分間積算雨量', '半減期1時間',
       '半減期1時間30分', '半減期2時間', '半減期3時間', '半減期4時間',
       '半減期6時間', '半減期8時間', '半減期10時間', '半減期12時間',
       '半減期24時間', '半減期48時間', '半減期72時間', '半減期96時間',
       '半減期120時間', '半減期144時間', '半減期240時間', '半減期500時間',
       '半減期1000時間', '半減期1500時間']
    
    
    st.sidebar.markdown('## 個別散布図')
    
    x = st.sidebar.selectbox(
        'X軸の項目を選択して下さい。',
        xcols)
    
    y = st.sidebar.selectbox(
        'Y軸の項目を選択して下さい。',
        ycols)
    
    cluster_plot(cno, select='災害の発生', title='非超過・超過散布図', hover_name='地域', hover_data=['土壌雨量指数', '60分間積算雨量'])
    
    cluster_plot(cno, select='地域', title='地域別マトリックス散布図', hover_name='災害の発生', hover_data=['土壌雨量指数', '60分間積算雨量'])
    
    matrix_basic_plot(cno, select='災害の発生', title='非超過・超過散布図')
    
    matrix_basic_plot(cno, select='地域', title='地域別マトリックス散布図')
    
    matrix_rain_plot(cno, df_plot, select='災害の発生', title='非超過・超過散布図')
    
    xy_plot(cno, x, y, select='災害の発生', title=x + '-' + y + '散布図')
    
    
if __name__ == '__main__':
    main()