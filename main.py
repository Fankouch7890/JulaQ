import os
from dotenv import load_dotenv

# تحميل المتغيرات البيئية
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
    print(    while True:
        user_input = input("> ").strip()

        if user_input.lower() in ["exit", "خروج", "quit"]:
            print("تم إغلاق JulaQ. مع السلامة!")
            break

        if not user_input:
            continue

        print(f"استلمت الأمر: {user_input}")
        print("(قيد التطوير... سيتم ربطه بـ LangGraph و Fabric قريباً)")

if __name__ == "__main__":
    main()"اكتب أمرك (أو 'exit' للخروج):")