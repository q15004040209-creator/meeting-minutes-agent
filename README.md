# meeting-minutes-agent · AWS Agents for Humans Hackathon

> 赛道：**Professional Agents**（让知识工作者大幅变强，处理重复且判断密集的任务）
> 框架：**Strands Agents SDK**（AWS 开源，原生对接 Bedrock）
> 提交截止：2026-09-14 17:00 PDT

## 它解决什么问题

知识工作者每周被会议淹没：平均 1 小时会 = 30 分钟整理纪要 + 行动项跟进。本 Agent 在后台吃掉会议转录文本，端到端产出**结构化纪要 + 责任人行动项 + 待决问题**，只在"有冲突/需拍板"时 ping 人——正好契合比赛"runs quietly, surfaces on real decisions"的要求。

## 运行

```bash
pip install strands-agents
export AWS_REGION=us-east-1        # 或配置 Bedrock 访问
python agent.py --transcript meeting.txt
```

输出 `minutes.md`：摘要 / 决策 / 行动项( owner + due ) / 开放问题。

## 结构（详见 ARCHITECTURE.md）
- 输入层：转录文本 / 历史纪要
- 代理层：Strands Agent + 结构化输出工具（JSON schema 约束）
- 决策层：冲突/待决项检测 → 触发人工确认
- 产出层：Markdown 纪要 + 可订阅行动项

## 许可
MIT（见 LICENSE）

## Demo 视频脚本（≤5 min，待人工录制）
1. 0:00 放一段 3 分钟模拟会议录音转文字
2. 1:00 运行 `python agent.py` 实时生成纪要
3. 2:30 高亮行动项自动提取 + owner 指派
4. 4:00 展示"开放问题"触发人工 ping 的设计
5. 4:40 复盘：省下的整理时间 + 可复用于任意会议

## 状态
- [x] README / agent.py / LICENSE / ARCHITECTURE 起步包
- [ ] Strands SDK 实测跑通（待环境）
- [ ] Demo 视频（待录屏）
- [ ] 公开仓库 + 提交（待 GitHub 凭证）
