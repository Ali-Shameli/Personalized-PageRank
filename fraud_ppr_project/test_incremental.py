"""
تست واقعی الگوریتم افزایشی - با گراف درست
"""
import sys
import os
import numpy as np
from scipy import sparse

sys.path.append('src')

def create_proper_test_graph():
    """ساخت یک گراف درست با dangling nodes handle شده"""
    n = 5
    
    # گراف: 
    # 0 → 1 (0.5), 0 → 2 (0.5)
    # 1 → 3 (1.0)
    # 2 → 4 (1.0)
    # 3 و 4 هیچ یال خروجی ندارند -> باید teleport کنند
    
    data = [0.5, 0.5, 1.0, 1.0]
    rows = [0, 0, 1, 2]
    cols = [1, 2, 3, 4]
    
    A = sparse.csr_matrix((data, (rows, cols)), shape=(n, n))
    
    print("گراف تست:")
    print("  0 → 1 (0.5), 0 → 2 (0.5)")
    print("  1 → 3 (1.0)")
    print("  2 → 4 (1.0)")
    print("  3,4 گره‌های آویزان (dangling)")
    
    return A

# گراف درست
A = create_proper_test_graph()

# Personalization: فقط گره ۰ seed است
from algorithms.ppr_power import make_personalization_vector
p = make_personalization_vector(5, [0])
print(f"\nPersonalization: گره ۰ = {p[0]:.2f}")

# PPR اولیه - با تابع درست
from algorithms.ppr_power import personalized_pagerank

print("\nمحاسبه PPR اولیه...")
result = personalized_pagerank(
    A, 
    alpha=0.85, 
    personalize=p,
    max_iter=100, 
    tol=1e-6
)

r_old = result[0] if isinstance(result, tuple) else result
r_old = r_old / r_old.sum()

print("\nامتیازهای اولیه (درست):")
for i in range(5):
    print(f"  گره {i}: {r_old[i]:.6f}")

# حالا الگوریتم افزایشی
from algorithms.ppr_incremental_exact import incremental_ppr_fixed

# یال جدید: گره ۴ (آویزان) به گره ۱ لینک می‌دهد
new_edges = [(4, 1, 1.0)]
print(f"\nاضافه کردن یال جدید: {new_edges[0]}")
print("(گره ۴ که آویزان بود، حالا به گره ۱ لینک می‌دهد)")

A_new, r_new = incremental_ppr_fixed(
    A_old=A,
    r_old=r_old,
    personalization=p,
    alpha=0.85,
    new_edges=new_edges
)

print("\nنتایج افزایشی:")
for i in range(5):
    print(f"  گره {i}: {r_new[i]:.6f} (تغییر: {r_new[i]-r_old[i]:+.6f})")

# محاسبه مستقیم برای مقایسه
print("\nمحاسبه مستقیم برای مقایسه...")
A_full = A.copy().tolil()
for src, dst, w in new_edges:
    A_full[src, dst] = w

# نرمال‌سازی
for i in range(5):
    row_sum = A_full[i].sum()
    if row_sum > 0:
        A_full[i] = A_full[i] / row_sum

A_full = A_full.tocsr()

result_full = personalized_pagerank(
    A_full, 
    alpha=0.85, 
    personalize=p,
    max_iter=100, 
    tol=1e-6
)

r_full = result_full[0] if isinstance(result_full, tuple) else result_full
r_full = r_full / r_full.sum()

print("\n" + "="*50)
print("مقایسه نتایج:")
print("گره | افزایشی | مستقیم | تفاوت")
print("-" * 40)

max_diff = 0
for i in range(5):
    diff = abs(r_new[i] - r_full[i])
    if diff > max_diff:
        max_diff = diff
    print(f"{i:3} | {r_new[i]:.6f} | {r_full[i]:.6f} | {diff:.6f}")

print(f"\nحداکثر تفاوت: {max_diff:.6f}")

if max_diff < 0.05:
    print("✅ عالی! الگوریتم درست کار می‌کند")
elif max_diff < 0.1:
    print("⚠️  قابل قبول برای پروژه")
else:
    print("❌ تفاوت زیاد است")

# تست دوم: یال از گره ۳ به گره ۰ (seed)
print("\n" + "="*50)
print("تست دوم: یال از گره آویزان به seed")
new_edges2 = [(3, 0, 1.0)]

A_new2, r_new2 = incremental_ppr_fixed(
    A_old=A,
    r_old=r_old,
    personalization=p,
    alpha=0.85,
    new_edges=new_edges2
)

# محاسبه مستقیم
A_full2 = A.copy().tolil()
for src, dst, w in new_edges2:
    A_full2[src, dst] = w
for i in range(5):
    row_sum = A_full2[i].sum()
    if row_sum > 0:
        A_full2[i] = A_full2[i] / row_sum
A_full2 = A_full2.tocsr()

result_full2 = personalized_pagerank(A_full2, alpha=0.85, personalize=p, max_iter=100, tol=1e-6)
r_full2 = result_full2[0] if isinstance(result_full2, tuple) else result_full2
r_full2 = r_full2 / r_full2.sum()

print("\nنتایج تست دوم:")
print("گره | افزایشی | مستقیم | تفاوت")
print("-" * 40)

max_diff2 = 0
for i in range(5):
    diff = abs(r_new2[i] - r_full2[i])
    if diff > max_diff2:
        max_diff2 = diff
    print(f"{i:3} | {r_new2[i]:.6f} | {r_full2[i]:.6f} | {diff:.6f}")

print(f"\nحداکثر تفاوت: {max_diff2:.6f}")

if max_diff2 < 0.1:
    print("✅ الگوریتم برای پروژه کافی است!")
else:
    print("⚠️  نیاز به بهبود دارد")