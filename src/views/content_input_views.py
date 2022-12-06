import datetime as dt
from flask import Blueprint, request, Response

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
        file_list = request.files.getlist("file[]")
        print(len(file_list))
        for file in file_list:
            # 파일 확장자 저장
            # extension = file.filename.split(".")[-1]
            # today = dt.datetime.now()
            # mytime = today.strftime("%Y%m%d-%H-%M-%S")
            # filename = f"image-{mytime}"
            # save_to = f"Demo/data/{filename}.{extension}"

            filename = f"image-{file.filename}"
            save_to = f"Demo/data/{filename}"
            file.save(save_to)
    # return redirect(url_for('test_html', data=data))
    return Response(status=201)


# 2. 받아 놓은 이미지와 받은 텍스트를 KoBert로 분류하여
#   이미지와 텍스트를 매칭한 결과를 응답함.
# json(kobert 문장 분류 결과) 요청 받아서 json(이미지-텍스트 매칭) 응답 보냄.
@bp.route("/matching-result", methods=["POST"])
def matching_result():
    if request.method == "POST" and request.is_json == True:
        # 텍스트 덩어리를 받아서 변수에 저장함.
        # 매칭을 수행하는 함수에 텍스트 전달해서 매칭 결과 받아옴.
        kobert_result = request.get_json()
        # print(kobert_result_json)   #[{}, {}, ...]
        # print(type(kobert_result_json))    #list
        kobert_result_list = []
        for element in kobert_result:
            kobert_result_list.append([element["pred_data"], element["target"]])

        print(kobert_result_list)  # 이중 리스트[["당도가 어쩌구저쩌구", 0], [] , [] ...]

        matching_result = match_text2image(kobert_result_list)
        # print("matching_result")
        # print(type(matching_result))

    return "json(이미지-텍스트 매칭)"


# 3. 색상 추천
@bp.route("/recommended-colors", methods=["GET"])
def recommended_colors():
    result = extract_colors()
    return "rgb color tuple(126, 51, 203)"


# 4. 글꼴 추천
@bp.route("/recommended-font/<adjective>", methods=["GET"])
def recommended_font(adjective):
    result = extract_font()
    return "1234분면 중 어디인지 OR (title font, body font)"


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
