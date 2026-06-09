def calculate_space_cost(monthly_rent: int, size_category: str) -> dict:
    """
    물건의 크기와 사용자의 월세를 바탕으로 낭비되는 공간 비용을 계산합니다.
    초소형 물건이거나 월세가 0원이면 공간 손실을 무시합니다.
    """
    size_ratios = {
        '초소형 (스마트폰, 필기구, 지갑 등)': 0.0,
        '소형 (서랍 한 칸, 선반 일부)': 0.005,
        '중형 (사과 박스 1~2개 크기)': 0.02,
        '대형 (소형 가구, 실내 자전거 등)': 0.05
    }
    
    ratio = size_ratios.get(size_category, 0.01)
    
    if ratio == 0.0 or monthly_rent == 0:
        return {
            "wasted_cost_per_month": 0,
            "wasted_cost_per_year": 0,
            "ratio_desc": "공간 차지 미미함",
            "is_negligible": True 
        }
        
    wasted_cost_per_month = int(monthly_rent * ratio)
    
    return {
        "wasted_cost_per_month": wasted_cost_per_month,
        "wasted_cost_per_year": wasted_cost_per_month * 12,
        "ratio_desc": f"전체 공간의 약 {ratio * 100:.1f}%",
        "is_negligible": False
    }