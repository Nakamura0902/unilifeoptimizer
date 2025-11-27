import streamlit as st
import json
import os
from datetime import date
import matplotlib.pyplot as plt
import io
import csv

DATA_FILE = "data.json"

# -------------------------
# データ関連
# -------------------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_data(records):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

def get_category_sum(records):
    category_sum = {}
    for r in records:
        cat = r["category"]
        category_sum[cat] = category_sum.get(cat, 0) + r["minutes"]
    return category_sum

def records_to_csv(records):
    """記録のリストをCSV文字列に変換する"""
    output = io.StringIO()
    writer = csv.writer(output)

    # ヘッダー行
    writer.writerow(["date", "category", "content", "minutes"])

    for r in records:
        writer.writerow([r["date"], r["category"], r["content"], r["minutes"]])

    # Excelで文字化けしにくいようにBOM付きutf-8で返す
    return output.getvalue().encode("utf-8-sig")


# -------------------------
# ページ設定・サイドバー
# -------------------------
st.set_page_config(
    page_title="UniLife Optimizer",
    page_icon="📊",
    layout="wide",
)

st.sidebar.title("📚 UniLife Optimizer")
st.sidebar.write("大学生活の勉強・部活・資格勉強を見える化するツール。")
st.sidebar.write("CLI版 / GUI版 / Web版の3形態で動作中🔥")

records = load_data()

# ざっくり統計をサイドバーに表示
st.sidebar.subheader("📈 概要")
st.sidebar.write(f"記録件数: {len(records)} 件")
if records:
    total_minutes = sum(r["minutes"] for r in records)
    st.sidebar.write(f"累計時間: {total_minutes} 分")
else:
    st.sidebar.write("まだデータがありません。")


# -------------------------
# メインタイトル
# -------------------------
st.title("UniLife Optimizer - Web版")

# タブ：①追加 ②一覧 ③グラフ ④今日の提案
tab1, tab2, tab3, tab4 = st.tabs(["記録を追加", "記録一覧", "グラフ", "今日の提案"])


# -------------------------
# タブ1：記録を追加
# -------------------------
with tab1:
    st.header("📝 記録を追加")

    col1, col2 = st.columns(2)

    with col1:
        category = st.text_input("カテゴリ（例：ITパス / 大学 / 部活）")
        content = st.text_input("内容（例：ITパス過去問50問）")

    with col2:
        minutes = st.number_input("時間（分）", min_value=0, step=10)
        date_str = st.date_input("日付", value=date.today())

    if st.button("記録を保存"):
        if category and content:
            record = {
                "date": date_str.isoformat(),
                "category": category,
                "content": content,
                "minutes": int(minutes),
            }
            records.append(record)
            save_data(records)
            st.success("✅ 記録を保存しました！")
        else:
            st.error("カテゴリと内容は必須です。")


# -------------------------
# タブ2：記録一覧
# -------------------------
with tab2:
    st.header("📋 記録一覧")

    if records:
        # 新しい順に表示
        sorted_records = sorted(records, key=lambda r: r["date"], reverse=True)

        for r in sorted_records:
            st.write(
                f"{r['date']} | {r['category']} | "
                f"{r['content']} | {r['minutes']}分"
            )

        # ▼ ここからCSVダウンロードボタン
        csv_bytes = records_to_csv(sorted_records)

        st.download_button(
            label="📥 CSVとしてダウンロード",
            data=csv_bytes,
            file_name="unilife_records.csv",
            mime="text/csv",
        )
    else:
        st.write("まだ記録がありません。")



# -------------------------
# タブ3：グラフ（棒 or 円）
# -------------------------
with tab3:
    st.header("📊 カテゴリ別の累計時間")

    if not records:
        st.write("データがありません。")
    else:
        category_sum = get_category_sum(records)

        graph_type = st.radio(
            "グラフの種類を選んでください",
            ["棒グラフ", "円グラフ"],
            horizontal=True,
        )

        if graph_type == "棒グラフ":
            fig, ax = plt.subplots()
            ax.bar(category_sum.keys(), category_sum.values())
            ax.set_xlabel("category")
            ax.set_ylabel("times (minutes)")
            ax.set_title("category vs. total time (minutes)")
            plt.xticks(rotation=20)
            st.pyplot(fig)

        else:  # 円グラフ
            fig, ax = plt.subplots()
            ax.pie(
                category_sum.values(),
                labels=category_sum.keys(),
                autopct="%1.1f%%",
                startangle=90,
            )
            ax.set_title("category vs. total time (minutes)")
            ax.axis("equal")
            st.pyplot(fig)


# -------------------------
# タブ4：今日の提案（レコメンド）
# -------------------------
with tab4:
    st.header("🎯 今日やるべきことの提案")

    if not records:
        st.write("まだ記録がありません。まずは何か1つ記録してみよう。")
    else:
        category_sum = get_category_sum(records)

        # 一番時間が少ないカテゴリを探す
        least_cat = min(category_sum, key=category_sum.get)
        least_minutes = category_sum[least_cat]

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("カテゴリ別 累計時間")
            for cat, mins in category_sum.items():
                st.write(f"- {cat}: {mins} 分")

        with col2:
            st.subheader("一番使えていないカテゴリ")
            st.metric(label="カテゴリ", value=least_cat)
            st.metric(label="累計時間（分）", value=least_minutes)

        st.markdown("---")
        st.subheader("💡 今日のおすすめアクション")

        if "IT" in least_cat or "パス" in least_cat:
            st.write(
                "・ITパスポートの勉強を **30分だけ** やっておくと、"
                "試験対策がかなり進むはず。"
            )
        elif "大" in least_cat:
            st.write(
                "・大学の授業の復習や、"
                "レポートを少しだけ進めておくと後がかなりラクになる。"
            )
        elif "部" in least_cat:
            st.write(
                "・部活のためのストレッチやフォーム研究を少しだけやるのもアリ。"
            )
        else:
            st.write(
                f"・「{least_cat}」にあと **30分** くらい使ってみると、"
                "生活のバランスが良くなりそう。"
            )

        st.caption("※ ロジックは CLI版/GUI版と同じで、カテゴリ別累計から一番弱いところを探しています。")
