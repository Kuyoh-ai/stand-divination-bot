import anthropic

class Claude:
  def __init__(self, token):
    self.client = anthropic.Anthropic(
      api_key=token
    )

  def generate_profile(self, username, messages, icon_base64):
    # ユーザーのプロファイルを取得
    message = self.client.messages.create(
      model="claude-3-opus-20240229",
      max_tokens=1024,
      temperature=0.3,
      system='''
      人物のプロファイルを分析するのがあなたのタスクです。
      ユーザーのアイコンの雰囲気と発言からプロファイリングを行ってください。
      アニメキャラのアイコン＝アニメ好きなど簡単な分析にとらわれず、そのキャラクターの内面を想像して分析してください。
      出力は以下のフォーマットに従って返答してください。

      <format>
      名前：
      性格：
      嗜好：
      MBTI診断の分類：
      </format>
      ''',
      messages=[
        {
          "role": "user",
          "content": [
            {
              "type": "image",
              "source": {
                "type": "base64",
                "media_type": "image/png",
                "data": icon_base64,
              }
            },
            {
                "type": "text",
                "text": f"名前：{username}\n\n{messages}"
            }
          ]
        }
      ]
    )
    return message.content[0].text;

  def divination_stand(self, username, profile):
    # ユーザーのプロファイルを取得
    message = self.client.messages.create(
      model="claude-3-opus-20240229",
      max_tokens=1024,
      temperature=0.6,
      system='''あなたはジョジョの奇妙な冒険におけるスタンド能力の診断士です。
        ユーザーのプロフィールからユーザーが持っているスタンド能力を診断してください。
        診断結果は以下のフォーマットで出力してください。
        補足情報を書き込む場合はおばあちゃんの口調（～じゃ）で話し、二人称は「おぬし」としてください。

        <format>
        スタンド名：[そのスタンドの能力にあったスタンド名をカタカナでつける。楽曲名にちなむことが多い]
        タイプ：[スタンドの能力に合ったタイプを書く]
        能力：[スタンドが持つ特殊な能力について説明する]

        破壊力：[能力を基にA-Eの5段階で評価、攻撃力で評価する]
        スピード：[能力を基にA-Eの5段階で評価、機敏さで評価する]
        射程距離：[能力を基にA-Eの5段階で評価、能力の有効距離で評価する]
        持続力：[能力を基にA-Eの5段階で評価、燃費のよさで評価する]
        精密動作性：[能力を基にA-Eの5段階で評価、正確さ器用さで評価する]
        成長性：[能力を基にA-Eの5段階で評価、能力の拡張性、進化の可能性で評価する]
        </format>

        <type_example>
        以下はタイプの一例です。例であるため独自に作り出してもかまいません。
        ・近接パワー型…近距離での攻撃力の高いスタンドが分類される
        ・遠隔操作型…遠距離から支援を行うスタンドが分類される
        ・群体型…複数体のスタンドを生み出す能力が分類される
        </type_example>''',
      messages=[
        {
          "role": "user",
          "content": [
            {
                "type": "text",
                "text": f"名前：{username}\n性格：{profile}"
            }
          ]
        }
      ]
    )
    return message.content[0].text;