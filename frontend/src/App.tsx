import React, { useState, useEffect } from "react";
import axios from 'axios';
import "./App.css";

function App() {
  const [crowdLevel, setCrowdLevel] = useState(55);
  const [animatedCrowdLevel, setAnimatedCrowdLevel] = useState(0);
  const [prediction] = useState(0);
  const [animatedPrediction, setAnimatedPrediction] = useState(0);
  const [data, setData] = useState({prediction: '', timestamp: '' });
  const [windowWidth, setWindowWidth] = useState(window.innerWidth);

  const fetchData = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5001/prediction');
      setData(response.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  useEffect(() => {
    fetchData();

    // ウィンドウサイズの変更を監視
    const handleResize = () => {
      setWindowWidth(window.innerWidth);
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const crowdStatus =
    animatedCrowdLevel <= 33
      ? "比較的空いています"
      : animatedCrowdLevel <= 66
      ? "少し混雑しています"
      : "かなり混雑しています";

  const calculateColor = (level: number) => {
    if (level <= 33) return "#34A853";
    if (level <= 66) return "#ee7800";
    return "#FF0000";
  };

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

  const handleUpdate = () => {
    setAnimatedCrowdLevel(0);
    setAnimatedPrediction(0);
    fetchData();
  };

  // 画面サイズに応じてSVGのサイズを計算
  const calculateSvgSize = () => {
    if (windowWidth <= 480) return 200;
    if (windowWidth <= 768) return 250;
    return 300;
  };

  const svgSize = calculateSvgSize();
  const radius = svgSize * 0.47; // SVGサイズに応じて半径を調整

  return (
    <div className="container">
      <header className="header">
        <img 
          src="/logo.png" 
          alt="PALTO-AI Logo" 
          className="logo" 
          style={{ height: windowWidth <= 768 ? '80px' : '130px' }}
        />
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
                fill="#ffffff"
              />
            </svg>
          </div>
          <div className="text">Update</div>
        </button>
      </header>

      <main className="content">
        <div className="crowd-status">
          <div className="crowd-icon">
            <div className="circle" style={{ width: svgSize, height: svgSize }}>
              <svg 
                className="progress-ring" 
                width={svgSize} 
                height={svgSize}
              >
                <circle
                  className="progress-ring__circle"
                  cx={svgSize / 2}
                  cy={svgSize / 2}
                  r={radius}
                  fill="none"
                  stroke={calculateColor(animatedCrowdLevel)}
                  strokeWidth={windowWidth <= 480 ? 10 : 13}
                  strokeDasharray={`${2 * Math.PI * radius}`}
                  strokeDashoffset={
                    2 * Math.PI * radius -
                    ((2 * Math.PI * radius) * animatedCrowdLevel) / 100
                  }
                  style={{ transition: "stroke-dashoffset 1.5s ease, stroke 1.5s ease" }}
                />
              </svg>
              <div 
                className="circle2" 
                style={{ 
                  width: svgSize * 0.9, 
                  height: svgSize * 0.9 
                }}
              >
                <div className="group-icon">
                  <div className="person left">
                    <div
                      className="head"
                      style={{
                        backgroundColor: calculateColor(animatedCrowdLevel),
                        transition: "background-color 1.5s ease",
                        width: windowWidth <= 480 ? '40px' : '50px',
                        height: windowWidth <= 480 ? '40px' : '50px',
                      }}
                    ></div>
                    <div
                      className="body"
                      style={{
                        backgroundColor: calculateColor(animatedCrowdLevel),
                        transition: "background-color 1.5s ease",
                        width: windowWidth <= 480 ? '70px' : '90px',
                      }}
                    ></div>
                  </div>
                  <div className="person center">
                    <div
                      className="head"
                      style={{
                        backgroundColor: calculateColor(animatedCrowdLevel),
                        transition: "background-color 1.5s ease",
                        width: windowWidth <= 480 ? '50px' : '60px',
                        height: windowWidth <= 480 ? '50px' : '60px',
                      }}
                    ></div>
                    <div
                      className="body"
                      style={{
                        backgroundColor: calculateColor(animatedCrowdLevel),
                        transition: "background-color 1.5s ease",
                        width: windowWidth <= 480 ? '85px' : '105px',
                      }}
                    ></div>
                  </div>
                  <div className="person right">
                    <div
                      className="head"
                      style={{
                        backgroundColor: calculateColor(animatedCrowdLevel),
                        transition: "background-color 1.5s ease",
                        width: windowWidth <= 480 ? '40px' : '50px',
                        height: windowWidth <= 480 ? '40px' : '50px',
                      }}
                    ></div>
                    <div
                      className="body"
                      style={{
                        backgroundColor: calculateColor(animatedCrowdLevel),
                        transition: "background-color 1.5s ease",
                        width: windowWidth <= 480 ? '70px' : '90px',
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
                <span>{data.prediction}<span className="unit">人</span></span>
              </div>
              <div className="status-label">
                <span>予測人数</span>
              </div>
            </div>
          </div>
        </div>
      </main>

      <footer className="footer">
        <p>予測時刻：{data.timestamp}</p>
      </footer>
    </div>
  );
}

export default App;