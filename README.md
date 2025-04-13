# Google ADK + Amazon Bedrock KB サンプル

Google Agent Development Kit (ADK)を使用して、Amazon Bedrockのナレッジベース機能を活用するマルチツールエージェントのお試しサンプルです。このプロジェクトは開発者が両サービスの連携方法を学ぶための簡易的なサンプルとして作成されました。

## 主な機能

- Amazon Bedrock Knowledge Basesからの情報検索
- 基本的な天気情報と時間情報の提供（クイックスタート用サンプル）
- Google ADKを使用したエージェント実装

## 前提条件

- Python 3.13以上
- AWS アカウントとAmazon Bedrockへのアクセス権
- Amazon Bedrock Knowledge Baseの設定済み
- Google ADK

## インストール方法

1. リポジトリをクローンします

```bash
git clone https://github.com/yourusername/google-adk-bedrock-kb-sample.git
cd google-adk-bedrock-kb-sample
```

2. uvを使用して依存関係をインストールします

```bash
uv sync
```

## 環境変数の設定

このプロジェクトを実行するには、以下の環境変数を設定する必要があります：

- `KNOWLEDGE_BASE_ID`: Amazon Bedrock Knowledge BaseのID
- `AWS_REGION`: AWSリージョン（例: `us-east-1`）

### .envファイルの設定

プロジェクトのルートディレクトリに`.env`ファイルを作成し、以下のように環境変数を設定します：

```bash
# .env
KNOWLEDGE_BASE_ID=your-knowledge-base-id
AWS_REGION=us-east-1

# AWS認証情報（必要に応じて）
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
```

## プロジェクト構造

```bash
google-adk-bedrock-kb-sample/
├── pyproject.toml        # プロジェクト設定ファイル
├── README.md             # このファイル
├── src/
│   ├── bedrock_kb/       # Bedrock KB関連のコード
│   │   ├── __init__.py
│   │   ├── agent.py      # Bedrock KBエージェントの定義
│   │   └── tools/
│   │       ├── __init__.py
│   │       └── bedrock_kb.py  # Bedrock KB検索ツール
│   └── quick_start/      # クイックスタート用のコード
│       ├── __init__.py
│       └── agent.py      # 天気・時間エージェントの定義
```

### 主要なファイルの説明

- `src/bedrock_kb/agent.py`: Amazon Bedrock Knowledge Basesを使用するエージェントを定義
- `src/bedrock_kb/tools/bedrock_kb.py`: Bedrock Knowledge Basesから情報を検索するツール

## ライセンス

このプロジェクトは[MITライセンス](LICENSE)の下で公開されています。
