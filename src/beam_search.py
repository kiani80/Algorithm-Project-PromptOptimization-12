# src/beam_search.py

from llm_oracle import generate_mutations, evaluate_prompt

def run_beam_search(initial_prompt, beam_width=2, max_depth=5, n_mutations=3):
    """
    اجرای الگوریتم Beam Search برای بهینه‌سازی پرامپت.
    """
    print("--- شروع الگوریتم Beam Search ---")
    
    # ارزیابی پرامپت اولیه
    initial_score = evaluate_prompt(initial_prompt)
    beam = [(initial_prompt, initial_score)]
    
    print(f"پرامپت اولیه: '{initial_prompt}' | امتیاز: {initial_score}")
    print(f"پهنای پرتو (Beam Width): {beam_width}")
    
    # تاریخچه بهترین امتیاز در هر عمق برای رسم نمودار
    history = [(0, initial_score)]
    
    depth = 1
    while depth <= max_depth:
        print(f"\n--- عمق {depth} ---")
        all_candidates = []
        
        # ۱. تولید همسایه برای تمام پرامپت‌های موجود در Beam
        for current_prompt, _ in beam:
            mutations = generate_mutations(current_prompt, n_mutations)
            for m in mutations:
                if m not in [c[0] for c in all_candidates]: # جلوگیری از تکرار
                    all_candidates.append(m)
                    
        print(f"کل کاندیداهای تولید شده در این عمق: {len(all_candidates)} مورد")
        
        # ۲. ارزیابی تمام کاندیداهای جدید
        candidate_scores = []
        for candidate in all_candidates:
            score = evaluate_prompt(candidate)
            candidate_scores.append((candidate, score))
            
        # ۳. مرتب‌سازی کاندیداها بر اساس امتیاز (نزولی)
        candidate_scores.sort(key=lambda x: x[1], reverse=True)
        
        # ۴. انتخاب B پرامپت برتر برای مرحله بعد
        beam = candidate_scores[:beam_width]
        
        print("پرامپت‌های انتخاب شده برای پرتو (Beam) بعدی:")
        for rank, (p, s) in enumerate(beam):
            print(f"  رتبه {rank+1}: '{p}' (امتیاز: {s})")
            
        # ثبت بهترین امتیاز این مرحله در تاریخچه
        best_score_at_depth = beam[0][1]
        history.append((depth, best_score_at_depth))
        
        # شرط توقف زودهنگام: اگر به بالاترین امتیاز ممکن (۱۰) رسیدیم
        if best_score_at_depth == 10:
            print("\n-> به امتیاز کامل (۱۰) رسیدیم! توقف زودهنگام جستجو.")
            break
            
        depth += 1

    best_prompt, best_score = beam[0]
    print("\n=== نتیجه نهایی Beam Search ===")
    print(f"بهترین پرامپت پیدا شده: '{best_prompt}'")
    print(f"امتیاز نهایی: {best_score}")
    
    return best_prompt, best_score, history

if __name__ == "__main__":
    # اجرای تست روی کد
    start_prompt = "خلاصه متن"
    run_beam_search(initial_prompt=start_prompt, beam_width=2, max_depth=3, n_mutations=3)