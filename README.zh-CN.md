# vision_loop · 视觉域能力位

> **用途一句话**：**原生四觉闭环**

<p>
<img alt="python" src="https://img.shields.io/badge/python-3.9%2B-blue">
<img alt="license" src="https://img.shields.io/badge/license-MIT-green">
<img alt="deps" src="https://img.shields.io/badge/runtime%20dependencies-0-brightgreen">
<img alt="capability" src="https://img.shields.io/badge/capability-335%20%2F%20341-orange">
</p>

这是 **GBT V8 的 341 个原生能力位中的第 335 个**（视觉域 · `vision`），
单独抽出来做成的独立仓库：可安装、可测试、零运行时依赖。

---

## 一、这一位是什么

> **原生四觉闭环**（主人令 2026-10-09：「她的视觉每次都要跟手分开去使用传统的**瞎子操作**……把视觉这么使用给她**钉死在上面**」「我看她每次执行任务就是**瞎还没脑**」＋「还有耳，嘴」）。**眼·耳·嘴·手四觉 → 脑 → 手 → 验**，缺一觉就不许动/说：①眼 tentacle see（已实测可看）②耳 voice listen（壳已对 digital-human 放 media）③嘴 voice TTS（**没内容不说**）④手 tentacle click/type（门层**眼手同票**）· ⑤脑 System-One 契约（与云插件 c02 Laya 同一插槽）⑥验 动完再看一次比对，没变化**如实说没动成**。op=look/hear/speak/think/act/verify/loop/status。

上面这句是**注册表原文**，逐字复制，没有改写。`tests/test_spec.py` 会把它钉死——
描述漂移会让测试失败，而不是悄悄发版。

---

## 二、用途：它解决什么问题

### 2.1 这一域在管什么

看图、定位、闭环：通用视觉（vision）、元素定位（vision_grounding）、打印/截图（vision_print）、多轮视觉闭环（vision_loop）、以及视觉流水线（vlx_flow）。

### 2.2 为什么这么设计

视觉域最贵的错误是「看到了但没定位准」。所以每个能力位都要求返回坐标与置信度，没有坐标的「我看到了」不算结果。

### 2.3 具体到 `vision_loop`

**该用它的时候**：

- 你的任务可以概括为「**原生四觉闭环**」，并且
- 它不需要任何必填参数，可以直接调用，并且
- 你已经接受它可能触及**不可逆状态**（注册表 `safe: false`，见第七节）。

**不该用它的时候**：

- 你只是想要一个「大概能做这件事」的模糊入口 —— 这一位有明确契约，不是万能入口。
- 你需要它**替你做决定**。它执行，不做价值判断；要不要执行是调用方的事。
- 你希望它自带模型/密钥/机器。它不自带，见 4.5 节接后端。

---

## 三、安装

```bash
git clone https://github.com/gbtweilai-star/gbt-vision-loop.git
cd gbt-vision-loop
python -m pip install -e ".[dev]"
```

零运行时依赖，只有 `pytest` 是开发期依赖。

---

## 四、使用方式

### 4.1 看它是什么（人类可读）

```bash
python -m gbt_vision_loop info
```

真实输出（本机捕获，非示意）：

```text
vision_loop  (vision)  v1.0.0
----------------------------------------
**原生四觉闭环**（主人令 2026-10-09：「她的视觉每次都要跟手分开去使用传统的**瞎子操作**……把视觉这么使用给她**钉死在上面**」「我看她每次执行任务就是**瞎还没脑**」＋「还有耳，嘴」）。**眼·耳·嘴·手四觉 → 脑 → 手 → 验**，缺一觉就不许动/说：①眼 tentacle see（已实测可看）②耳 voice listen（壳已对 digital-human 放 media）③嘴 voice TTS（**没内容不说**）④手 tentacle click/type（门层**眼手同票**）· ⑤脑 System-One 契约（与云插件 c02 Laya 同一插槽）⑥验 动完再看一次比对，没变化**如实说没动成**。op=look/hear/speak/think/act/verify/loop/status。

gated      : True   <- needs explicit consent
external   : False
multi-op   : True
params     : (none)
values     : look, hear, speak, think, act, verify, loop, status
```

### 4.2 看它的契约（机器可读）

```bash
python -m gbt_vision_loop spec --json
```

输出是一个 JSON 对象，字段与注册表一一对应：`name` / `domain` / `desc` / `handler` /
`safe` / `gated` / `external` / `requires_params` / `params` / `params_hint` /
`multi_op` / `ops` / `ops_hint`。下游可以直接拿它做能力发现，不需要读文档。

### 4.3 只校验、不执行

```bash
python -m gbt_vision_loop check --payload '{}'
```

`check` 永远不会抛异常，只返回「哪里不满足契约」。适合在花掉一次模型调用之前，
先把缺的参数摆给用户看。退出码：`0` 通过、`1` 契约不满足、`2` JSON 本身不合法。

### 4.4 执行

```bash
python -m gbt_vision_loop run --payload '{}'
```

默认后端是 **stub**，所以你会拿到这样的信封：

```json
{
  "cap": "vision_loop",
  "status": "validated",
  "backend": "stub",
  "data": { "executed": false, "reason": "no backend wired" },
  "note": "payload checked against the contract; nothing was executed."
}
```

注意 `status` 是 `"validated"` 而**不是** `"ok"`。这是刻意的：一个把 stub 报成成功的库，
会让调用方停止寻找真正的实现。`bool(result)` 对 stub 结果是 `False`。

### 4.5 接上你自己的后端

```python
from gbt_vision_loop import SPEC, run

class MyBackend:
    name = "my-backend"

    def invoke(self, cap, payload):
        # 这里才是真实实现：调模型、调浏览器、调你的服务
        return {"cap": cap, "handled": sorted(payload)}

result = run({}, backend=MyBackend())
assert result.status == "ok"      # 真实后端才会是 ok
print(result.as_dict())
```

也可以进程级注册一次，之后所有 `run()` 都走它：

```python
from gbt_vision_loop.backend import register_backend
register_backend(MyBackend())
```

`Backend` 是一个 `Protocol`，只需要 `name` 属性和 `invoke(cap, payload) -> dict`。
不继承任何基类，你的实现不需要依赖本包。

### 4.6 作为库用

```python
from gbt_vision_loop import SPEC, run
from gbt_vision_loop.core import check

print(SPEC.name, SPEC.domain, SPEC.gated)

problems = check({})
if problems:
    for p in problems:
        print("缺:", p)
else:
    print(run({}).as_dict())
```

---

## 五、参数

| 参数 | 必填 | 说明 |
|---|---|---|
| — | 否 | 注册表未标注必填参数 |

> 注册表原话（`params_hint`）：（空）

**注册表登记的取值 / 子动作（8 个）**：`look`、`hear`、`speak`、`think`、`act`、`verify`、`loop`、`status`


**为什么表里只有「必填/否」两档**：注册表只标注了哪些参数是必填的，没有标注类型与取值范围。
本包没有替它编造类型 —— 编造出来的类型比没有类型更危险，因为调用方会相信它。

---

## 六、返回值

`run()` 返回一个不可变的 `Result`：

| 字段 | 类型 | 含义 |
|---|---|---|
| `cap` | `str` | 能力位名，恒等于 `vision_loop` |
| `status` | `str` | `validated`（stub 校验通过）/ `ok`（真实后端执行）/ `error` |
| `backend` | `str` | 实际执行后端的 `name` |
| `data` | `dict` | 后端返回的原始字典 |
| `note` | `str` | 人类可读的补充说明（stub 会在这里说明自己没执行） |
| `elapsed_ms` | `float` | 后端耗时 |

`Result.as_dict()` 可直接 `json.dumps`。

---

## 七、边界与注意

- **需要显式授权**（注册表 `safe: false`）。这一位会改变无法用「反向操作」还原的状态，所以原框架把它放在授权闸后面，用完即焚、不做时间窗复用。本包只负责描述与校验，不负责发授权——授权属于调用方的人类。
- **多位一体**（注册表 `multi_op: true`）。同一个能力名下挂着多个子动作，调用前必须读清楚 `op` 的含义，否则「调对了能力、用错了动作」是最常见的误用。
- **本包不含真实实现**。这是刻意设计：真实实现依附于原运行时（模型、密钥、机器）。本包发布的是契约、校验、CLI 与类型接缝；接上你自己的 `Backend` 就能跑。

---

## 八、它不会做什么

- **不会假装执行成功**。默认 stub 的 `status` 是 `validated`，`executed` 是 `false`。
- **不会替你决定要不要执行**。授权是人的动作，不是库的动作。
- **不会编造参数类型**。注册表没写的，本包也不写。
- **不会静默吞掉错误**。后端抛异常就往上抛，返回非 dict 就报 `CapError`。
- **不会联网**。零运行时依赖，`run()` 只调用你给的后端。

---

## 九、测试

```bash
python -m pytest
```

真实输出：

```text
20 passed, 3 skipped in 0.10s
```

测试里有一条**漂移守卫**：`test_description_is_verbatim` 把 `SPEC.desc` 与注册表快照逐字比对。
描述被改了一个字，构建立刻失败。

---

## 十、出处与核对

| 项 | 值 |
|---|---|
| 能力位名 | `vision_loop` |
| 域 | `vision`（视觉域，共 341 位 / 30 域中的一位） |
| 注册表 handler | `vision_loop` |
| `safe` | `False` → gated = `True` |
| `external` | `False` |
| `multi_op` | `True` |
| 索引页 | [vision/vision_loop](https://github.com/gbtweilai-star/gbt-caps/blob/main/caps/vision/vision_loop.md) |
| 全量图谱 | [https://github.com/gbtweilai-star/gbt-caps](https://github.com/gbtweilai-star/gbt-caps) |

**关于 341 这个数**：父仓 README 写的是 348，但按 AST 解析注册表实际可枚举的是
`341 个能力位 + 0 个未实现 + 0 个已禁用 = 341`。差出来的 7 个是历史重名/已合并条目。
本仓库按 341 编号，编号与 `gbt-caps` 的索引一致，可逐条核对。

---

## License

MIT。见 [LICENSE](LICENSE)。
