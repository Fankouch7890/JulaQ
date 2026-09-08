import os
import asyncio
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

from agent import create_julaq_agent
from tools.fabric import RobotController

load_dotenv()

async def async_main():
    print("=" * 40)
    print("  JulaQ AI Agent")
    print("  مساعد ذكي للروبوتات والأتمتة")
    print("=" * 40)
    print()
    print("✅ جاهز تكامل Fabric")
    print("✅ الوكيل جاهز للعمل")
    print()
    print("اكتب أمرك (أو exit للخروج):")

    has_openai_key = bool(os.getenv("OPENAI_API_KEY"))
    agent_app = None
    if has_openai_key:
        try:
            agent_app = create_julaq_agent()
        except Exception as e:
            print(f"⚠️ تعذر إعداد وكيل LangGraph: {e}")

    robot_controller = RobotController()

    while True:
        try:
            user_input = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nتم إغلاق JulaQ. مع السلامة!")
            break

        if user_input.lower() in ["exit", "خروج", "quit"]:
            print("تم إغلاق JulaQ. مع السلامة!")
            break

        if not user_input:
            continue

        if agent_app and has_openai_key:
            try:
                inputs = {"messages": [HumanMessage(content=user_input)]}
                result = await agent_app.ainvoke(inputs)
                last_msg = result["messages"][-1]
                print(f"\nJulaQ: {last_msg.content}\n")
            except Exception as e:
                print(f"⚠️ حدث خطأ أثناء معالجة الطلب بالذكاء الاصطناعي: {e}")
                print("جاري تنفيذ المعالجة الاحتياطية المباشرة...")
                await handle_fallback(user_input, robot_controller)
        else:
            await handle_fallback(user_input, robot_controller)


async def handle_fallback(user_input: str, controller: RobotController):
    """
    معالجة احتياطية للأوامر عند عدم توفر مفتاح OpenAI API.
    """
    print(f"استلمت الأمر: {user_input}")
    words = user_input.split()

    # مثال بسيط للتعرف على أوامر الروبوت المباشرة
    if len(words) >= 2 and words[0] in ["حرك", "move"]:
        robot_id = words[1]
        res = await controller.move(robot_id)
        print(f"النتيجة: {res}")
    elif len(words) >= 2 and words[0] in ["أوقف", "stop"]:
        robot_id = words[1]
        res = await controller.stop(robot_id)
        print(f"النتيجة: {res}")
    elif len(words) >= 2 and words[0] in ["حالة", "status"]:
        robot_id = words[1]
        res = await controller.get_status(robot_id)
        print(f"النتيجة: {res}")
    else:
        print("(تم استلام الأمر - نظام الذكاء الاصطناعي يتطلب ضبط OPENAI_API_KEY للاستجابة الكاملة)")


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
