from math import *
import pandas as pd

standard_descriptions_1 = [
    "A person holding an apple in their hand." "A bunch of red apples",
    "A pile of red apples",
    "baskets of red apples",
]

standard_descriptions_2 = [
    "A bunch of apples growing on a tree in a garden.",
    "A bunch of red apples hanging from a tree in a field.",
    "A group of green trees in a field.",
    "A woman standing in a field with tree." "People with red apples on a tree.",
    "A group of red apples in a field.",
]

standard_descriptions_3 = [
    "An apple and a plastic container on a table.",
    "An apple and a missing the top of a table.",
    "on top of apples.",
    "A green machine with apples on top of apples.",
]

standard_descriptions_4 = [
    "A group of apples in a box with a cup of coffee.",
    "coffee cups sitting on top of a table.",
    "A group of apples sitting next to a cup on a table.",
    " A row of apples sitting on a table.",
]

standard_descriptions_5 = ["A bunch of red apples in a box.", "A group of boxes of apples."]

standard_descriptions = [
    standard_descriptions_1,
    standard_descriptions_2,
    standard_descriptions_3,
    standard_descriptions_4,
    standard_descriptions_5,
]


def jaccard_similarity(x=[], y=[]):
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))

    return intersection_cardinality / float(union_cardinality)


def get_image(idx, standard_descriptions, data_df):
    for standard_description in standard_descriptions:
        similarity = []

        # 토큰화를 수행
        tokenized_doc1 = standard_description.split()

        for caption in data_df["imageCaption"]:
            # 토큰화를 수행
            tokenized_doc2 = caption.lower().split()
            similarity.append(jaccard_similarity(tokenized_doc1, tokenized_doc2))

        data_df["similarity" + str(idx)] = similarity


# 이미지 유형별 유사도 가져오기
def get_description_similarity(result_df, description):
    # simi_s = pd.Series(result_df[description])
    # simi_s.sort_values(ascending=False, inplace=True)

    # simi_s = pd.DataFrame(result_df[description])
    simi_s = result_df[["fileName", description]]
    simi_s.sort_values(by=description, ascending=False, inplace=True)

    return simi_s[:1]  # 5가지 유형 중 유사도가 높은 1개만 뽑아서 return함.


# 사진 유형별 유사도 가져오기
def get_image_similarity(result_df, image_idx):
    img_simi_s = pd.Series(result_df.loc[image_idx].iloc[2:])
    img_simi_s.sort_values(ascending=False, inplace=True)

    return img_simi_s


def get_similarity(pred_caption_list):  # [[3033.jpg, 'apple is...'], [  ], ... ]
    # data_df = pd.read_csv("image_caption_test_data.csv", low_memory=False)
    col_name = ["fileName", "imageCaption"]
    data_df = pd.DataFrame(pred_caption_list, columns=col_name)

    print("data_df")
    print(data_df)

    for i in range(5):
        get_image(i + 1, standard_descriptions[i], data_df)

    print("After get_image() data_df : ")
    print(data_df)

    result_df = data_df

    priority = ["3", "4", "2", "5", "1"]
    result_dict = {}

    for index in range(5):
        result_s = get_description_similarity(result_df, "similarity" + priority[index])
        print("--------result_a-------")
        print(result_s)

        result_dict[priority[index]] = result_s.loc[result_s.index, "fileName"]

        index_arr = result_s.index
        print("index_arr")
        print(index_arr)

        for idx in index_arr:
            result_df.drop(index=idx, errors="ignore", inplace=True)
        # 우선순위가 높은 3,4,2,5,1 순으로 3개의 이미지를 뽑은 뒤, df에서 그 행을 인덱스를 이용해서 제거한다.

    print("!!!!!!!!!!!!!!!!!!!!!result_dict!!!!!!!!!!!!!!!!!")
    print(result_dict)
    print(type(result_dict))
    return result_dict
    # result_a_arr는 length가 5인 리스트. 요소는 DataFrame이다.
    # result_a_arr[0]은 [index, similarity3] [0, 0.14] ...
    # result_a_arr[1]은 [index, similarity4] [0, 0.14] ...
