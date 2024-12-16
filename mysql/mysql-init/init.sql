CREATE TABLE IF NOT EXISTS ble_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,  -- スキャン時刻
    other_data JSON NOT NULL  -- 残りのデータ（位置情報、RSSIなど）
);

-- 初期データを挿入（例として1回目のスキャン結果）
INSERT INTO ble_data (timestamp, other_data) VALUES
('2024-12-04 12:00:00', '[{"address": "54:33:c1:60:d6:52", "rssi": -83}, {"address": "46:73:87:c6:79:51", "rssi": -62}, {"address": "98:80:bb:41:7e:47", "rssi": -80}, {"address": "7e:18:21:7c:6d:38", "rssi": -82}, {"address": "06:fc:b5:b8:4c:88", "rssi": -57}]'),
('2024-12-04 12:05:00', '[{"address": "28:7c:c8:9a:cf:bc", "rssi": -62}, {"address": "39:8f:d4:e1:d5:ed", "rssi": -84}, {"address": "14:18:93:00:ad:f2", "rssi": -63}, {"address": "ff:0f:00:12:6d:82", "rssi": -81}, {"address": "3e:cd:e3:ab:43:03", "rssi": -64}, {"address": "45:2a:48:3e:dc:4f", "rssi": -81}]');