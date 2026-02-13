# src/hill_climbing.py

import sys
import os
# این دو خط برای این است که بتوانیم فایل llm_oracle را به درستی ایمپورت کنیم
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from llm_oracle import generate_mutations, evaluate_prompt

def run_hill_climbing(initial_prompt, max_steps=10, n_mutations=3):
    """
    اجرای الگوریتم تپه‌نوردی (Hill Climbing) برای بهینه‌سازی پرامپت.
    """
    current_prompt = initial_prompt
    current_score = evaluate_prompt(current_prompt)
    
    print("--- شروع الگوریتم Hill Climbing ---")
    print(f"پرامپت اولیه: '{current_prompt}' | امتیاز: {current_score}")
    
    # ذخیره تاریخچه برای رسم نمودار همگرایی (Convergence Plot) در آینده
    history = [(0, current_score)] 
    
    step = 1
    while step <= max_steps:
        print(f"\n--- گام {step} ---")
        
        # ۱. تولید همسایه‌ها (تولید کاندیداها با کمک LLM)
        candidates = generate_mutations(current_prompt, n_mutations)
        print(f"کاندیداهای تولید شده: {candidates}")
        
        best_candidate = None
        best_candidate_score = -1
        
        # ۲. ارزیابی تمام کاندیداها
        for candidate in candidates:
            score = evaluate_prompt(candidate)
            print(f"ارزیابی کاندیدا '{candidate}': {score}")
            
            if score > best_candidate_score:
                best_candidate_score = score
                best_candidate = candidate
                
        # ۳. حرکت به سمت همسایه بهتر
        if best_candidate_score > current_score:
            print(f"-> پیشرفت! تغییر پرامپت به: '{best_candidate}' (امتیاز جدید: {best_candidate_score})")
            current_prompt = best_candidate
            current_score = best_candidate_score
            history.append((step, current_score))
        else:
            # اگر هیچ همسایه‌ای بهتر از حالت فعلی نبود، در نقطه بهینه محلی گیر کرده‌ایم
            print("-> هیچ همسایه بهتری پیدا نشد. توقف در نقطه بهینه محلی (Local Optimum).")
            history.append((step, current_score)) # ثبت امتیاز تکراری برای نمودار
            break
            
        step += 1
        
    print("\n=== نتیجه نهایی Hill Climbing ===")
    print(f"بهترین پرامپت پیدا شده: '{current_prompt}'")
    print(f"امتیاز نهایی: {current_score}")
    
    return current_prompt, current_score, history

if __name__ == "__main__":
    # اجرای یک تست ساده روی کد
    # ما از یک پرامپت ضعیف شروع می‌کنیم که امتیازش ۲ است
    start_prompt = "خلاصه متن" 
    run_hill_climbing(initial_prompt=start_prompt, max_steps=5, n_mutations=3)