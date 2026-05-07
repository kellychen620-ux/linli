import json, urllib.request
from collections import defaultdict

url = "https://shequ.980512.com/qun/api/nwn/base_goods_list.htm?mid=6258355454&page=1&size=5000"
data = json.loads(urllib.request.urlopen(url).read())
items = data['data']['dataList']
hot = [i for i in items if i.get('sale_qty', 0) >= 1000]
hot.sort(key=lambda x: x['sale_qty'], reverse=True)

cats = {5091:'应季鲜果',5094:'绿色蛋品',5090:'新鲜蔬菜',5087:'早餐烘焙',5089:'绿植花卉',
        5101:'酒水乳品',5085:'肉禽冻品',5084:'休闲食品',5086:'水产海鲜',5083:'滋补食养',
        5093:'营养保健',5082:'粮油调味',5081:'美妆护肤',5077:'居家百货',5092:'文娱用品',
        5121:'快递包邮',5263:'清仓福利'}

groups = defaultdict(list)
for i in hot:
    groups[i.get('cat_id', 0)].append(i)

sections = ''
for cat_id, goods in sorted(groups.items(), key=lambda x: -sum(g['sale_qty'] for g in x[1])):
    cat_name = cats.get(cat_id, f'其他({cat_id})')
    rows = ''
    for g in goods:
        price = g.get('price', '--')
        dp = g.get('discount_price', '')
        if dp and dp != price:
            price_html = f'<span style="color:#e44;font-weight:bold">¥{price}</span> <span style="text-decoration:line-through;color:#999;font-size:12px">¥{dp}</span>'
        else:
            price_html = f'<span style="color:#e44;font-weight:bold">¥{price}</span>'
        goods_url = f'https://shequ.980512.com/qun/goods/detail?mid=6258355454&goods_id={g["goods_id"]}'
        rows += f'<tr><td><img src="{g["image_url"]}" width="70" height="70" style="object-fit:cover;border-radius:4px"></td><td><a href="{goods_url}" target="_blank" style="color:#2d6a4f;text-decoration:none">{g["goods_name"]}</a></td><td>{price_html}</td><td style="text-align:right;font-weight:bold;color:#e44">{g["sale_qty"]:,}</td></tr>'
    sections += f'<div class="section"><h3>🏷 {cat_name} <span class="badge">{len(goods)}件</span></h3><table><tr><th>图片</th><th>商品名称</th><th>价格</th><th>销量</th></tr>{rows}</table></div>'

from datetime import datetime, timezone, timedelta
updated = datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M')

html = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>林里生活 · 热销榜</title>
<style>
body{{font-family:sans-serif;padding:12px;background:#f5f5f5;margin:0}}
h2{{color:#2d6a4f;border-bottom:3px solid #2d6a4f;padding-bottom:8px;font-size:18px}}
.updated{{color:#999;font-size:12px;margin-top:-8px;margin-bottom:16px}}
.section{{background:#fff;border-radius:8px;padding:12px;margin-bottom:16px;box-shadow:0 1px 4px rgba(0,0,0,.08)}}
h3{{margin:0 0 10px;color:#2d6a4f;font-size:15px}}
.badge{{background:#e8f5e9;color:#2d6a4f;font-size:11px;padding:2px 7px;border-radius:10px;font-weight:normal}}
table{{border-collapse:collapse;width:100%}}
th{{background:#2d6a4f;color:#fff;padding:7px 10px;text-align:left;font-size:12px}}
td{{padding:7px 10px;border-bottom:1px solid #f0f0f0;vertical-align:middle;font-size:12px}}
</style></head><body>
<h2>林里生活 · 销量超1000商品（{len(hot)}件）</h2>
<p class="updated">更新时间：{updated} UTC+8</p>
{sections}
</body></html>'''

open('index.html', 'w').write(html)
print(f'生成完成，共 {len(hot)} 件商品')
