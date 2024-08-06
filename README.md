# custom_search项目介绍
## 简介
google custom search api 二次封装项目。
## 一、目录结构

#### 二、使用 Docker 部署项目
- Docker
    ```bash
    pip install docker
    ```
1. 克隆仓库到本地：
   ```bash
   git clone git@github.com:drinkatmoon/custom_search.git
   cd custom_search
    ```
2. 构建并启动 Docker 容器：
- 使用docker命令构建镜像：
    ```bash
   docker build -t custom_search .
   ```
   配置环境变量，并启动容器：
   ```bash
   cp local.env.example local.env 
   #修改 local.env 文件中的环境变量，设置 Google Custom Search API 密钥和搜索引擎 ID
   docker run -d -p 5300:5300  --env-file local.env  custom_search 
   ```

3. 应用将会在 http://127.0.0.1:5300 运行。

#### 三、使用uvicorn启动项目
- uvicorn
    ```bash
    pip install fastapi uvicorn
    ```
1. 克隆仓库到本地并启动：
   ```bash
   git clone git@github.com:drinkatmoon/custom_search.git
   cd custom_search
   uvicorn app:app --host 0.0.0.0 --port 5300 --reload
   ##以后台形式启动应用
   nohup uvicorn app:app --host 0.0.0.0 --port 5300 --reload &
   ```
   需要注意使用该方式启动应用时，需要提前配置好如下几项环境变量：
   - GOOGLE_API_KEY,SEARCH_ENGINE_ID
   
2. 应用将会在 5300启动，通过浏览器访问 http://serverip:5300 即可。
