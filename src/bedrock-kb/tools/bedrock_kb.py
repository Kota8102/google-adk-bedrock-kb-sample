import os

import boto3
from google.adk.tools import FunctionTool


def bedrock_kb_retrieval(query: str) -> dict:
    """Amazon Bedrock Knowledge Basesから情報を検索します。

    ユーザーが特定の情報やドキュメントについて質問した場合にこのツールを使用してください。
    ナレッジベースに保存されている情報に基づいて回答を提供します。

    Args:
        query (str): 検索クエリ。ユーザーの質問や検索したい内容。

    Returns:
        dict: 検索結果を含む辞書。以下の形式：
            {
                "status": "success" または "error",
                "results": [
                    {
                        "content": "取得したコンテンツ",
                        "source": "情報のソース",
                        "score": 検索スコア,
                        "metadata": {属性: 値, ...}
                    },
                    ...
                ],
                "error_message": エラーが発生した場合のメッセージ
            }

    """
    knowledge_base_id = os.environ.get("KNOWLEDGE_BASE_ID")
    if knowledge_base_id is None:
        raise ValueError("Environment variable KNOWLEDGE_BASE_ID is not set")

    try:
        # Bedrockクライアントの初期化
        bedrock_runtime = boto3.client(
            "bedrock-agent-runtime", region_name=os.environ.get("AWS_REGION")
        )

        # 検索パラメータの設定
        retrieve_params = {
            "knowledgeBaseId": knowledge_base_id,
            "retrievalQuery": {
                "text": query,
            },
            "retrievalConfiguration": {
                "vectorSearchConfiguration": {
                    "numberOfResults": 7,
                },
            },
        }

        # 検索を実行
        response = bedrock_runtime.retrieve(**retrieve_params)

        # 結果をフォーマット
        results = []
        for result in response.get("retrievalResults", []):
            content = result.get("content", {}).get("text", "")
            source = result.get("location", {}).get("s3Location", {}).get("uri", "不明")
            score = result.get("score", 0)

            # メタデータの抽出
            metadata = {}
            for attr in result.get("metadata", {}).get("attributes", []):
                key = attr.get("key", "")
                value = attr.get("value", {}).get("text", "")
                if key and value:
                    metadata[key] = value

            results.append(
                {
                    "content": content,
                    "source": source,
                    "score": score,
                    "metadata": metadata,
                }
            )

        return {
            "status": "success",
            "results": results,
        }

    except Exception as e:
        return {
            "status": "error",
            "results": [],
            "error_message": f"検索中にエラーが発生しました: {e!s}",
        }


# FunctionToolとしてラップ
bedrock_kb_tool = FunctionTool(func=bedrock_kb_retrieval)
