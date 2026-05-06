# 星轨 Demo

这是一个轻量 Flask 演示，展示两个高光页面：

- 数据诊断大屏（Data Diagnostic）
- 智能排期沙盘（Intelligent Scheduler）

运行方法：

1. 创建并激活虚拟环境（可选但推荐）

```bash
python3 -m venv venv
source venv/bin/activate
```

2. 安装依赖：

```bash
pip install -r requirements.txt
```

3. 运行应用：

```bash
python app.py
```

打开浏览器访问 http://127.0.0.1:5000


---

## Streamlit 演示

本仓库同时包含一个基于 Streamlit 的前端演示（`streamlit_app.py`），用于展示星轨的交互式控制台与可视化页面：

- Overview 控制台
- Causal Diagnosis 内容诊断大屏
- Scheduler 智能排期沙盘

运行步骤（推荐 Python 3.10+）：

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

打开浏览器访问 http://localhost:8501

注意：Streamlit 页面使用 mock 数据生成可视化，适合演示用途。

