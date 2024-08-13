import sqlite3
import streamlit as st

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

# ページ選択
page = st.sidebar.selectbox("ページを選択してください", ["入力フォーム", "データベース表示"])

if page == "入力フォーム":
    # MEL/CDLの選択肢をラジオボタンで表示
    option = st.radio("MEL/CDLを選択してください", ["MEL", "CDL"])

    # 入力フォーム
    if option == "MEL":
        input_value = st.text_input("MEL番号:", "")

    elif option == "CDL":
        input_value = st.text_input("CDL番号:", "CDL")

        calc_option = st.radio("機種を選択してください", ["B6", "B3"])

        input_value_1 = st.number_input("ENRT ClimbのWeight Reductionを入力")

        # 計算結果を表示
        if calc_option == "B6":
            result = input_value_1 / 1000 * 0.45
            st.write(f"計算結果: {result}")
            st.write("計算式：Weight Reduction/ 1000 * 0.45")
        elif calc_option == "B3":
            result = input_value_1 / 100 * 0.15
            st.write(f"計算結果: {result}")
            st.write("計算式：Weight Reduction/ 100 * 0.45")

    # ops の入力フォーム
    ops = st.text_input("OPS:")
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

    # メモのダウンロード
    if st.button('ダウンロード'):
        # SQLiteデータベースからデータを取得
        cur.execute('SELECT * FROM users ORDER BY id DESC')
        saved_data = cur.fetchall()
        
        # ダウンロード用のテキストファイルを生成
        saved_text = "\n".join([f"ID: {row[0]}, MEL/CDL: {row[1]}, OPS: {row[2]}, ITEM: {row[3]}" for row in saved_data])
        
        st.download_button(label="ダウンロード",
                        data=saved_text,
                        file_name='saved_memo.txt',
                        mime='text/plain')

elif page == "データベース":
    st.header("データベースの内容")
    
    # データベースからデータを取得して表示（新しい順に並べ替え）
    cur.execute('SELECT * FROM users ORDER BY id DESC')
    rows = cur.fetchall()

    if rows:
        for row in rows:
            st.markdown(f"<div style='font-size:20px;'>ID: {row[0]}, MEL/CDL: {row[1]}, OPS: {row[2]}, ITEM: {row[3].replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
    else:
        st.write("データベースに保存されているデータはありません。")

# データベース接続を閉じる
conn.close()
