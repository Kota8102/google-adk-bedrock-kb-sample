import os
from typing import Dict, List, Any

import boto3
from google.adk.tools import FunctionTool


def get_bedrock_client():
    """Bedrockクライアントを初期化して返します。"""
    region = os.environ.get("AWS_REGION")
    return boto3.client("bedrock-agent-runtime", region_name=region)


def validate_environment():
    """必要な環境変数が設定されているか検証します。"""
    knowledge_base_id = os.environ.get("KNOWLEDGE_BASE_ID")
    if knowledge_base_id is None:
        raise ValueError("Environment variable KNOWLEDGE_BASE_ID is not set")
    return knowledge_base_id


def format_retrieval_results(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """APIレスポンスから検索結果を抽出してフォーマットします。"""
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

        results.append({
            "content": content,
            "source": source,
            "score": score,
            "metadata": metadata,
        })
    
    return results


def bedrock_kb_retrieval(query: str) -> Dict[str, Any]:
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
                "error_message": エラーメッセージ（エラー発生時のみ）
            }
    """
    try:
        # 環境変数の検証
        knowledge_base_id = validate_environment()
        
        # Bedrockクライアントの初期化
        bedrock_runtime = get_bedrock_client()

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
        results = format_retrieval_results(response)

        return {
            "status": "success",
            "results": results,
        }

    except ValueError as e:
        # 環境変数関連のエラー
        return {
            "status": "error",
            "results": [],
            "error_message": str(e)
        }
    except Exception as e:
        # その他の例外
        error_msg = f"検索中にエラーが発生しました: {str(e)}"
        return {
            "status": "error",
            "results": [],
            "error_message": error_msg
        }


bedrock_kb_tool = FunctionTool(func=bedrock_kb_retrieval)