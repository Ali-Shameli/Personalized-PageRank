# src/algorithms/ppr_incremental_exact.py
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve


def incremental_ppr_power_exact(A_old, scores_old, p, alpha, new_edges):
    """
    Exact incremental PPR for Power iteration algorithm.
    
    Parameters:
    -----------
    A_old : csr_matrix (n x n) - Original adjacency matrix
    scores_old : array (n,) - Original PPR scores
    p : array (n,) - Personalization vector
    alpha : float - Damping factor
    new_edges : list of (src, dst, weight)
    
    Returns:
    --------
    A_new : csr_matrix - Updated adjacency matrix
    scores_new : array - Updated PPR scores
    """
    n = A_old.shape[0]
    
    # ۱. کپی ماتریس قدیم
    A_new = A_old.copy()
    
    # ۲. اضافه کردن یال‌های جدید
    for src, dst, weight in new_edges:
        # اگر node جدید داریم، ماتریس رو resize کن
        max_idx = max(src, dst) + 1
        if max_idx > n:
            A_new.resize((max_idx, max_idx))
            # scores_old و p رو هم resize کن
            # (این بخش نیاز به توجه بیشتر داره)
            n = max_idx
        
        # اضافه/آپدیت یال
        A_new[src, dst] = weight
    
    # ۳. نرمال‌سازی سطرهای affected
    affected_rows = set(src for src, _, _ in new_edges)
    for i in affected_rows:
        row_sum = A_new[i].sum()
        if row_sum > 0:
            A_new[i] = A_new[i] / row_sum
    
    # ۴. محاسبه ماتریس انتقال
    # M = A (چون قبلاً نرمال‌سازی شده)
    M_old = A_old
    M_new = A_new
    
    # ۵. محاسبه ΔM = M_new - M_old
    # فقط سطرهای affected تغییر کردن
    delta_M = sparse.lil_matrix((n, n))
    for i in affected_rows:
        delta_M[i] = M_new[i] - M_old[i]
    delta_M = delta_M.tocsr()
    
    # ۶. حل سیستم خطی: (I - α*M_new) * x = v
    # که v = (1-α)p + α * scores_old * M_old
    I = sparse.eye(n, format='csr')
    
    # محاسبه v
    v = (1 - alpha) * p + alpha * (scores_old @ M_old)
    
    # حل: x = (I - α*M_new)^(-1) * v
    x = spsolve(I - alpha * M_new, v)
    
    # ۷. محاسبه امتیازهای جدید
    scores_new = scores_old + alpha * (scores_old @ delta_M) @ x
    
    # ۸. نرمال‌سازی (اختیاری)
    scores_new = scores_new / scores_new.sum()
    
    return A_new, scores_new
