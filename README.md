# 📚 UniLife Optimizer
大学生活・資格勉強・部活の記録を  
**CLI / GUI / Web / Mobile（Kivy）** の4形態で管理できるアプリ。

- 学習・部活の記録  
- カテゴリ別の累計時間グラフ  
- 今日のおすすめアクション（レコメンド）  
- CSV出力（Excel対応）  
- スマホアプリ版（Kivy）での利用  
- Web版はスマホのホーム画面に追加すれば PWA として使える  

Python学習・アプリ開発・就活ポートフォリオに最適。

---

# ✨ Features（機能）

## ✔ 記録管理
- 日付  
- カテゴリ（例：ITパス、大学、部活など）  
- 内容  
- 勉強／活動時間（分）  
- 自動で `data.json` に保存

---

## ✔ グラフ機能
- **棒グラフ（カテゴリ別の累計時間）**  
- **円グラフ（カテゴリ別割合）**  
- GUI版・Web版・Mobile版で表示可能  
- Matplotlibを利用  
- スマホ版（Kivy）は PNG 保存して画面に表示

---

## ✔ 今日の提案（レコメンド）
カテゴリ別の累計時間から  
**「一番さぼっているカテゴリ」** を検出して  
今日やるべきことを提案する機能。

例：  
> 「ITパスの時間が一番少ないので、今日は30分だけ進めるのがおすすめです」

---

## ✔ CSV出力（Web版）
記録一覧タブから  
**1クリックでCSVをダウンロード**

- Excel（日本語環境）向けに `cp932` で出力  
- ダブルクリックで文字化けしない  
- グラフや分析に活用可能

---

## ✔ マルチUI対応（4形態）

### 🔹 1. CLI版
- ターミナルで操作  
- 最もシンプルなインターフェース  
- JSONに保存

---

### 🔹 2. GUI版（Tkinter）
- 実際のアプリのようなウィンドウで操作  
- 入力フォーム  
- 記録一覧  
- グラフ表示（別ウィンドウでMatplotlib表示）

---

### 🔹 3. Web版（Streamlit）
- ブラウザで動くアプリ  
- レスポンシブ対応  
- グラフ／レコメンド表示  
- スマホのホーム画面に追加で PWA 化可能

## 🌐 デモ（Web版）

Streamlitで動くデモはこちらから利用できます👇  
https://unilifeoptimizer.streamlit.app


---

### 🔹 4. Mobile版（Kivy）
- スマホアプリ風UI  
- スクロール可能な記録一覧  
- 棒グラフ・円グラフを PNG で表示  
- 日本語フォント（NotoSansJP）対応必須  
- Buildozerを使えばAPK作成も可能（後述）

---

# 🛠 技術スタック

| 機能 | 技術 |
|------|------|
| CLI | Python（標準入力） |
| GUI | Tkinter |
| Web | Streamlit / Matplotlib |
| Mobile | Kivy |
| データ保存 | JSON |
| グラフ生成 | Matplotlib |
| CSV出力 | csv + cp932 encoding |
| 日本語フォント（Kivy） | NotoSansJP |

---

# 📂 フォルダ構成（例）
project/
├── main.py # CLI版
├── gui.py # GUI版
├── web_app.py # Web版（Streamlit）
├── mobile_app.py # Kivyモバイル版
├── NotoSansJP-Regular.ttf # 日本語フォント（Kivy）
├── data.json # 記録データ
└── README.md

---

# 📦 インストール
pip install streamlit
pip install matplotlib
pip install kivy

---

# 🚀 実行方法

### CLI
python main.py

### GUI
python gui.py

### Web
streamlit run web_app.py

### Mobile
python mobile_app.py

---

# 📱 スマホアプリとして使う方法（おすすめ）
Web版（Streamlit）をデプロイして  
スマホで開いたら

### iPhone  
「共有」→「ホーム画面に追加」

### Android  
右上「…」→「ホーム画面に追加」

**→ アプリみたいに使える（PWA化）**

---
## 画面イメージ

### Web版 
![web](images/web1.png)
![web](images/web2.png)
![web](images/web3.png)
![web](images/web4.png)
![web](images/web5.png)


### GUI版 
![gui](images/gui1.png)
![gui](images/gui2.png)
![gui](images/gui3.png)
![gui](images/gui4.png)
![gui](images/gui5.png)

### APP版 
![app](images/app1.png)
![app](images/app2.png)


## ✅ TODO / Roadmap

- [x] CLI版の実装
- [x] GUI版（Tkinter）の実装
- [x] Web版（Streamlit）の実装
- [x] Mobile版（Kivy）の実装
- [x] グラフ機能（棒・円）
- [x] CSV出力機能（Excel対応）
- [ ] 期間フィルター（今日 / 週間 / 月間）
- [ ] ダークモード対応
- [ ] Web版のタグ管理
- [ ] GUI版の見た目改善
- [ ] Kivy版のタブUI
- [ ] ログイン機能の追加


# 📄 ライセンス
MIT License

---

# ✍ 作者コメント

Python学習のために  
**CLI → GUI → Web → モバイル**  
と段階的に成長できるよう構成した、マルチUIアプリです。

プログラミング学習だけでなく、  
実際の大学生活の記録管理ツールとしても使えます。

作成者: Ayaki

---


