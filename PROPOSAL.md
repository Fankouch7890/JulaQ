# JulaQ AI Agent — Fabric Foundation Project Proposal & Submission Package

---

## 📄 Executive Summary | الملخص التنفيذي

**JulaQ (جولاق)** هو وكيل ذكاء اصطناعي محادثاتي ومستقل تم تطويره لدعم شبكة **Fabric Foundation** والأتمتة الروبوتية المتقدمة. يهدف المشروع إلى تمكين المستخدمين والشركات من إدارة الروبوتات والأنظمة الذكية عبر لغة طبيعية (باللغة العربية والإنجليزية) والربط مع خدمات Fabric API بنقرة واحدة.

---

## 🎯 Value Proposition | القيمة المضافة لشبكة Fabric

1. **تسهيل التفاعل مع شبكة Fabric:** تحويل الأوامر المعقدة إلى محادثة بسيطة مع الوكيل الذكي JulaQ.
2. **مرونة الهيكلية (LangGraph Architecture):** نظام قائم على الرسوم البيانية للحالات (State Graph) يسمح بتتبع مسار الأوامر واتخاذ القرارات وتنفيذ الأدوات تلقائياً.
3. **التكامل مع نظام RoboPay والتحكم:** دعم متكامل لمعالجة متطلبات الدفع واستجابات خطأ HTTP 402 من Fabric API.
4. **جاهزية للاستخدام والإنتاج (Production-Ready):** اختبارات شاملة وتصميم كائني يدعم الاستجابة السريعة وتجنب الأخطاء التشغيلية.

---

## 🏗️ System Architecture | الهيكلية البرمجية

```
┌─────────────────────────────────────────────────────────────┐
│                       JulaQ CLI REPL                        │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 LangGraph Agent (JulaQ Core)                 │
│  - System Prompt (Arabic & Robotics Context)                 │
│  - Multi-turn Message Routing & Tool Calling                │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                        Agent Tools                          │
│  move_robot | stop_robot | get_robot_status | fabric_action  │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    Fabric RobotController                   │
│  - Abstracted methods (move, stop, get_status, send_action)  │
│  - Retry mechanism, timeouts & error handling               │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                     Fabric Foundation API                   │
│             https://api.fabric.foundation/api/core           │
└─────────────────────────────────────────────────────────────┘
```

---

## 📧 Application Letter Draft | صيغة خطاب التقديم الرسمي

يمكنك نسخ وتعديل الرسالة التالية لإرسالها عبر البريد الإلكتروني أو نموذج التقديم لـ Fabric Foundation:

```text
Subject: Proposal Submission: JulaQ AI Agent - Smart Automation for the Fabric Network

Dear Fabric Foundation Ecosystem Team,

We are excited to present JulaQ (جولاق), an open-source AI agent powered by LangChain and LangGraph, explicitly designed to empower and streamline robotics automation on the Fabric Network.

Key Highlights of JulaQ:
- Natural Language Robotics Control: Translates natural language commands (Arabic/English) directly into structured, reliable Fabric API robot actions.
- Resilient Robot Controller: Includes built-in handling for timeouts, linear backoff retries, and RoboPay payment status triggers.
- Modular & Production-Ready: Complete with end-to-end integration tests, structured CLI interface, and seamless API extensibility.

GitHub Repository: [Insert your GitHub Repository URL here]
Video Demo: [Insert Video Demo Link here]

We look forward to collaborating with Fabric Foundation and exploring Ecosystem Grant / Partnership opportunities to bring intelligent, conversational robotics to the global Fabric ecosystem.

Best regards,
JulaQ Development Team
Contact Email: [Insert Email Here]
```

---

## 🛠️ Requirements & Quick Start | التثبيت والتشغيل السريع

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd JulaQ

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment variables
cp .env.example .env
# Fill in FABRIC_API_KEY and OPENAI_API_KEY in .env

# 4. Run JulaQ AI Agent
python main.py

# 5. Run tests
python3 -m pytest
```
