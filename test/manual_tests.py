# tests/manual_tests.py

import sys
import os
import unittest

# تنظیم مسیر برای دسترسی به پوشه src
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../src'))

from llm_oracle import evaluate_prompt
from hill_climbing import run_hill_climbing
from beam_search import run_beam_search

class TestPromptOptimization(unittest.TestCase):

    def test_oracle_evaluation(self):
        """
        تست شماره ۱: بررسی عملکرد تابع ارزیاب (Oracle) روی ورودی‌های مختلف 
        (شامل حالت‌های ساده، سخت و سناریوهای شکست)
        """
        # تست یک پرامپت عالی (حالت ایده آل)
        self.assertEqual(evaluate_prompt("متن زیر را به صورت حرفه‌ای، بدون زیاده‌گویی و در سه خط برای مدیرم خلاصه کن"), 10)
        
        # تست یک پرامپت ضعیف (حالت ساده)
        self.assertEqual(evaluate_prompt("خلاصه متن"), 2)
        
        # سناریوی شکست (Failure Case): پرامپت نامفهوم که در دیکشنری ما نیست
        # باید امتیاز حداقل (۱) بگیرد تا الگوریتم آن را رد کند
        self.assertEqual(evaluate_prompt("خلاصه خلاصه 123!"), 1)

    def test_hill_climbing_improvement(self):
        """
        تست شماره ۲: بررسی اینکه آیا Hill Climbing واقعاً امتیاز را بهبود می‌بخشد یا خیر
        """
        initial_prompt = "متن زیر را خلاصه کن"
        initial_score = evaluate_prompt(initial_prompt)
        
        # اجرای الگوریتم
        final_prompt, final_score, history = run_hill_climbing(initial_prompt, max_steps=5, n_mutations=3)
        
        # امتیاز نهایی باید بزرگتر یا مساوی امتیاز اولیه باشد (الگوریتم پسرفت نمی‌کند)
        self.assertGreaterEqual(final_score, initial_score)
        # تاریخچه باید حداقل شامل یک گام (گام صفر) باشد
        self.assertGreater(len(history), 0)

    def test_beam_search_improvement(self):
        """
        تست شماره ۳: بررسی عملکرد Beam Search
        """
        initial_prompt = "لطفا این مقاله را به صورت خلاصه بنویس"
        initial_score = evaluate_prompt(initial_prompt)
        
        # اجرای الگوریتم با پهنای پرتو ۲
        final_prompt, final_score, history = run_beam_search(initial_prompt, beam_width=2, max_depth=3, n_mutations=2)
        
        self.assertGreaterEqual(final_score, initial_score)

    def test_10_real_inputs(self):
        """
        تست شماره ۴: اجرای الگوریتم روی ۱۰ ورودی مختلف برای پوشش خواسته استاد
        """
        ten_inputs = [
            "خلاصه متن", # ساده
            "متن زیر را خلاصه کن", # ساده
            "لطفا این مقاله را به صورت خلاصه بنویس", # متوسط
            "متن زیر را در یک پاراگراف کوتاه خلاصه کن", # متوسط
            "متن زیر را در سه خط خلاصه کن", # متوسط
            "مهم‌ترین نکات متن زیر را استخراج کرده و خلاصه کن", # متوسط
            "به عنوان یک ویراستار، متن را در دو خط خلاصه کن", # سخت
            "مهم‌ترین وقایع، تاریخ‌ها و نام افراد را در ۳ خط خلاصه کن", # سخت
            "به عنوان یک استاد دانشگاه، متن را به زبان ساده و با حفظ اصطلاحات خلاصه کن", # سخت
            "خلاصه کن سریع" # Edge case
        ]
        
        # فقط می‌خواهیم مطمئن شویم الگوریتم روی همه این ورودی‌ها بدون خطا اجرا می‌شود
        for prompt in ten_inputs:
            final_prompt, final_score, _ = run_hill_climbing(prompt, max_steps=2, n_mutations=2)
            self.assertIsNotNone(final_prompt)
            self.assertGreaterEqual(final_score, 1)

if __name__ == '__main__':
    unittest.main()