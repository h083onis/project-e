import React from 'react';
import logo from './logo.svg';
import './App.css';
import axios from 'axios'
import { useEffect, useState } from 'react'

type PredictionData = {
  prediction: string;
  timestamp: string;
};

function App() {
  const [data, setData] = useState({prediction: '', timestamp: '' })
  const [error, setError] = useState<string | null>(null);  // error状態の定義
  const [refresh, setRefresh] = useState<boolean>(false);  // 更新用状態

  const fetchData = () => {
    axios
      .get('http://localhost:5001/prediction')
      .then((res) => {
        setData(res.data);
        setError(null);  // エラーメッセージをリセット
      })
      .catch((err) => {
        console.error('Error fetching data:', err);
        setError('データの取得に失敗しました');
      });
  };

  // 依存配列にrefreshを追加して、refreshが変更されるたびにuseEffectが実行される
  useEffect(() => {
    fetchData();  // データを取得する関数を呼び出し
  }, [refresh]); // refreshが変更されるたびに再実行

  // 更新ボタンのクリックイベントハンドラ
  const handleRefreshClick = () => {
    setRefresh((prev) => !prev);  // refreshの状態をトグル（切り替え）
  };

  if (error) {
    return (
      <div className="App">
        <h1>予測データ</h1>
        <p style={{ color: 'red' }}>{error}</p>
        <button onClick={handleRefreshClick}>更新</button> {/* 更新ボタン */}
      </div>
    );
  }

  return (
    <div className="App">
      {/* <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header> */}
      <h1>予測データ</h1>
      {data ? (
        <div>
          <p>
            <strong>予測値:</strong> {data.prediction}
          </p>
          <p>
            <strong>タイムスタンプ:</strong> {data.timestamp}
          </p>
        </div>
      ) : (
        <p>データを読み込み中...</p>
      )}
      <button onClick={handleRefreshClick}>更新</button> {/* 更新ボタン */}
    </div>
  );
}

export default App;
