# 示例 A · 最小可用流程（本机 / 靶场）

> **适用前提**：目标是你自己的机器，或你拥有完全处置权的本地靶场。
>
> **本文档不含任何真实扫描输出。** 所有"期望结果"都是**结构描述**，你需要自己跑一遍并对照。

## A.1 目标选择

| 选项 | 地址 | 说明 |
| --- | --- | --- |
| 回环地址 | `127.0.0.1` | 永远属于你自己，最安全 |
| 本机内网地址 | `192.168.1.x` | 你自己的机器，需确认不是别人的设备 |
| 本地虚拟机 | `192.168.56.x` / `192.168.11.x` | Host-only 或 NAT 网络里的靶机 |
| 容器 | `172.17.0.x` | Docker 默认网桥 |

**不要**用 `192.0.2.x` 这类文档地址做练习——它们不会路由到任何主机，你只会得到 `Host seems down`，学不到东西。

## A.2 第 1 步：确认环境

```bash
nmap --version
```

**期望**：输出 Nmap 版本、编译选项、可用脚本数、平台信息。

**如果失败**：

| 现象 | 处理 |
| --- | --- |
| `command not found` | 安装：`sudo apt install nmap` / `brew install nmap` / Windows 官方安装包（勾选 Npcap） |
| 版本过老（缺 `--reason` 等参数） | 升级到当前稳定版 |

## A.3 第 2 步：扫本机

```bash
nmap -F 127.0.0.1
```

**期望结构**：

```text
Starting Nmap <版本> ( https://nmap.org ) at <时间>
Nmap scan report for localhost (127.0.0.1)
Host is up (<延迟>s latency).
Not shown: <N> closed tcp ports (reset)
PORT     STATE SERVICE
<端口>/tcp open  <服务名>
...
Nmap done: 1 IP address (1 host up) scanned in <秒> seconds
```

**你要观察的三件事**：

1. `Not shown` 那一行是 `closed (reset)` 还是 `filtered`——本机通常是 `closed`，说明没有防火墙拦你；
2. 开放端口的数量——取决于你本机跑着什么服务；
3. 结尾耗时——这是你后续比较的基线。

**如果本机也全 `filtered`**：本机防火墙在拦。Windows Defender 防火墙 / `iptables` / `ufw` 都可能。这是很好的第一课：**你以为的"端口关闭"可能只是"被自己的防火墙挡了"**。

## A.4 第 3 步：加版本探测

```bash
nmap -sV -p <上一步发现的开放端口> 127.0.0.1
```

**期望**：`VERSION` 列出现产品与版本，例如你的 SSH 服务、本地 Web 服务。

**观察**：

- 同一端口在 `-F` 时 `SERVICE` 列只有名字，`-sV` 后多了 `VERSION`；
- 若某端口显示 `unknown`，试 `--version-all` 单独扫它。

## A.5 第 4 步：看系统识别

```bash
nmap -O -p <开放端口>,1 127.0.0.1
```

**期望**：底部出现 `OS details` 或 `Aggressive OS guesses`。

**为什么加 `-p 1`**：`-O` 需要"至少一个开放端口 + 一个关闭端口"。端口 1 几乎肯定是关闭的，用它凑条件。

**如果完全没有 OS 段**：可能权限不足（需要 root/管理员），或本机所有端口都开着（少见）。

## A.6 第 5 步：默认脚本

```bash
nmap -sV -sC -p <开放端口> 127.0.0.1
```

**期望**：端口表下方出现脚本输出，形如：

```text
<端口>/tcp open  <服务>  <版本>
|_<脚本名>: <单行结果>
| <脚本名>: <第一行>
| <后续行>
|_<最后一行>
```

**重点练习**：分清 `|` 与 `|_`。`|_` 是某个脚本输出的最后一行。

## A.7 第 6 步：存档

```bash
nmap -sV -sC -p <开放端口> -oA basic-local-$(date +%Y%m%d) 127.0.0.1
```

**期望**：当前目录出现三个文件：

```text
basic-local-<日期>.nmap
basic-local-<日期>.xml
basic-local-<日期>.gnmap
```

打开 `.nmap`，确认第一行包含完整命令行与时间——**这就是你的证据链**。

## A.8 完整脚本版

```bash
#!/usr/bin/env bash
# 仅用于本机 / 自有靶场。使用前把 TARGET 改成一个你拥有控制权的地址。
set -euo pipefail

TARGET="${TARGET:-127.0.0.1}"
STAMP="$(date +%Y%m%d-%H%M%S)"
PREFIX="example-basic-${STAMP}"

echo "[1/4] 主机发现"
nmap -sn "$TARGET" -oA "${PREFIX}-01-discovery" || true

echo "[2/4] 常见端口"
nmap -F "$TARGET" -oA "${PREFIX}-02-ports"

echo "[3/4] 版本与脚本"
nmap -sV -sC -T4 "$TARGET" -oA "${PREFIX}-03-service"

echo "[4/4] 完成，产物："
ls -1 "${PREFIX}"*
```

## A.9 常见错误对照

| 你可能看到的 | 原因 | 处理 |
| --- | --- | --- |
| `Host seems down` | 目标禁 ICMP 或地址不存在 | `-Pn`；确认地址 |
| 全 `filtered` | 本机/目标防火墙 | 检查防火墙规则 |
| `requires root privileges` | 用了 `-sS`/`-O` 但没提权 | `sudo` 或换 `-sT` |
| 端口数与你预期不符 | 服务没起 / 端口改了 | `ss -tlnp`（Linux）或 `netstat -ano`（Windows）核对 |
| `.gnmap` 文件不存在 | 用了 `-oN` 而非 `-oA` | 改用 `-oA` |

## A.10 这一组练习教会你什么

| 练习 | 对应能力 | 相关章节 |
| --- | --- | --- |
| 扫本机 | 读懂端口表 | [04](../docs/04-port-scan.md) |
| 加 `-sV` | 区分"端口开"与"服务是什么" | [05](../docs/05-service-os.md) |
| 加 `-O` | 理解"至少一个开放+一个关闭端口"的前提 | [05](../docs/05-service-os.md) |
| 加 `-sC` | 读 `\|` / `\|_` 分组 | [06](../docs/06-nse.md) |
| `-oA` | 建立证据意识 | [07](../docs/07-speed-evasion-output.md) |
