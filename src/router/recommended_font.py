def extract_font(adjective):

    # 1사분면:
    quadrant1 = ["온화한", "깔끔한", "자연적인", "편안한", "단정한", "우아한", "심플한"]
    # 2사분면:
    quadrant2 = ["맑은", "신선한", "감성적인", "귀여운", "자유로운"]
    # 3사분면:
    quadrant3 = ["돋보이는", "개성적인", "실용적인", "모던한"]
    # 4사분면:
    quadrant4 = ["고급스러운", "세련된", "클래식한", "차분한"]
    quadrant = 0

    if adjective in quadrant1:
        quadrant = 1
        title_font, body_font = "나눔명조체", "나눔명조체"
    elif adjective in quadrant2:
        quadrant = 2
        title_font, body_font = "배달의 민족 주아체", "카페24 심플해"
    elif adjective in quadrant3:
        quadrant = 3
        title_font, body_font = "잘난체", "카페24 고운밤"
    elif adjective in quadrant4:
        quadrant = 4
        title_font, body_font = "Gmarket Sans Medium", "카페24 심플해"

    return quadrant, title_font, body_font
