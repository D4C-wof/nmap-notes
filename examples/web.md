# 示例 B · Web 场景流程（授权目标）

> **适用前提**：已获得对目标 Web 资产的**书面授权**，且授权覆盖"目录枚举"这类高频请求。
>
> **本文档不含任何真实扫描输出。** 所有"期望结果"为结构描述。
>
> ⚠️ 本流程第 5 步会发送数百至数千个 HTTP 请求。**没有明确授权就不要做这一步。**

## B.1 场景

你拿到一个授权目标 `www.example.com`（示例域名），任务是回答三个问题：

1. 它对外暴露了哪些 Web 入口？
2. 每个入口跑的是什么中间件、什么版本？
3. 有没有明显的配置问题（证书不匹配、默认页面、备份文件）？

**注意**：`www.example.com` 是 RFC 2606 保留域名，永远不指向真实站点。实际使用时替换为你获得授权的域名。

## B.2 第 1 步：先确认解析

```bash
dig +short www.example.com
```

**为什么先做这步**：

| 解析结果 | 含义 | 后续动作 |
| --- | --- | --- |
| 1 个 IP | 单点部署 | 直接扫 |
| 多个 IP | 负载均衡 / CDN | 确认这些 IP 是否都在授权范围内 |
| CNAME 指向 CDN 域名 | 你扫的是 CDN 边缘节点 | **停下**，确认授权是否覆盖 CDN；通常不覆盖 |
| 无结果 | 域名不存在或 DNS 问题 | 见 [09 章 9.3](../docs/09-troubleshooting.md#93-dns-解析失败) |

> **这是 Web 场景最常见的事故点**：扫到 CDN 节点，误以为扫到了源站，报告里写"源站暴露"，结果全是错的。

## B.3 第 2 步：端口摸底

```bash
nmap -F -Pn www.example.com -oA web-01-ports
```

**期望结构**：

```text
PORT     STATE SERVICE
80/tcp   open  http
443/tcp  open  https
```

**判读**：

| 现象 | 含义 |
| --- | --- |
| 只有 80/443 | 典型前置反代，源站在后面 |
| 多了 8080/8443 | 可能有管理面或后端直接暴露 |
| 多了 22 | 运维入口，注意授权是否覆盖 |
| 全 `filtered` | 有 WAF/防火墙，见 [09 章 9.5](../docs/09-troubleshooting.md#95-结果全是-filtered) |

**如果目标是"只开放 443"，还要扫 UDP 吗**：一般不需要。Web 场景 UDP 收益极低，且 `-sU` 很慢。

## B.4 第 3 步：服务与证书

```bash
nmap -sV -p 80,443 --script "http-title,http-headers,ssl-cert" www.example.com -oA web-02-service
```

**期望结构**：

```text
PORT    STATE SERVICE  VERSION
80/tcp  open  http     <产品名> <版本>
|_http-title: <页面标题>
443/tcp open  ssl/http <产品名> <版本>
| ssl-cert: Subject: commonName=<域名>
| Subject Alternative Name: DNS:<域名1>, DNS:<域名2>
| Not valid before: <日期>
|_Not valid after:  <日期>
|_http-title: <页面标题>
```

**判读清单**：

| 观察点 | 说明 | 能推断什么 | **不能**推断什么 |
| --- | --- | --- | --- |
| `Server` 头 | 中间件与版本 | 最外层是什么 | 后端是什么（可能被反代掩盖） |
| `http-title` | 页面标题 | 站点用途（登录页/默认页/错误页） | 是否存在漏洞 |
| 证书 SAN 列表 | 该证书覆盖的域名 | **可能还有其他资产**（重要线索） | 那些域名一定属于同一授权范围 |
| 证书 CN ≠ 访问域名 | 配置不匹配 | 配置问题或多域名部署 | "证书伪造" |
| 证书已过期 | 运维疏漏 | 低危配置问题 | — |
| 80 返回 301/302 | 强制跳转 HTTPS | 正常配置 | — |

**`Server` 头被改写的常见情况**：

```text
Server: nginx              ← 只说明最外层是 nginx
X-Powered-By: <框架>       ← 应用层框架，可能泄漏
（无 Server 头）           ← 被安全配置移除，属正常加固
```

## B.5 第 4 步：默认页面与常见路径线索（低风险）

```bash
nmap -p 80,443 --script "http-headers" --script-args http.useragent="Mozilla/5.0" www.example.com
```

**说明**：这里只换 UA。有些 WAF 会对默认 UA 直接返回 403，换 UA 能让探测拿到正常响应——**这属于正常访问行为，不是绕过**。

**如果你在结果里看到 403 / 429 / 验证码页**：说明被 WAF 拦了。**停下来联系授权方**，不要继续加大请求量。

## B.6 第 5 步：目录枚举（高风险，需专门授权）

> [!WARNING]
> `http-enum` 会向目标发送**数百到数千个** HTTP 请求。它：
>
> - 会出现在 Web 日志与 WAF 日志里，极易触发告警；
> - 可能被 WAF 判定为扫描并封禁你的出口 IP；
> - **在没有明确授权的环境里，这可能已经越界。**
>
> 执行前请确认：授权书写明允许"目录/路径枚举"，且约定了速率。

```bash
nmap -p 80,443 --script http-enum -T2 www.example.com -oA web-03-enum
```

**期望结构**：

```text
80/tcp open  http
| http-enum:
|   /admin/: <描述>
|   /backup/: <描述>
|_  /phpmyadmin/: <描述>
```

**发现路径后该做什么**：

| ❌ 错误做法 | ✅ 正确做法 |
| --- | --- |
| 立刻打开 `/admin/` 试着登录 | 记录路径，写进报告 |
| 试着猜备份文件名下载 | 标注"疑似备份目录，未验证" |
| 对 `/phpmyadmin/` 试默认口令 | 交人工与授权方确认后续动作 |

**理由**：发现路径是"信息收集"，登录尝试是"访问控制测试"。这两者在授权书里通常是分开的条目。

## B.7 第 7 步：整理输出

```bash
ls -1 web-*
# web-01-ports.nmap / .xml / .gnmap
# web-02-service.nmap / .xml / .gnmap
# web-03-enum.nmap / .xml / .gnmap
```

**报告里该写什么**：

| 字段 | 来源 |
| --- | --- |
| 扫描时间窗 | `.nmap` 头部的 `scan initiated` |
| 完整命令 | `.nmap` 头部的 `as:` 之后 |
| 开放端口 | 端口表 |
| 中间件与版本 | `VERSION` 列 + `Service Info` |
| 证书信息 | `ssl-cert` 脚本输出 |
| 发现的路径 | `http-enum` 输出（标注"未验证"） |

## B.8 一页命令汇总

```bash
# 0. 解析确认
dig +short <授权域名>

# 1. 端口
nmap -F -Pn <授权域名> -oA web-01-ports

# 2. 服务 + 证书 + 标题
nmap -sV -p 80,443 --script "http-title,http-headers,ssl-cert" <授权域名> -oA web-02-service

# 3. 目录枚举（需专门授权）
nmap -p 80,443 --script http-enum -T2 <授权域名> -oA web-03-enum

# 4. 复核：只对确认端口重扫一次，确保结果可复现
nmap -sV -p 80,443 <授权域名> -oA web-04-verify
```

## B.9 常见坑

| 坑 | 现象 | 处理 |
| --- | --- | --- |
| 扫到 CDN | 版本显示 CDN 厂商的产品 | 停下，确认是否为源站 |
| 80 和 443 结果不一致 | 443 有 `http-title`，80 只有 301 | 正常，80 是跳转 |
| `http-title` 为空 | 页面无 `<title>` 或是二进制响应 | 正常，改用 `http-headers` 看 |
| 大量 403 | WAF 拦了 | 停，联系授权方 |
| 证书里有一堆陌生域名 | SAN 列表 | 记录为资产关联线索，**不要**自行扩大扫描范围 |
| 版本号与官方公告不符 | 反代改写或自定义编译 | 记【待核实】，不要断言 |

## B.10 对应章节

| 步骤 | 章节 |
| --- | --- |
| 解析确认 | [02](../docs/02-target.md) / [09](../docs/09-troubleshooting.md) |
| 端口摸底 | [04](../docs/04-port-scan.md) |
| 服务与证书 | [05](../docs/05-service-os.md) / [06](../docs/06-nse.md) |
| 目录枚举与风险 | [06](../docs/06-nse.md#66-脚本类别与风险分级) |
| 输出存档 | [07](../docs/07-speed-evasion-output.md) |
| 授权边界 | [10](../docs/10-legal-and-safety.md) |
