import cv2
import numpy as np
from sklearn.cluster import KMeans
import colorsys
from numpy import random
from numpy.lib.index_tricks import index_exp


def centroid_histogram(clt):
    # 각 클러스터의 픽셀의 숫자를 기반으로 히스토그램 형식으로 색을 반환 함.

    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    # normalize the histogram, such that it sums to one
    hist = hist.astype("float")
    hist /= hist.sum()  # hist = hist/hist.sum()

    # return the histogram
    return hist


def plot_colors(hist, centroids):
    # initialize the bar chart representing the relative frequency of each of the colors
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0

    # loop over the percentage of each cluster and the color of each cluster
    for (percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50), color.astype("uint8").tolist(), -1)
        startX = endX

    # return the bar chart
    return bar


hsv_value_arr = []

# gather() : hsv값으로 변환하고 rgb와 hsv 값을 2차원 배열로 저장함.
def gather(rgb_ndarray):
    print(rgb_ndarray)

    for rgb in rgb_ndarray:
        # rgb = [72, 73, 46] ndarray임.
        rgb_value_arr = []

        # input
        (r, g, b) = rgb
        rgb_value_arr.append([r, g, b])
        # normalize
        (r, g, b) = (r / 255, g / 255, b / 255)
        # convert to hsv
        (h, s, v) = colorsys.rgb_to_hsv(r, g, b)
        # denormalize
        (h, s, v) = (int(h * 360), int(s * 100), int(v * 100))

        hsv_value_arr.append([h, s, v])
        print("HSV : ", h, s, v)


# 이미지와 컬러 히스토그램 보여줌.
def image_color_cluster(image_path, k=4):
    image = cv2.imread(image_path)
    # image의 shape을 찍어보면, height, width, channel 순으로 나옴
    # channel은 RGB를 말함

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # plt.imshow(image)

    # cv에서는 RGB가 아닌 BGR 순으로 나오기 때문에 순서를 RGB로 전환
    image = image.reshape((image.shape[0] * image.shape[1], 3))
    # shape의 0,1번째 즉, height와 width를 통합시킴

    clt = KMeans(n_clusters=k)  # 평균 알고리즘 KMeans
    clt.fit(image)

    hist = centroid_histogram(clt)

    # clt.cluster_centers_는 RGB값이 저장된 numpy.ndarray이다.
    # k=4인 경우 (4,3) 모양임.
    gather(np.int64(np.round(clt.cluster_centers_)))


def quadranted_choice(color_selected, adjective_quadrant):
    if adjective_quadrant == 1:  # 1사분면
        # S-채도값 조정
        color_selected[1] = random.randint(33, 51)
        # V-명도값 조정
        color_selected[2] = random.randint(66, 85)
        return color_selected

    if adjective_quadrant == 2:
        # S-채도값 조정
        color_selected[1] = random.randint(35, 70)
        # V-명도값 조정
        color_selected[2] = random.randint(86, 100)
        return color_selected

    if adjective_quadrant == 3:
        # S-채도값 조정
        color_selected[1] = random.randint(75, 100)
        # V-명도값 조정
        color_selected[2] = random.randint(73, 100)
        return color_selected

    if adjective_quadrant == 4:
        # S-채도값 조정
        color_selected[1] = random.randint(72, 98)
        # V-명도값 조정
        color_selected[2] = random.randint(55, 81)
        return color_selected

    else:
        print("1~4사이의 사분면을 넘겨주세요.")


def color_recommend(hsv_value_arr, adjective_quadrant):
    hsv_color_space = np.empty((0, 3), int)
    # hsv_value_arr = [[1,2,3],[4,5,6]...] 2차원 넘파이 배열.
    for hsv_value in hsv_value_arr:  # hsv값 np.array를 뽑아냄. ex) [210, 36, 78]
        # S-채도값이 20보다 작으면 뺌.
        # V-명도값이 30보다 작으면 뺌.
        if hsv_value[1] < 20:
            continue
        if hsv_value[2] < 30:
            continue

        # list에 [h,s,v]를 저장함.
        hsv_color_space = np.append(hsv_color_space, [hsv_value], axis=0)

    print("hsv_color_space")
    print(hsv_color_space)

    # 1사분면: 온화한, 말끔한, 자연적인, 편안한, 단정한, 우아한, 심플한 -> 채도 낮음, 명도 높음
    # 2사분면: 맑은, 신선한, 감성적인, 귀여운, 자유로운 -> 채도 높음, 명도 높음
    # 3사분면: 돋보이는, 개성적인, 실용적인, 모던한 -> 채도 높음, 명도 낮음
    # 4사분면: 고급스러운, 세련된, 클래식한, 차분한 -> 채도 낮음, 명도 낮음

    # 고른 형용사에 따라 그 형용사 이미지에 해당하는 S(채도)와 V(명도)값에 가까운 컬러를 3개 뽑음.
    # elif문으로 사분면 구분하기: adjective_quadrant

    index = random.randint(0, len(hsv_color_space), size=1)  # 1개의 hsv값을 추출함.
    color_selected = np.empty((0, 3), int)
    for _ in range(3):  # 선택된 값을 3번 넣음
        color_selected = np.append(color_selected, [hsv_color_space[0]], axis=0)

    color_selected = color_selected.tolist()

    # 추천된 hsv 컬러 3개 들어있는 list 반환함.
    return [quadranted_choice(one_color, adjective_quadrant) for one_color in color_selected]


def extract_colors(image_name_list, which_quadrant):
    # 매개변수(이미지 이름 list, 형용사의 사분면 상의 위치 )

    # 이미지 보여주고, rgv와 hsv 배열 보여줌.
    for image_name in image_name_list:
        image_color_cluster("Demo/data/" + image_name)

    # hsv_value_arr = []
    hsv_value_arr1 = np.array(hsv_value_arr)

    # hsv값 들어있는 2차원 배열과 형용사에 해당하는 사분면 값 넣어줌.
    hsv_selected_list = color_recommend(hsv_value_arr1, which_quadrant)  # n사분면

    # def hsv2rgb(h,s,v):
    #     return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

    rgb_selected_list = []
    for i in range(3):
        [h, s, v] = hsv_selected_list[i]
        (r, g, b) = colorsys.hsv_to_rgb(h / 360, s / 100, v / 100)
        rgb_selected_list.append([int(r * 255), int(g * 255), int(b * 255)])

    print("추천된 rgb 컬러 3개")
    print(rgb_selected_list)

    return rgb_selected_list
