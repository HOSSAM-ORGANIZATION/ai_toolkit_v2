# 📋 دليل التشغيل وقائمة المهام | Universal AI Toolkit v2 Playbook & Checklist

> **دليل عملي تفصيلي خطوة بخطوة (Playbook & Interactive Checklist) يوضح المسار الذهبي لاستخدام كافة قدرات الـ Toolkit، مقسم إلى خطوات إجبارية واختيارية لضمان أعلى جودة بأقل مجهود.**

---

## 🧭 فهرس مراحل الدليل

1. [المرحلة 0: التثبيت وتهيئة هوية المشروع (Setup & Initialization)](#1-المرحلة-0-التثبيت-وتهيئة-هوية-المشروع-setup--initialization)
2. [المرحلة 1: تهيئة منصات التشغيل والبنية التحتية (Platform & Infrastructure Ops)](#2-المرحلة-1-تهيئة-منصات-التشغيل-والبنية-التحتية-platform--infrastructure-ops)
3. [المرحلة 2: استيعاب التصاميم ونظام التصميم (Design Ingestion & Design System)](#3-المرحلة-2-استيعاب-التصاميم-ونظام-التصميم-design-ingestion--design-system)
4. [المرحلة 3: استخدام السقالات والبلوبرنتس الجاهزة (Blueprint Scaffolding)](#4-المرحلة-3-استخدام-السقالات-والبلوبرنتس-الجاهزة-blueprint-scaffolding)
5. [المرحلة 4: تخطيط وتطوير الميزات البرمجية (Feature Planning & Coding)](#5-المرحلة-4-تخطيط-وتطوير-الميزات-البرمجية-feature-planning--coding)
6. [المرحلة 5: الفحص الآلي المستقل واختبارات المتانة (Autonomous QA & Chaos Testing)](#6-المرحلة-5-الفحص-الآلي-المستقل-واختبارات-المتانة-autonomous-qa--chaos-testing)
7. [المرحلة 6: إنهاء الجلسة وإدارة الذاكرة الحية (Session Wrap-up & Living Memory)](#7-المرحلة-6-إنهاء-الجلسة-وإدارة-الذاكرة-الحية-session-wrap-up--living-memory)
8. [جدول الأوامر السريعة اليومية (Quick Daily Cheat-Sheet)](#8-جدول-الأوامر-السريعة-اليومية-quick-daily-cheat-sheet)

---

## 1. المرحلة 0: التثبيت وتهيئة هوية المشروع (Setup & Initialization)

هذه المرحلة تُنفذ **مرة واحدة فقط** عند بداية ربط الـ Toolkit بالمشروع (سواء كان مشروعاً جديداً أو قائماً).

### [ ] الخطوة 0.1: تهيئة Git للمشروع `[إجباري / MANDATORY]`
تأكد أن المشروع الأساسي هو Git Repository سليم:
```bash
git status || git init
```

### [ ] الخطوة 0.2: تشغيل أمر الإعداد السريع (Quickstart) `[إجباري / MANDATORY]`
اربط الـ Toolkit كـ Submodule ونفذ أمر الإعداد الشامل بضغطة واحدة:
```bash
git submodule add <TOOLKIT_REPO_URL> ai_toolkit && bash ai_toolkit/setup/quickstart.sh
```
*ما يتم تلقائياً:* نسخ الـ Makefile، تفعيل `./toolkit`، وتثبيت قواعد IDE للـ AI في `.cursor/rules` و `CLAUDE.md`.

### [ ] الخطوة 0.3: إعداد بطاقة هوية المشروع (`project_profile.yaml`) `[إجباري / MANDATORY]`
إذا لم يتم إنشاؤه أثناء الـ Quickstart، شغّل معالج الهوية:
```bash
./toolkit init
```
*الخيارات المتوفرة أثناء التوليد:*
- **[اختياري] الاستنتاج التلقائي من الـ PRD:** لو عندك ملف مواصفات:
  ```bash
  ./toolkit init --prd docs/prd.md
  ```
- **[اختياري] استخدام نموذج مسبق (Preset):** لاختيار معمارية جاهزة مباشرة:
  ```bash
  ./toolkit init --preset enterprise_clean_bloc    # لمشاريع BLoC و Clean Architecture
  ./toolkit init --preset modern_modular_riverpod  # لمشاريع Riverpod المقسمة موديولياً
  ./toolkit init --preset lean_mvp                 # للمشاريع السريعة والنماذج الأولية
  ```

### [ ] الخطوة 0.4: فحص سلامة التثبيت (Integrity Verification) `[إجباري / MANDATORY]`
تأكد أن جميع القواعد والملفات والروابط سليمة 100%:
```bash
./toolkit verify
```

---

## 2. المرحلة 1: تهيئة منصات التشغيل والبنية التحتية (Platform & Infrastructure Ops)

تُنفذ هذه الخطوات حسب احتياج مشروعك للميزات المتقدمة وتجهيز بيئات العمل.

### [ ] الخطوة 1.1: إعداد الفليفورز (Flavors Setup) `[اختياري / حسب الحاجة]`
لو تطبيقك يحتاج بيئات تشغيل متعددة (Dev / Staging / Production):
```bash
./toolkit flavors setup
```
*النتيجة:* يتم إنشاء ملفات Kotlin DSL/Groovy للأندرويد، و xcconfig و Schemes لـ iOS، ونقاط الدخول في Flutter (`lib/main_dev.dart`, `lib/main_prod.dart`) طبقاً للتوثيق الرسمي.

### [ ] الخطوة 1.2: حقن الصلاحيات وتبريرات المتاجر (Permissions) `[اختياري / حسب الحاجة]`
لإضافة صلاحيات الكاميرا، الموقع، الإشعارات، أو التخزين مع نصوص تبرير مقبولة في مراجعات Apple App Store:
```bash
./toolkit permissions camera location notifications
```

### [ ] الخطوة 1.3: إعداد التوقيع المشفر للأندرويد (Signing & Keystore) `[اختياري / لمرحلة الـ Release]`
لتوليد مفتاح تشفير أندرويد حقيقي وإعداد `key.properties` وربطه بالـ `build.gradle` تلقائياً:
```bash
./toolkit signing
```

### [ ] الخطوة 1.4: توليد الأيقونات وشاشات البداية (Icons & Splash) `[اختياري]`
لتجهيز الأيقونات وشاشات السبلاش المتوافقة مع أندرويد 12+ ولكل الفليفورز:
```bash
./toolkit icons-splash
```

### [ ] الخطوة 1.5: مزامنة حزم pub.dev المطلوبة (Sync Dependencies) `[اختياري / موصى به]`
لمزامنة الباقات المطلوبة في `pubspec.yaml` طبقاً لما اخترته في `project_profile.yaml`:
```bash
./toolkit deps sync
```

### [ ] الخطوة 1.6: الربط السحابي ومتاجر التطبيقات (Cloud & Stores) `[اختياري]`
لأتمتة ربط Firebase وتجهيز Fastlane للرفع على Google Play و Apple App Store:
```bash
./toolkit cloud register
```

---

## 3. المرحلة 2: استيعاب التصاميم ونظام التصميم (Design Ingestion & Design System)

تُنفذ هذه المرحلة عند تسلّم تصميم شاشة أو ميزة جديدة وقبل البدء في كتابة كود الواجهات.

### [ ] الخطوة 2.1: استخراج التوكنز من التصميم (Figma / Stitch) `[إجباري / MANDATORY]`
- استوعب التصميم إما عبر **Figma MCP Server** أو من خلال مجلد محلي يحتوي على شاشات **Google Stitch**.
- راجع ملف الدليل: [`workflows/product-analysis/design-ingestion.md`](file:///workflows/product-analysis/design-ingestion.md).
- استخرج بالترتيب:
  - الألوان الدلالية والأساسية (Semantic & Brand Colors).
  - مقاسات وأوزان الخطوط (Typography Scale).
  - الفراغات والحواف والظلال (Spacing, Border Radii, Elevation).

### [ ] الخطوة 2.2: مراجعة قاعدة منع القيم الثابتة (Zero-Hardcoding Check) `[إجباري / MANDATORY]`
- ❌ **ممنوع نهائياً:** كتابة أكواد ألوان مباشرة (`Color(0xFF...)`) أو مقاسات نصوص عشوائية (`fontSize: 16`) أو هوامش عشوائية (`EdgeInsets.all(13)`).
- ✅ **المطلوب دائماً:** استخدام توكنز التصميم من `Theme.of(context)` أو `ColorScheme` أو كلاس التوكنز المحدد في مشروعك.

---

## 4. المرحلة 3: استخدام السقالات والبلوبرنتس الجاهزة (Blueprint Scaffolding)

بدلاً من كتابة المكونات المكررة من الصفر أو استهلاك آلاف التوكنز مع الـ AI، استخدم السقالات الجاهزة.

### [ ] الخطوة 3.1: فحص كتالوج البلوبرنتس المتاح `[اختياري / موصى به بقوة]`
راجع الكتالوج في [`templates/blueprints/CATALOG.md`](file:///templates/blueprints/CATALOG.md) لاختيار المكون المطلوب.

### [ ] الخطوة 3.2: توليد المكونات بضغطة زر `[اختياري]`
أمثلة للمكونات الأكثر استخداماً:
```bash
# مكونات واجهة المستخدم الأساسية:
./toolkit add button              # زر متعدد الحالات والستايلات
./toolkit add text_field          # حقل إدخال بخصائص الفحص والـ Password toggle
./toolkit add image               # عارض صور ذكي (Network/SVG/Shimmer)
./toolkit add shimmer             # أنيميشن تحميل عالي الأداء بدون مكتبات
./toolkit add empty_widget        # شاشة فارغة بـ CTA
./toolkit add fail_widget         # شاشة خطأ مع زر إعادة المحاولة

# الأنماط المعمارية والـ Patterns:
./toolkit add async_state         # حالات الشاشة بـ Sealed Classes
./toolkit add pagination          # قائمة Infinite Scroll متكاملة
./toolkit add observer            # Event Bus لفك ارتباط الشاشات
./toolkit add chaos_interceptor   # معترض لشبكة Dio لفحص حالات الفشل
```

### [ ] الخطوة 3.3: التأكد من تسجيل المكون في الذاكرة الحية `[إجباري / MANDATORY]`
تأكد أن المكون الجديد تم تسجيله تلقائياً داخل ملف [`ai_docs/conventions.md`](file:///ai_docs/conventions.md) لكي يعيد الـ AI استخدامه مستقبلاً ولا يكرر بناءه.

---

## 5. المرحلة 4: تخطيط وتطوير الميزات البرمجية (Feature Planning & Coding)

المسار القياسي عند مطالبة الـ AI بتنفيذ أي ميزة (Feature) في التطبيق.

### [ ] الخطوة 4.1: التخطيط الصارم وحساب ميزانية التوكنز `[إجباري / MANDATORY]`
- اطلب من الـ AI كتابة خطة تنفيذية للميزة في ملف `plan.md`.
- احسب ميزانية التوكنز المطلوبة:
  ```bash
  ./toolkit context <FEATURE_NAME>
  ```
- قسّم الميزة إلى مراحل صغيرة (Phases).

### [ ] الخطوة 4.2: مصفوفة حالات الشاشة الخمسة (Screen States Matrix) `[إجباري / MANDATORY]`
وفقاً لـ [`workflows/feature-delivery/screen-states-protocol.md`](file:///workflows/feature-delivery/screen-states-protocol.md)، يجب تغطية الحالات الخمسة لكل شاشة:
1. `Loading`: استخدام Shimmer Skeleton حصرياً (ممنوع Fullscreen CircularProgressIndicator).
2. `Error`: رسالة خطأ واضحة للمستخدم وزر "إعادة المحاولة" (Retry).
3. `Loaded / Success`: عرض المحتوى السليم بالاعتماد على Design System.
4. `Empty`: ويدجت الشاشة الفارغة مع إيقونة وزر إجراء (CTA) يوجه المستخدم للخطوة التالية.
5. `Refreshing`: دعم Pull-to-refresh دون حجب المحتوى الحالي.

### [ ] الخطوة 4.3: تطبيق معايير Dart 3+ في طبقة الواجهة `[إجباري / MANDATORY]`
- استخدام **Sealed Classes** مع `switch` لضمان استيفاء كافة الحالات المعمارية.
- استخدام **Records** لتمرير البيانات المؤقتة دون بناء كلاسات إضافية.
- استخدام `const` constructors في كل مكان ممكن.

### [ ] الخطوة 4.4: حماية الذاكرة ومنع تسريب الموارد (Memory Leaks) `[إجباري / MANDATORY]`
- التخلص الإلزامي داخل دالة `dispose()` من:
  - `AnimationController` و `Ticker`.
  - `ScrollController` و `TextEditingController`.
  - `StreamSubscription` والـ Timers.
- عزل الرسوم الثقيلة والـ `CustomPainter` داخل `RepaintBoundary`.

### [ ] الخطوة 4.5: تقطيع الخطة والحفاظ على سياق الـ AI `[إجباري عند اكتمال كل مرحلة]`
بعد إتمام أي Phase، قم بتشغيل أداة تدوير الخطط:
```bash
./toolkit plan-split
```
*الفائدة:* نقل المهام المنتهية إلى `history.md` وإبقاء `plan.md` دائماً أصغر من 8KB لحماية ذاكرة الـ AI من التشتت.

---

## 6. المرحلة 5: الفحص الآلي المستقل واختبارات المتانة (Autonomous QA & Chaos Testing)

تُنفذ هذه الخطوات للتأكد من خلو التطبيق من العيوب والشاشات المكسورة قبل عمل Commit.

### [ ] الخطوة 5.1: توليد سيناريو فحص Maestro للميزة `[اختياري / موصى به بقوة]`
```bash
./toolkit qa gen <FEATURE_NAME>
```
ينشئ ملف فحص في `test/qa_flows/<feature>_flow.yaml` يفحص الشاشة تفاعلياً.

### [ ] الخطوة 5.2: تشغيل الفحص الآلي الذاتي `[إجباري قبل التسليم]`
```bash
./toolkit qa run <FEATURE_NAME>
# أو لتشغيل كل سيناريوهات الفحص:
make qa
```
*ما يتم تحليله:*
- رصد وتحديد أي **RenderFlex Overflows** (الخطوط الصفراء المكسورة).
- توليد بطاقة التقرير في `test/qa_reports/` لتمكين الـ AI من إصلاح الخطأ ذاتياً (Self-Healing).

### [ ] الخطوة 5.3: اختبار الشاشات تحت ظروف الشبكة الصعبة (Chaos Testing) `[اختياري]`
- تفعيل `qa_chaos_interceptor.dart` لفحص ظهور شاشات الخطأ وإعادة المحاولة في حالات (500 Error, Timeout, Offline Mode).

### [ ] الخطوة 5.4: التحقق من معايير الكود والـ Linting `[إجباري / MANDATORY]`
```bash
make format && make analyze
```

---

## 7. المرحلة 6: إنهاء الجلسة وإدارة الذاكرة الحية (Session Wrap-up & Living Memory)

تُنفذ في نهاية كل جلسة عمل لضمان استمرار التعلم التراكمي للـ AI في مشروعك.

### [ ] الخطوة 7.1: توثيق الدروس المستفادة والـ Gotchas `[إجباري / MANDATORY]`
- افتح ملف [`ai_docs/memory.md`](file:///ai_docs/memory.md).
- سجّل أي مشكلة خاصة واجهتك (مثلاً: مشكلة في إصدار مكتبة، إعداد خاص بالـ Gradle، أو تعارض ألوان).
- *النتيجة:* لن يكرر الـ AI نفس الخطأ مرة ثانية في الجلسات القادمة أبداً.

### [ ] الخطوة 7.2: تحديث سجل العمل اليومي `[اختياري]`
سجل المهام المنجزة في ملف `ai_docs/worklog.md` لحفظ تاريخ التطوير اليومي.

### [ ] الخطوة 7.3: سحب تحديثات الـ Toolkit من GitHub `[اختياري - دوري]`
لسحب أي تحسينات جديدة على الـ Toolkit ومزامنة قواعد الـ IDE:
```bash
./toolkit pull
```

---

## 8. جدول الأوامر السريعة اليومية (Quick Daily Cheat-Sheet)

| الهدف اليومي | الأمر السريع عبر الـ Makefile | الأمر المقابل عبر الـ CLI |
| :--- | :--- | :--- |
| **تشغيل التطبيق** | `make run` (أو `make dev run`) | `flutter run` |
| **بناء نسخة أندرويد** | `make apk` (أو `make prod apk`) | `flutter build apk` |
| **إضافة مكوّن جديد** | `make toolkit-add NAME=button` | `./toolkit add button` |
| **فحص الكود والـ Lint** | `make analyze && make format` | `flutter analyze && dart format .` |
| **تشغيل فحص الـ QA** | `make qa` | `./toolkit qa run` |
| **تقطيع الخطة والأرشفة** | — | `./toolkit plan-split` |
| **مزامنة الحزم تلقائياً** | `make deps-sync` | `./toolkit deps sync` |
| **تحديث الـ Toolkit** | `make toolkit-pull` | `./toolkit pull` |
| **فحص سلامة القواعد** | — | `./toolkit verify` |
