"""The capability contract, copied verbatim from the GBT V8 registry.

Do not hand-edit: ``tests/test_spec.py`` pins every field against the
registry snapshot so drift fails the build instead of shipping quietly.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

_RAW = r"""{
 "name": "vision_loop",
 "domain": "vision",
 "desc": "**原生四觉闭环**（主人令 2026-10-09：「她的视觉每次都要跟手分开去使用传统的**瞎子操作**……把视觉这么使用给她**钉死在上面**」「我看她每次执行任务就是**瞎还没脑**」＋「还有耳，嘴」）。**眼·耳·嘴·手四觉 → 脑 → 手 → 验**，缺一觉就不许动/说：①眼 tentacle see（已实测可看）②耳 voice listen（壳已对 digital-human 放 media）③嘴 voice TTS（**没内容不说**）④手 tentacle click/type（门层**眼手同票**）· ⑤脑 System-One 契约（与云插件 c02 Laya 同一插槽）⑥验 动完再看一次比对，没变化**如实说没动成**。op=look/hear/speak/think/act/verify/loop/status。",
 "handler": "vision_loop",
 "safe": false,
 "external": false,
 "requires_params": false,
 "params": [],
 "params_hint": "",
 "multi_op": true,
 "ops": [
  "look",
  "hear",
  "speak",
  "think",
  "act",
  "verify",
  "loop",
  "status"
 ],
 "ops_hint": ""
}"""


@dataclass(frozen=True)
class CapSpec:
    """Immutable description of one capability bit."""

    name: str
    domain: str
    desc: str
    handler: str
    safe: bool
    external: bool
    requires_params: bool
    params: Tuple[str, ...] = ()
    params_hint: str = ""
    multi_op: bool = False
    ops: Tuple[str, ...] = ()
    ops_hint: str = ""

    @property
    def gated(self) -> bool:
        """True when the registry marks this bit ``safe: false``.

        Gated does not mean "dangerous"; it means the action can change state
        that cannot be restored by running the inverse action.
        """
        return not self.safe

    @property
    def summary(self) -> str:
        """First clause of the description, for one-line listings."""
        for sep in ("\uff08", "\uff1b", "\u3002", ";"):
            if sep in self.desc:
                head = self.desc.split(sep, 1)[0].strip()
                if head:
                    return head
        return self.desc.strip()

    def as_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "domain": self.domain,
            "desc": self.desc,
            "handler": self.handler,
            "safe": self.safe,
            "gated": self.gated,
            "external": self.external,
            "requires_params": self.requires_params,
            "params": list(self.params),
            "params_hint": self.params_hint,
            "multi_op": self.multi_op,
            "ops": list(self.ops),
            "ops_hint": self.ops_hint,
        }


_data = json.loads(_RAW)

SPEC = CapSpec(
    name=_data["name"],
    domain=_data["domain"],
    desc=_data["desc"],
    handler=_data["handler"],
    safe=_data["safe"],
    external=_data["external"],
    requires_params=_data["requires_params"],
    params=tuple(_data["params"]),
    params_hint=_data["params_hint"],
    multi_op=_data["multi_op"],
    ops=tuple(_data["ops"]),
    ops_hint=_data["ops_hint"],
)
