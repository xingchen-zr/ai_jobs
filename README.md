# AI 求职职位检索与回复助手

基于 Streamlit 的职位搜索、分析与回复应用 — 由 SQLite、Chroma 和基于 LLM 的 RAG 技术驱动。

> **状态：** v0.1-local-mvp（开发中）  
> **范围：** 单用户、本地 CSV/JSON 数据、有证据支撑的 AI 回答

---

## 架构

```
┌──────────┐    ┌──────────────┐    ┌───────────┐    ┌──────────┐
│ CSV/JSON │───▶│ Pandas 清洗  │───▶│  SQLite   │───▶│ Streamlit│
│ (本地)   │    │ + 去重       │    │ (结构化   │    │   界面   │
└──────────┘    └──────────────┘    │  搜索)    │    └──────────┘
                                    └─────┬─────┘
                                          │ 候选 ID
                                    ┌─────▼─────┐    ┌──────────┐
                                    │  Chroma   │───▶│   LLM    │
                                    │ (语义     │    │  (RAG)   │
                                    │  排序)    │    └──────────┘
                                    └───────────┘
```

- **SQLite** 负责结构化筛选（城市、薪资、经验、学历）。
- **Chroma** 在 SQLite 筛选出的候选集中进行语义排序。
- **LLM** 仅总结检索到的证据 — 绝不编造职位详情。

---

## 快速开始

### 前置条件

- Python 3.10+
- 一个 LLM API 密钥（兼容 OpenAI 接口）

### 安装

```bash
# 1. 克隆仓库
git clone <repo-url>
cd ai-jobs

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置
cp .env.example .env
# 编辑 .env — 填入你的 LLM_API_KEY 和 EMBEDDING_API_KEY
```

### 导入示例数据

```bash
# 将 CSV/JSON 文件放入 data/raw/ 目录
python -m app.import_data --input data/raw/your_jobs.csv
```

### 构建搜索索引

```bash
python -m app.build_index
```

### 启动

```bash
streamlit run app.py
```

---

## 项目结构

```
ai-jobs/
├── docs/               # 文档与范围说明
│   └── mvp_scope.md
├── models/             # 领域模型（JobPosition、UserProfile 等）
├── sources/            # 数据源适配器（JobSource 接口）
├── repositories/       # 数据访问层（JobRepository）
├── services/           # 业务逻辑（Retriever、LLMService）
├── prompts/            # LLM 提示词模板（带版本号）
├── ui/                 # Streamlit 页面与组件
├── tests/              # pytest 测试套件
├── data/               # 原始与处理后数据（gitignored）
├── samples/            # 匿名化示例数据（已提交）
├── requirements.txt
├── .env.example
└── README.md
```

---

## 测试

```bash
# 运行所有测试
pytest

# 带覆盖率报告
pytest --cov=. --cov-report=html
```

---

## 已知限制（v0.1）

- 仅支持本地 CSV/JSON — 未对接实时招聘平台
- 单用户 — 无认证或多账号支持
- 无自动投递或自动提交功能
- 中文优先优化；其他语言表现可能下降
- LLM 回答质量取决于所配置的模型

---

## 许可证

待定
