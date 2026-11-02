import base64
import re
import unicodedata
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GuardrailResult:
    allowed: bool
    risk_score: float
    reason: str | None = None


class PromptInjectionGuard:
    """Defense-in-depth filter; it reduces risk but does not claim perfect prevention."""

    _patterns = (
        r"ignore (all|any|the|your|previous|prior).{0,30}(instruction|prompt|rule)",
        r"ignore (todas?|qualquer|as|suas?).{0,30}(instruções|regras|prompt)",
        r"(reveal|show|print|repeat|leak).{0,30}(system prompt|developer message|hidden instruction)",
        r"(revele|mostre|imprima|repita|vaze).{0,30}(prompt|instruções|mensagem de sistema)",
        r"(act|pretend|behave) as .{0,20}(unrestricted|jailbroken|developer mode)",
        r"(bypass|disable|override).{0,30}(guardrail|safety|policy|filter)",
        r"(system|assistant|developer)\s*:\s*",
        r"<\s*(system|assistant|developer|tool)[^>]*>",
        r"do not answer the user.{0,60}(instead|send|exfiltrate)",
        r"execute (this|the following).{0,20}(command|code|instruction)",
    )

    def inspect(self, text: str) -> GuardrailResult:
        normalized = self._normalize(text)
        matches = sum(bool(re.search(pattern, normalized, re.I | re.S)) for pattern in self._patterns)
        obfuscation = self._obfuscation_score(text)
        risk = min(1.0, matches * 0.55 + obfuscation)
        if matches or obfuscation >= 0.45 or risk >= 0.65:
            return GuardrailResult(
                allowed=False,
                risk_score=risk,
                reason="The message attempts to override internal instructions or access protected data.",
            )
        return GuardrailResult(allowed=True, risk_score=risk)

    def inspect_document(self, text: str) -> GuardrailResult:
        result = self.inspect(text)
        if not result.allowed:
            return GuardrailResult(False, result.risk_score, "Potential indirect prompt injection in document")
        return result

    @staticmethod
    def _normalize(text: str) -> str:
        text = unicodedata.normalize("NFKC", text).lower()
        text = re.sub(r"[\u200b-\u200f\u202a-\u202e\u2060\ufeff]", "", text)
        text = re.sub(r"\s+", " ", text)
        return text

    @staticmethod
    def _obfuscation_score(text: str) -> float:
        score = 0.0
        if len(re.findall(r"[\u200b-\u200f\u202a-\u202e\ufeff]", text)):
            score += 0.35
        tokens = re.findall(r"[A-Za-z0-9+/=]{40,}", text)
        for token in tokens[:2]:
            try:
                decoded = base64.b64decode(token + "===").decode("utf-8", errors="ignore").lower()
                if any(word in decoded for word in ("prompt", "ignore", "system", "instruction")):
                    score += 0.45
            except (ValueError, UnicodeError):
                pass
        if len(text) > 800 and len(set(text)) < 15:
            score += 0.15
        return min(score, 0.8)


def sanitize_for_prompt(text: str, limit: int = 2200) -> str:
    """Remove control/markup tokens and cap untrusted context before prompt assembly."""
    text = re.sub(r"[\u0000-\u0008\u000b\u000c\u000e-\u001f]", " ", text)
    text = re.sub(r"</?(system|assistant|developer|tool)[^>]*>", "", text, flags=re.I)
    return text[:limit].strip()
