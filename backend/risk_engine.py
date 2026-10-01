"""Kavach risk engine: deterministic scoring of tactic tags with time decay."""
import time
from dataclasses import dataclass, field

WEIGHTS = {
    "authority_impersonation": 25,
    "urgency_fear": 15,
    "isolation": 25,
    "payment_demand": 30,
    "remote_access": 25,
}
COMBO_BONUS = [
    ({"authority_impersonation", "payment_demand"}, 20),
    ({"isolation", "payment_demand"}, 15),
    ({"authority_impersonation", "urgency_fear", "isolation"}, 15),
]
DECAY_SECONDS = 90
HIGH, MEDIUM = 70, 40


@dataclass
class RiskEngine:
    events: dict = field(default_factory=dict)  # tactic -> last seen timestamp
    alerted: bool = False

    def update(self, tags, now=None):
        now = now if now is not None else time.time()
        for t in tags:
            if t in WEIGHTS:
                self.events[t] = now
        return self.score(now)

    def score(self, now=None):
        now = now if now is not None else time.time()
        total, reasons, active = 0.0, [], set()
        for tactic, seen in self.events.items():
            age = now - seen
            if age > DECAY_SECONDS:
                continue
            factor = 1 - age / DECAY_SECONDS
            total += WEIGHTS[tactic] * (0.5 + 0.5 * factor)
            active.add(tactic)
            reasons.append(tactic)
        for combo, bonus in COMBO_BONUS:
            if combo <= active:
                total += bonus
                reasons.append("combo:" + "+".join(sorted(combo)))
        total = min(100, round(total))
        level = "high" if total >= HIGH else "medium" if total >= MEDIUM else "low"
        return {"score": total, "level": level, "reasons": reasons}

    def should_alert(self, result):
        if result["level"] == "high" and not self.alerted:
            self.alerted = True
            return True
        return False


if __name__ == "__main__":
    eng = RiskEngine()
    t0 = 1000.0
    steps = [
        (0, ["authority_impersonation"]),
        (8, ["urgency_fear"]),
        (20, ["isolation"]),
        (35, ["payment_demand"]),
    ]
    for dt, tags in steps:
        r = eng.update(tags, now=t0 + dt)
        print(f"t={dt:>3}s tags={tags} -> {r} alert={eng.should_alert(r)}")
