import streamlit as st
import json
import os
from datetime import date, datetime, timedelta
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
    """記録のリストをCSVバイト列に変換する（Excel向けにCP932でエンコード）"""
    output = io.StringIO(newline="")
    writer = csv.writer(output)

    # ヘッダー行
    writer.writerow(["date", "category", "content", "minutes"])

    for r in records:
        writer.writerow([r["date"], r["category"], r["content"], r["minutes"]])

    # Excel（日本語環境）のデフォルトに合わせて cp932 で返す
    return output.getvalue().encode("cp932")


def filter_records_by_period(records, period: str):
    """表示期間に応じて記録を絞り込む"""
    if not records:
        return []

    if period == "全期間":
        return records

    today = date.today()

    if period == "今日":
        return [r for r in records if r["date"] == today.isoformat()]

    if period == "今週":
        # 月曜スタートの今週
        # today.weekday() : 月=0, 日=6
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=7)
        def to_date(dstr):
            return datetime.fromisoformat(dstr).date()
        return [
            r for r in records
            if week_start <= to_date(r["date"]) < week_end
        ]

    if period == "今月":
        def to_date(dstr):
            return datetime.fromisoformat(dstr).date()
        return [
            r for r in records
            if to_date(r["date"]).year == today.year
            and to_date(r["date"]).month == today.month
        ]

    # 想定外の文字列が来たときは全期間
    return records


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
st.sidebar.write("CLI / GUI / Web / Mobile の4形態で動作中🔥")

# 生データ（全期間）
records = load_data()

# 🔥 期間フィルタ（全タブ共通）
st.sidebar.subheader("📅 表示期間")
period = st.sidebar.selectbox(
    "表示する期間を選択",
    ["全期間", "今日", "今週", "今月"],
    index=0,
)
filtered_records = filter_records_by_period(records, period)

# ざっくり統計（選択期間ベース）
st.sidebar.subheader("📈 概要（" + period + "）")
st.sidebar.write(f"記録件数: {len(filtered_records)} 件")
if filtered_records:
    total_minutes = sum(r["minutes"] for r in filtered_records)
    st.sidebar.write(f"累計時間: {total_minutes} 分")
else:
    st.sidebar.write("この期間のデータはありません。")


# -------------------------
# メインタイトル
# -------------------------
st.title("UniLife Optimizer - Web版")
st.caption(f"現在の表示期間：**{period}**")

# タブ：①追加 ②一覧 ③グラフ ④今日の提案
tab1, tab2, tab3, tab4 = st.tabs(["記録を追加", "記録一覧", "グラフ", "今日の提案"])


# -------------------------
# タブ1：記録を追加（ここは期間関係なく常に追加）
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
            st.success("✅ 記録を保存しました！\n※ 期間フィルタを変更すると今の期間にも反映されます。")
        else:
            st.error("カテゴリと内容は必須です。")


# -------------------------
# タブ2：記録一覧（期間フィルタ反映）
# -------------------------
with tab2:
    st.header("📋 記録一覧")

    if filtered_records:
        # 新しい順に表示
        sorted_records = sorted(filtered_records, key=lambda r: r["date"], reverse=True)

        for r in sorted_records:
            st.write(
                f"{r['date']} | {r['category']} | "
                f"{r['content']} | {r['minutes']}分"
            )

        # CSVダウンロード（表示期間の分だけ）
        csv_bytes = records_to_csv(sorted_records)

        st.download_button(
            label=f"📥 CSVとしてダウンロード（{period}）",
            data=csv_bytes,
            file_name=f"unilife_records_{period}.csv",
            mime="text/csv",
        )
    else:
        st.write(f"{period} の範囲には記録がありません。")


# -------------------------
# タブ3：グラフ（棒 or 円）（期間フィルタ反映）
# -------------------------
with tab3:
    st.header("📊 カテゴリ別の累計時間")

    if not filtered_records:
        st.write(f"{period} のデータがありません。")
    else:
        category_sum = get_category_sum(filtered_records)

        graph_type = st.radio(
            "グラフの種類を選んでください",
            ["棒グラフ", "円グラフ"],
            horizontal=True,
        )

        if graph_type == "棒グラフ":
            fig, ax = plt.subplots()
            ax.bar(category_sum.keys(), category_sum.values())
            ax.set_xlabel("カテゴリ")
            ax.set_ylabel("累計時間 [分]")
            ax.set_title(f"カテゴリ別 累計時間（{period}・棒グラフ）")
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
            ax.set_title(f"カテゴリ別の割合（{period}・円グラフ）")
            ax.axis("equal")
            st.pyplot(fig)


# -------------------------
# タブ4：今日の提案（期間フィルタ反映）
# -------------------------
with tab4:
    st.header("🎯 今日やるべきことの提案")

    if not filtered_records:
        st.write(f"{period} の範囲でまだ記録がありません。まずは何か1つ記録してみよう。")
    else:
        category_sum = get_category_sum(filtered_records)

        # 一番時間が少ないカテゴリを探す
        least_cat = min(category_sum, key=category_sum.get)
        least_minutes = category_sum[least_cat]

        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"カテゴリ別 累計時間（{period}）")
            for cat, mins in category_sum.items():
                st.write(f"- {cat}: {mins} 分")

        with col2:
            st.subheader("一番使えていないカテゴリ")
            st.metric(label="カテゴリ", value=least_cat)
            st.metric(label="累計時間（分）", value=least_minutes)

        st.markdown("---")
        st.subheader("💡 今日のおすすめアクション")

        # カテゴリ名に応じて軽く条件分岐（ここは好きにカスタム可）
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

        st.caption(
            "※ 選択中の期間（サイドバーの表示期間）に基づいて、"
            "カテゴリ別累計から一番弱いところを探しています。"
        )
