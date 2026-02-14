def calculate_energy_score(metrics: dict, user: "User") -> float:
    """Simple score based on sleep, HRV and steps"""
    sleep_factor = min(metrics["sleep"] / 8, 1.0)  # Normalize to 0-1
    hrv_factor = min(metrics["hrv"] / 80, 1.0)      # Normalize to 0-1
    steps_factor = min(metrics["steps"] / 10000, 1.0)  # Normalize to 0-1
    
    return (sleep_factor * 0.4 + hrv_factor * 0.4 + steps_factor * 0.2)

def get_energy_avatar(score: float) -> dict:
    """Energy Avatar: 🐢 → 🏃 → 🚀"""
    if score < 0.4:
        return {
            "emoji": "🐢",
            "name": "Черепаха",
            "tip": "Снизь нагрузку, сделай 3 перерыва на дыхание"
        }
    elif score < 0.7:
        return {
            "emoji": "🏃",
            "name": "Бегун",
            "tip": "Поддерживай текущий ритм, спи 7+ часов"
        }
    else:
        return {
            "emoji": "🚀",
            "name": "Ракета",
            "tip": "Идеальный день для сложных задач и тренировок"
        }

def generate_advice(avatar: dict, user: "User") -> str:
    """Rule-based advice (no LLM)"""
    base = avatar["tip"]
    
    if user.goal == "energy":
        return f"{base}\n⚡ Дополнительно: Сделай 5-минутную зарядку утром"
    elif user.goal == "recovery":
        return f"{base}\n🌙 Дополнительно: Избегай кофеина после 14:00"
    return base
