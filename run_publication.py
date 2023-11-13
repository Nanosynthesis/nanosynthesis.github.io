import os

import numpy
import pandas as pd

df = pd.read_excel("./nano_pubs.xlsx")

images = os.listdir("./images")

all_pubs = ""

for idx, i in enumerate(df.iterrows()):

    if numpy.isnan(df['序号'][idx]):
        continue

    # check images
    if f"{int(df['序号'][idx])}.bmp" in images:
        image_tag = f"""<div class="img_box"><img class="img-thumbnail img-rounded face_img" src="images/{int(df['序号'][idx])}.bmp"></div>"""
    else:
        image_tag = ""

    sample = f"""
    
        <div class="item_line">
            <div class='left_box'><span>{int(df['序号'][idx])}. </span><span class='pub_title'>{str(df['论文标题'][idx])}</span>,
                <span class='pub_author'>{str(df['作者'][idx]).replace("Hongyu Chen", "<b>Hongyu Chen</b>")}</span>,
                <span class='pub_publish'><i><u>{str(df['期刊'][idx])}</u></i></span>, <span
                        class='pub_year'>{int(df['年份'][idx])}</span>, <span class='pub_page'>{str(df['页码'][idx]).replace(" ", "")}</span>.<a href='{
    str(df['DOI'][idx]).strip().replace(" ", "") if "https://doi.org/" in str(df['DOI'][idx]).strip() else "https://doi.org/" + str(df['DOI'][idx]).strip().replace(" ", "")
    }'><span class='pub_doi'>link</span></a></div>
            {image_tag}
            <br/><br/><br/>
        </div>
        
    """
    print(sample)
    all_pubs += sample


with open("./pubs.html", mode='w', encoding='utf-8') as f:
    f.write(all_pubs)