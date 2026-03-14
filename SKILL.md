---
name: vue-fastapi-admin
description: 基于Vue和FastAPI构建的后台管理系统技能包
---

# vue-fastapi-admin

基于Vue 3和FastAPI构建的现代化后台管理系统，提供完整的CRUD操作、权限管理、数据可视化等功能。

## When to use

当你需要：
- 快速构建一个基于Vue 3和FastAPI的后台管理系统
- 学习前后端分离架构的最佳实践
- 了解企业级应用的开发流程和技术栈
- 实现完整的用户权限管理和数据管理功能

## 技术栈

### 前端
- Vue 3 + TypeScript
- Element Plus UI组件库
- Pinia状态管理
- Vue Router路由管理
- Axios网络请求
- Vite构建工具

### 后端
- FastAPI
- SQLAlchemy ORM
- MySQL数据库
- Redis缓存
- JWT认证

## 项目结构

### 前端结构
```
frontend/
├── src/
│   ├── api/              # API请求封装
│   ├── assets/           # 静态资源
│   ├── components/       # 通用组件
│   ├── directive/        # 自定义指令
│   ├── icons/            # 图标资源
│   ├── layout/           # 布局组件
│   ├── router/           # 路由配置
│   ├── stores/           # 状态管理
│   ├── theme/            # 主题样式
│   ├── views/            # 页面组件
│   ├── App.vue           # 根组件
│   └── main.ts           # 入口文件
└── package.json          # 依赖配置
```

### 后端结构
```
backend/
├── app/
│   ├── apis/             # API路由
│   ├── corelibs/         # 核心库
│   ├── db/               # 数据库配置
│   ├── exceptions/       # 异常处理
│   ├── init/             # 初始化配置
│   ├── models/           # 数据模型
│   ├── schemas/          # 数据验证
│   ├── services/         # 业务逻辑
│   ├── tasks/            # 定时任务
│   └── utils/            # 工具函数
├── config.py             # 配置文件
└── main.py               # 入口文件
```

## 核心功能

### 系统管理
- 用户管理：用户CRUD、角色分配
- 角色管理：角色CRUD、权限配置
- 菜单管理：菜单CRUD、路由配置

### 业务管理
- 公司管理：公司信息CRUD、资质管理
- 人员管理：人员信息CRUD、证书管理
- 项目管理：项目信息CRUD、投标管理
- 投标管理：投标信息CRUD、人员绑定

### 数据可视化
- 统计报表
- 数据图表

## 开发指南

### 前端开发
1. 安装依赖：`npm install`
2. 启动开发服务器：`npm run dev`
3. 构建生产版本：`npm run build`

### 后端开发
1. 安装依赖：`pip install -r requirements`
2. 启动开发服务器：`python main.py`

## 部署说明

### 前端部署
1. 构建生产版本：`npm run build`
2. 将`dist`目录部署到Web服务器

### 后端部署
1. 安装依赖：`pip install -r requirements`
2. 配置环境变量
3. 启动应用：`python main.py` 或使用Gunicorn

## 权限管理

系统采用基于角色的权限控制（RBAC）：
- 超级管理员：拥有所有权限
- 管理员：拥有部分管理权限
- 普通用户：拥有基本操作权限

## 数据安全

- 密码加密存储
- JWT token认证
- 接口权限验证
- 数据输入验证

## 最佳实践

1. **代码规范**：遵循TypeScript和Python的代码规范
2. **命名约定**：使用语义化的命名
3. **模块化**：合理划分模块，提高代码复用性
4. **错误处理**：统一的错误处理机制
5. **日志记录**：详细的日志记录便于问题排查

## 常见问题

1. **前端页面显示暂无数据**：检查API响应格式是否与前端预期一致
2. **权限验证失败**：检查用户角色和权限配置
3. **数据库连接失败**：检查数据库配置和连接状态
4. **部署后访问缓慢**：考虑使用缓存和优化数据库查询

## 扩展建议

1. **添加更多业务模块**：根据实际需求扩展业务功能
2. **集成第三方服务**：如短信验证、邮件发送等
3. **优化性能**：使用缓存、异步处理等技术
4. **添加测试**：编写单元测试和集成测试

## 技术文档

- [Vue 3官方文档](https://vuejs.org/)
- [FastAPI官方文档](https://fastapi.tiangolo.com/)
- [Element Plus文档](https://element-plus.org/)
- [SQLAlchemy文档](https://www.sqlalchemy.org/)

## 许可证

MIT License