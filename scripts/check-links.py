#!/usr/bin/env python3
"""检查仓库内 Markdown 的相对链接与锚点是否有效。

用法（在仓库根目录）：
    python scripts/check-links.py
    python scripts/check-links.py --ignore-missing-images   # 截图未补齐时用

退出码：0 = 全部通过；1 = 存在问题。
不联网，只做本地文件与标题锚点校验。
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def iter_md():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in ('.git', 'node_modules')]
        for name in filenames:
            if name.endswith('.md'):
                yield os.path.join(dirpath, name)


def slug(text):
    """近似 GitHub 的标题锚点算法：小写、去标点、空格转连字符。"""
    t = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text.strip())
    for ch in ('`', '*', '~'):
        t = t.replace(ch, '')
    t = t.lower()
    out = []
    for ch in t:
        if ch.isalnum() or ch in '-_':
            out.append(ch)
        elif ch == ' ':
            out.append('-')
    return ''.join(out)


def anchors(path):
    result = set()
    in_code = False
    with open(path, encoding='utf-8') as fh:
        for line in fh:
            if line.strip().startswith('```'):
                in_code = not in_code
                continue
            if in_code:
                continue
            m = re.match(r'^(#{1,6})\s+(.*?)\s*$', line)
            if m:
                result.add(slug(m.group(2)))
    return result


LINK = re.compile(r'(?<!!)\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)')
IMG = re.compile(r'!\[([^\]]*)\]\(([^)\s]+)')

SKIP_PREFIX = ('http://', 'https://', 'mailto:')
IGNORE_MISSING_IMAGES = '--ignore-missing-images' in sys.argv


def main():
    md_files = list(iter_md())
    anchor_map = {os.path.normpath(p): anchors(p) for p in md_files}
    problems = []

    for path in md_files:
        text = open(path, encoding='utf-8').read()
        rel = os.path.relpath(path, ROOT)
        for kind, rx in (('link', LINK), ('img', IMG)):
            for m in rx.finditer(text):
                label, target = m.group(1), m.group(2)
                if target.startswith(SKIP_PREFIX):
                    continue
                if kind == 'img' and not label.strip():
                    problems.append(f'[EMPTY ALT] {rel} -> {target}')
                target_path, _, anchor = target.partition('#')
                resolved = path if target_path == '' else os.path.normpath(
                    os.path.join(os.path.dirname(path), target_path))
                if not os.path.exists(resolved):
                    if kind == 'img' and IGNORE_MISSING_IMAGES:
                        continue
                    problems.append(f'[MISSING FILE] {rel} -> {target}')
                    continue
                if anchor and resolved in anchor_map and anchor not in anchor_map[resolved]:
                    problems.append(f'[BAD ANCHOR] {rel} -> {target}')

    print(f'checked {len(md_files)} markdown files')
    for p in problems:
        print('  ' + p)
    if problems:
        print(f'{len(problems)} problem(s)')
        return 1
    print('all links ok')
    return 0


if __name__ == '__main__':
    sys.exit(main())
