from django.shortcuts import render
from django.http import HttpResponse
import os
import markdown

def view_memo(request):
    """MEMO_20251010.mdを表示するビュー"""
    memo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'md', 'MEMO_20251010.md')

    try:
        with open(memo_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # MarkdownをHTMLに変換
        html_content = markdown.markdown(
            content,
            extensions=['fenced_code', 'tables', 'codehilite']
        )

        # シンプルなHTMLテンプレート
        html = f"""
        <!DOCTYPE html>
        <html lang="ja">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>2025年10月10日の変更履歴</title>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 900px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    background-color: white;
                    padding: 40px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #2c3e50;
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 10px;
                }}
                h2 {{
                    color: #34495e;
                    margin-top: 30px;
                    border-bottom: 2px solid #ecf0f1;
                    padding-bottom: 8px;
                }}
                h3 {{
                    color: #546e7a;
                    margin-top: 20px;
                }}
                code {{
                    background-color: #f8f9fa;
                    padding: 2px 6px;
                    border-radius: 3px;
                    font-family: 'Courier New', monospace;
                    color: #e74c3c;
                }}
                pre {{
                    background-color: #f8f9fa;
                    padding: 15px;
                    border-radius: 5px;
                    overflow-x: auto;
                    border-left: 4px solid #3498db;
                }}
                pre code {{
                    background-color: transparent;
                    color: #333;
                }}
                ul, ol {{
                    padding-left: 25px;
                }}
                li {{
                    margin: 8px 0;
                }}
                strong {{
                    color: #2c3e50;
                }}
                .back-link {{
                    display: inline-block;
                    margin-bottom: 20px;
                    padding: 8px 16px;
                    background-color: #3498db;
                    color: white;
                    text-decoration: none;
                    border-radius: 4px;
                }}
                .back-link:hover {{
                    background-color: #2980b9;
                }}
                blockquote {{
                    border-left: 4px solid #3498db;
                    padding-left: 20px;
                    margin-left: 0;
                    color: #666;
                    font-style: italic;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <a href="/" class="back-link">← トップページに戻る</a>
                {html_content}
            </div>
        </body>
        </html>
        """

        return HttpResponse(html)

    except FileNotFoundError:
        return HttpResponse(
            "<h1>エラー</h1><p>MEMO_20251010.mdファイルが見つかりません。</p>",
            status=404
        )
