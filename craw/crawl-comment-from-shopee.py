import re
import json
import requests
import pandas as pd

def get_cmt_from_shopee_url(url):

    r = re.search(r"i\.(\d+)\.(\d+)", url)
    shop_id, item_id = r[1], r[2]
    ratings_url = "https://shopee.vn/api/v2/item/get_ratings?filter=0&flag=1&itemid={item_id}&limit=50&offset={offset}&shopid={shop_id}&type={rating}"

    d = {"id": [], "comment": [], "label": []}

    for rate in range(1, 6):  # Chỉ lấy đánh giá 2, 3, 4, 5 sao
        offset = 0
        while True:
            try:
                data = requests.get(ratings_url.format(shop_id=shop_id, item_id=item_id, offset=offset, rating=rate)).json()
                for rating in data["data"]["ratings"]:
                    d["id"].append(rating["rating_star"])
                    d["comment"].append(rating["comment"])
                    d["label"].append(0 if rate >= 4 else 1) 
                offset += 50
            except TypeError:
                break
    return d

def save_to_txt(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for i in range(len(data['comment'])):
            id_str = f"train_{str(i).zfill(6)}"  # Tạo chuỗi ID theo định dạng train_xxxxxx
            f.write(f"{id_str}\n")
            f.write(f'"{data["comment"][i]}"\n')
            f.write(f"{data['label'][i]}\n\n")

# Sử dụng hàm get_cmt_from_shopee_url để lấy dữ liệu từ URL và lưu vào biến d
data = get_cmt_from_shopee_url("https://shopee.vn/%C3%81o-s%C6%A1-mi-tay-ng%E1%BA%AFn-nam-n%E1%BB%AF-form-r%E1%BB%99ng-s%C6%A1-mi-c%E1%BB%95-vest-unisex-tay-l%E1%BB%A1-ch%E1%BA%A5t-v%E1%BA%A3i-l%E1%BB%A5a-m%E1%BB%8Bn-ch%E1%BB%91ng-nh%C4%83n-i.310912000.5852968977")

# Sử dụng hàm save_to_txt để lưu dữ liệu vào file txt
save_to_txt(data, "shopee_data.crash")
