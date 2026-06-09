from openai import OpenAI

def analyze_item_with_ai(api_key: str, item_desc: str, space_cost_info: dict) -> str:
    """
    OpenAI API(gpt-4o-mini)를 사용하여 물건에 대한 냉정한 처분 또는 유지 판결을 내립니다.
    """
    client = OpenAI(api_key=api_key)
    
    if space_cost_info.get("is_negligible"):
        space_info_text = "- 이 물건은 크기가 매우 작거나 주거비가 0원으로 설정되어, 물리적인 공간 손실 측정은 생략합니다."
    else:
        space_info_text = f"- 매달 이 물건 때문에 낭비되는 방세: {space_cost_info['wasted_cost_per_month']:,}원 ({space_cost_info['ratio_desc']} 차지)"
    
    prompt = f"""
    당신은 '미니멀리스트 물건 버리기 기준 제안기(비워내기)'의 냉철하고 분석적인 AI 에이전트입니다.
    사용자가 입력한 물건 정보를 바탕으로 객관적인 가치를 평가하여, 버려야 할지 유지해야 할지 명확한 판결을 내려주세요.

    [평가 기준]
    1. 무조건 버리라고 하지 마세요. 스마트폰, 매일 쓰는 볼펜, 유용한 전공 서적 등 객관적으로 실용성이 높거나 대체 불가능한 필수품이라면 **'현상 유지(Keep)'**하라고 조언하세요. 진정한 미니멀리즘은 꼭 필요한 물건을 잘 남기는 것입니다.
    2. 반면, 과거의 미련, '언젠가 쓰겠지'하는 막연한 기대감, 공간만 차지하는 물건이라면 T발 C성향의 뼈때리는 팩트 폭력으로 가차 없이 **'처분'**을 명령하세요.

    [사용자 물건 및 상황 정보]
    - 물건 설명 및 상태: {item_desc}
    {space_info_text}

    반드시 아래의 마크다운 포맷에 맞추어 답변을 작성해주세요.

    **[비워내기 AI 최종 판결: (예: 당근마켓 방출, 의류수거함, 종량제 봉투, 혹은 '현상 유지' 등 결정)]**
    * **한 줄 팩트:** (유지해야 한다면 그 타당한 이유를, 버려야 한다면 미련을 깰 수 있는 현실적인 팩트 폭력을 1문장으로 작성)
    * **공간 손실:** (공간 손실이 미미하다면 '공간 차지가 거의 없는 소형 물건입니다.'라고 작성하고, 비용이 발생한다면 1년이면 얼마가 낭비되는지 자각하게 하는 1문장 작성)
    * **액션 가이드:** (유지라면 어떻게 더 잘 활용할지, 처분이라면 구체적으로 어떻게 처분해야 하는지 행동 지침 제시)
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a sharp, pragmatic minimalist advisor who knows when to keep useful things and when to throw away useless clutter."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI 분석 중 오류가 발생했습니다. API 상태를 확인해주세요.\n(에러 내용: {e})"