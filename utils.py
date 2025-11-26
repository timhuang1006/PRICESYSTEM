def custom_round(price):
    """
    Rounds the price to the nearest 100, but the hundreds digit must be 0, 5, or 7.
    Example:
    55955 -> 56000 (0)
    4158 -> 4000 (0)
    """
    if not isinstance(price, (int, float)):
        return 0
    
    price = int(price)
    
    # 1. Round to nearest 100 first to get a base
    # But wait, the rule is "nearest 100's multiple where hundreds digit is 0, 5, 7"
    # Let's try a different approach.
    # We want to find a target T such that T % 100 == 0 AND (T // 100) % 10 in {0, 5, 7}
    # And abs(price - T) is minimized.
    
    # Get the thousands part and the rest
    thousands = (price // 1000) * 1000
    remainder = price % 1000
    
    # Possible candidates for the hundreds part:
    # 000, 500, 700, 1000 (which is 000 of next thousand), 
    # 1500, 1700...
    # Actually, for any given price, the candidates are:
    # thousands + 0
    # thousands + 500
    # thousands + 700
    # thousands + 1000 (next thousand + 0)
    # thousands - 300 (prev thousand + 700) -> 700 of prev thousand
    # thousands - 500 (prev thousand + 500)
    
    candidates = [
        thousands + 0,
        thousands + 500,
        thousands + 700,
        thousands + 1000, # 0 of next thousand
        thousands - 300,  # 700 of prev thousand
        thousands - 500,  # 500 of prev thousand
        thousands - 1000  # 0 of prev thousand
    ]
    
    # Filter out negative candidates if any (price shouldn't be negative but just in case)
    candidates = [c for c in candidates if c >= 0]
    
    # Find the candidate with minimum difference
    best_candidate = candidates[0]
    min_diff = abs(price - best_candidate)
    
    for cand in candidates:
        diff = abs(price - cand)
        if diff < min_diff:
            min_diff = diff
            best_candidate = cand
        elif diff == min_diff:
            # Tie-breaking: usually round up or to even? 
            # Requirement doesn't specify. Let's pick the larger one for better profit? 
            # Or standard round half up.
            # Let's stick to the first one found or max?
            # 4158 -> 4000 (diff 158). 4500 (diff 342). 
            # 55955 -> 56000 (diff 45). 55700 (diff 255).
            pass
            
    return best_candidate
