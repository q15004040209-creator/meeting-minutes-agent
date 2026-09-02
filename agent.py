#!/usr/bin/env python3
"""
meeting-minutes-agent — AWS Agents for Humans Hackathon (Professional track)
用 Strands Agents SDK 把会议转录端到端转成结构化纪要 + 行动项。

运行：
    pip install strands-agents
    export AWS_REGION=us-east-1   # Strands 默认走 Bedrock，需可访问的模型
    python agent.py --transcript meeting.txt

说明：本文件为参赛起步实现，真实模型/model_id 以你 Bedrock 可用区为准。
"""
import argparse
import json
import sys


# 结构化输出 schema：约束模型只产出可机器解析的纪要
MINUTES_SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {"type": "string", "description": "3 句话内的会议摘要"},
        "decisions": {"type": "array", "items": {"type": "string"}},
        "action_items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "task": {"type": "string"},
                    "owner": {"type": "string"},
                    "due": {"type": "string"},
                },
            },
        },
        "open_questions": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["summary", "decisions", "action_items", "open_questions"],
}


def build_agent():
    """构造 Strands Agent。仅依赖 strands-agents 公共 API。"""
    from strands import Agent

    # model 用环境变量或默认；真实部署时换成你 Bedrock 可用的 model_id
    agent = Agent(
        system_prompt=(
            "你是一名严谨的会议纪要秘书。把会议转录压缩成结构化纪要："
            "摘要、决策、行动项(含 owner/due)、开放问题。"
            "行动项 owner 无法从文本确定时写'待定'。"
            "只在确有冲突或需拍板时才标注 open_questions。"
        ),
        # Strands 支持用工具/structured output 约束；此处以 prompt 约束为主
    )
    return agent


def render_markdown(minutes: dict) -> str:
    lines = ["# 会议纪要", ""]
    lines += ["## 摘要", minutes.get("summary", ""), ""]
    lines += ["## 决策"]
    for d in minutes.get("decisions", []):
        lines.append(f"- {d}")
    lines += ["", "## 行动项"]
    for a in minutes.get("action_items", []):
        lines.append(f"- [{a.get('owner','待定')}] {a.get('task')}（截止 {a.get('due','未定')}）")
    lines += ["", "## 开放问题"]
    for q in minutes.get("open_questions", []):
        lines.append(f"- {q}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--transcript", required=True, help="会议转录文本文件路径")
    args = ap.parse_args()

    with open(args.transcript, encoding="utf-8") as f:
        transcript = f.read()

    agent = build_agent()
    # 用 JSON 约束让输出可被程序消费；真实环境可用 agent.tool / structured output
    prompt = (
        f"请按以下 JSON schema 产出纪要：\n{json.dumps(MINUTES_SCHEMA, ensure_ascii=False)}\n\n"
        f"会议转录：\n{transcript}"
    )
    raw = agent(prompt)
    text = getattr(raw, "text", str(raw))

    try:
        minutes = json.loads(text)
    except json.JSONDecodeError:
        # 兜底：模型未严格返回 JSON，原样保存待人工整理
        minutes = {"summary": text, "decisions": [], "action_items": [], "open_questions": []}

    md = render_markdown(minutes)
    with open("minutes.md", "w", encoding="utf-8") as f:
        f.write(md)
    print(md)
    print("\n[ok] 已写入 minutes.md", file=sys.stderr)


if __name__ == "__main__":
    main()
