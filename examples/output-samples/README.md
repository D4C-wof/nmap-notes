# 输出样本：为什么这里是空的

## 结论

本仓库**不收录真实扫描输出**——整份的不收，片段也不收，脱敏过的同样不收。这不是没做完，是设计如此。

## 为什么这样设计

1. **输出带环境指纹**：Nmap 版本、网络路径、目标系统、防火墙策略不同，同一条命令的输出就不同。把别人的输出
   当标准答案，会把别人的误判一起学走（最典型：把 `filtered` 当成「端口关闭」）。
2. **脱敏无法被审计**：读者没法验证一份「已脱敏」的输出是否真的干净；漏一个内网 IP 或主机名，代价由仓库承担。
3. **笔记应该长在你自己的环境上**：自己跑一次、贴进对应章节，才是与你日常工作对得上的版本。

## 那 55 处【自测留白】怎么填

与 [README 4.6](../../README.md#46-用自己的输出填满留白推荐用法) 一致，三步：

1. **跑**：用留白上方那条命令，在你自己拥有控制权的环境里执行（本机、本地虚拟机、容器、隔离靶场）。
2. **抄**：把真实输出整段贴到留白下方，用 ```` ```text ```` 包起来，并注明环境（系统 / Nmap 版本 / 目标类型）。
3. **对**：拿自己的输出比照紧随其后的「结果判读」；对不上就回 [09 章](../../docs/09-troubleshooting.md)。

## 想在本地长期保存

Fork 本仓库 → 在**你自己的 fork** 里新建 `output-samples/` → 按下面规范放样本。升级上游时不会冲突，
也不会把真实数据带进公共仓库。

### 生成命令

```bash
nmap -sV -sC -oA sample-<主题>-<日期> <目标IP>     # 同时得到 .nmap / .xml / .gnmap
```

`.nmap` 给人读，`.xml` 给工具解析（也可用 Zenmap 打开），`.gnmap` 给 `grep` 用。

### 命名建议（自用）

```text
output-samples/
├─ basic-localhost.nmap             # 本机默认扫描
├─ ports-three-states.nmap          # 同时含 open/closed/filtered 的端口表
├─ service-web-ssh.nmap             # -sV 识别出 Web + SSH
├─ os-detection-linux.nmap          # -O 成功识别
├─ nse-default-scripts.nmap         # -sC 脚本输出（含 | 与 |_ 两种行）
├─ udp-openfiltered.nmap            # UDP 扫描的 open|filtered 实例
└─ host-seems-down.nmap             # 失败案例，同样有价值
```

**失败案例同样值得留。**「全 `filtered` 长什么样」「`Host seems down` 长什么样」比成功案例更能帮你排错。

### 脱敏自查（放进公开仓库前必做）

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

自查（有输出就说明还有未脱敏的地址）：

```bash
grep -nE '([0-9]{1,3}\.){3}[0-9]{1,3}' sample.nmap \
  | grep -vE '192\.0\.2\.|198\.51\.100\.|203\.0\.113\.|192\.168\.|127\.0\.0\.1'
```

### 给自己写一行说明

```markdown
- 文件：ports-three-states.nmap
- 命令：nmap -sS -p 22,80,443 192.0.2.10
- 环境：Ubuntu 靶机（VMware NAT），Nmap <版本>
- 想说明什么：STATE 列在同一张表里出现 open / closed / filtered 时如何判读
- 已脱敏：是（IP 已替换为 192.0.2.x）
```

## 相关章节

- [04 · 端口状态](../../docs/04-port-scan.md#41-六种端口状态)
- [05 · 服务与系统](../../docs/05-service-os.md#57-输出怎么读一个完整例子)
- [06 · 脚本输出读法](../../docs/06-nse.md)
- [CONTRIBUTING.md](../../CONTRIBUTING.md)
