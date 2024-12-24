import React, { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [crowdLevel, setCrowdLevel] = useState(55); // 初期値は0%
  const [animatedCrowdLevel, setAnimatedCrowdLevel] = useState(0);
  const [prediction, setPrediction] = useState(0);
  const [animatedPrediction, setAnimatedPrediction] = useState(0);

  const crowdStatus =
    animatedCrowdLevel <= 33
      ? "比較的空いています"
      : animatedCrowdLevel <= 66
      ? "少し混雑しています"
      : "かなり混雑しています";

  // 色の計算ロジック
  const calculateColor = (level: number) => {
    if (level <= 33) return "#34A853"; // 緑
    if (level <= 66) return "#ee7800"; // オレンジ
    return "#FF0000"; // 赤
  };

  // 数値アニメーションの処理
  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (animatedCrowdLevel < crowdLevel) {
      interval = setInterval(() => {
        setAnimatedCrowdLevel((prev) => Math.min(prev + 1, crowdLevel));
      }, 20);
    }
    return () => clearInterval(interval);
  }, [crowdLevel]);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (animatedPrediction < prediction) {
      interval = setInterval(() => {
        setAnimatedPrediction((prev) => Math.min(prev + 1, prediction));
      }, 20);
    }
    return () => clearInterval(interval);
  }, [prediction]);

  // データ更新時の処理
  const handleUpdate = () => {
    const newCrowdLevel = Math.floor(Math.random() * 101); // 0〜100%のランダム値
    setCrowdLevel(newCrowdLevel);
    setPrediction(Math.floor(newCrowdLevel * 1.2)); // 仮の予測人数
    setAnimatedCrowdLevel(0); // アニメーション用の数値をリセット
    setAnimatedPrediction(0);
  };

  return (
    <div className="container">
      <header className="header">
        <img src="/logo.png" alt="PALTO-AI Logo" className="logo" />
        <button className="Btn" onClick={handleUpdate}>
          <div className="sign">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              width="30"
              height="30"
            >
              <path
                d="M12 4V1L8 5l4 4V6c3.31 0 6 2.69 6 6 0 1.01-.25 1.97-.7 2.8l1.46 1.46C19.54 15.03 20 13.57 20 12c0-4.42-3.58-8-8-8zm0 14c-3.31 0-6-2.69-6-6 0-1.01.25-1.97.7-2.8L5.24 7.74C4.46 8.97 4 10.43 4 12c0 4.42 3.58 8 8 8v3l4-4-4-4v3z"
                fill="#000000"
              />
            </svg>
          </div>
          <div className="text">Update</div>
        </button>
      </header>

      <main className="content">
        <div className="crowd-status">
          <div className="crowd-icon">
            <div className="circle">
              <svg className="progress-ring" width="300" height="300">
                <circle
                  className="progress-ring__circle"
                  cx="150"
                  cy="150"
                  r="140"
                  fill="none"
                  stroke={calculateColor(animatedCrowdLevel)}
                  strokeWidth="13"
                  strokeDasharray="879" // 円周の長さ（2 * π * r）
                  strokeDashoffset={879 - (879 * animatedCrowdLevel) / 100}
                  style={{ transition: "stroke-dashoffset 1.5s ease, stroke 1.5s ease" }}
                />
              </svg>
              <div className="circle2">
                <div className="group-icon">
                <div className="person left">
                  <div
                    className="head"
                    style={{
                      backgroundColor: calculateColor(animatedCrowdLevel),
                      transition: "background-color 1.5s ease",
                    }}
                  ></div>
                  <div
                    className="body"
                    style={{
                      backgroundColor: calculateColor(animatedCrowdLevel),
                      transition: "background-color 1.5s ease",
                    }}
                  ></div>
                </div>
                <div className="person center">
                  <div
                    className="head"
                    style={{
                      backgroundColor: calculateColor(animatedCrowdLevel),
                      transition: "background-color 1.5s ease",
                    }}
                  ></div>
                  <div
                    className="body"
                    style={{
                      backgroundColor: calculateColor(animatedCrowdLevel),
                      transition: "background-color 1.5s ease",
                    }}
                  ></div>
                </div>
                <div className="person right">
                  <div
                    className="head"
                    style={{
                      backgroundColor: calculateColor(animatedCrowdLevel),
                      transition: "background-color 1.5s ease",
                    }}
                  ></div>
                  <div
                    className="body"
                    style={{
                      backgroundColor: calculateColor(animatedCrowdLevel),
                      transition: "background-color 1.5s ease",
                    }}
                  ></div>
                </div>
                </div>
              </div>
            </div>
          </div>
          <div className="status-container">
            <div className="status-box">
              <div className="status-value">
                <span>{animatedCrowdLevel}<span className="unit">%</span></span>
              </div>
              <div className="status-label">
                <span>ただいまの混雑度</span>
              </div>
            </div>

            <div className="status-box">
              <div className="status-value">
                <span className="status-text">{crowdStatus}</span>
              </div>
              <div className="status-label">
                <span>ただいまの混雑状況</span>
              </div>
            </div>

            <div className="status-box">
              <div className="status-value">
                <span>{animatedPrediction}<span className="unit">人</span></span>
              </div>
              <div className="status-label">
                <span>予測人数</span>
              </div>
            </div>
          </div>
        </div>
      </main>

      <footer className="footer">
        <p>現在時刻：{new Date().toLocaleString()}</p>
      </footer>
    </div>
  );
}

export default App;
