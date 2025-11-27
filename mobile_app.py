
import json
import os
from datetime import date
import matplotlib.pyplot as plt
from kivy.uix.image import Image
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

DATA_FILE = "data.json"


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

class UniLifeRoot(BoxLayout):
    def show_pie_graph(self, instance):
        if not self.records:
            return

        # カテゴリ別合計
        category_sum = get_category_sum(self.records)
        categories = list(category_sum.keys())
        minutes = list(category_sum.values())

        # matplotlib 円グラフ → PNG
        plt.figure(figsize=(15, 15))
        plt.pie(minutes, labels=categories, autopct="%1.1f%%", startangle=90)
        plt.title("category vs. total time (minutes)")
        plt.axis("equal")
        plt.tight_layout()

        graph_path = "pie_graph.png"
        plt.savefig(graph_path, dpi=300)
        plt.close()

        # 画面（レイアウト作成）
        pie_screen = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # グラフ画像表示
        pie_screen.add_widget(Image(source=graph_path))

        # 戻るボタン
        back_btn = Button(text="back", size_hint_y=None, height=40)
        back_btn.bind(on_press=lambda x: self.remove_widget(pie_screen))

        pie_screen.add_widget(back_btn)

        # 画面追加
        self.add_widget(pie_screen)

    def show_graph(self, instance):
        if not self.records:
            return

        # カテゴリ別合計
        category_sum = get_category_sum(self.records)
        categories = list(category_sum.keys())
        minutes = list(category_sum.values())

        # matplotlibでPNG保存
        plt.figure(figsize=(15, 15))
        plt.bar(categories, minutes)
        plt.xlabel("category")
        plt.ylabel("times (minutes)")
        plt.title("category vs. total time (minutes)")
        plt.tight_layout()

        graph_path = "graph.png"
        plt.savefig(graph_path, dpi=300)
        plt.close()

        # 新しい画面を作る
        graph_screen = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # 画像表示
        graph_screen.add_widget(Image(source=graph_path))

        # 戻るボタン
        back_btn = Button(text="back", size_hint_y=None, height=40)
        back_btn.bind(on_press=lambda x: self.remove_widget(graph_screen))

        graph_screen.add_widget(back_btn)

        # メイン画面に追加
        self.add_widget(graph_screen)

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=10, spacing=10, **kwargs)

        self.records = load_data()

        # タイトル
        self.add_widget(Label(text="UniLife Optimizer - Mobile", font_size=24, size_hint_y=None, height=40))

        # 入力エリア
        input_box = BoxLayout(orientation="vertical", size_hint_y=None, height=180, spacing=5)

        self.category_input = TextInput(hint_text="category(english)", multiline=False)
        self.content_input = TextInput(hint_text="content(english)", multiline=False)
        self.minutes_input = TextInput(hint_text="time(minute)(english)", multiline=False, input_filter="int")

        input_box.add_widget(self.category_input)
        input_box.add_widget(self.content_input)
        input_box.add_widget(self.minutes_input)

        save_button = Button(text="save", size_hint_y=None, height=40)
        save_button.bind(on_press=self.on_save)

        input_box.add_widget(save_button)

        self.add_widget(input_box)

        # 記録一覧（スクロール）
        self.records_area = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.records_area.bind(minimum_height=self.records_area.setter("height"))
        # グラフを見るボタン
        graph_button = Button(text="bar chart", size_hint_y=None, height=40)
        graph_button.bind(on_press=self.show_graph)
        self.add_widget(graph_button)

        # 円グラフを見るボタン
        pie_button = Button(text="pie chart", size_hint_y=None, height=40)
        pie_button.bind(on_press=self.show_pie_graph)
        self.add_widget(pie_button)

        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.records_area)
        self.add_widget(scroll)


        # 初期表示
        self.refresh_records_view()

    def on_save(self, instance):
        cat = self.category_input.text.strip()
        content = self.content_input.text.strip()
        mins_text = self.minutes_input.text.strip()

        if not cat or not content or not mins_text:
            # 本当はポップアップとかでエラーを出したいが、まずは簡単にスルー
            return

        try:
            mins = int(mins_text)
        except ValueError:
            return

        record = {
            "date": date.today().isoformat(),
            "category": cat,
            "content": content,
            "minutes": mins,
        }

        self.records.append(record)
        save_data(self.records)

        # 入力欄クリア
        self.category_input.text = ""
        self.content_input.text = ""
        self.minutes_input.text = ""

        # 再描画
        self.refresh_records_view()

    def refresh_records_view(self):
        # いったん全部消す
        self.records_area.clear_widgets()

        # 新しい順に表示
        sorted_records = sorted(self.records, key=lambda r: r["date"], reverse=True)

        for r in sorted_records:
            text = f"{r['date']} | {r['category']} | {r['content']} | {r['minutes']}minutes"
            lbl = Label(text=text, size_hint_y=None, height=30, halign="left", valign="middle")
            lbl.bind(size=lambda inst, _: setattr(inst, "text_size", inst.size))
            self.records_area.add_widget(lbl)


class UniLifeMobileApp(App):
    def build(self):
        return UniLifeRoot()


if __name__ == "__main__":
    UniLifeMobileApp().run()
