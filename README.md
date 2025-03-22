# MNIST 手寫數字辨識專案

## 1. 專案介紹
本專案實作一個基於 **Flask** 的 API 服務，使用 **PyTorch** 訓練的 **CNN** 模型來辨識手寫數字，並透過 **Docker** 容器化部署到 **Google Cloud Platform (GCP)**。

## 2. 專案結構
```
mnist_project/
├── model/                 # 存放訓練好的模型
├── static/                # 前端靜態資源
├── templates/             # HTML 模板
├── app.py                 # Flask 服務主程式
├── train.py               # 訓練模型的腳本
├── requirements.txt       # 依賴套件清單
├── Dockerfile             # Docker 設定檔
├── README.md              # 專案說明
```

## 3. 環境設定
### (1) 安裝必要套件
```sh
pip install -r requirements.txt
```

### (2) 訓練與部署
#### 訓練模型
```sh
python train.py
```
訓練完成後，模型權重將存放於 `model/mnist_model.pth`。

#### 啟動 Flask API
```sh
python app.py
```
預設 Flask 會在 `http://127.0.0.1:5000` 提供服務。

## 4. 主要功能
- **手寫數字辨識 API**：上傳手寫數字圖片，模型會預測數字。
- **前端互動介面**：透過瀏覽器手寫數字並進行預測。
- **Docker 容器化**：使用 Docker 進行封裝，方便部署。
- **雲端部署**：可部署到 **Google Cloud Platform (GCP)**。

## 5. API 端點
| 方法  | 端點       | 說明 |
|------|-----------|------------|
| POST | `/predict` | 接收手寫數字圖片，回傳預測結果 |

範例請求：
```sh
curl -X POST -F "file=@test.png" http://127.0.0.1:5000/predict
```

## 6. 前端介面
- 本專案提供簡單的 **HTML + JavaScript** 介面，可手寫數字並進行預測。
- 瀏覽器開啟： `http://127.0.0.1:5000`

## 7. Docker 部署
### (1) 建立 Docker 映像
```sh
docker build -t mnist-flask .
```

### (2) 啟動容器
```sh
docker run -p 5000:5000 mnist-flask
```

## 8. 部署到 GCP
### (1) 啟動 GCP VM 並開放 5000 端口
```sh
gcloud compute instances create mnist-instance \
    --machine-type=e2-medium \
    --image-family=debian-11 \
    --image-project=debian-cloud \
    --tags=http-server,https-server,port-5000
```

### (2) 部署服務
SSH 進入 VM 後執行：
```sh
docker run -p 5000:5000 mnist-flask
```

確認 `http://<你的外部 IP>:5000` 可正常存取。



