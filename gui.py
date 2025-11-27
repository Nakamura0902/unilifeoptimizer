import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import date
import matplotlib.pyplot as plt


DATA_FILE = "data.json"

# データ読み込み
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# データ保存
def save_data(records):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

def get_category_sum(records):
    """カテゴリ別の合計時間を辞書で返す"""
    category_sum = {}
    for r in records:
        cat = r["category"]
        category_sum[cat] = category_sum.get(cat, 0) + r["minutes"]
    return category_sum

# メインウィンドウ
class UniLifeApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("UniLife Optimizer - GUI版")
        self.geometry("400x300")

        self.records = load_data()

        label = tk.Label(self, text="UniLife Optimizer GUI版", font=("Arial", 16))
        label.pack(pady=20)

        btn_add = tk.Button(self, text="記録を追加する", command=self.add_record_window)
        btn_add.pack(pady=10)

        btn_show = tk.Button(self, text="記録一覧を見る", command=self.show_records_window)
        btn_show.pack(pady=10)

        btn_graph = tk.Button(self, text="グラフで見る", command=self.graph_menu)
        btn_graph.pack(pady=10)


    # 記録追加の小窓
    def add_record_window(self):
        win = tk.Toplevel(self)
        win.title("記録を追加")
        win.geometry("300x250")

        tk.Label(win, text="カテゴリ").pack()
        category = tk.Entry(win)
        category.pack()

        tk.Label(win, text="内容").pack()
        content = tk.Entry(win)
        content.pack()

        tk.Label(win, text="時間（分）").pack()
        minutes = tk.Entry(win)
        minutes.pack()

        def save():
            try:
                minutes_val = int(minutes.get())
            except:
                messagebox.showerror("エラー", "時間は数字で入力して！")
                return

            record = {
                "date": date.today().isoformat(),
                "category": category.get(),
                "content": content.get(),
                "minutes": minutes_val
            }
            self.records.append(record)
            save_data(self.records)
            messagebox.showinfo("保存完了", "記録を保存したよ！")
            win.destroy()

        tk.Button(win, text="保存", command=save).pack(pady=10)

    # 一覧表示
    def show_records_window(self):
        win = tk.Toplevel(self)
        win.title("記録一覧")
        win.geometry("350x400")

        for r in self.records:
            tk.Label(win, text=f"{r['date']} | {r['category']} | {r['content']} | {r['minutes']}分").pack()
            
    def graph_menu(self):
        if not self.records:
            messagebox.showinfo("情報", "まだ記録がありません。先に記録を追加してね。")
            return

        win = tk.Toplevel(self)
        win.title("グラフメニュー")
        win.geometry("250x180")

        tk.Label(win, text="どのグラフで見る？").pack(pady=10)

        tk.Button(win, text="棒グラフ", command=lambda: self.show_bar()).pack(pady=5)
        tk.Button(win, text="円グラフ", command=lambda: self.show_pie()).pack(pady=5)

    def show_bar(self):
        if not self.records:
            return

        category_sum = get_category_sum(self.records)
        categories = list(category_sum.keys())
        minutes = list(category_sum.values())

        plt.figure()
        plt.bar(categories, minutes)
        plt.xlabel("category")
        plt.ylabel("time (minutes)")
        plt.title("category vs time (bar graph)")
        plt.tight_layout()
        plt.show()

    def show_pie(self):
        if not self.records:
            return

        category_sum = get_category_sum(self.records)
        categories = list(category_sum.keys())
        minutes = list(category_sum.values())

        plt.figure()
        plt.pie(minutes, labels=categories, autopct="%1.1f%%", startangle=90)
        plt.title("category vs time (pie chart)")
        plt.axis("equal")
        plt.show()

if __name__ == "__main__":
    app = UniLifeApp()
    app.mainloop()
