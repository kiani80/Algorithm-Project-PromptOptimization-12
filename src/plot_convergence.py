# src/plot_convergence.py

import os
import sys
import time
import matplotlib.pyplot as plt

# تنظیم مسیر برای دسترسی به ماژول‌ها
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from hill_climbing import run_hill_climbing
from beam_search import run_beam_search

def plot_algorithm_comparison():
    # یک پرامپت ضعیف انتخاب می‌کنیم تا مسیر رشد الگوریتم‌ها را به خوبی ببینیم
    initial_prompt = "خلاصه متن"
    
    print("در حال اجرای Hill Climbing...")
    _, _, hc_history = run_hill_climbing(initial_prompt, max_steps=6, n_mutations=3)
    
    print("\nدر حال اجرای Beam Search...")
    _, _, bs_history = run_beam_search(initial_prompt, beam_width=2, max_depth=6, n_mutations=3)
    
    # استخراج داده‌ها برای رسم نمودار
    # hc_history و bs_history لیستی از تاپل‌ها (گام، امتیاز) هستند
    hc_steps = [item[0] for item in hc_history]
    hc_scores = [item[1] for item in hc_history]
    
    bs_steps = [item[0] for item in bs_history]
    bs_scores = [item[1] for item in bs_history]
    
    # --- رسم نمودار ---
    plt.figure(figsize=(10, 6))
    
    # خط مربوط به Hill Climbing (رنگ آبی)
    plt.plot(hc_steps, hc_scores, marker='o', linestyle='-', color='b', label='Hill Climbing')
    
    # خط مربوط به Beam Search (رنگ نارنجی)
    plt.plot(bs_steps, bs_scores, marker='s', linestyle='--', color='orange', label='Beam Search (B=2)')
    
    # تنظیمات ظاهری نمودار
    plt.title('Convergence Plot: Prompt Optimization Algorithms', fontsize=14)
    plt.xlabel('Iteration / Depth Step', fontsize=12)
    plt.ylabel('LLM Evaluator Score (1 to 10)', fontsize=12)
    plt.ylim(0, 11)
    plt.xticks(range(0, 8))
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend(loc='lower right', fontsize=12)
    
    # ساخت پوشه charts اگر وجود نداشت (طبق ساختار استاندارد پروژه)
    project_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
    charts_dir = os.path.join(project_root, 'charts')
    os.makedirs(charts_dir, exist_ok=True)
    
    # ذخیره تصویر
    plot_path = os.path.join(charts_dir, f'convergence_plot_{time.strftime("%Y%m%d_%H%M%S", time.localtime())}.png')
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    
    print(f"\nنمودار با موفقیت رسم شد و در مسیر زیر ذخیره شد:\n{plot_path}")
    plt.show()

if __name__ == "__main__":
    plot_algorithm_comparison()