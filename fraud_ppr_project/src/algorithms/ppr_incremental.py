import numpy as np
from scipy import sparse
from src.algorithms.ppr_power import power_iteration_sparse  # فرض بر این است که این تابع را داری

def update_ppr_incremental(adj_matrix, old_scores, personalization_dict, alpha, new_edges, tol=1e-6):
    """
    Update PPR efficiently using Warm Start (starting from old_scores).
    
    Parameters:
    -----------
    adj_matrix : csr_matrix (n x n) - Current adjacency matrix
    old_scores : array (n,) - Previous PPR scores
    personalization_dict : dict - {node_id: weight}
    alpha : float - Damping factor
    new_edges : list of (src, dst, weight)
    
    Returns:
    --------
    new_adj : csr_matrix - Updated adjacency matrix
    new_scores : array - Updated PPR scores
    """
    # 1. تبدیل به lil برای ویرایش آسان
    A = adj_matrix.tolil()
    n = A.shape[0]

    # محاسبه سایز جدید اگر نود جدید داشته باشیم
    max_node_idx = n - 1
    for s, d, w in new_edges:
        max_node_idx = max(max_node_idx, s, d)
    
    new_n = max_node_idx + 1

    # اگر گراف بزرگ شده، باید ریسایز کنیم
    if new_n > n:
        A.resize((new_n, new_n))
        # پدینگ اسکورهای قدیمی با صفر
        old_scores = np.pad(old_scores, (0, new_n - n), 'constant')
        n = new_n

    # 2. اعمال تغییرات یال‌ها
    for s, d, w in new_edges:
        # اگر یال قبلاً بوده، می‌توانیم جمع کنیم یا جایگزین (اینجا جایگزین فرض شده)
        # برای گراف بدون وزن (weight=1.0) هم همین کار می‌کند
        A[s, d] = w

    new_adj = A.tocsr()

    # 3. ساخت بردار شخصی‌سازی با سایز جدید (اگر نود جدید اضافه شده)
    # (power_iteration_sparse معمولاً دیکشنری می‌گیرد و خودش بردار می‌سازد،
    # اما اگر بردار می‌گیرد باید اینجا هندل شود. فرض می‌کنیم دیکشنری می‌گیرد)
    
    # 4. اجرای Power Iteration با نقطه شروع گرم (Warm Start)
    # نکته کلیدی: start_vec=old_scores باعث همگرایی بسیار سریع می‌شود.
    new_scores = power_iteration_sparse(
        new_adj,
        personalization_vector=personalization_dict,  # دیکشنری سیدها
        alpha=alpha,
        tol=tol,
        max_iter=50,       # تعداد دور کمتر چون گرم شروع می‌کنیم
        start_vec=old_scores  # <--- این پارامتر باید در power_iteration_sparse پشتیبانی شود
    )

    return new_adj, new_scores