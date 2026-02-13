# src/demo.py

import sys
import os
import time

# تنظیم مسیر
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from hill_climbing import run_hill_climbing
from beam_search import run_beam_search
from llm_oracle import evaluate_prompt

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    clear_screen()
    print("="*50)
    print(" 🚀 سیستم بهینه‌سازی پرامپت (Prompt Optimization) 🚀")
    print("="*50)
    print("درس طراحی الگوریتم - مسیر دوم")
    print("="*50)
    
    # گرفتن ورودی از کاربر (استاد/TA)
    initial_prompt = input("\nلطفاً یک پرامپت اولیه و خام وارد کنید (مثلا 'خلاصه متن'):\n> ")
    if not initial_prompt.strip():
        initial_prompt = "خلاصه متن"
        print(f"ورودی خالی بود. از پرامپت پیش‌فرض استفاده می‌شود: '{initial_prompt}'")
        
    initial_score = evaluate_prompt(initial_prompt)
    print(f"\n📊 امتیاز ارزیاب (LLM Oracle) به این پرامپت: {initial_score} از 10")
    
    print("\nکدام الگوریتم را برای بهینه‌سازی انتخاب می‌کنید؟")
    print("1. تپه‌نوردی (Hill Climbing) - سریع اما احتمال گیر کردن در بهینه محلی")
    print("2. جستجوی شعاعی (Beam Search) - جستجوی گسترده‌تر و دقیق‌تر")
    
    choice = input("\nانتخاب شما (1 یا 2): ")
    
    print("\n" + "*"*40)
    print("⏳ در حال اجرای الگوریتم... لطفاً صبر کنید...")
    time.sleep(1) # وقفه مصنوعی برای جذابیت دمو
    
    if choice == '1':
        final_prompt, final_score, _ = run_hill_climbing(initial_prompt, max_steps=5, n_mutations=3)
    elif choice == '2':
        final_prompt, final_score, _ = run_beam_search(initial_prompt, beam_width=2, max_depth=4, n_mutations=3)
    else:
        print("انتخاب نامعتبر! الگوریتم پیش‌فرض (تپه‌نوردی) اجرا می‌شود.")
        final_prompt, final_score, _ = run_hill_climbing(initial_prompt, max_steps=5, n_mutations=3)

    print("*"*40)
    print("\n🎉 بهینه‌سازی به پایان رسید!")
    print("="*50)
    print(f"🔹 پرامپت اولیه: '{initial_prompt}' (امتیاز: {initial_score})")
    print(f"✅ پرامپت نهایی: '{final_prompt}' (امتیاز: {final_score})")
    print("="*50)
    
    # نمایش میزان پیشرفت
    improvement = final_score - initial_score
    if improvement > 0:
        print(f"📈 میزان بهبود کیفیت پرامپت: +{improvement} نمره")
    else:
        print("➖ الگوریتم نتوانست پرامپت بهتری در فضای جستجو پیدا کند.")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nخروج از برنامه.")