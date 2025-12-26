from app.services.prompt_manager import PromptManager
import json

def test_prompt_manager_zh():
    print("\n=== 测试中文提示词 ===")
    pm = PromptManager(language="zh")
    perception = "你在家里，现在是晚上。"
    memory = "你记得今天工作很努力。"
    stats = {"energy": 30, "wealth": 100, "health": 80}
    
    prompts = pm.get_decision_prompt(perception, memory, stats)
    print(f"System Prompt: {prompts['system']}")
    print(f"User Prompt:\n{prompts['user']}")
    
    assert "你是一个虚拟世界中的数字灵魂" in prompts["user"]
    assert "当前处境：\n你在家里，现在是晚上。" in prompts["user"]

def test_prompt_manager_en():
    print("\n=== 测试英文提示词 ===")
    pm = PromptManager(language="en")
    perception = "You are at home. It's evening."
    memory = "You remember you worked hard today."
    stats = {"energy": 30, "wealth": 100, "health": 80}
    
    prompts = pm.get_decision_prompt(perception, memory, stats)
    print(f"System Prompt: {prompts['system']}")
    print(f"User Prompt:\n{prompts['user']}")
    
    assert "You are a digital soul in a virtual world" in prompts["user"]
    assert "Current Situation:\nYou are at home. It's evening." in prompts["user"]

if __name__ == "__main__":
    test_prompt_manager_zh()
    test_prompt_manager_en()
    print("\n✓ PromptManager 测试通过!")
