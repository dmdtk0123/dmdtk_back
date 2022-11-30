from Demo.demo import get_caption_pred
from controller.similarity import get_similarity


def match_text2image():
    pred_caption_list = get_caption_pred()

    similarity_result = get_similarity(pred_caption_list)

    # return (pred_caption_list, similarity_result)
    return similarity_result
