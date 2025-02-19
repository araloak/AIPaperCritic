# AIPaperCritic - 智能AI论文评审助手 🤖📄

让大型语言模型为您的论文提供建议帮您更好地准备投稿！该工具可以自动解析AI领域的论文，从多个角度和细粒度层次进行深入分析，并生成结构化的评审报告。 [English README](./README.md)

## 🚀 功能亮点

支持解析 .pdf/.md/.tex 格式的论文，并从多个角度对论文工作进行细粒度的分析和批评，如：

- 研究动机
- 方法论的有效性/合理性
- 实验效果

生成的评审报告以 .md 格式保存。

## 快速开始

1. **安装**

   ```bash
   git clone https://github.com/yourusername/AIPaperCritic.git
   
   pip install docling openai
   pip install --upgrade 'volcengine-python-sdk[ark]'
   ```

2. **准备论文**
   将要评审的论文放入 `data/papers/` 目录中。

   （如需将pdf转换为md，请访问[此处](https://www.modelscope.cn/models/AI-ModelScope/docling-models/files)下载 docling-models。解压后将模型放置在 `model/` 目录下。）

3. **配置**

   在 `util.py` 中指定相关超参数：

   ```python
   API_KEY = "YOUR OPENAI API KEY"
   BASE_URL = "YOUR OPENAI BASE URL"
   MODEL_NAME = "OPENAI MODEL NAME"
   
   reviewer_role = "openai"  # 从 ["doubao", "openai"] 中选择
   language = "cn" # 从 ["en", "cn"] 中选择使用中文或者英文为审稿语言
   ```

4. **运行评审**

   ```bash
   python main.py --file-path "../data/papers/example.md"
   ```


## 贡献

欢迎参与以下方向的优化：

1. 提示工程优化🔧
   - **改进 `prompts/` 中的评审问题模板**，以提高评审的专业性。
2. 多模型支持🌐
   - 增加对**更多平台LLM推理**的支持（如推理模型）

如果此项目对您有帮助，请给它一个⭐并关注更新！您的支持是我持续优化的最大动力！🎉

---

## 免责声明

1. AI生成的内容仅供参考。
2. 本项目出于兴趣进行研究，仅可用于批评**您自己正在撰写的论文草稿**。它**不能用于正式学术出版物的同行评审过程**。
3. 本项目不能用于商业用途。