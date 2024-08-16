import sqlite3
import streamlit as st
import numpy as np

# データベースに接続（なければ作成される）
conn = sqlite3.connect('sample.db')
cur = conn.cursor()

# テーブルを作成（存在しない場合）
cur.execute('''
CREATE TABLE IF NOT EXISTS users(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  mel_cdl TEXT,
  ops TEXT,
  item TEXT
)
''')

st.title('MELCDLヘルパーくん')
# ページ選択
page = st.sidebar.selectbox("ページを選択してください", ["入力フォーム", "データベース表示"])
if page == "入力フォーム":
    st.header("入力フォーム")
    # MEL/CDLの選択肢をラジオボタンで表示
    option = st.radio("MEL/CDLを選択してください", ["MEL", "CDL"])

    # 入力フォーム
    if option == "MEL":
        input_value = st.text_input("MEL番号", "")

    elif option == "CDL":
        input_value = st.text_input("CDL番号", "CDL")

        calc_option = st.radio("機種を選択してください", ["B6", "B3"])

        input_value_1 = st.number_input("ENRT ClimbのWeight Reductionを入力")

        # 計算結果を表示
        if calc_option == "B6":
            result = input_value_1 / 1000 * 0.45
            st.write(f"計算結果: {result}%")
            st.write("計算式：Weight Reduction/ 1000 * 0.45")
        elif calc_option == "B3":
            result = input_value_1 / 100 * 0.15
            st.write(f"計算結果: {result}%")
            st.write("計算式：Weight Reduction/ 100 * 0.15")

    # ops の入力フォーム（改行可能）
    ops = st.text_area("OPS")
    if "below" in ops.lower() or "use" in ops.lower():
        st.warning("ALTNも確認しましたか？")

    # item の入力フォーム（改行可能）
    item = st.text_area("ITEM")

    # 入力内容を表示
    st.write(f"番号: {input_value}")
    st.write(f"OPS: {ops}")
    st.write(f"ITEM: {item}")

    # データ保存ボタン
    if st.button('保存'):
        # SQLiteデータベースに入力データを保存
        cur.execute('''
        INSERT INTO users (mel_cdl, ops, item) VALUES (?, ?, ?)
        ''', (input_value, ops, item))
        conn.commit()
        st.success('データベースに保存されました。')


elif page == "データベース表示":
    st.header("データベースの内容")

    # 検索バーを作成
    search_query = st.text_input("検索キーワードを入力してください:")

    # データベースからデータを取得して表示（新しい順に並べ替え）
    cur.execute('SELECT * FROM users ORDER BY id DESC')
    rows = cur.fetchall()

    # 検索クエリが入力されている場合、フィルタリングを行う
    if search_query:
        rows = [row for row in rows if search_query.lower() in (row[1].lower() + row[2].lower() + row[3].lower())]

    if rows:
        for row in rows:
            st.markdown(f"<div style='font-size:20px;'>ID: {row[0]}, 番号: {row[1]}, OPS: {row[2]}, ITEM: {row[3]}</div>", unsafe_allow_html=True)
    else:
        st.write("検索結果に一致するデータはありません。")

# データベース接続を閉じる
conn.close()


