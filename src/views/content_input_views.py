from flask import Blueprint, request, Response
import json
import base64

from router.matching_text2image import match_text2image
from router.recommended_colors import extract_colors
from router.recommended_font import extract_font

bp = Blueprint("main", __name__, url_prefix="/")


# 1. 이미지 여러장 받아서 저장함.
@bp.route("/upload", methods=["POST"])
def upload_file():
    # request의 body에 있는 사진을 Demo.data 폴더에 저장함.
    if request.method == "POST":
        # 파일(이미지) 리스트 받음
        file_list = request.files.getlist("files[]")
        print(len(file_list))

        for file in file_list:
            filename = f"image-{file.filename}"
            save_to = f"Demo/data/{filename}"
            file.save(save_to)

        kobert_result = request.form.get("data")  # .get_json()
        kobert_result = eval(kobert_result)
        print(type(kobert_result))
        print(kobert_result)
        final_result = matching_result(kobert_result)
    # return Response(status=201)
    return Response(final_result)


# 2. 받아 놓은 이미지와 KoBert로 분류한 텍스트를 매칭한 결과를 응답함.
# json(kobert 문장 분류 결과) 요청 받아서 json(이미지-텍스트 매칭) 응답 보냄.
def matching_result(kobert_result):
    print(kobert_result)
    print(type(kobert_result))
    # kobert_result   =[{}, {}, ...] , type=list
    print(kobert_result.keys())
    print(type(kobert_result.keys()))

    kobert_result_dict = {1: [], 2: [], 3: []}
    for key in kobert_result:
        dict_key = kobert_result[key]["target"]
        kobert_result_dict[dict_key].append(kobert_result[key]["pred_data"])

    print("!!!!!!여기가!!!!!!!!!!!!!!!kobert-result-dict")
    print(kobert_result_dict)

    # 매칭을 수행하는 함수에 텍스트 전달해서 매칭 결과 받아옴.
    matching_result = match_text2image(kobert_result_dict)

    # 추천된 5장의 이미지의 이름을 json 파일에 저장함(뒤에 글꼴과 색상 추천에서 쓰기 위함)
    with open("./selected_image.json", "w") as outfile:
        image = {}
        image["image_name"] = []
        for key in matching_result["image"]:
            image["image_name"].append(matching_result["image"][key])
        json.dump(image, outfile)

    # 이미지 파일을 인코딩해서 matchig_result 딕셔너리에 더함
    for key in matching_result["image"].keys():
        with open("Demo/data/" + matching_result["image"][key], "rb") as image_file:
            image_binary = image_file.read()
            encoded_string = base64.b64encode(image_binary)
            matching_result["image"][key] = encoded_string.decode()

    return json.dumps(matching_result)
    # matching_result = {"image": {"close_shot": , "farm_landscape": }, "text": {"taste": , }}


# 3. 글꼴과 색상 추천
@bp.route("/recommended-design", methods=["GET"])
def recommended_design():
    # 형용사에 맞는 사분면에 따라 title font, body font 반환함.
    adjective = request.args.get("adj")
    quadrant, title_font, body_font = extract_font(adjective)

    with open("./selected_image.json", "r") as file:
        data = json.load(file)
        selected_image_list = data["image_name"]

    # (뽑힌 이미지 이름 list, 해당하는 사분면(quadrant))
    color_result = extract_colors(selected_image_list, quadrant)

    design_result = {}
    design_result["title_font"] = title_font
    design_result["body_font"] = body_font
    design_result["color"] = color_result
    design_result["adj"] = adjective
    design_result["quadrant"] = quadrant
    return json.dumps(design_result)
    # return "title font, body font와 rgb color list[126, 51, 203] * 3"


"""
@app.route("/test/{file}/{data}")
def test_html():
    return render_template("test.html")
    


@app.route("/")
def index_html():  # 루트에서는 index.html을 response로 보냄
    return render_template("index.html")
    


@app.errorhandler(404)
def not_found(e):  # SPA 이므로 404 에러는 index.html을 보냄으로써 해결한다.
    return index_html()



@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"), "favicon.ico", mimetype="image/vnd.microsoft.icon"
    )
    """
