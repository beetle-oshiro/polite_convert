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

    # フォームの表示状態を保持するための変数
    original_text = ''
    selected_style = 'business'

    if request.method == 'POST':
        original_text = (request.form.get('text') or '').strip()
        selected_style = (request.form.get('style') or 'business').strip()

        if original_text:
            # スタイルごとの指示文
            style_instructions = {
                "business": """
相手は上司や取引先です。
失礼のない、自然で丁寧なビジネス文にしてください。
敬語をしっかり使い、ややフォーマル寄りにしてください。
ただし、堅すぎて不自然な表現にはしないでください。
メールや業務連絡でそのまま使える文章にしてください。
""",
                "polite": """
文章を正しい日本語で、自然で読みやすい丁寧な文にしてください。
文法や語尾、言い回しを整えてください。
必要以上に堅くせず、一般的で自然な丁寧文にしてください。
読みやすく、落ち着いた印象の文章にしてください。
""",
                "casual": """
親しい相手に向けた、やわらかいカジュアルな文章にしてください。
少しフレンドリーな雰囲気を含めてください。
堅い敬語は使わず、自然で話しやすい雰囲気にしてください。
ただし、乱暴すぎる表現や失礼な表現は避けてください。
友達や親しい同僚とのチャットで使えるくらいの自然な文にしてください。
""",
                "youth": """
若者同士の会話っぽい、かなり今どきの文章にしてください。
流行語、軽いノリ、テンション感、若者っぽい言い回しを適度に入れてください。
少し大げさなくらい「今の若者が使いそう」な表現に寄せてください。
ただし、意味は変えないでください。
不自然に壊れすぎた日本語にはせず、読む人が意味を理解できる範囲にしてください。
極端なネットスラング、攻撃的表現、不快な表現は避けてください。
同じ表現を何度も繰り返さず、若者っぽさがちゃんと伝わる文にしてください。
"""
            }

            selected_instruction = style_instructions.get(
                selected_style,
                style_instructions["polite"]
            )

            prompt = f"""
以下の日本語を、指定されたスタイルに合わせて自然に書き換えてください。
意味や要点は変えず、文章表現だけを整えてください。
出力は変換後の文章のみで、説明や前置きは不要です。

【共通ルール】
・原文の意味は変えない
・長すぎる文章にしない
・1回読んで自然に伝わる文章にする
・スタイルごとの差がはっきり分かるようにする

【変換スタイル】
{selected_instruction}

【原文】
{original_text}
"""

            try:
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "あなたは日本語の文章校正と文体変換が得意なアシスタントです。指示されたスタイルに合わせて、自然で分かりやすい日本語に整えてください。"
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.7,
                )
                converted_text = (res.choices[0].message.content or "").strip()

            except Exception as e:
                converted_text = f"（変換に失敗しました: {e}）"

        else:
            converted_text = "（文章が空です）"

    return render_template(
        'index.html',
        converted_text=converted_text,
        original_text=original_text,
        selected_style=selected_style
    )


if __name__ == '__main__':
    app.run(debug=True)