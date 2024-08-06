import logging

import requests
import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Query, Path
import os

# 配置Google Custom Search API 密钥和搜索引擎 ID
API_KEY = os.environ.get("GOOGLE_API_KEY")
# google搜索引擎 ID
SEARCH_ENGINE_ID = os.environ.get("SEARCH_ENGINE_ID")

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,  # 设置日志记录级别
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # 设置日志格式
    handlers=[
        logging.FileHandler("custom_search_app.log"),  # 输出日志到文件
        logging.StreamHandler()  # 输出日志到控制台
    ]
)
# 创建一个日志记录器
logger = logging.getLogger(__name__)

app = FastAPI()

print(API_KEY,SEARCH_ENGINE_ID)
@app.get('/customsearch/v1', summary="根据关键词以及指定网站进行检索查询")
def get_entities(keyword: str = Query(..., description="关键词"),
                 sites: str = Query('*', description="指定网站")):

    logger.info(f"keyword:{keyword},sites:{sites}")
    # 构建请求 URL
    url = f'https://www.googleapis.com/customsearch/v1?q={keyword}&key={API_KEY}&cx={SEARCH_ENGINE_ID}'
    if sites != '*':
        url = f'https://www.googleapis.com/customsearch/v1?q={keyword}&key={API_KEY}&cx={SEARCH_ENGINE_ID}&siteSearch={sites}'

    # 发送请求并获取结果
    response = requests.get(url)
    results = response.json()
    # 打印搜索结果
    for item in results.get('items', []):
        title = item.get('title')
        link = item.get('link')
        snippet = item.get('snippet')
        print(f'Title: {title}\nLink: {link}\nSnippet: {snippet}\n')

    return {"results": results}

def get_public_ip():
    response = requests.get('https://api.ipify.org?format=json')
    data = response.json()
    return data['ip']  # 示例数据，你可以根据需要修改

servers = [
    {"url": f"http://{get_public_ip()}:5300", "description": "Production server"}
]

templates = Jinja2Templates(directory="templates")
# app.mount("/static", StaticFiles(directory="static"), name="static")


def custom_openapi(app: FastAPI):
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = app.openapi()
    openapi_schema["servers"] = servers  # 添加自定义服务器列表
    app.openapi_schema = openapi_schema
    return app


app = custom_openapi(app)  # 替换默认的 openapi 方法

@app.route('/', methods=["POST", "GET"])  ## response_class=HTMLResponse,
def index(request: Request):
    logger.info("开始加载index.html...")
    return templates.TemplateResponse("index.html", {"request": request})



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5300, log_level="info")
