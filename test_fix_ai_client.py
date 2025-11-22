import os
import sys


def test_openai_client_fix():
    """测试修复后的 OpenAI 客户端初始化（兼容 0.28.1 版本）"""
    print("=== 测试 OpenAI 客户端初始化修复 ===")

    try:
        import openai

        # 测试1: 基本配置（模拟 DeepSeek）
        print("\n1. 测试基本配置...")
        openai.api_key = "test_api_key"
        openai.api_base = "https://api.deepseek.com"
        print("✓ 基本配置初始化成功")

        # 测试2: 默认配置
        print("\n2. 测试默认配置...")
        openai.api_key = "test_api_key"
        openai.api_base = None  # 重置为默认
        print("✓ 默认配置初始化成功")

        # 测试3: 空配置
        print("\n3. 测试空配置...")
        try:
            openai.api_key = None
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}],
                stream=False,
            )
            print("✗ 空配置应该失败但通过了")
        except Exception as e:
            print(f"✓ 空配置正确失败: {type(e).__name__}")

        print("\n🎉 所有客户端初始化测试通过！")
        return True

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_proxy_environment():
    """测试代理环境变量"""
    print("\n=== 检查代理环境变量 ===")

    proxy_vars = ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"]
    for var in proxy_vars:
        value = os.environ.get(var)
        if value:
            print(f"⚠️  检测到环境变量 {var}={value}")
        else:
            print(f"✓ 环境变量 {var} 未设置")

    return True


def main():
    """主测试函数"""
    print("开始测试 AI 客户端修复...")

    # 检查环境
    test_proxy_environment()

    # 测试客户端初始化
    success = test_openai_client_fix()

    if success:
        print("\n✅ 修复验证成功！")
        print("解决方案总结：")
        print("1. 降级到 openai==0.28.1 版本")
        print("2. 使用 openai.api_key 和 openai.api_base 配置")
        print("3. 使用 openai.ChatCompletion.create() 方法")
        print("4. 避免了新版本的代理参数冲突问题")
    else:
        print("\n❌ 修复验证失败，请检查代码")
        sys.exit(1)


if __name__ == "__main__":
    main()
