from flask import Flask, render_template, request
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv(override=True)


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret")

# OpenAIクライアント
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/', methods=['GET', 'POST'])
def index():
    converted_text = None

    # ★追加：フォームの表示状態を保持するための変数
    original_text = ''
    selected_style = '上司'

    if request.method == 'POST':
        # ★編集：text/style を original_text/selected_style に入れる
        original_text = (request.form.get('text') or '').strip()
        selected_style  = (request.form.get('style') or '上司').strip()

        if original_text:
            # --- 敬語変換プロンプト（最小実装） ---
            prompt = f"""
対象: {selected_style}
以下の日本語を、対象にふさわしい敬語・文体・語彙・結びに直してください。
意味は変えず、冗長にせず、体裁のみ整えてください。
出力は変換後の文章のみ（説明や前置きは不要）。

原文:
{original_text}
"""

            try:
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "あなたは日本語のビジネス敬語の校正が得意なアシスタントです。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,
                )
                converted_text = (res.choices[0].message.content or "").strip()
            except Exception as e:
                converted_text = f"（変換に失敗しました: {e}）"
        else:
            converted_text = "（文章が空です）"
            
    # ★編集：original_text / selected_style をテンプレへ渡す
    return render_template(
            'index.html',
            converted_text=converted_text,
            original_text=original_text,
            selected_style=selected_style
        )
if __name__ == '__main__':
    app.run(debug=True)
