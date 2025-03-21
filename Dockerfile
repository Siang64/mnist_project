# 使用 Python 3.9 作為基礎映像
FROM python:3.9

# 設定工作目錄
WORKDIR /app

# 複製專案檔案
COPY . /app

# 安裝必要套件
RUN pip install --no-cache-dir -r requirements.txt

# 設定 Flask 環境變數
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# 暴露 5000 端口
EXPOSE 5000

# 執行 Flask 應用
CMD ["python", "app.py"]
