---
artifact_contract: ce-unified-plan/v1
artifact_readiness: implementation-ready
execution: code
product_contract_source: ce-plan-bootstrap
title: "Simplify PrepBench Public Workspace Contract"
date: 2026-07-05
target_repo: "."
owner: "PrepBench"
---

## Goal Capsule

PrepBench 公开使用方式只保留三个 mode：

- `clarified`：给消歧后的 query 和输入表，agent 直接产出结果表。
- `interactive`：给原始 query 和输入表，agent 先和 user simulator 交互消歧，再产出结果表。
- `workflow`：在 `interactive` 基础上额外给 workflow/operator prompt，agent 可调用 workflow executor，最后产出结果表。

核心边界：推理由用户自己的黑盒 agent 完成；PrepBench 只负责初始化 case workspace、提供 simulator/executor 工具、评估最终结果表。

资产隔离采用 **honor-system**：workspace 只暴露当前 mode 允许的输入（`clarified` 给 `query_full.md` → `query.md`，`interactive`/`workflow` 给 `query.md`）。但 `query_full.md`、`amb_kb.json`、GT (`src/evaluate/gt/`) 仍然存在于 repo 中，PrepBench 不做强制沙箱隔离。契约靠诚信规则约束选手：`interactive`/`workflow` 下不得直接读取 `query_full.md`/`amb_kb.json`/GT。文档必须明确声明这一点，不得暗示这些资产被"藏起来"。

inputs 形态（缓解父目录逃逸）：workspace 里创建**真实** `inputs/` 目录，再把 `data/<case_id>/inputs/` 下的文件**逐个 symlink** 进去（碰到子目录则递归建目录+逐文件 symlink）。这样 `inputs/` 的父目录就是 workspace 本身，`inputs/../` 不再直达 `data/<case_id>/` 里的 `query_full.md`/`amb_kb.json`。honor-system 声明仍写，但只需约束"不要主动去 repo 的 `data/` 里翻敏感文件"，压力更小。`query.md` 本就是单文件 symlink，不涉及目录逃逸。

## Product Contract

### 用户流程

```text
prepare_run -> user agent runs in case workspace -> result/output_*.csv -> evaluate_submission
```

每个 case workspace 放在：

```text
@runs/<agent>/<mode>/<case_id>/
```

最终评分只读取：

```text
@runs/<agent>/<mode>/<case_id>/result/output_*.csv
```

### Workspace 形态

```text
@runs/<agent>/<mode>/<case_id>/
  query.md
  inputs/
  simulator.md              # interactive/workflow mode
  result/
  workflow_prompt.yaml      # 仅 workflow mode
```

mode 对应初始化：

```text
clarified:
  query.md -> data/<case_id>/query_full.md
  inputs/  -> 真实目录，内含 data/<case_id>/inputs/* 的逐文件 symlink

interactive:
  query.md -> data/<case_id>/query.md
  inputs/  -> 真实目录，内含 data/<case_id>/inputs/* 的逐文件 symlink
  simulator.md

workflow:
  query.md            -> data/<case_id>/query.md
  inputs/             -> 真实目录，内含 data/<case_id>/inputs/* 的逐文件 symlink
  simulator.md
  workflow_prompt.yaml -> src/agents/prompts/flow_agent.yaml（改造后的纯算子契约 prompt，见 Unit 0）
```

### 用户入口形态

初始化：

```bash
python scripts/prepare_run.py \
  --mode clarified \
  --case case_001 \
  --run-root @runs/my_agent/clarified
```

评估：

```bash
python scripts/evaluate_submission.py \
  --mode clarified \
  --run-root @runs/my_agent/clarified
```

workflow executor 以 Python API 形式暴露给用户 agent；命令行只作为调试入口保留，不作为公开主路径。agent 在 case workspace 内运行，`execute_flow_file` 默认从 workspace 读写，无需传路径：

```python
from py2flow.api import execute_flow_file

# agent 站在 case workspace 里运行；默认 input_root=./inputs、output_root=./result
execute_flow_file(flow_path="<agent-flow-json>")
```

默认路径规则：`input_root` 默认为当前工作目录下的 `inputs/`，`output_root` 默认为当前工作目录下的 `result/`；两者均可显式传参覆盖。flow JSON 内的 `inputs/xxx.csv` 与输出文件名由 `exec_flow` 分别重写到 `input_root`/`output_root`。

`<agent-flow-json>` 路径由 agent 自己决定；workflow 文件不参与硬评分。

参数约定（实现时定死）：

- `--run-root` 指向 `@runs/<agent>/<mode>/`（不含 case_id）。run-root 路径里已带 mode 段，`--mode` 只做校验：若 `--mode` 与 run-root 末段不一致则报错。
- `prepare_run.py --case <case_id>` 必填，指定要初始化哪个 case。
- `evaluate_submission.py` 默认评估 GT 下全部 case；`--case <case_id>` 可选，用于只评单个 case（调试）。Verification 里的 `--case case_099` 属于这种单 case 调试用法。

## Planning Contract

已定决策：

- 公开 mode 只有 `clarified`、`interactive`、`workflow`。
- 旧的 `direct`（原始 query、无 simulator）从公开面删除。`docs/RESULTS.md` 里的 direct 数据保留为 paper-only 历史结果，并明确标注公开 mode 不含 direct，避免读者拿 paper 三档对公开 mode。
- 资产隔离采用 honor-system，不做强制沙箱。文档需含诚信声明。
- 用户 agent 只需要面对 case workspace。
- 三种 mode 的最终产物统一为 `result/output_*.csv`。
- workflow mode 额外 symlink workflow/operator prompt。
- workflow executor 是 agent 可调用工具，用于执行 agent 生成的 workflow。
- workspace 使用 symlink。
- 评测核心只保留一份，留在 `evaluate/` 包里；旧的 `evaluate.batch`（读 `solution/cand`）退休或改成薄 wrapper。

实现时需要定死：

- `workflow_prompt.yaml` 的源文件是 `src/agents/prompts/flow_agent.yaml`，但**必须先原地改写**为纯算子契约（见 Unit 0）。现状：`flow_agent.yaml` 全文是「把给定 solution.py 翻译成 flow.json」的语义（`system`/`core_guidelines` 明写 solution.py，输出路径写死 `flow_cand/`，末尾还有内部 retry-feedback 协议）。`data/` 里没有 solution.py，新 `workflow` mode 是 agent 基于 query/workspace 直接产出 workflow，直接 symlink 会让 agent 读到不存在的 solution.py。已确认 `flow_agent.yaml`/`flow_agent.jinja2` 无任何 Python 代码加载（仅三处文档引用），改写不影响任何内部路径。
- `evaluate_submission.py` 正式评估遇到缺失 case（`NOT_FOUND`）时**非零退出**：正式评估的消费者是 leaderboard/CI gate，漏交 case 应为硬失败，不引入 `--allow-missing` 之类只为测试改接口的开关。
- simulator 目前只有 Python API（`simulator.LocalUserSimulatorAPI`），没有 CLI。本次不新增 simulator CLI；`simulator.md` 只给 Python API 使用示例。workflow executor 也以 Python API 作为公开主路径，CLI 仅保留为调试/维护入口。
- `evaluate_submission.py` 输出格式：`summary.json`（per-case + aggregate）和 `summary.csv` 都写。
- 评估输出位置固定为 `@runs/<agent>/<mode>/evaluation/summary.json` 和 `@runs/<agent>/<mode>/evaluation/summary.csv`。
- `--run-root` 已在路径里编码了 mode/agent，但仍保留显式 `--mode` 参数，并在入口处校验 `--mode` 与 run-root 末段一致，不一致直接报错。
- `--case` 为可选参数：不传则评估 GT 下全部 case，传则只评估指定 case（用于调试）。`prepare_run.py` 的 `--case` 为必填。

## Implementation Units

### Unit 0: 把 flow_agent.yaml 改写成纯算子契约

文件：

- `src/agents/prompts/flow_agent.yaml`
- `src/agents/prompts/templates/flow_agent.jinja2`
- `docs/prompts/WORKFLOW_DAG_PROMPT.md`

前提事实：

- `flow_agent.yaml` 现状是 solution.py 翻译器语义；`operator_definitions` + `operator_cookbook` 是纯算子契约，与「输入从哪来」无关，可原样保留。
- 无 Python 代码加载 `flow_agent.yaml`/`flow_agent.jinja2`；simulator 走的是独立的 `clarify_agent.jinja2`。因此可安全原地改写。

改动：

- `system:` / `core_guidelines:`：去掉「translate the given solution.py」，改成「依据 py2flow 执行器契约，基于 query 和输入表设计一个可被 py2flow 校验并执行的 flow.json」。职责收敛为「说明执行器接受什么样的 workflow」。
- 输出路径：与执行器默认对齐。agent 站在 workspace 里，写 `output_*.csv`（`exec_flow` 会把 `flow_cand/` 前缀或裸文件名归一到 `output_root`/`result/`）。
- 保留 `operator_definitions` + `operator_cookbook` 主体。
- 删除 `exec_error_instructions:` 内部 retry-feedback 段（public 不需要）。
- `flow_agent.jinja2`：去掉 solution.py 注入块与 feedback 块；若 template 不再被 prepare_run 使用可直接删，由实现时决定。
- `docs/prompts/WORKFLOW_DAG_PROMPT.md`：同步去掉 solution.py 语义，或并入 `docs/WORKFLOW_EXECUTION.md`。

### Unit 1: 改公开文档

文件：

- `README.md`
- `docs/DATASET.md`
- `docs/EVALUATION.md`
- `docs/USER_SIMULATOR.md`
- `docs/WORKFLOW_EXECUTION.md`
- `docs/RESULTS.md`
- `examples/`

改动：

- README 首屏讲清三个 mode、workspace、结果表目录、评估命令。
- 删除旧的 `direct`、`oracle`、`solution/cand`、`@output/<method>/<setting>` 公共路径。
- `docs/WORKFLOW_EXECUTION.md` 改成 workflow mode agent 可调用工具说明。

### Unit 2: 新增 workspace 初始化

文件：

- `scripts/prepare_run.py`
- `src/prepbench/workspaces.py`
- `tests/test_prepare_run.py`

行为：

- 校验 mode。
- 创建 case workspace。
- `query.md`：单文件 symlink（clarified 指向 `query_full.md`，interactive/workflow 指向 `query.md`）。
- `inputs/`：创建真实目录，把 `data/<case_id>/inputs/` 下的文件逐个 symlink 进去（碰到子目录则递归建目录 + symlink 文件）。目的是让 `inputs/` 的父目录是 workspace 自己，堵掉 `inputs/../query_full.md` 这类父目录逃逸。
- interactive/workflow mode 创建 `simulator.md`，只放 Python API 最小示例和诚信边界，不新增 simulator CLI。
- 创建 `result/`。
- workflow mode 额外 symlink `workflow_prompt.yaml`（源为 Unit 0 改写后的 `src/agents/prompts/flow_agent.yaml`）。
- 默认不覆盖已有目录，提供 `--force`。
- `--case` 必填。

### Unit 3: 结果目录评估入口（复用现有评测核心）

文件：

- `scripts/evaluate_submission.py`
- `src/evaluate/batch.py`（抽取核心 + 旧入口退休/薄 wrapper）
- `src/prepbench/submission_eval.py`（仅 run-root/mode 布局解析这层薄逻辑）
- `tests/test_evaluate_submission.py`

前提事实：

- 真正的评测逻辑只有 `evaluate.core.evaluate()` 一份；`evaluate.batch.run_batch()` 只是「发现 case + 选结果目录 + 写 summary」的外壳。
- 现在 `make check` 只跑 `evaluate.batch --help` 冒烟，CI 未跑全量 batch。

行为：

- 把 `run_batch` 中「遍历 GT case → 定位结果目录 → 调 evaluate → 写 summary」抽成与目录布局无关的核心函数（放 `evaluate/` 包内），结果目录定位方式由调用方传入。
- `evaluate_submission.py` 复用该核心：默认从 GT 发现全部 case，结果目录定位到 `result/`，读取 `output_*.csv`。
- 缺结果表时把该 case 记为失败（`NOT_FOUND`）。
- 退出码：只要有任一 case 缺失或评估失败即非零退出（供 leaderboard/CI gate 用）；全部通过才退出 0。不引入 `--allow-missing` 之类为测试改产品接口的旁路。
- 输出 per-case 和 aggregate 到 `evaluation/summary.json` 和 `evaluation/summary.csv`。
- 旧 `evaluate.batch`（读 `solution/cand`）退休：删除或改成指向新核心的薄 wrapper；`make check` 冒烟改指 `evaluate_submission.py --help`。
- 不要把评测逻辑复制进 `prepbench` 包；`submission_eval.py` 只做布局/mode 解析。

### Unit 4: 对齐 workflow executor（API 为主，CLI 保留调试）

前提事实：

- `py2flow/api.py` 现在暴露 `execute_flow_dict`；需要新增 `execute_flow_file(flow_path, ...)`，加载 flow JSON 后调用 `exec_flow` 执行。
- `exec_flow` 强校验 `input_root`/`output_root`（必须存在的目录），并把 flow 内 `inputs/xxx.csv`、输出文件名分别重写到这两个 root。因此 `execute_flow_file` 必须能确定这两个 root。

文件：

- `src/py2flow/api.py`（新增 `execute_flow_file`）
- `docs/WORKFLOW_EXECUTION.md`（改写为 workflow mode 可调用 API 说明；CLI 只作为调试入口）
- `tests/test_workflow_execution.py`（补 `execute_flow_file` 用例）
- `scripts/execute_workflow.py`（仅在默认 output 路径描述上与新契约对齐，逻辑不必大改）

行为：

- 暴露 `execute_flow_file(flow_path, input_root=None, output_root=None, **kw)`。
- 默认路径规则：agent 在 case workspace 内运行，`input_root` 默认为当前工作目录下的 `inputs/`，`output_root` 默认为当前工作目录下的 `result/`；显式传参则覆盖默认。
- `output_root` 不存在时先创建（`result/` 可能是空目录）。
- `--evaluate` 只作为调试便利，正式评分仍走 `evaluate_submission.py`。

### Unit 5: 清理示例和检查项

文件：

- `README.md`
- `examples/`
- `Makefile`
- `.gitignore`
- `tests/fixtures/workflows/`

改动：

- 提供一个 case 的最小跑通示例。
- 可选新增 `make smoke-public-contract`。
- 加文档残留检查，避免旧 mode 和旧目录继续出现。
- `.gitignore` 忽略 `@runs/`；Makefile 的 clean target 一并清 `@runs/`（现有 clean-outputs 只清 `@output`）。
- 将 `data/case_099/flow_compressed.json` 移到 `tests/fixtures/workflows/case_099_workflow.json`，避免 reference workflow 出现在 public case input 目录中。

## Verification Contract

实现后跑：

```bash
PYTHON=python3 make check
PYTHON=python3 make release-validate
python scripts/prepare_run.py --mode clarified --case case_001 --run-root @runs/smoke/clarified --force
python scripts/prepare_run.py --mode interactive --case case_001 --run-root @runs/smoke/interactive --force
python scripts/prepare_run.py --mode workflow --case case_099 --run-root @runs/smoke/workflow --force
PYTHONPATH=src python -m unittest tests.test_workflow_execution tests.test_prepare_run tests.test_evaluate_submission
# smoke 用 case_099 自带的 flow_compressed.json 当「参考选手」，真跑一遍 executor 产出
# result/output_*.csv，再评估，从而端到端验证 executor -> evaluate，且退出码应为 0。
cp tests/fixtures/workflows/case_099_workflow.json @runs/smoke/workflow/case_099/flow.json
# cd 进 workspace 后 py2flow 不在 import 路径上，需把 repo 的 src 加到 PYTHONPATH（用绝对路径）。
REPO_SRC="$(pwd)/src"
( cd @runs/smoke/workflow/case_099 && PYTHONPATH="$REPO_SRC" python -c "from py2flow.api import execute_flow_file; execute_flow_file(flow_path='flow.json')" )
python scripts/evaluate_submission.py --mode workflow --run-root @runs/smoke/workflow --case case_099
# 残留检查：direct/oracle 不应出现在公开使用路径。RESULTS.md 保留 direct 作为 paper-only
# 历史结果，需从残留检查中排除（或限定在明确标注的历史章节内）。
rg -n "\b(direct|oracle)\b" README.md docs examples --glob '!docs/RESULTS.md' --glob '!docs/plans/**'
rg -n "solution/cand|@output" README.md docs examples --glob '!docs/plans/**'
```

## Definition of Done

- README 只讲 `clarified`、`interactive`、`workflow`。
- 用户能初始化 workspace、运行自己的 agent、提交结果表目录、调用评估。
- workflow mode workspace 额外包含 `workflow_prompt.yaml`。
- interactive/workflow workspace 包含 `simulator.md`。
- `flow_agent.yaml` 已改为纯算子契约（无 solution.py 翻译语义、无 retry 协议、输出路径与执行器对齐）；`flow_agent.jinja2` 和 `docs/prompts/WORKFLOW_DAG_PROMPT.md` 同步或删除。
- 三种 mode 统一评估 `result/output_*.csv`。
- workflow executor 可作为 Python API 被 agent 调用；CLI 只作为调试/维护入口。
- 旧 mode 和旧输出 layout 不再出现在公开使用路径里。
- 公开 mode 不含 `direct`；`docs/RESULTS.md` 中的 direct 数据明确标注为 paper-only 历史结果。
- 文档含 honor-system 诚信声明：`query_full.md`/`amb_kb.json`/GT 仍在 repo 中，靠规则约束选手不越权读取。
- 评测核心只有一份（在 `evaluate/` 包内）；旧 `evaluate.batch` 已退休或改为薄 wrapper。
- 测试和 release validation 通过。
