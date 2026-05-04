# 基础镜像：Python 3.11 轻量版
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# 复制当前项目所有文件到容器内
COPY . /app

# 安装项目本身
RUN pip install --no-cache-dir -e .

# 初始化 Git 仓库并提交初始状态
RUN git init && \
    git add -A && \
    git config --global user.email "agent@example.com" && \
    git config --global user.name "Agent" && \
    git commit -m "Initial commit"

# 默认打开 bash
CMD ["bash"]