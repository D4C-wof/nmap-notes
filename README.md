# Nmap 学习笔记与实战速查表（中文）

> 面向初学者的 Nmap 笔记：讲清「什么时候用什么命令、结果怎么读、下一步换什么命令」。

[![License: CC BY-SA 4.0](https://img.shields.io/badge/docs-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![License: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Release](https://img.shields.io/github/v/release/D4C-wof/nmap-notes?label=release&color=blue)](https://github.com/D4C-wof/nmap-notes/releases)

**这是一个文档型仓库，不是软件项目**：没有构建步骤、没有运行时依赖、没有 API。`git clone` 下来就是一摞
Markdown，用浏览器或任意编辑器打开即可读。仓库里唯一的可执行文件是 `scripts/check-links.py`——一个只用
标准库的链接自检脚本。

---

## 1. 项目解决了什么问题

### 1.1 三个卡点

初学者学 Nmap 卡住的地方，通常不是「参数不够多」，而是：

1. 面对一个目标，**第一个命令敲什么**；
2. 命令跑完了，屏幕上这张表**到底在说什么**；
3. 结果不符合预期时，**下一条命令应该换成什么**。

能搜到的中文材料大多停在「参数清单 + 命令合集」：查得到 `-sS` 是什么，查不到「我这次该不该用 `-sS`」、
「表里 `filtered` 意味着什么」、「下一步换哪条」。本仓库按「一个问题 → 一条命令 → 一次判读 → 下一步」
组织正文，11 章都落在这三个卡点上。

### 1.2 它和其他材料的分工

| 材料 | 强项 | 不解决什么 |
| --- | --- | --- |
| `nmap --help` 与官方手册 | 参数权威、随版本更新 | 不告诉你先跑哪条、输出怎么判读 |
| 网上的命令合集 | 能直接抄 | 缺少前提条件与判读，抄错了也不知道 |
| **本仓库** | 命令 + 场景 + 示例 + 判读 + 下一步 | 不追求参数全覆盖，冷门参数请回官方手册 |

### 1.3 适合谁

| 适合 | 不太适合 |
| --- | --- |
| 刚接触网络安全、想系统掌握 Nmap 的学生与转行者 | 想找现成「一条命令打穿目标」的人（本书不提供） |
| 需要做资产盘点、端口巡检的运维 / 值班工程师 | 需要大规模分布式扫描平台的团队（本书是单机用法） |
| 准备 OSCP / CEH / 国内 SRC 笔试，需要一份中文速查表的人 | 只想看 GUI 截图、不想理解命令行的人 |
| 已经在用 Nmap，但只会 `-sV -sC` 两个参数的人 | — |

### 1.4 前置知识

TCP/IP 基础（三次握手、端口、ICMP），能在 Linux 或 Windows 上开一个终端。不需要编程基础。

## 2. 主要功能

### 2.1 内容清单

| 章节 | 文件 | 解决什么问题 |
| --- | --- | --- |
| 01 | [docs/01-zenmap.md](docs/01-zenmap.md) | 用 Zenmap 建立「目标 → 配置 → 命令 → 结果」的直觉，并看懂它生成的命令 |
| 02 | [docs/02-target.md](docs/02-target.md) | 目标怎么写：IP、网段、范围、`-iL`、排除、IPv6 |
| 03 | [docs/03-host-discovery.md](docs/03-host-discovery.md) | 先确认谁在线：`-sn`、`-Pn`、`-PS`、`-PR` 怎么选 |
| 04 | [docs/04-port-scan.md](docs/04-port-scan.md) | 端口扫描技术选型与 6 种端口状态的判读（全书核心） |
| 05 | [docs/05-service-os.md](docs/05-service-os.md) | 服务版本探测与操作系统识别，以及结果可信度怎么判断 |
| 06 | [docs/06-nse.md](docs/06-nse.md) | NSE 脚本引擎：类别、风险分级、传参、脚本输出怎么读 |
| 07 | [docs/07-speed-evasion-output.md](docs/07-speed-evasion-output.md) | 速度控制、规避、三种输出格式与事后检索 |
| 08 | [docs/08-workflow.md](docs/08-workflow.md) | 五阶段实战工作流与决策树，把前面的参数放回整体流程 |
| 09 | [docs/09-troubleshooting.md](docs/09-troubleshooting.md) | 常见报错：主机看似 down、DNS 解析失败、全 filtered、扫得慢 |
| 10 | [docs/10-legal-and-safety.md](docs/10-legal-and-safety.md) | 授权、合规与安全边界（**动手前必读**） |
| 11 | [docs/11-glossary.md](docs/11-glossary.md) | 术语表：中文 / 英文 / 一句话解释 |
| 示例 A | [examples/basic.md](examples/basic.md) | 本机 / 靶场最小可用流程：6 步 + 一键 bash 脚本 + 常见错误对照 |
| 示例 B | [examples/web.md](examples/web.md) | 授权 Web 目标流程：5 步 + 一页命令汇总 + 常见坑 |
| 样本规范 | [examples/output-samples/README.md](examples/output-samples/README.md) | 真实输出样本的收录、脱敏、命名与审稿标准 |
| 自检脚本 | [scripts/check-links.py](scripts/check-links.py) | 校验全书相对链接与标题锚点 |

### 2.2 每条命令的统一模板

核心命令都按同一模板组织，读者不必猜「这条命令的说明在哪一节」：

```text
命令 → 适用场景 → 示例 → 示例输出 → 结果判读 → 注意事项 → 下一步决策
```

个别章节在「适用场景」后多一段「原理」（例如 04 章 4.2.1 `-sS`）。每章结尾固定两节：**本章初学者检查清单**
（3–6 条自测）与**本章修改说明**（相对原笔记改了什么、为什么）。

### 2.3 两个可照做的完整流程

- **示例 A**（`examples/basic.md`）：从 `nmap --version` 到 `-sV -sC -oA` 存档，6 步走完；末尾给了一键串起来的
  bash 脚本（默认扫 `127.0.0.1`），并附「常见错误对照」表。
- **示例 B**（`examples/web.md`）：面向授权 Web 目标的 5 步流程，含 `http-title` / `ssl-cert` / `http-enum`
  的使用位置与风险标注，末尾是可直接复制的命令汇总。

### 2.4 链接自检脚本

`scripts/check-links.py` 是仓库唯一的代码，用来保证文档长期不烂链：

| 能力 | 说明 |
| --- | --- |
| 相对链接目标是否存在 | 例如 `docs/09-troubleshooting.md` 是否真的存在 |
| 标题锚点是否有效 | 按 GitHub 规则近似计算锚点，校验 `#41-六种端口状态` 这类跳转 |
| 图片是否缺 alt 文本 | 空 alt 报 `EMPTY ALT` |
| 依赖 | 只用标准库 `os` / `re` / `sys`，**不需要 pip install** |
| 联网 | 不联网，只做本地文件与标题校验 |
| 退出码 | `0` 全部通过；`1` 有问题（可直接放进 CI） |
| 可选参数 | `--ignore-missing-images`：跳过缺失图片，仅在图未补齐时使用 |

### 2.5 写作与脱敏约定

[CONTRIBUTING.md](CONTRIBUTING.md) 给出了命令模板、占位符写法、脱敏替换表（真实 IP / 域名 / 主机名 / MAC /
证书 CN → RFC 5737 文档地址段）、PR 审核五条标准，以及提交前要跑的两条检查。

### 2.6 明确不提供什么

- **不提供**「一条命令打穿目标」的攻击链、PoC 或绕过流程；
- **不默认推荐** `brute` / `dos` / `exploit` / `intrusive` / `vuln` 类 NSE 脚本，只说明用途与风险；
- **不收录真实扫描输出**：每处该放输出的位置都写成【自测留白】，并说明这一处要记录什么。
  输出与你的环境强相关（Nmap 版本、网络、目标），别人的输出会被初学者当成标准答案——所以这里留空，由你自己跑一次填进去。

### 2.7 当前完成度（如实说明）

| 项 | 状态 |
| --- | --- |
| 正文 | 11 章、2 个示例、1 个脚本，16 个 Markdown 文件，约 4 万汉字 |
| 自测留白 | `docs/` 正文内 55 处【自测留白】（04 章 10、07 章 13、05 章 8、02 章 7、06 章 6、08 章 5、03 章 4、01/10 各 1），**设计如此**：由读者在自己环境跑一次填写，见 4.6 |
| 输出样本 | 不收录真实样本，原因与方法见 [examples/output-samples/README.md](examples/output-samples/README.md) |
| 截图 | 全书不含截图，界面类内容用文字 + 表格描述 |
| 格式检查 | `markdownlint-cli2` 0 issue；`check-links.py` 全部通过 |

## 3. 安装方法

### 3.1 只读（推荐，零安装）

直接在 GitHub 网页上读：本页 2.1 的「内容清单」就是目录，点进去即可。手机、平板、公司电脑都不需要装任何东西。

### 3.2 拿到本地

```bash
git clone https://github.com/<你的用户名>/nmap-notes.git
cd nmap-notes
```

不想用 git：仓库页点绿色 `Code` → `Download ZIP`，解压即可。

### 3.3 环境要求

| 用途 | 需要 | 说明 |
| --- | --- | --- |
| 阅读 | 任意浏览器 / 编辑器 | 不需要任何依赖 |
| 跑链接自检 | Python 3.6+ | 只用标准库，无需 `pip install` |
| 跑格式检查（可选） | Node.js 18+ | `npx markdownlint-cli2 "**/*.md"`，规则见 `.markdownlint.json` |
| 照示例实操 | 本机装 Nmap | Debian/Ubuntu `sudo apt install nmap`；macOS `brew install nmap`；Windows 官方安装包（勾选 Npcap） |

### 3.4 安装后验证

在仓库根目录执行：

```bash
python scripts/check-links.py
```

预期输出（本机实测）：

```text
checked 16 markdown files
all links ok
```

退出码为 `0` 即表示文档内部链接完好。

## 4. 使用方法

### 4.1 五分钟先跑起来

```bash
nmap --version                          # ① 确认装了、能跑
nmap -F 127.0.0.1                       # ② 第一次扫描：回环地址永远属于你自己
nmap -sn 192.0.2.0/24                   # ③ 网段里谁在线（不发端口包）
nmap -sV -p 22,80,443 192.0.2.10        # ④ 端口上跑的是什么服务、什么版本
nmap -sV -sC -p 22,80,443 -oA scan-192.0.2.10 192.0.2.10   # ⑤ 加默认安全脚本并存三种格式
```

`nmap --version` 没有输出说明未安装（装法见 3.3）。第 ⑤ 条会生成 `scan-192.0.2.10.nmap/.xml/.gnmap`
三份文件——注意 `.gitignore` 已排除这类扫描产物，不会被误提交。

> `192.0.2.0/24`、`198.51.100.0/24`、`203.0.113.0/24` 是 RFC 5737 保留给文档使用的地址段，**不会路由到任何真实主机**。
> 本书所有示例一律使用这些地址或 `192.168.x.x` 私网地址，你照抄不会扫到别人的机器。

### 4.2 按顺序系统学

```mermaid
flowchart LR
    A[01 Zenmap 建立直觉] --> B[02 目标怎么写]
    B --> C[03 主机发现]
    C --> D[04 端口扫描]
    D --> E[05 服务与系统识别]
    E --> F[06 NSE 脚本]
    F --> G[07 速度/规避/输出]
    G --> H[08 五阶段工作流]
    H --> I[09 排错]
    I --> J[10 授权与合规]
```

建议顺序：**01 → 02 → 03 → 04 → 05 → 08 → 06 → 07 → 09 → 10**。先看第 08 章的工作流，能让你知道前面每个参数
在整体流程里站在哪一格；第 09、10 章随时可以跳读，但**在真正对着任何目标发包之前，必须先读完第 10 章**。

### 4.3 当速查表用（按问题查）

| 你现在的问题 | 去这里 |
| --- | --- |
| 想先看清整体流程再学参数 | [08 章](docs/08-workflow.md) |
| 网段里到底谁在线 | [03 章](docs/03-host-discovery.md) |
| 这台机器开了哪些端口 | [04 章](docs/04-port-scan.md) |
| 端口上跑的是什么服务、什么版本 | [05 章](docs/05-service-os.md) |
| 想用现成脚本多拿点信息 | [06 章](docs/06-nse.md) |
| 扫得太慢，或者被防火墙挡住 | [07 章](docs/07-speed-evasion-output.md)、[09 章](docs/09-troubleshooting.md) |
| 报错了不知道怎么办 | [09 章](docs/09-troubleshooting.md) |
| 这次能不能扫、怎么留证据 | [10 章](docs/10-legal-and-safety.md) |
| 某个词看不懂 | [11 章](docs/11-glossary.md) |

### 4.4 改完文档跑自检

```bash
python scripts/check-links.py          # 校验相对链接与锚点
npx markdownlint-cli2 "**/*.md"        # 校验 Markdown 格式（可选，需 Node.js）
```

两条都返回成功（退出码 0）再提交；`check-links.py` 的退出码可直接用于 CI 判失败。

### 4.5 照示例练一遍

先跑[示例 A](examples/basic.md)（默认目标 `127.0.0.1`，永远属于你自己，不需要授权），把 6 步走完、产物存下来；
再按[示例 B](examples/web.md) 的结构，对一个**你有书面授权**的目标复现一遍。跑完的输出按 [4.6](#46-用自己的输出填满留白推荐用法)
贴进各章的【自测留白】，笔记才真正变成你自己的。

### 4.6 用自己的输出填满留白（推荐用法）

全书 55 处【自测留白】没有现成输出，这是有意设计：**输出带环境指纹**（Nmap 版本、网络路径、目标系统），
抄别人的输出只会把误判一起抄过来。正确用法是把它当练习册：

1. **跑**：按留白上方那条命令，在你自己拥有控制权的环境里执行（本机、本地虚拟机、隔离靶场）。
2. **抄**：把终端里的真实输出整段粘到留白下方，用 ```` ```text ```` 包起来；顺手写一行环境（系统 / Nmap 版本 / 目标类型）。
3. **对**：拿你自己的输出去比照紧随其后的「结果判读」，看每一行能不能对上；对不上就回 [09 章](docs/09-troubleshooting.md)。

想让改动长期留存，先 `Fork` 仓库到你自己账号，在 fork 里填——**不要**提 PR 把真实输出塞回本仓库（见
[CONTRIBUTING.md 的「绝对不能提交的内容」](CONTRIBUTING.md)）。这样一个仓库读完，你手上就有一份只属于你环境的笔记。

### 4.7 反馈与贡献

错别字、命令写错、输出判读有误：开 Issue，标题格式 `[docs/04] -sT 权限说明有误`。想直接改：先读
[CONTRIBUTING.md](CONTRIBUTING.md) 再提 PR。

## 5. 输入输出示例

### 5.1 输入一个问题，输出一条命令条目

**输入**（你脑子里的问题）：`-sS` 到底什么时候该用？

**输出**（`docs/04-port-scan.md` 中 4.2.1 节的实际结构）：

```text
### 4.2.1 `-sS`：TCP SYN 扫描（半开扫描）
#### 命令
#### 适用场景
#### 原理
#### 示例
#### 示例输出
#### 结果判读
#### 注意事项
#### 下一步决策
```

「命令」段给出可抄的骨架（原文）：

```bash
nmap -sS -p <端口列表> <目标IP>
```

「适用场景」段第一条直接给结论（原文）：

- **默认首选**的 TCP 扫描方式；

也就是说：不用翻别的章节找前提，一条命令从「长什么样」到「什么时候别用」都在同一节里。

### 5.2 输入一条扫描命令，输出一张端口表（结构示意）

**输入**：

```bash
sudo nmap -sV -p 22,80,443 192.0.2.10
```

**输出形态**（与 [05 章](docs/05-service-os.md) 一致）：

```text
PORT    STATE SERVICE  VERSION
22/tcp  open  ssh      <产品名> <版本>(protocol 2.0)
80/tcp  open  http     <产品名> <版本>
443/tcp open  ssl/http <产品名> <版本>
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

> 上面是**结构示意**：字段位置真实，`<产品名> <版本>` 必须由你自己扫描后填入。本仓库不收录输出样本——
> 请在你自己的环境里跑一次，把结果贴进对应章节的【自测留白】处（做法见 4.6）。

**怎么读**：`open` 只说明端口有服务在听；产品名和版本都抓到，可信度高；只有产品名、版本缺失，说明指纹部分匹配；
`unknown` 表示没匹配上，需要人工介入。完整判读表见 05 章「结果判读」一节。

### 5.3 输入一处坏链接，输出脚本报错（实测）

在一个副本的 `README.md` 末尾插入两条坏链接后运行 `python scripts/check-links.py`，实际输出：

```text
checked 16 markdown files
  [MISSING FILE] README.md -> docs/99-not-exist.md
  [BAD ANCHOR] README.md -> docs/04-port-scan.md#不存在的锚点
2 problem(s)
```

退出码 `1`。这就是 4.4 节那两条检查在 PR 里拦人的方式。

### 5.4 输入一个目标，输出一组存档文件

[示例 A](examples/basic.md) 的 `A.8` 脚本（默认 `TARGET=127.0.0.1`）跑完后，`-oA` 生成三件套：

```text
example-basic-<时间戳>-01-discovery.nmap / .xml / .gnmap   # -sn 主机发现
example-basic-<时间戳>-02-ports.nmap     / .xml / .gnmap   # -F 常见端口
example-basic-<时间戳>-03-service.nmap   / .xml / .gnmap   # -sV -sC 版本与脚本
```

`.nmap` 给人读，`.xml` 给工具解析（也可用 Zenmap 打开），`.gnmap` 给 `grep` 用。

## 占位符约定

书中所有命令使用统一占位符，首次出现时会在正文解释：

| 占位符 | 含义 | 示例值 |
| --- | --- | --- |
| `<目标IP>` | 单个目标主机地址 | `192.0.2.10` |
| `<目标网段>` | CIDR 写法的网段 | `192.0.2.0/24` |
| `<端口>` | 单个端口号 | `443` |
| `<端口列表>` | 逗号分隔的多个端口 | `22,80,443` |
| `<文件名>` | 输入或输出的文件名 | `targets.txt` |
| `<脚本名>` | NSE 脚本名或脚本类别名 | `http-title` |
| `<DNS服务器IP>` | 用于解析目标域名的 DNS 服务器 | `192.0.2.53` |

看到尖括号就说明**这一格必须由你替换**，直接复制粘贴会失败。

## 三条硬规则

1. **只扫描你有书面授权、或属于你自己的目标。** 详见[第 10 章](docs/10-legal-and-safety.md)。
2. **`brute` / `dos` / `exploit` / `intrusive` / `vuln` 类脚本默认不要跑。** 它们可能让服务崩溃、写日志、
   触发告警，甚至改变目标状态。本书只说明它们的用途与风险，不提供组合攻击流程。
3. **慢一点。** `-T4` 已经足够快；对生产目标用 `-T2` 或 `--min-rate` 限速，既是礼貌，也是避免 IP 被封的现实手段。

## 免责声明

本书内容仅用于**授权的安全测试、教学与本地靶场练习**。

- 书中所有命令示例均以文档保留地址或私网地址书写，不指向任何真实系统。
- 作者不对任何人使用本书内容造成的直接或间接损失负责，包括但不限于服务中断、数据损坏、法律责任。
- 未取得目标所有者明确书面许可的扫描行为，在多数国家和地区属于违法行为。**「我只是扫了一下端口」不是抗辩理由。**
- 书中涉及的第三方工具、脚本与链接，其安全性与可用性由原作者负责，本项目不做担保。

如果你不确定某次扫描是否合规，**停下来，先去拿授权**。

## 贡献方式

欢迎修正错别字、纠正技术细节、增加新场景示例。请先读 [CONTRIBUTING.md](CONTRIBUTING.md)，
其中规定了脱敏规则与命令模板——**任何包含真实 IP、域名、主机名、个人信息的 PR 都会被直接关闭**。

**本仓库不收录真实扫描输出**（整份或片段）：输出带环境指纹，属于每位读者自己的笔记。想在本地保存，
Fork 后在 fork 里填，见 [4.6](#46-用自己的输出填满留白推荐用法)。

## License

本项目采用**双许可**：

| 内容 | 许可 | 说明 |
| --- | --- | --- |
| 文档（`docs/`、`README.md`、`examples/*.md`） | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) | 允许转载、改编、商用，须署名并以相同方式共享 |
| 代码（`.sh`、`.py`、配置片段） | [MIT](https://opensource.org/licenses/MIT) | 允许任意使用，保留版权声明即可 |

**为什么这样选**：

- 文档用 CC BY-SA：教学内容被大量转载是常态，署名 + 相同方式共享能防止有人把笔记改一改就闭源卖课。
- 代码用 MIT：示例脚本要能被人直接抄进工程，任何附加限制都会降低可用性。
- 若你希望允许他人把改编版闭源（例如做内部培训材料），把文档许可换成 **CC BY 4.0** 即可——去掉 ShareAlike 这一条。

替换方式：修改 `LICENSE-NOTES.md`，并同步更新本节与 README 顶部的徽章。标准全文随仓库提供：
文档见 `LICENSE-CC-BY-SA-4.0.txt`（CC 官方 legalcode.txt，未作修改），代码见 `LICENSE-MIT`；
版权归属与各部分适用范围写在 `LICENSE-NOTES.md`。

---

**开始阅读** → [01 · Zenmap 图形界面入门](docs/01-zenmap.md)
