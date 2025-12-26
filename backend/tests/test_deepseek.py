"""
DeepSeek API 连接测试
用于诊断 API 连接问题
"""
import os
import sys
from pathlib import Path

backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from openai import OpenAI
from app.core.config import settings
import time


def test_basic_connection():
    """测试基本连接"""
    print("\n=== 测试 1: 基本连接 ===")
    print(f"API Key: {settings.LLM_API_KEY[:20]}...")
    print(f"Base URL: {settings.LLM_BASE_URL}")
    print(f"Model: {settings.LLM_MODEL}")
    
    client = OpenAI(
        api_key=settings.LLM_API_KEY,
        base_url=settings.LLM_BASE_URL,
        timeout=60.0
    )
    
    try:
        start_time = time.time()
        response = client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": "Say 'Hello' in one word"},
            ],
            stream=False
        )
        elapsed = time.time() - start_time
        
        print(f"✓ 请求成功!")
        print(f"响应时间: {elapsed:.2f}秒")
        print(f"响应内容: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"✗ 请求失败!")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        return False


def test_json_response():
    """测试 JSON 格式响应"""
    print("\n=== 测试 2: JSON 格式响应 ===")
    
    client = OpenAI(
        api_key=settings.LLM_API_KEY,
        base_url=settings.LLM_BASE_URL,
        timeout=60.0
    )
    
    try:
        start_time = time.time()
        response = client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Respond with JSON only."},
                {"role": "user", "content": 'Return a JSON object with one field: {"status": "ok"}'},
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        elapsed = time.time() - start_time
        
        print(f"✓ JSON 请求成功!")
        print(f"响应时间: {elapsed:.2f}秒")
        print(f"响应内容: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"✗ JSON 请求失败!")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        return False


def test_decision_prompt():
    """测试决策提示词"""
    print("\n=== 测试 3: 决策提示词 ===")
    
    client = OpenAI(
        api_key=settings.LLM_API_KEY,
        base_url=settings.LLM_BASE_URL,
        timeout=60.0
    )
    
    prompt = """You are a digital soul in a virtual world.

Current Situation:
You are at home. It's evening.

Your Memories:
You remember you worked hard today.

Your Stats:
{
  "energy": 30,
  "wealth": 100,
  "health": 80
}

Available Actions:
- IDLE: Do nothing
- SLEEP: Rest and recover energy
- WORK_996: Work to earn money
- REST_PARK: Relax at the park

Decide your next action. Respond with JSON:
{
  "action": "ACTION_NAME",
  "target": null,
  "thought": "your reasoning"
}"""
    
    try:
        start_time = time.time()
        response = client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=[
                {"role": "system", "content": "You are a digital soul making decisions in a virtual world. Respond with JSON only."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        elapsed = time.time() - start_time
        
        print(f"✓ 决策请求成功!")
        print(f"响应时间: {elapsed:.2f}秒")
        print(f"响应内容: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"✗ 决策请求失败!")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        
        if hasattr(e, '__cause__'):
            print(f"原因: {e.__cause__}")
        
        return False


def test_with_different_timeouts():
    """测试不同超时设置"""
    print("\n=== 测试 4: 不同超时设置 ===")
    
    timeouts = [10.0, 30.0, 60.0, 120.0]
    
    for timeout in timeouts:
        print(f"\n尝试超时时间: {timeout}秒")
        client = OpenAI(
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_BASE_URL,
            timeout=timeout
        )
        
        try:
            start_time = time.time()
            response = client.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=[
                    {"role": "user", "content": "Hello"},
                ],
                stream=False
            )
            elapsed = time.time() - start_time
            
            print(f"  ✓ 成功! 实际耗时: {elapsed:.2f}秒")
            return timeout
            
        except Exception as e:
            print(f"  ✗ 失败: {type(e).__name__}")
    
    return None


if __name__ == "__main__":
    print("=" * 60)
    print("DeepSeek API 连接诊断测试")
    print("=" * 60)
    
    results = []
    
    results.append(("基本连接", test_basic_connection()))
    results.append(("JSON 响应", test_json_response()))
    results.append(("决策提示", test_decision_prompt()))
    optimal_timeout = test_with_different_timeouts()
    
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{name}: {status}")
    
    if optimal_timeout:
        print(f"\n建议超时时间: {optimal_timeout}秒")
    else:
        print("\n所有超时设置均失败，请检查网络连接")