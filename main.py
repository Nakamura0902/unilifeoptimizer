# UniLife Optimizer v0.2
# JSON保存対応版

import json
import os
from datetime import date
import matplotlib.pyplot as plt

DATA_FILE = "data.json"


def load_data():
    """アプリ起動時にJSONファイルを読み込む"""
    if not os.path.exists(DATA_FILE):
        return []  # ファイルがなければ空リスト

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []  # 壊れてても一旦空でOK


def save_data(records):
    """記録をJSONファイルに保存"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

def get_category_sum(records):
    """カテゴリ別の合計を返す"""
    category_sum = {}
    for r in records:
        cat = r["category"]
        category_sum[cat] = category_sum.get(cat, 0) + r["minutes"]
    return category_sum

def visualize_bar(records):
    if not records:
        print("まだ記録がありません。\n")
        return

    category_sum = get_category_sum(records)
    categories = list(category_sum.keys())
    minutes = list(category_sum.values())

    plt.figure()
    plt.bar(categories, minutes)
    plt.xlabel("category")
    plt.ylabel("time (minutes)")
    plt.title("category vs time (bar graph)")
    plt.tight_layout()
    plt.show()

def visualize_pie(records):
    if not records:
        print("まだ記録がありません。\n")
        return

    category_sum = get_category_sum(records)
    categories = list(category_sum.keys())
    minutes = list(category_sum.values())

    plt.figure()
    plt.pie(minutes, labels=categories, autopct="%1.1f%%", startangle=90)
    plt.title("category vs time (pie chart)")
    plt.axis("equal")  # 円を真円にする
    plt.show()


def graph_menu(records):
    while True:
        print("\n--- グラフメニュー ---")
        print("1) 棒グラフで見る")
        print("2) 円グラフで見る")
        print("3) 戻る")
        choice = input("番号を選んでください：").strip()

        if choice == "1":
            visualize_bar(records)
        elif choice == "2":
            visualize_pie(records)
        elif choice == "3":
            print("メインメニューに戻ります。\n")
            return
        else:
            print("1～3で選んでね。\n")


def get_todays_records(records):
    """今日の記録だけを抽出して返す"""
    today = date.today().isoformat()
    return [r for r in records if r["date"] == today]


def show_menu():
    print("===================================")
    print("   UniLife Optimizer v0.5")
    print("===================================")
    print("1) 記録を追加する")
    print("2) 記録を一覧表示する")
    print("3) 集計を見る")
    print("4) 今日やるべきことの提案を見る")
    print("5) グラフで学習状況を見る")
    print("6) 終了する")
    print("===================================")




def add_record(records):
    print("\n--- 新しい記録を追加 ---")

    today_str = date.today().isoformat()
    input_date = input(f"日付（Enterで今日: {today_str}）：").strip()
    if input_date == "":
        input_date = today_str

    print("種類例：ITパス / 大学 / 部活 / その他")
    category = input("種類：").strip()
    content = input("内容：").strip()

    while True:
        minutes_str = input("時間（分）：").strip()
        try:
            minutes = int(minutes_str)
            break
        except ValueError:
            print("数字で入力してね。")

    record = {
        "date": input_date,
        "category": category,
        "content": content,
        "minutes": minutes,
    }

    records.append(record)
    save_data(records)

    print("\n✅ 記録を保存しました！\n")


def show_records(records):
    print("\n--- 記録一覧（最新10件） ---")

    if not records:
        print("まだ記録がありません。\n")
        return

    # ▼ ここ追加：日付順にソート（新しい→古い）
    sorted_records = sorted(records, key=lambda r: r["date"], reverse=True)

    # ▼ ここ追加：直近10件だけ表示
    recent = sorted_records[:10]

    for i, r in enumerate(recent, start=1):
        print(f"[{i}] {r['date']} | {r['category']} | {r['content']} | {r['minutes']}分")

    print()

def suggest_today(records):
    print("\n--- 今日やるべきことの提案 ---")

    if not records:
        print("まだ記録がありません。まずは何か1つ記録してみよう！\n")
        return

    # カテゴリ別の累計時間を集計
    category_sum = get_category_sum(records)

    # 一番時間が少ないカテゴリを探す
    least_cat = min(category_sum, key=category_sum.get)
    least_minutes = category_sum[least_cat]

    print("\nこれまでの累計時間（カテゴリ別）：")
    for cat, mins in category_sum.items():
        print(f"  - {cat}: {mins} 分")

    print("\n👀 一番時間を使えていないのは…")
    print(f"➡ {least_cat}（{least_minutes} 分）")

    # カテゴリごとにちょっとだけコメント
    print("\n💡 今日のおすすめ：")
    if "IT" in least_cat or "パス" in least_cat:
        print("  ITパスポートの勉強を30分だけでもやっておくと、試験対策がかなり進むよ。")
    elif "大" in least_cat:  # 「大学」「大学の勉強」などをゆるく拾う
        print("  大学の授業の復習や、レポートを少しだけ進めておくと後が楽！")
    elif "部" in least_cat:
        print("  部活のための筋トレやストレッチ、フォーム研究を少しやるのもアリ。")
    else:
        print(f"  「{least_cat}」にあと30分くらい使ってみるとバランスが良くなりそう！")

    print()


def show_summary(records):
    print("\n--- 集計（今日・累計） ---")

    if not records:
        print("まだ記録がありません。\n")
        return

    # 今日だけの記録
    todays = get_todays_records(records)

    # 累計のカテゴリ別
    total_category = get_category_sum(records)





def main():
    print("UniLife Optimizer を起動中…")

    # 起動時に保存データ読み込み
    records = load_data()

    while True:
        show_menu()
        choice = input("番号を選んでください：").strip()

        if choice == "1":
            add_record(records)
        elif choice == "2":
            show_records(records)
        elif choice == "3":
            show_summary(records)
        elif choice == "4":
            suggest_today(records)
        elif choice == "5":
            graph_menu(records)
        elif choice == "6":
            print("終了します。おつかれ！")
            break
        else:
            print("1〜6で選んでね。\n")


if __name__ == "__main__":
    main()