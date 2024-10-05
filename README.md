# بوت ذكر للتلغرام

## نظرة عامة

بوت ذكر هو بوت تلغرام يقدم للمستخدمين أدعية، أذكار، وآيات قرآنية بشكل دوري. تم تطوير هذا البوت بواسطة [فارس عبد الرؤوف](https://github.com/farsabdraouf) لمساعدة المسلمين على البقاء على اتصال مع إيمانهم في حياتهم اليومية.

## الميزات

- إرسال أدعية عشوائية من مصادر موثوقة
- مشاركة أذكار يومية من مختلف الفئات
- تقديم آيات قرآنية مع معلومات تفصيلية
- إمكانية تخصيص وتيرة الإشعارات لكل نوع من المحتوى
- دعم اللغة العربية بالكامل

## كيفية الاستخدام

1. ابدأ محادثة مع البوت على تلغرام
2. استخدم الأوامر التالية لضبط تفضيلاتك:
   - `/duaa` لضبط إعدادات الأدعية
   - `/adkar` لضبط إعدادات الأذكار
   - `/quran` لضبط إعدادات الآيات القرآنية
3. اختر الوتيرة المفضلة لديك (30 دقيقة، ساعة، ساعتين، مرة في اليوم)
4. حدد ما إذا كنت تريد المحتوى بشكل عشوائي أو مرتب
5. استمتع بالتذكيرات الدورية!

## التثبيت والإعداد

لتشغيل هذا البوت على الخادم الخاص بك، اتبع الخطوات التالية:

1. قم بتثبيت Python 3.7 أو أحدث
2. قم بتثبيت المكتبات المطلوبة:
   ```
   pip install telebot schedule
   ```
3. قم بتنزيل ملفات البيانات التالية ووضعها في نفس المجلد مع الكود:
   - `duaa.json`
   - `adkar.json`
   - `quran.json`
4. قم بإنشاء بوت تلغرام جديد واحصل على الـ TOKEN الخاص به
5. استبدل `TOKEN` في الكود بالتوكن الخاص ببوتك
6. قم بتشغيل البوت:
   ```
   python app.py
   ```

## هيكل الكود

- `app.py`: الملف الرئيسي للبوت
- تحميل البيانات من ملفات JSON
- تعريف الدوال المساعدة لجلب المحتوى
- معالجة أوامر المستخدم
- جدولة الرسائل باستخدام مكتبة `schedule`

## المساهمة

نرحب بالمساهمات لتحسين هذا البوت! إذا كان لديك اقتراحات أو تحسينات، يرجى فتح issue أو تقديم pull request.

## الترخيص

هذا المشروع مرخص تحت رخصة MIT. انظر ملف [LICENSE](LICENSE) للمزيد من التفاصيل.

## الاتصال

لمزيد من المعلومات أو الاستفسارات، يمكنك التواصل مع المطور:

- [فارس عبد الرؤوف](https://github.com/farsabdraouf)

## شكر وتقدير

- شكر خاص لجميع المساهمين في مصادر [الأدعية](https://github.com/AhmedElTabarani/100-duaa-from-the-book-and-authentic-sunnah) و [الأذكار وأيات القرآن الكريم](https://github.com/nawafalqari/ayah/tree/main/src/data) المستخدمة في هذا البوت.
- شكر للمجتمع الإسلامي على الدعم والتشجيع المستمر.
