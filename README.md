#### 后端
- 基于 python + fastApi + celery + sqlalchemy + redis

- 使用软件版本
- python version <= 3.10
- mysql version 8.0.23
- redis version 6.0.9
- node version 18.15.0

#### 前端

- 基于 vite + vue3 + element-plus

- 使用软件版本
- node version 18.15.0
- vue  version 3.2.45
- element-plus  version 2.2.26

#### 🚧 项目启动初始化-后端

```bash
# 进入项目
cd vue-fastapi-admin/backend

# 修改对应的数据库地址，redis 地址
backend/config.py
# 或者
backend/.env # 环境文件中的地址修改

# 安装依赖
pip install -r  requirements

# 运行项目 zerorunner/backend 目录下执行
python main.py

# 异步任务依赖 celery 启动命令

#  windows 启动，只能单线程 zerorunner/backend 目录下执行
celery -A celery_worker.worker.celery worker --pool=solo -l INFO 

# linux 启动
elery -A celery_worker.worker.celery worker --loglevel=INFO -c 10 -P solo -n zerorunner-celery-worker

# 定时任务启动
celery -A celery_worker.worker.celery beat -S celery_worker.scheduler.schedulers:DatabaseScheduler -l INFO

# 定时任务心跳启动
celery -A celery_worker.worker.celery beat  -l INFO 

```

#### 🚧 项目启动初始化-前端

```bash
# node 版本
node -v 
v18.15.0
```

- 复制代码(桌面 cmd 运行) `npm install -g cnpm --registry=https://registry.npm.taobao.org`
- 复制代码(桌面 cmd 运行) `npm install -g yarn`

```bash
# 进入项目
cd vue-fastapi-admin/frontend

# 安装依赖
cnpm install 
# 或者
yarn insatll

# 运行项目
cnpm run dev
# 或者 
yarn dev

# 打包发布
cnpm run build
# 或者 
yarn build
```

