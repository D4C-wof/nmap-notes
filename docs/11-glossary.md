# 11 · 术语表

> 按拼音/字母混排不太适合检索，这里按**主题分组**，组内按字母序。带 ★ 的是必须掌握的。

## 11.1 端口与状态

| 术语 | 英文 | 含义 |
| --- | --- | --- |
| ★ 端口 | port | 传输层用 0–65535 的编号区分同一主机上的不同服务。TCP 与 UDP 的同一编号是两个独立入口 |
| ★ 开放 | open | 有程序在监听，且对探测有正常响应 |
| ★ 关闭 | closed | 主机可达，但没有程序监听该端口（TCP 通常回 RST） |
| ★ 被过滤 | filtered | 探测包被丢弃，**无法判断**端口开关。不等于"关闭" |
| 未过滤 | unfiltered | 包能到达主机，但当前扫描技术不判断开关（`-sA` 的典型结果） |
| 开放或被过滤 | open\|filtered | 无响应时无法区分"开着但不回包"与"被丢弃"（UDP、FIN 类扫描常见） |
| 关闭或被过滤 | closed\|filtered | 同上，但针对关闭方向；日常少见 |
| ★ 探测 | probe | Nmap 发给目标、用于引发可识别响应的数据包 |
| 判定原因 | reason | Nmap 对某端口状态给出判定所依据的响应类型，`--reason` 显示 |

## 11.2 扫描技术

| 术语 | 英文 | 含义 |
| --- | --- | --- |
| ★ 半开扫描 | SYN scan / half-open | `-sS`，只完成三次握手前两步，不建立完整连接 |
| ★ 全连接扫描 | TCP connect scan | `-sT`，调用 `connect()` 完成完整握手 |
| NULL 扫描 | NULL scan | `-sN`，发送不带任何 TCP 标志位的包 |
| FIN 扫描 | FIN scan | `-sF`，只带 FIN 标志 |
| 圣诞树扫描 | Xmas scan | `-sX`，FIN+PSH+URG 全置位，像点亮的圣诞树 |
| ACK 扫描 | ACK scan | `-sA`，只判断端口是否被防火墙过滤，**不判断开关** |
| UDP 扫描 | UDP scan | `-sU`，靠 ICMP 端口不可达或应用响应判定 |
| 原始套接字 | raw socket | 直接构造 IP/TCP 包的能力，多数扫描技术需要它（root/管理员） |
| 三次握手 | three-way handshake | SYN → SYN/ACK → ACK |
| RST | reset | TCP 重置包。收到它说明**主机可达**但连接被拒 |
| ★ 指纹 | fingerprint | 由响应特征构成的识别依据（服务指纹、OS 指纹） |

## 11.3 主机发现

| 术语 | 英文 | 含义 |
| --- | --- | --- |
| ★ 主机发现 | host discovery | 扫描前判断目标是否存活的过程 |
| ★ 存活 | up | 至少一种探测得到回应 |
| ARP 扫描 | ARP scan | `-PR`，二层探测，仅局域网有效，最可靠 |
| ICMP echo | ICMP echo | 传统 `ping`，最容易被防火墙拦 |
| 诱饵 | decoy | `-D`，用其他源地址混入扫描流量 |
| 源地址伪造 | source spoofing | `-S`，伪造发包源地址。会导致收不到回包 |

## 11.4 服务与系统识别

| 术语 | 英文 | 含义 |
| --- | --- | --- |
| ★ 服务版本探测 | version detection | `-sV`，主动发探测包匹配指纹库，得出产品与版本 |
| 探测强度 | version intensity | 0–9。`--version-light`=2，默认=7，`--version-all`=9 |
| ★ 操作系统识别 | OS detection | `-O`，靠 TCP/IP 栈实现差异比对指纹 |
| 激进猜测 | aggressive guessing | `--osscan-guess`，列出低置信度候选系统 |
| 置信度 | confidence | 猜测的正确概率估计，如 95% |
| CPE | Common Platform Enumeration | 标准化产品命名，形如 `cpe:/a:vendor:product:version` |
| Banner | banner | 服务在连接时主动返回的标识字符串 |
| 反向代理改写 | — | 反代/WAF 会改或去除真实服务的 banner，导致版本误判 |

## 11.5 NSE 与脚本

| 术语 | 英文 | 含义 |
| --- | --- | --- |
| ★ 脚本引擎 | NSE (Nmap Scripting Engine) | 用 Lua 编写的可扩展扫描能力 |
| 脚本类别 | script category | 脚本的标签，如 `safe`、`discovery`、`brute`、`dos` |
| 默认脚本集 | default scripts | `-sC` / `--script=default` |
| 脚本参数 | script args | `--script-args key=value` 传给脚本 |
| 表达式 | script expression | `default and not intrusive` 这类集合运算 |
| `\|` / `\|_` | — | 脚本输出的中间行 / 最后一行标记 |

## 11.6 速度与输出

| 术语 | 英文 | 含义 |
| --- | --- | --- |
| ★ 定时模板 | timing template | `-T0`~`-T5`，预设的超时/重试/并发/延迟组合 |
| 发包速率 | packet rate | 每秒发出的探测包数，`--min-rate` / `--max-rate` |
| 重试 | retries | 未收到响应时的重发次数，`--max-retries` |
| 主机超时 | host timeout | `--host-timeout`，超时则跳过该主机（静默） |
| 分片 | fragmentation | `-f`，把 IP 包拆成小片 |
| 诱饵 | decoy | 见 11.3 |
| ★ 标准输出 | normal output | `-oN`，给人读 |
| ★ XML 输出 | XML output | `-oX`，给工具读，信息最全 |
| grep 输出 | grepable output | `-oG`，一行一主机，已被上游标记为过时 |
| 全格式输出 | all formats | `-oA`，一次产出 `.nmap`/`.xml`/`.gnmap` |

## 11.7 网络与合规

| 术语 | 英文 | 含义 |
| --- | --- | --- |
| ★ 授权 | authorization | 资产所有者或有权委托方给出的书面许可 |
| ★ 范围 | scope | 授权中明确列出的目标与手段边界 |
| 交战规则 | rules of engagement (RoE) | 测试的时间窗、手段、速率、联系人等约定 |
| 文档保留地址 | documentation address | RFC 5737 的 `192.0.2.0/24`、`198.51.100.0/24`、`203.0.113.0/24`，永不由真实主机使用 |
| 私网地址 | private address | RFC 1918 的 `10/8`、`172.16/12`、`192.168/16` |
| IPv6 文档段 | — | RFC 3849 的 `2001:db8::/32` |
| 有状态防火墙 | stateful firewall | 按连接状态判断，能识别半开扫描 |
| 无状态包过滤 | stateless packet filter | 只看单个包的头部，可被分片/标志位技巧绕过 |
| IDS / IPS | Intrusion Detection/Prevention System | 入侵检测/防御系统。IPS 会主动阻断 |
| WAF | Web Application Firewall | Web 应用防火墙，对 `http-*` 脚本特别敏感 |
| 速率限制 | rate limiting | 超过阈值即丢包或封禁，表现为突然全 `filtered` |

## 11.8 常用缩写

| 缩写 | 全称 | 中文 |
| --- | --- | --- |
| CIDR | Classless Inter-Domain Routing | 无类别域间路由，`192.0.2.0/24` 这种写法 |
| TTL | Time To Live | IP 包生存跳数，可用于推断网络距离 |
| MTU | Maximum Transmission Unit | 最大传输单元，分片相关 |
| OUI | Organizationally Unique Identifier | MAC 地址前 24 位，可用于识别设备厂商 |
| PTR | Pointer Record | 反向 DNS 记录，IP → 域名 |
| AXFR | Zone Transfer | DNS 区域传送，`dns-zone-transfer` 脚本尝试的操作 |
| SMB | Server Message Block | Windows 文件共享协议（445） |
| SNMP | Simple Network Management Protocol | 网络设备管理协议（161/udp） |

## 本章初学者检查清单

- [ ] 能准确解释 `open` / `closed` / `filtered` 三者的判定依据差异
- [ ] 知道 `open|filtered` 为什么会出现，以及它不能当"开放"用
- [ ] 能说出 `-sS` 与 `-sT` 在协议层面的差别
- [ ] 知道 CPE 是什么，以及它能拿去做什么
- [ ] 记得文档保留地址段（`192.0.2.x` 等）为什么安全
- [ ] 能区分 IDS 与 IPS 的行为差异

## 本章修改说明

1. 本章为**完全新增**。原笔记未定义任何术语，直接使用"半开扫描""filtered""指纹"等词，初学者无法自查。
2. 按主题分组而非字母序，因为本书读者是"边读边查"，按场景分组比按字母更易命中。
3. 术语解释一律给"判定依据"而非"结论"。例如 `filtered` 强调"无法判断"，`RST` 强调"主机可达"——这两处是初学者最高频的误读点。
4. 收录 11.7 网络与合规术语，与 [10 章](10-legal-and-safety.md) 呼应；文档保留地址段单独列条，因为全书所有示例都依赖它。
