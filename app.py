from flask import Flask, request, jsonify, send_file
from flask import render_template
from werkzeug.exceptions import BadRequest
import openai
import math
import csv

# Flask app initialization
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/api/generateQuestions', methods=['POST'])
def generate_questions():
    data = request.json
    input_text = data['inputText']
    api_key = data['apiKey']
    question_count = data['questionCount']

    # ここで問題を生成するロジックを実装します。

    return jsonify(questions)
openai.api_key = "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"
questions = []

# Split text into chunks
def split_text(text, max_chars=3000):
    split_texts = []
    while len(text) > max_chars:
        idx = text.rfind('.', 0, max_chars)
        if idx == -1:
            idx = max_chars
        split_texts.append(text[:idx + 1].strip())
        text = text[idx + 1:].strip()
    split_texts.append(text)
    return split_texts

def create_direct_questions(text, n):
    messages=[
     {"role": "system", "content":"You are a good NLP machine.You will return me pairs of question and answer,each question and each answer must be divided with \n, each pair of question and answer must be divided with \t."},
     {"role": "user", "content":"In Japanese, Extract 2 important parts to remember from the following text.And Create 2 simple, single-word or single-phrase  question and answer pair for the important part:\n\n"+"V-A ECMO，IMPELLAの適応は心原性ショックであり，心原性ショック状態にある，または前段階にある血行動態か否かの評価が必要である．心原性ショックは，適切な強心薬，血管作動薬などによる循環補助を行っても血行動態の異常と乳酸値上昇などの代謝異常，組織の低灌流の所見を認める状態であり，統一された詳細な定義はないが，血行動態の異常としては，30分以上にわたる収縮期血圧90 mmHg未満または基礎値より30 mmHg以上の低下と心係数2.2 L/分/m2未満（循環補助がない場合は1.8 L/分/m2未満）が臨床試験でよく用いられる．しかし，血圧は血管収縮反射により保たれている場合があること，組織低灌流をきたす心係数はAMIによるものか慢性心不全の増悪によるものかという病因や感染などの修飾因子によって異なること，慢性心不全では乳酸値と血行動態が乖離する場合があることなどから，これらの数値は絶対的なものではなく，臓器の低灌流所見とあわせて評価することが必要である"},
     {"role": "assistant", "content":"V-A ECMO，IMPELLAの適応はなにか？\n心原性ショック/t心原性ショックはどのように評価するか？数値を絶対的なものと考えず、臓器の低還流所見とあわせて評価する"},
     {"role": "user", "content":"In Japanese, Extract 3 important parts to remember from the following text.And Create 3 simple, single-word or single-phrase question and answer pair for the important part:\n\n"+"自然言語処理は、最終目標である「絵（文章）」を完成させるために、形態素解析：各パズルの色や構造情報を表す構文解析：各パズルの凹凸を確認してつなぎ合わせる意味解析：ひとかたまりのパズル群が全体のどこにいるのか確認する文脈解析：最終調整を行うなどの行程を経てジグソーパズルを組み立てていくものだと仮定します。まず処理を行う前準備として、機械可読目録とコーパスが必要になります。機械可読目録機械可読目録（MARC, MAchine-Readable Catalog）とは、書き言葉の書籍情報や関連情報を機械が読める形に置き換えた通信規格です。言い換えると、ロボットの目であり、文字を認識することそのものです。1960年に開発され、応用技術のひとつに図書館などの書籍検索システム「OPAC」があります。俗に自然言語処理用の「辞書」と定義され、ここで文字を機械が読み取れる規格に変換します。コーパスコーパスコーパス（Corpus）とは、自然言語の文章などの使用方法を構造化して大規模に集め、記録したものです。言い換えると、ロボットの頭脳であり、パズルの形状（構造）や色（品詞）を確認するものです。構造化した後、言語情報（動詞、形容詞などの品詞・統語構造）などのタグ付けをします。日本語では「言語全集」などと言われることもあります。コーパスは、この後解説する解析時に利用します。そしてここから、自然言語処理は主に4つの行程を踏まえて処理されます。形態素解析構文解析意味解析文脈解析段階ごとに詳しく説明していきます。1. 形態素解析まずは出来上がっているジグソーパズルをバラバラにしていきます。形態素解析とは、文章をそれぞれの意味を担う最小の単位（＝形態素）に分割し、それぞれに品詞など各種情報を振り分ける作業です。大小感覚は、文＞単語＞形態素という具合です。パズルゲームに置き換えると、各パズルの色や構造情報を表します。これにより、文章のなかにある形態素の意味をデータとして抽出することが可能になります。形態素解析は主に形態素解析エンジンを使って解析を行い、代表的なものとしては、無料で使えるMeCab, ChaSen, KyTeaや、商用で使われているRosette, IBM Watson, MARIMOなどが挙げられます。具体例として次の文を形態素解析してみましょう。"},
     {"role": "assistant", "content":"自然言語処理のおおまかな四つのプロセスはなにか？\n形態素解析、構文解析、意味解析、文脈解析\t自然言語の文章などの使用方法を構造化して大規模に集め、記録したものをなんというか？\nコーパス(Corpus)\t文章をそれぞれの意味を担う最小の単位に分割し、それぞれに品詞など各種情報を振り分ける作業をなんというか？\n形態素解析"},
     {"role": "user", "content": f"In Japanese, Extract {n} important parts to remember from the following text.And Create {n} simple, single-word or single-phrase questions and answers pairs for the important part:\n\n{text}"},
    ]
    try:
        summary_response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        result = summary_response['choices'][0]['message']['content'].strip()
        print(f"Output: {result}")
        resultQA=result.split('\t')
        for pair in resultQA:
            # '\n'が含まれているか確認
            if '\n' in pair:
                try:
                    question, answer = pair.split('\n', 1)
                    questions.append((question, answer.strip()))
                except ValueError:
                    print(f"Error splitting response into question and answer: {pair}")
            else:
                # '\n'が含まれていない場合、Answerに"失敗！"を追加
                questions.append((pair, "失敗！"))
        return questions 
    except Exception as e:
        print(f"Error occured: {e}")
        import traceback
        traceback.print_exc()  # Print the detailed traceback
        return "Error occured"
 

def create_csv(questions, output_file='output.csv'):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Question', 'Answer'])
        for pair in questions:
            try:
                # Try unpacking the pair into question and answer
                question, answer = pair
                csv_writer.writerow([question, answer])
            except ValueError:
                # If unpacking fails, use the entire pair as the question and set answer as "惜しかった！"
                csv_writer.writerow([pair, "惜しかった！"])

# Generate questions and return them in JSON format
@app.route('/api/generate-questions', methods=['POST'])
def generate_questions():
    data = request.get_json()
    try:
        text = data['text_input']
        n = data['number_input']
    except (TypeError, KeyError):
        raise BadRequest('Request body must be JSON with "text_input" and "number_input" fields')
    split_texts = split_text(text)
    m = len(split_texts)
    n_per_text = math.ceil(n / m)
    all_questions = []
    for split_text in split_texts:
        questions = create_direct_questions(split_text, n_per_text)
        all_questions.extend(questions)
    create_csv(all_questions)
    return jsonify(all_questions)

# Serve the CSV file
@app.route('/api/download-csv', methods=['GET'])
def download_csv():
    return send_file('output.csv', as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
