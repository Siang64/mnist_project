import torch
import torch.optim as optim
import torch.nn as nn
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import json
import os
from src.model import MNISTModel

# 設備設置
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 創建目錄
os.makedirs("model", exist_ok=True)
os.makedirs("metrics", exist_ok=True)

# 訓練參數
params = {
    "epochs": 20,  # 增加 epochs
    "batch_size": 128,
    "learning_rate": 0.0005  # 降低學習率
}
with open("metrics/params.json", "w") as f:
    json.dump(params, f, indent=4)

# 數據處理（標準化）
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))  # 確保與推論時一致
])
train_dataset = datasets.MNIST(root="data", train=True, transform=transform, download=True)
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=params["batch_size"], shuffle=True)

# 初始化
model = MNISTModel().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=params["learning_rate"])
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.5)  # 調整學習率

# 訓練
metrics = {"loss": [], "accuracy": []}
for epoch in range(params["epochs"]):
    total_loss, correct = 0, 0
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
        correct += (outputs.argmax(dim=1) == labels).sum().item()
    
    scheduler.step()  # 更新學習率
    avg_loss = total_loss / len(train_loader)
    accuracy = correct / len(train_dataset)
    metrics["loss"].append(avg_loss)
    metrics["accuracy"].append(accuracy)
    print(f"Epoch {epoch+1}: Loss={avg_loss:.4f}, Accuracy={accuracy:.4f}")

torch.save(model.state_dict(), "model/mnist_model.pth")
with open("metrics/metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

print("Training Complete!")
