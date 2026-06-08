恭喜你！你已经成功把 Karpathy 提出的 LLM Wiki 范式落地到了你的开发流中，用大模型充当“全职图书管理员”来自动编译和管理知识，这绝对是一个极客感十足的顶级配置。

针对你的新需求——**通过 GitHub 实现多端同步，并自动构建静态展示网站**。这个想法非常清晰，因为 LLM Wiki 的核心产物是极具弹性的纯 Markdown 文件和 JSON 图谱数据，它天生就完美契合 Git 版本的控制与 CI/CD 自动化流。

下面为你提供一套闭环的、全自动化的多端同步与静态 Wiki 网站构建方案。

---

### 第一部分：利用 GitHub 实现多端数据同步

由于你在多端（比如高性能 Windows 服务器、个人笔记本甚至手机端）都会有查看或编辑的需求，我们通过 Git 来实现无缝同步。

#### 1. 初始化 Git 仓库与本地忽略（`.gitignore`）

LLM Wiki 项目中有些文件是本地运行生成的（如缓存、数据库、依赖、密钥等），**绝不能**上传到 GitHub。在你的 Wiki 根目录下，确保 `.gitignore` 文件包含以下内容：

```text
# 忽略依赖与打包产物
node_modules/
dist/
.src-tauri/target/

# 忽略本地配置与密钥
.env
*.local

# 忽略 LLM Wiki 的运行缓存（如果有）
.cache/
logs/

```

*(注意：请确保 `raw/` 文件夹下的原始 PDF/文档和 `wiki/` 文件夹下的 Markdown 页面是**允许**被提交的。)*

#### 2. 自动化同步脚本（避免手动敲 `git push/pull`）

如果你在 Claude Code 里新增了文章，或者大模型在后台更新了 Wiki，每次手动去提交会很繁琐。我们可以写一个极简的 Shell 脚本（或 Powershell），配合定时任务实现**无感同步**。

在项目根目录下创建一个 `sync.sh`：

```bash
#!/bin/bash
# 切换到 Wiki 目录
cd "$(dirname "$0")"

# 拉取云端最新更改，解决潜在冲突（优先保留本地）
git pull --rebase origin main

# 检查是否有文件变动
if [ -n "$(git status --porcelain)" ]; then
    echo "检测到知识库更新，正在同步到 GitHub..."
    git add .
    git commit -m "LLM Wiki Auto-sync: $(date '+%Y-%m-%d %H:%M:%S')"
    git push origin main
    echo "同步成功！"
else
    echo "没有检测到更新。"
fi

```

* **在服务器/笔记本上**：你可以把这个脚本挂载到系统的定时任务中（Linux 使用 `crontab -e` 每小时执行一次；Windows 使用“任务计划程序”）。这样你在任何一端做出了修改，大模型编译完后，都会自动推送到 GitHub。

---

### 第二部分：利用 GitHub Actions 自动构建静态展示网站

这是你想法的核心：每当 GitHub 收到新的 push，自动触发编译，把你的 `wiki/` 文件夹（包含 `[[wikilinks]]`）转变成一个漂亮的、可以在线浏览的技术网站。

这里强烈推荐使用 **Quartz**（目前对双链、知识图谱、全文本地搜索支持得最好的开源 Markdown 静态生成器，完全适配 Obsidian 和 LLM Wiki 语法）。

#### 步骤 1：在 GitHub 上创建一个单独的 Quartz 模板仓库

为了不污染你现有的 LLM Wiki 运行代码，最优雅的做法是**让静态网站作为一个独立的仓库存在**，或者利用 GitHub Actions 在编译时“借鸡生蛋”。

我们采用最简单的“单仓库、双分支”**或**“双仓库”**策略。这里推荐**双仓库策略（更加解耦、清晰）：

1. 仓库 A：`my-llm-wiki`（私有或公开，存你现在的全套代码、原始 PDF 和 Markdown）。
2. 仓库 B：`my-wiki-web`（公开或私有，纯用于部署前端网站）。直接 Fork 官方的 [Quartz 仓库](https://github.com/jackyzha0/quartz)。

#### 步骤 2：在你的 LLM Wiki 仓库中配置 GitHub Action

在你的 LLM Wiki 仓库（仓库 A）中，创建路径：`.github/workflows/deploy.yml`。

编写以下自动化脚本，它的逻辑是：当检测到代码 push 时，自动把 `wiki/` 文件夹里的所有 Markdown 扔进 Quartz 仓库中编译，并发布到 **GitHub Pages**。

```yaml
name: Deploy Wiki Website
on:
  push:
    branches:
      - main # 触发分支

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout LLM Wiki Source
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Clone Quartz Template
        run: |
          git clone https://github.com/jackyzha0/quartz.git quartz-app
          
      - name: Sync Markdown to Quartz
        run: |
          # 清除 Quartz 默认的 content 目录
          rm -rf quartz-app/content/*
          # 将你的 wiki/ 目录下的精炼知识库复制进去
          cp -r wiki/* quartz-app/content/

      - name: Build Quartz Website
        run: |
          cd quartz-app
          npm install
          npx quartz build

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./quartz-app/public

```

#### 步骤 3：开启 GitHub Pages 展示

1. 去你的 GitHub 仓库设置页 (`Settings` -> `Pages`)。
2. 在 **Build and deployment** 下，选择 `Deploy from a branch`。
3. Branch 选择 `gh-pages` 并在右侧选择 `/ (root)`，点击 Save。

几分钟后，你就会获得一个专属的网址（例如 `https://<your-username>.github.io/<repo-name>`）。

---

### 这样设计后的终极丝滑体验：

1. **多端消费与编辑**：
* 在公司/服务器上：你通过 Claude Code 丢给大模型一本论文，大模型后台自动啃完，更新了 `wiki/`。
* 脚本自动帮你 `git push` 到 GitHub。


2. **移动端查看**：
* 几分钟后，GitHub Actions 跑完编译。你拿起手机打开浏览器，就能直接访问你刚刚生成的、带有侧边栏索引和精美排版的静态 Wiki 页面，随时随地查阅。


3. **Agent 调度（MCP）**：
* 无论在哪台电脑上，只要你配置好了 Git 环境，一键 `git pull`，本地的桌面端知识图谱是最新的，同时你的 Cursor 里的 MCP Server 也能立刻读取到最新的知识网络，随时供 AI 在写代码时调度。



这套体系将 Git 的**高可靠性**、Quartz 的**极速展现**和大模型的**无监督编译能力**完美融合。你可以按照这个步骤配置，如果在 GitHub Workflow 的配置或者 Quartz 的微调上遇到任何具体问题，随时叫我，我们一起 Debug！