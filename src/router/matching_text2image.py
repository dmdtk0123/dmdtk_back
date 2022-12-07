from random import sample
from Demo.demo import get_caption_pred
from controller.similarity import get_similarity


def match_text2image(kobert_result_dict):
    # 캡셔닝 진행해서
    pred_caption_list = get_caption_pred()
    # 유형1~5, 6 중 가장 잘 맞는 사진(이름)을 받아옴.
    similarity_result = get_similarity(pred_caption_list)
    # similarity_result = dict{1: "1023.jpg", 2: "3243.jpg" ...5: "2034.jpg"}
    # kobert_result_dict = {1: ['dsf', 'sdfw'], 2: ['dsf','ew'], 3: ['dsf','ew']}

    # kobert 분류된 문장을 1~2줄 골라줌.
    for key in kobert_result_dict.keys():
        value_list = kobert_result_dict[key]
        value_list = sample(value_list, 2)
        kobert_result_dict[key] = ". ".join(value_list)

    matching_result = {1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}}
    for key in similarity_result.keys():
        matching_result[key]["image"] = similarity_result[key]

    for key in kobert_result_dict.keys():
        matching_result[key]["text"] = kobert_result_dict[key]

    return matching_result
