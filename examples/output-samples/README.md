# 输出样本目录

本目录用于存放**真实的、已脱敏的** Nmap 输出样本，供读者对照"我的输出长什么样才算正常"。

## 当前状态

**本目录暂无可用的真实输出样本。** 这是有意为之，不是遗漏。

原因：仓库维护者不能在缺少真实运行环境的情况下生成这些文件。**任何"看起来像真的"但未经实际运行产出的输出，都会被读者当作标准答案，从而掩盖真正的问题**（比如把 `filtered` 当成 `closed`）。这比没有样本更糟。

## 如何贡献一个合格的样本

### 1. 环境要求

- 必须是你**拥有完全控制权**的环境：本机、本地虚拟机、容器、隔离靶场。
- 必须在文件中注明：操作系统、Nmap 版本、目标类型（本机/靶机/容器）。

### 2. 生成命令

用 `-oA` 生成三份，取 `.nmap` 与 `.xml`：

```bash
nmap -sV -sC -oA sample-<主题>-<日期> <目标IP>
```

### 3. 脱敏（必须逐项检查）

| 检查项 | 替换为 |
| --- | --- |
| IP 地址 | `192.0.2.x` / `198.51.100.x` / `203.0.113.x` |
| 主机名 / 域名 | `host-a` / `example.com` |
| MAC 地址 | `00:00:5e:00:53:xx` |
| 证书 CN / SAN | `test.example.com` |
| 服务 banner 中的产品序列号、内部路径 | 删除 |
| 用户名、邮箱、组织名 | `user-a` / `example.com` |
| 你自己的出口 IP | 删除或替换 |
| 时间戳 | 可保留（相对时间更有参考价值），但确认不泄露内部信息 |

自查：

```bash
grep -nE '([0-9]{1,3}\.){3}[0-9]{1,3}' sample.nmap \
  | grep -vE '192\.0\.2\.|198\.51\.100\.|203\.0\.113\.|192\.168\.|127\.0\.0\.1'
```

有输出就说明还有未脱敏的地址。

### 4. 命名规范

```text
output-samples/
├─ README.md
├─ basic-localhost.nmap             # 本机默认扫描
├─ ports-three-states.nmap          # 同时含 open/closed/filtered 的端口表
├─ service-web-ssh.nmap             # -sV 识别出 Web + SSH
├─ os-detection-linux.nmap          # -O 成功识别
├─ nse-default-scripts.nmap         # -sC 脚本输出（含 | 与 |_ 两种行）
├─ udp-openfiltered.nmap            # UDP 扫描的 open|filtered 实例
└─ host-seems-down.nmap             # 失败案例，同样有价值
```

**失败案例同样值得收录。** "全 `filtered` 长什么样""`Host seems down` 长什么样"比成功案例更有教学价值。

## 每个样本需要配的说明

在 PR 描述或同目录的 `.md` 里写清：

```markdown
- 文件：ports-three-states.nmap
- 命令：nmap -sS -p 22,80,443 192.0.2.10
- 环境：Ubuntu 靶机（VMware NAT），Nmap <版本>
- 想说明什么：STATE 列在同一张表里出现 open / closed / filtered 时如何判读
- 已脱敏：是（IP 已替换为 192.0.2.x）
```

## 审稿标准

| 检查 | 不通过 |
| --- | --- |
| 有真实运行痕迹 | 格式不合法、字段缺失、时间戳矛盾 |
| 已脱敏 | 出现文档段以外的 IP / 真实域名 |
| 有配套说明 | 只有文件，不说命令与用途 |
| 有教学价值 | 只是一份普通扫描，说明不了任何判读要点 |

## 相关章节

- [04 · 端口状态](../../docs/04-port-scan.md#41-六种端口状态)
- [05 · 服务与系统](../../docs/05-service-os.md#57-输出怎么读一个完整例子)
- [06 · 脚本输出读法](../../docs/06-nse.md)
- [CONTRIBUTING.md](../../CONTRIBUTING.md)
