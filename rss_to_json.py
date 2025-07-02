# أضف هذه الاستيرادات في بداية سكربت بايثون الخاص بك:
import google.generativeai as genai
import os # لتحميل مفتاح API بأمان من متغيرات البيئة
import time # هذا مهم لتحديد معدل الاستدعاء إذا قمت بإجراء مكالمات متعددة

# --- تهيئة Gemini API ---
# هذا السطر يربط سكربت الخاص بك بـ Gemini API باستخدام المفتاح السري
# الذي توفره GitHub Actions عبر متغيرات البيئة.
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# أضف فحصًا لمفتاح API. هذا مفيد أثناء الاختبار المحلي.
if os.environ.get("GOOGLE_API_KEY") is None:
    print("تحذير: متغير البيئة 'GOOGLE_API_KEY' غير موجود. قد لا تعمل وظائف Gemini API محليًا.")
    print("للاختبار المحلي، قم بتعيينه (مثال: export GOOGLE_API_KEY='YOUR_KEY_HERE' على Linux/macOS، أو set GOOGLE_API_KEY='YOUR_KEY_HERE' على Windows CMD)")


def paraphrase_arabic_article(text_to_paraphrase, max_output_tokens=1000, temperature=0.7):
    """
    يعيد صياغة مقال إخباري باللغة العربية باستخدام نموذج Gemini Pro.

    Args:
        text_to_paraphrase (str): النص الأصلي للمقال المراد إعادة صياغته.
        max_output_tokens (int): الحد الأقصى لعدد التوكنات في النص المعاد صياغته.
                                 قم بضبط هذا بناءً على الطول المتوقع للمقالات المعاد صياغتها.
        temperature (float): يتحكم في إبداع/عشوائية الناتج.
                             القيم الأقل (مثل 0.2-0.5) لناتج أكثر دقة/واقعية.
                             القيم الأعلى (مثل 0.7-1.0) لناتج أكثر تنوعًا/إبداعًا.

    Returns:
        str: النص المعاد صياغته، أو رسالة خطأ إذا فشلت العملية.
    """
    if not text_to_paraphrase or not text_to_paraphrase.strip():
        return "خطأ: لم يتم توفير نص لإعادة الصياغة."
    
    # فحص حاسم: تأكد من توفر مفتاح API قبل إجراء الاستدعاء
    if os.environ.get("GOOGLE_API_KEY") is None:
        return "خطأ: GOOGLE_API_KEY غير مهيأ. لا يمكن استدعاء Gemini API."

    try:
        model = genai.GenerativeModel(
            'gemini-pro', # 'gemini-pro' هو النموذج الأنسب للمهام النصية
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_output_tokens,
            }
        )

        # صياغة توجيه احترافي للنموذج لأداء إعادة الصياغة
        # التوجيه المفصل والواضح يؤدي عادة إلى نتائج أفضل.
        prompt = (
            f"أنت خبير في التحرير الصحفي وإعادة الصياغة الإبداعية. "
            f"مهمتك هي إعادة صياغة المقال الإخباري العربي التالي بأسلوب احترافي وجذاب، "
            f"مع الحفاظ بدقة على المعنى الأصلي وجميع الحقائق الهامة. "
            f"تجنب أي تكرار في الأفكار أو المفردات. استخدم مفردات غنية ومتنوعة وأسلوبًا صحفيًا موضوعيًا ومقنعًا. "
            f"تأكد من أن النص الجديد يتدفق بسلاسة وسهل القراءة، ومناسب للنشر الفوري."
            f"\n\nالمقال الأصلي:\n{text_to_paraphrase}"
            f"\n\nالنسخة المعاد صياغتها:\n"
        )

        response = model.generate_content(prompt)

        # فحص بنية الاستجابة للنص الذي تم إنشاؤه
        if response and response.candidates and response.candidates[0].text:
            paraphrased_text = response.candidates[0].text
            return paraphrased_text.strip()
        else:
            # معالجة الحالات التي تكون فيها الاستجابة فارغة أو لا تحتوي على النص المتوقع
            return f"خطأ: لم يتمكن نموذج Gemini من إعادة صياغة المقال. تفاصيل الاستجابة غير المتوقعة: {response}"

    except genai.types.BlockedPromptException as e:
        # يحدث هذا إذا تم حظر المحتوى لأسباب تتعلق بالسلامة
        return f"خطأ: فشلت إعادة الصياغة حيث تم حظر المحتوى لأسباب تتعلق بالسلامة. التفاصيل: {e.safety_ratings}"
    except Exception as e:
        # التقاط الأخطاء المحتملة الأخرى (مشاكل الشبكة، تجاوز حدود الاستخدام، مفتاح API غير صالح، إلخ.)
        return f"حدث خطأ غير متوقع أثناء استدعاء Gemini API: {e}"

# --- مثال على كيفية استخدام الدالة محليًا (لأغراض الاختبار) ---
if __name__ == "__main__":
    # سيتم تشغيل هذه الكتلة فقط عندما يتم تنفيذ سكربت بايثون مباشرة.
    # تأكد من تعيين متغير البيئة GOOGLE_API_KEY للاختبار المحلي!
    
    sample_article_to_paraphrase = """
    قال الرئيس التنفيذي لشركة التكنولوجيا الفضائية الجديدة إن الإطلاق التجريبي الأخير للصاروخ كان ناجحًا بشكل باهر، وفتح آفاقًا جديدة لاستكشاف الفضاء التجاري. وأضاف أن الشركة تخطط لإرسال أول بعثة مأهولة إلى المريخ في غضون السنوات الخمس المقبلة، مؤكداً التزامهم بتحقيق هذا الهدف الطموح. وقد أثار هذا الإعلان حماسًا كبيرًا في الأوساط العلمية والتكنولوجية حول العالم.
    """

    print("النص الأصلي:")
    print(sample_article_to_paraphrase)
    print("\n" + "="*50 + "\n")

    print("جاري إعادة الصياغة بواسطة Gemini...")
    paraphrased_output = paraphrase_arabic_article(sample_article_to_paraphrase, max_output_tokens=700)
    
    print("\nالنص المعاد صياغته بواسطة Gemini:")
    print(paraphrased_output)
    print("\n" + "="*50 + "\n")

    # التكامل المفاهيمي مع منطق جلب الأخبار الخاص بك:
    # بعد أن تقوم دالة `fetch_and_save_news()` بملء `all_articles`:
    # for article in all_articles:
    #     original_summary = article.get('summary', '')
    #     if original_summary and len(original_summary) > 50: # أعد الصياغة فقط إذا كان الملخص موجودًا وطويلاً بما يكفي
    #         print(f"جاري إعادة صياغة الملخص لـ: {article.get('title', 'بدون عنوان')}")
    #         paraphrased_version = paraphrase_arabic_article(original_summary, max_output_tokens=500)
    #         article['paraphrased_summary'] = paraphrased_version # أضف حقلًا جديدًا للملخص المعاد صياغته
    #         time.sleep(0.5) # مهم: أضف تأخيرًا بسيطًا لتجنب تجاوز حدود معدل استدعاء API
