# ベースイメージとして公式のNode.jsイメージを使用
FROM node:18

# 作業ディレクトリを作成
WORKDIR /app

# パッケージファイルをコンテナにコピー
COPY package*.json ./

# 依存関係をインストール
RUN npm install

# プロジェクトファイルをすべてコピー
COPY . .

# Reactアプリの開発サーバーを起動
CMD ["npm", "start"]

# デフォルトで使用するポート
EXPOSE 3000
