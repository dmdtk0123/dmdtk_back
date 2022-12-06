from Demo.demo import get_caption_pred
from controller.similarity import get_similarity


def match_text2image(kobert_result_list):
    # 캡셔닝 진행해서
    pred_caption_list = get_caption_pred()
    # 1~5 중 가장 잘 어울리는 사진이름과 캡셔닝 결과를
    similarity_result = get_similarity(pred_caption_list)  # 5개의 df이 들어가 있는 리스트.

    # return (pred_caption_list, similarity_result)
    return similarity_result
