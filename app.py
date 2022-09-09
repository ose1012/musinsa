from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.rfofzeu.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta
url = 'https://www.musinsa.com/ranking/best'

response = requests.get(url)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    ul = soup.select_one('#goodsRankList')
    titles = ul.select('p.item_title > a')
    rank = ul.select_one('p.txt_num_rank').text[0:20].strip()
    image = ul.select('div.list_img > a > img')
    comment = ul.select('p.list_info > a')
    price = ul.select('div.article_info > p.price')
    sex = ul.select('div.icon_group > ul > li')
    url = ul.select('div.list_img > a')

    # for i, title in enumerate(titles):
    #     print(str(i + 1) + f"위", title.text, image[i]["data-original"], comment[i]["title"],
    #           price[i].text[10:38].strip().replace("\n", "").replace(" ", ""), sex[i]['title'], url[i]['href'])

    for i, title in enumerate(titles):
        titles[i] = title.text.strip()
        title = titles[i]
        rank = str(i + 1)
        musinsa_list = list(db.musinsa.find({}, {'_id': False}))
        count = len(musinsa_list) + 1
        doc = {
            'rank': rank,
            'title': title,
            'image': image[i]["data-original"],
            'comment': comment[i]["title"],
            'price': price[i].text[10:38].strip().replace("\n", "").replace(" ", ""),
            'sex': sex[i]["title"],
            'url': url[i]['href']
        }
        # print(rank, title, image[i]["data-original"], comment[i]["title"], price[i].text[10:38].strip(), sex[i]['title'])
        # db.musinsa.insert_one(doc)
else:
    print(response.status_code)


@app.route('/')
def home():
    return render_template('index.html')


# @app.route('/reply')
# def reply():
#     return render_template('reply.html')

# API 역할을 하는 부분
# @app.route('/musinsa', methods=['GET'])
# def show_stars():
#     mystar = list(db.musinsa.find({}, {'_id': 0}))
#     return jsonify({'dbdata': mystar, 'msg': 'list 연결되었습니다!'})
#
# @app.route('/musinsa/like', methods=['POST'])
# def like_star():
#     title_receive = request.form['title_give']					# 받아온 title값을 선언
#     target_star = db.mystar.find_one({'title':title_receive})		# like 누른 대상 선언
#     target_like_count = target_star['like']						# 대상의 현재 like수 선언
#     target_new_count = target_like_count + 1					# 현재 like 수 + 1
#     db.musinsa.update_one({'title': title_receive}, {'$set': {'like': target_new_count}}) # 업데이트 진행
#     return jsonify({'result': 'like', 'msg': 'like 연결되었습니다!'})
#
# @app.route('/musinsa/delete', methods=['POST'])
# def delete_star():
#     title_receive = request.form['title_give']
#     target_star = db.mystar.find_one({'title': title_receive})
#     target_like_count = target_star['like']
#     target_new_count = target_like_count - 1
#     db.musinsa.update_one({'title': title_receive}, {'$set': {'like': target_new_count}})
#     return jsonify({'msg': 'delete 연결되었습니다!'})

@app.route('/reply/<int:rank>')
def reply(rank):
    print(rank)
    return render_template("reply.html", rank=rank)


@app.route("/musinsa", methods=["GET"])
def musinsa_get():
    musinsa_list = list(db.musinsa.find({}, {'_id': False}))

    return jsonify({'musinsas': musinsa_list})


@app.route("/reply", methods=["POST"])
def reply_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    doc = {
        'name': name_receive,
        'comment': comment_receive
    }

    db.reply.insert_one(doc)

    return jsonify({'msg': '후기 작성 완료!'})


@app.route("/reply", methods=["GET"])
def reply_get():
    comment_list = list(db.reply.find({}, {'_id': False}))
    return jsonify({'reply': comment_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
