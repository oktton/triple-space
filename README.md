# Triple Space Translator

三连击 `Space × 3`，即刻翻译当前输入框内容。  
本项目分为 **Agent（本地客户端）** 与 **Server（FastAPI 后端）** 两部分，提供跨 Windows / macOS 的即时翻译体验。

## 功能亮点
1. 零学习成本：连续按三次空格即可触发，自动全选 → 复制 → 调 GPT 翻译 → 粘贴回原处  
2. 高质量 GPT 译文：内置 `translate_v2` 安全分析模板，支持多语言、专业术语与润色模式  
3. 原生跨平台：Windows 使用 Win32 API，macOS 使用 AppKit 与 Quartz，无需额外驱动  
4. 托盘弹窗对照（计划）：翻译后在系统托盘弹窗显示原文 / 译文，可一键复制或撤销  


## 安装与运行
### 1. 克隆仓库并安装依赖
~~~bash
git clone https://github.com/oktton/triple-space.git
cd triple-space
poetry install
~~~

### 2. 设置环境变量
~~~bash
export OPENAI_API_KEY="sk-xxxxxxxx"
~~~

### 3. 启动服务端
~~~bash
python server\server.py        # 默认监听 0.0.0.0:8000
~~~

### 4. 启动客户端
~~~bash
python agent\main.py
~~~


## 测试与评测
### 单元测试
For windows
~~~bash
cd agent 
.\test.cmd
~~~

For mac
~~~bash
cd agent 
./test.sh
~~~
### Benchmark
~~~bash
cd server\benchmark
python caculate_translation_accuracy.py
~~~
脚本输出 CSV 与日志，可查看延迟 P95、BLEU、注入检测指标。

## License
MIT
