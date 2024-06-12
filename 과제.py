def recommend_food():
    print("안녕하세요! 음식 추천 프로그램에 오신 것을 환영합니다.")
    
    # 질문 1: 음식 종류
    cuisine = input("어떤 종류의 요리를 원하시나요? (한식, 중식, 일식, 양식): ").strip()
    
    # 질문 2: 재료
    ingredient = input("특정한 재료가 필요하신가요? (예: 고기, 생선, 채소, 상관없음): ").strip()
    
    # 질문 3: 매운 음식
    spicy = input("매운 음식을 좋아하시나요? (네, 아니오): ").strip()
    
    # 질문 4: 식이 제한
    dietary_restriction = input("특정한 식이 제한이 있으신가요? (예: 채식, 글루텐 프리, 상관없음): ").strip()

    # 추천 로직
    if cuisine == "한식":
        if ingredient == "고기":
            if spicy == "네":
                if dietary_restriction == "상관없음":
                    return "매운 돼지 불고기를 추천합니다!"
                elif dietary_restriction == "채식":
                    return "채식 가능한 불고기 버섯볶음을 추천합니다!"
            elif spicy == "아니오":
                return "갈비찜을 추천합니다!"
        elif ingredient == "채소":
            return "비빔밥을 추천합니다!"
    elif cuisine == "중식":
        if ingredient == "생선":
            return "탕수어를 추천합니다!"
        elif ingredient == "채소":
            return "마파두부를 추천합니다!"
    elif cuisine == "일식":
        if ingredient == "생선":
            if spicy == "네":
                return "스파이시 참치 롤을 추천합니다!"
            else:
                return "사시미를 추천합니다!"
    elif cuisine == "양식":
        if ingredient == "고기":
            if spicy == "네":
                return "스파이시 치킨 윙을 추천합니다!"
            else:
                return "스테이크를 추천합니다!"
        elif ingredient == "채소":
            if dietary_restriction == "채식":
                return "그린 샐러드를 추천합니다!"
            else:
                return "채소 라자냐를 추천합니다!"
    
    return "요청하신 조건에 맞는 음식을 찾지 못했습니다. 다른 조건을 시도해 주세요."

# 프로그램 실행
print(recommend_food())
