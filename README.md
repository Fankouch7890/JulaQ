# JulaQ AI Agent (جولاق)

مساعد ذكي للروبوتات والأتمتة في شبكة Fabric
Smart AI Agent for Robots & Automation on the Fabric Network

---

## 🌟 المميزات الرئيسية
- **التكامل المعزز مع Fabric Foundation:** ارتباط مباشر مع Fabric API للتحكم بالروبوتات وإدارة الدفع والتنبيهات.
- **وكيل ذكاء اصطناعي تفاعلي (LangGraph Agent):** معالجة الأوامر باللغة الطبيعية (العربية والإنجليزية) وتوجيه الأوامر التلقائي للروبوتات.
- **متحكم الروبوتات المتقدم (`RobotController`):** إدارات كائنية مجهزة بخصائص إعادة المحاولة (Retries) والمهلة التلقائية (Timeout).
- **واجهة تفاعلية أسرع وأسهل (CLI REPL):** دعم التشغيل التفاعلي مع وضع معالجة احتياطي (Fallback Mode) للعمل أونلاين وأوفلاين.
- **اختبارات جودة شاملة:** مغطى باختبارات وحدة وتكامل قياسية باستخدام `pytest`.

---

## 🛠️ التقنيات المستخدمة
- **Python 3.12+**
- **LangChain & LangGraph**
- **httpx & AsyncIO**
- **Fabric API & RoboPay**
- **pytest & pytest-asyncio**

---

## 📁 هيكلية المشروع
```
JulaQ/
├── agent/                  # وحدة الوكيل الذكي والأدوات
│   ├── __init__.py
│   ├── agent.py            # رسم بياني لحالات الوكيل (LangGraph Agent Graph)
│   └── tools.py            # أدوات التحكم بالروبوتات المربوطة بـ LangChain
├── tools/
│   └── fabric/             # وحدة التكامل مع شبكة Fabric
│       ├── __init__.py
│       ├── client.py        # العميل الأساسي لطلب شبكة Fabric API
│       └── robot_control.py # فئة RobotController المتقدمة
├── tests/                  # الاختبارات الشاملة
│   ├── agent/              # اختبارات الوكيل والأدوات
│   └── tools/fabric/       # اختبارات التحكم بالروبوتات
├── main.py                 # نقطة التشغيل الرئيسية (CLI REPL)
├── PROPOSAL.md             # ملف التقديم الرسمي لشركة Fabric Foundation
├── .env.example            # نموذج المتغيرات البيئية
└── requirements.txt        # المكتبات التبعية
```

---

## 🚀 التشغيل والتثبيت

### 1. تثبيت المتغيرات والاعتمادات
```bash
pip install -r requirements.txt
```

### 2. إعداد المتغيرات البيئية
قم بنسخ ملف `.env.example` إلى `.env` وضبط المفاتيح:
```bash
cp .env.example .env
```
مفاتيح هامّة في `.env`:
- `FABRIC_API_KEY`: مفتاح حساب Fabric الخاص بك.
- `OPENAI_API_KEY`: مفتاح نموذج OpenAI لتشغيل المعالجة بالذكاء الاصطناعي.

### 3. تشغيل التطبيق
```bash
python main.py
```

---

## 🧪 تشغيل الاختبارات الآلية
لتأكيد صحة واستقرار جميع وظائف النظام:
```bash
python3 -m pytest
```

---

## 📄 ملف التقديم لـ Fabric Foundation
تم إعداد ملخص تنفيذي وخطاب تقديم رسمي ومخطط القيمة المضافة في ملف **`PROPOSAL.md`**.
