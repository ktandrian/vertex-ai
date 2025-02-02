# pylint: disable=invalid-name
"""
Demo for Google Gemini use case in hotel inventory management.
"""

import requests
import streamlit as st
import time
from decouple import config
from bs4 import BeautifulSoup
from google import genai
from google.genai import types

PROJECT_ID = config("PROJECT_ID", default="YOUR_PROJECT_ID")

# Vertex AI Configurations
client = genai.Client(
    vertexai=True,
    location="us-central1",
    project=PROJECT_ID,
)
generate_content_config = types.GenerateContentConfig(
    temperature = 1,
    top_p = 0.95,
    max_output_tokens = 8192,
    response_modalities = ["TEXT"],
    safety_settings = [types.SafetySetting(
        category="HARM_CATEGORY_HATE_SPEECH",
        threshold="OFF"
    ),types.SafetySetting(
        category="HARM_CATEGORY_DANGEROUS_CONTENT",
        threshold="OFF"
    ),types.SafetySetting(
        category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
        threshold="OFF"
    ),types.SafetySetting(
        category="HARM_CATEGORY_HARASSMENT",
        threshold="OFF"
    )],
)


def scrape(url: str):
    reviews_url = url + "kuchikomi/"
    headers = {
        'Referer': 'https://www.jalan.net/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    }
    
    # Get images
    html_1 = requests.get(url, headers=headers)
    html_1.encoding = html_1.apparent_encoding
    soup_1 = BeautifulSoup(html_1.text, 'html.parser')
    
    image_urls = []
    image_comps = soup_1.find_all("p", { 'class': 'jlnpc-slideImage__item--img' })
    for i in image_comps:
        image_urls.append(i.find('img')['src'])
    
    # Get reviews
    html = requests.get(reviews_url, headers=headers)
    html.encoding = html.apparent_encoding
    soup = BeautifulSoup(html.text, 'html.parser')
    
    # Get data
    hotel_name = soup.find("div", { 'id': 'yado_header_hotel_name' }).find('a').text
    reviews = []
    review_comps = soup.find_all('div', { 'class': "jlnpc-kuchikomiCassette__rightArea" })
    for i in review_comps:
        reviews.append({
            'title': (i.find('p', {'class':'jlnpc-kuchikomiCassette__lead'})).find('a').text,
            'body': (i.find('p', {'class':'jlnpc-kuchikomiCassette__postBody'})).text,
        })
    return { 'hotel_name': hotel_name, 'image_urls': image_urls, 'reviews': reviews }

def get_tags(hotel_name: str, image_urls: list, reviews: list):
    text1 = types.Part.from_text(text="""
<instructions>
あなたは、オンライン旅行代理店 (OTA) でホテル、ヴィラ、リゾートを強調し、宣伝するための説明的なタグを生成する専門の旅行ボットです。
これらのタグは、レビューの内容と画像に基づいて作成されます。
あなたのタスクは、関連する日本のホテル関連のタグを抽出し、各タグを、それぞれのソース (レビューまたは画像) 内の感情と詳細に基づいて1から5のスケールで評価することです。
あなたの応答は常に日本語でなければなりません。以下のタグ付けとスコアリングのルールに従ってください。
</instructions>

<tags_rules>
タグの形式: タグは日本語のenum形式でなければなりません（例：朝食、部屋の広さ）。タグ自体は中立でなければならず、感情はスコアで示されます（例：朝食を低いスコアで使用し、不満な朝食は使用しない）。具体的で明確である必要があります（例：ショッピングへの近さをショッピングの代わりに）。粒度が細かく、冗長にならないようにします（例：屋外スイミングプールをスイミングプールの代わりに。プールとスイミングプールは避けてください）。各タグは単独で成立するほど記述的である必要があります。

タグの内容: ホテルの施設、部屋の設備とアメニティ、ホテルのサービス、および部屋から見える特別なアトラクション*（特定のランドマークの眺めを含む）*など、画像と記事からのホテル関連のすべての側面を含めます。旅行の適合性、近さ、雰囲気、デザイン、ホテルの眺め、ユーザーの意図、および外部または季節のイベントを含めます。すべての旅行テーマとセグメント（例：ステイケーション、家族、ビジネス、ロマンチック、季節の旅行）を含めます。非常に具体的またはありそうもない外部イベント（例：テイラースイフトのコンサート）のタグは作成しないでください。

データソースの処理: 画像を視覚的な手がかりとして使用して、注目すべきランドマークや特定の眺めを含む詳細なホテルの特徴を特定します。仮定はしないでください。タグは事実に基づいた観察可能な情報に基づいていなければなりません。不一致の場合には、記事からの情報を優先してください。スコアを含む記事ごとにタグを生成します。すべての画像に対して一度タグを生成します。レビューのタグが記事または画像で説明または表示されている場合は、そのタグを生成します。

タグ生成ロジック: 複数のデータソースで言及または紹介されているタグを特定することを目指します。既存のリストにない、新しい関連タグを生成します。
</tags_rules>

<tags_scoring_rules>
スコアリング (1-5):
1: 非常に否定的/状態が悪い
2: 否定的
3: 中立
4: 肯定的
5: 素晴らしい

タグは、タグが由来するソースのみに基づいてスコアリングしてください。同じタグであっても、記事と画像ソースに対して別々のスコアを維持してください。
</tags_scoring_rules>

<output_format>
出力形式 (JSON):
```json
{{
    "hotel_name": "...",
    "tags": {{
        "image": [ 
            {{ "tag_name": "...", "tag_score": ... }}, 
            {{ "tag_name": "...", "tag_score": ... }} 
        ], 
        "review": [ 
            {{ "review_title":"...", "tag_name": "...", "tag_score": ... }}, 
            {{ "review_title":"...", "tag_name": "...", "tag_score": ... }} 
        ] 
    }} 
}}
```
</output_format>

Hotel name: {hotel_name_input}

Reviews: {reviews_input}

Images:""".format(hotel_name_input=hotel_name, reviews_input=reviews))
    
    image_parts = []
    for i in image_urls:
        image_parts.append(types.Part.from_uri(file_uri=i, mime_type="image/jpeg"))

    model = "gemini-2.0-flash-exp"
    contents = [
        types.Content(
            role="user",
            parts=[
                text1,
                *image_parts,
            ]
        )
    ]
    resp = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )
    return resp.text

def get_top_tags(hotel_name, tags):
    text1 = types.Part.from_text(text="""
<instruction>
あなたは、オンライン旅行代理店（OTA）向けの旅行ボットで、ホテル、ヴィラ、リゾートの最も魅力的なセールスポイントを特定することに特化しています。あなたのタスクは、レビューから抽出されたユーザー生成のタグのリストを分析し、ホテルの独自の価値提案を最もよく表し、潜在的な顧客を予約に誘うトップ5のタグを選択することです。選択されたこれらのタグは、モバイルアプリ内の商品カードにラベルとして表示されます。ホテルを特別なものにする本質を捉えることを目指し、際立っていて望ましい特徴を強調するタグを優先してください。ゲストエクスペリエンス、アメニティ、ロケーションの利点、全体的な雰囲気などの要素を考慮してください。より具体的で影響力のある代替案が存在する場合は、一般的なタグの選択を避けてください。
</instruction>

<output_format>
出力は、次のJSON形式で記述してください。
{{
    "hotel_name": "...",
    "tags": {{
        "tag_1": "...",
        "tag_2": "...",
        "tag_3": "...",
        "tag_4": "...",
        "tag_5": "..."
    }}
}}
JSONの結果のみを出力し、マークダウン形式や余分なテキストは含めないでください。出力タグが入力タグと同じ大文字の列挙形式であることを確認してください。
</output_format>

Hotel name: {hotel_name_input}
Tags:
{tags_input}
""".format(hotel_name_input=hotel_name, tags_input=tags))
    model = "gemini-2.0-flash-exp"
    contents = [
        types.Content(
            role="user",
            parts=[
                text1,
            ]
        )
    ]
    resp = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )
    return resp.text
    

st.set_page_config(page_title="Hotel Tags", page_icon="🏷️")
st.title("ホテルタグ | Hotel Tags")
st.markdown(
    "Google Vertex AI と Gemini モデルを搭載した究極のホテルタグ ジェネレーター。"
)
st.markdown(
    "_The ultimate hotel tag generator powered by Google Vertex AI and Gemini model._"
)

st.divider()

platform = st.selectbox(
    "プラットフォーム _Platform_",
    ["Jalan (www.jalan.net)"]
)

url = st.text_input("URL", placeholder="https://www.jalan.net/yad306452")

if st.button("タグを生成する _Generate Tags_", type="primary"):
    if url:
        with st.status("Generating tags...", expanded=True) as status:
            s_time = time.time()
            # Scraping
            st.write(f"Getting information from {url}.")
            data = scrape(url)
            hotel_name = data['hotel_name']
            image_urls = data['image_urls']
            reviews = data['reviews']
            
            # Tagging
            st.write("Generating tags from reviews and images.")
            tags_resp = get_tags(hotel_name, image_urls, reviews)
            
            # Top tags
            st.write("Getting top tags from generated tags")
            top_tags_resp = get_top_tags(hotel_name, tags_resp)
            status.update(
                label=f"Tags generation completed in {round(time.time() - s_time, 3)}s.", state="complete", expanded=False
            )
        
        st.write(top_tags_resp)
        
        with st.expander("All generated tags"):
            st.write(tags_resp)
        col1, col2, col3 = st.columns(3)
            
        # Display the images in 3 columns. If there are more than 3 images, divide them
        for i in range(len(image_urls)):
            if i % 3 == 0:
                col1.image(image_urls[i])
            elif i % 3 == 1:
                col2.image(image_urls[i])
            else:
                col3.image(image_urls[i])
    else:
        st.warning("Please enter a URL.")
