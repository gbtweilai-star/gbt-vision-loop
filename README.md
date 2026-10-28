# vision_loop

**One capability bit from GBT V8, packaged standalone.** No. 335 of 341,
`vision` domain (Vision).

<p>
<img alt="python" src="https://img.shields.io/badge/python-3.9%2B-blue">
<img alt="license" src="https://img.shields.io/badge/license-MIT-green">
<img alt="deps" src="https://img.shields.io/badge/runtime%20dependencies-0-brightgreen">
</p>

> **原生四觉闭环**（主人令 2026-10-09：「她的视觉每次都要跟手分开去使用传统的**瞎子操作**……把视觉这么使用给她**钉死在上面**」「我看她每次执行任务就是**瞎还没脑**」＋「还有耳，嘴」）。**眼·耳·嘴·手四觉 → 脑 → 手 → 验**，缺一觉就不许动/说：①眼 tentacle see（已实测可看）②耳 voice listen（壳已对 digital-human 放 media）③嘴 voice TTS（**没内容不说**）④手 tentacle click/type（门层**眼手同票**）· ⑤脑 System-One 契约（与云插件 c02 Laya 同一插槽）⑥验 动完再看一次比对，没变化**如实说没动成**。op=look/hear/speak/think/act/verify/loop/status。

That description is copied verbatim from the registry. `tests/test_spec.py` pins it,
so documentation drift fails the build instead of shipping quietly.

## What this package actually is

It is the **contract** for one capability: its name, its parameters, the values it
accepts, and whether it can change state that cannot be restored. It is not the
implementation — that lives in the runtime this bit was extracted from.

So `run()` goes through a narrow `Backend` protocol, and the default backend is a
stub that **says so**:

```
status="validated"   backend="stub"   data={"executed": false}
```

Never `status="ok"`. A stub that reports success is worse than no stub, because the
caller stops looking for the real thing.

## Install

```bash
git clone https://github.com/gbtweilai-star/gbt-vision-loop.git
cd gbt-vision-loop
python -m pip install -e ".[dev]"
```

## Use

```bash
python -m gbt_vision_loop info                  # capability card
python -m gbt_vision_loop spec --json           # machine-readable contract
python -m gbt_vision_loop check --payload '{}'
python -m gbt_vision_loop run   --payload '{}'
```

Real `info` output from this machine:

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

Wire a real implementation:

```python
from gbt_vision_loop import run

class MyBackend:
    name = "my-backend"
    def invoke(self, cap, payload):
        return {"cap": cap, "handled": sorted(payload)}

result = run({}, backend=MyBackend())
assert result.status == "ok"
```

## Parameters

| name | required | notes |
|---|---|---|
| — | no | the registry declares no required parameters |

Registry hint (`params_hint`): (empty)

**注册表登记的取值 / 子动作（8 个）**：`look`、`hear`、`speak`、`think`、`act`、`verify`、`loop`、`status`

Types are deliberately absent: the registry does not declare them, and an invented
type is worse than no type, because callers believe it.

## Boundaries

- Gated: this bit is marked `safe: false` in the registry — it can change state that no inverse action restores.
- No external service dependency declared.
- Multi-op (`multi_op: true`): several sub-actions share one name — read `op` before calling.
- No implementation ships here. Bring a backend; the protocol is one method.

## What this is not

Not a wrapper around a hosted API. Not a model. Not a promise that calling it does
anything on its own. It is the typed seam plus the validation, which is the part that
stays correct even when the implementation changes.

## Tests

```bash
python -m pytest
```

```text
20 passed, 3 skipped in 0.10s
```

## Provenance

| field | value |
|---|---|
| capability | `vision_loop` |
| domain | `vision` |
| handler | `vision_loop` |
| safe | `False` (gated = `True`) |
| external | `False` |
| atlas page | [vision/vision_loop](https://github.com/gbtweilai-star/gbt-caps/blob/main/caps/vision/vision_loop.md) |
| full index | [https://github.com/gbtweilai-star/gbt-caps](https://github.com/gbtweilai-star/gbt-caps) |

The parent README says 348 capabilities; an AST pass over the registry enumerates
`341 + 0 unimplemented + 0 disabled = 341`. The extra 7 are historical duplicates.
Numbering here follows 341 and matches the `gbt-caps` index one-to-one.

## License

MIT.
