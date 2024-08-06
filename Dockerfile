# 使用官方的Python基础镜像
FROM python:3.10.14

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN #pip install --no-cache-dir -r requirements.txt --default-timeout=100  -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install  -r requirements.txt --default-timeout=100  -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制应用代码
COPY . .

# 启动FastAPI应用
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5300"]