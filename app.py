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
            'num': count,
            'dune': 0,
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


@app.route("/musinsa", methods=["GET"])
def musinsa_get():
    musinsa_list = list(db.musinsa.find({}, {'_id': False}))

    return jsonify({'musinsas': musinsa_list})


@app.route('/reply/view?rank=<int:rank>')
def reply(rank):
    print(rank)
    return render_template("reply.html", rank=rank)

# @app.route("/reply", methods=['GET', 'POST'])
# def show_comment():
#     rank = int(request.args["rank"])
#
#     # comment_list = list(db.reply.find({'rank': rank}, {'_id': False}))
#     return render_template('reply.html', rank=rank)

@app.route("/reply", methods=["POST"])
def reply_post(rank):
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    doc = {
        'rank': int(rank),
        'name': name_receive,
        'comment': comment_receive
    }

    db.reply.insert_one(doc)

    return jsonify({'msg': '후기 작성 완료!'})


@app.route("/reply", methods=["GET"])
def show_comment():
    rank = int(request.args["rank"])

    comment_list = list(db.reply.find({'rank': rank}, {'_id': False}))
    return jsonify({'reply': comment_list})


@app.route("/musinsa/done", methods=["POST"])
def musinsa_done():
    num_receive = request.form['num_give']
    db.musinsa.update_one({'num': int(num_receive)}, {'$set': {'dune': 1}})
    return jsonify({'msg': '찜하기 완료!'})


@app.route('/musinsa/delete', methods=['POST'])
def delete_star():
    num_receive = request.form['num_give']
    db.musinsa.update_one({'num': int(num_receive)}, {'$set': {'dune': 0}})
    return jsonify({'msg': '찜하기 취소!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
