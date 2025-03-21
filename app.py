import torch
import torchvision.transforms as transforms
from flask import Flask, request, jsonify, render_template
from PIL import Image
import io
import base64
from src.model import MNISTModel  # 確保模型與訓練時相同

# 設備設定
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 加載模型
model = MNISTModel().to(device)
model.load_state_dict(torch.load("model/mnist_model.pth", map_location=device))
model.eval()

# 圖片轉換，與訓練時保持一致
transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=1),  # 轉換為灰階
    transforms.Resize((28, 28)),  # 確保 28x28 大小
    transforms.ToTensor(),  # 轉換為 Tensor
    transforms.Normalize((0.1307,), (0.3081,))  # MNIST 官方標準化
])

# 啟動 Flask 應用
app = Flask(__name__)

# 前端頁面（畫布）
@app.route("/")
def index():
    return render_template("index.html")

# 接收圖片並回傳預測結果
@app.route("/predict", methods=["POST"])
def predict():
    try:
        # 獲取 Base64 編碼的圖片
        data = request.json.get("image")
        if not data:
            return jsonify({"error": "缺少圖片數據"}), 400

        image_data = base64.b64decode(data.split(",")[1])  # 解碼 Base64
        image = Image.open(io.BytesIO(image_data)).convert("L")  # 轉換為灰階
        image = transform(image).unsqueeze(0).to(device)  # 預處理

        # 進行預測
        with torch.no_grad():
            output = model(image)
            prediction = torch.argmax(output, dim=1).item()

        return jsonify({"prediction": prediction})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 啟動 Flask 伺服器
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)