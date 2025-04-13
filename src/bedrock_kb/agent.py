from google.adk.agents import Agent

from .tools.bedrock_kb import bedrock_kb_tool

root_agent = Agent(
    model="gemini-2.0-flash-exp",
    name="root_agent",
    description="This is the root agent for the Bedrock KB project.",
    instruction="""質問に答える際には、可能な限り Amazon Bedrock Knowledge Base から情報を検索してください。

**ユーザーが特定のトピックについて質問した場合、'bedrock_kb_retrieval' ツールを使用して関連情報を取得してください。**

**もしツールが有用な情報を返した場合、その情報を使って詳細な回答を提供してください。**

**もしツールがエラーを返したり、関連情報が見つからなかった場合は、一般的な知識に基づいて回答し、情報が制限されていることを伝えてください。**

検索結果の情報源は常に明示してください。""",
    tools=[bedrock_kb_tool],
)
