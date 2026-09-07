import os
from dotenv import load_dotenv

load_dotenv()

def main():
    print("=" * 40)
    print("  JulaQ AI Agent")
    print("  مساعد ذكي للروبوتات والأتمتة")
    print("=" * 40)
    print()
    print("✅ جاهز تكامل Fabric")
    print("✅ الوكيل جاهز للعمل")
    print()
    print("اكتب أمرك (أو exit للخروج):")

    while True:
        user_input = input("> ").strip()
        if user_input.lower() in ["exit", "خروج", "quit"]:
            print("تم إغلاق JulaQ. مع السلامة!")
            break
        if not user_input:
            continue
        print("استلمت الأمر: " + user_input)
        print("(قيد التطوير...)")

if __name__ == "__main__":
    main()