#!/usr/bin/env python3
"""Generate the two retrospective HTML pages (zh + en) from the extracted JSON files.
Layout mirrors publication.html: same head assets, same Bootstrap-grid top nav,
same bordered content container; content respects original Word order
(paragraphs with first-line indent + centered images)."""
import json
import os
import html

ROOT = "/Users/mellen/Desktop/nanosynthesis.github.io"

HEAD = """<!DOCTYPE html>
<html lang="{lang}">

<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <link rel="stylesheet" type="text/css" href="./css/reset-min.css" />
    <link rel="stylesheet" type="text/css" href="./css/page-index.css" />
    <link rel="stylesheet" href="./css/bootstrap.min.css">
    <style type="text/css">
    a {{
        text-decoration: none;
    }}
    a:hover {{
        color: #0090ff;
    }}
    .title {{
        text-align: center;
        padding-top: 10px;
        transition: .5s;
        border-right: 3px rgba(192, 192, 192, 0.17) solid;
    }}
    .title>a {{
        color: #575757;
        margin-top: 0px;
        font-weight: 700;
        font-size: 2.1rem;
        text-decoration: none;
        text-align: center;
        border-bottom: 4px solid rgba(234, 234, 234, 0.17);
        transition: .5s;
    }}
    .title:hover {{
        transition: 1s;
        background: rgba(255, 255, 255, 0.55);
    }}
    .button>i {{
        color: rgba(140, 140, 140, 0.68);
        font-size: 1.5rem;
    }}
    .back-top {{
        padding: 20px;
        border: 1px silver solid;
        position: fixed;
        bottom: 50px;
        right: 50px;
        float: right;
        cursor: pointer;
        background: #fff;
        z-index: 999;
    }}
    /* Retrospective body content */
    .retro-title {{
        font-size: 34px;
        background: rgb(237, 237, 237);
        border: 1px black dashed;
        margin-bottom: 40px;
        text-align: center;
        font-weight: 800;
        padding: 18px 0;
        color: #333;
    }}
    .retro-body {{
        {body_font}
        font-size: 1.8rem;
        line-height: 2;
        color: #222;
        {text_align}
    }}
    .retro-body p {{
        margin: 0 0 1.2em 0;
        text-indent: 2em;
    }}
    .retro-body p.no-indent {{
        text-indent: 0;
    }}
    .retro-body .img_box {{
        width: 680px;
        max-width: 100%;
        margin: 24px auto 30px auto;
        text-align: center;
    }}
    .retro-body .img_box img {{
        width: 100%;
        height: auto;
        display: block;
        border: 1px solid #e0e0e0;
        border-radius: 4px;
        padding: 4px;
        background: #fff;
    }}
    .lang-switch {{
        text-align: center;
        margin-bottom: 30px;
        font-size: 1.6rem;
    }}
    .lang-switch a {{
        color: #4289ff;
        font-weight: 700;
        margin: 0 12px;
        border-bottom: 1px dashed #4289ff;
    }}
    @media (max-width: 768px) {{
        .retro-body {{
            font-size: 1.6rem;
        }}
        .retro-body .img_box {{
            width: 100%;
        }}
    }}
    </style>
</head>

<body>
    <div>
        <a href="#">
            <span class="back-top">返回顶部</span>
        </a>
    </div>

    <div class="container-fluid" style="padding-top: 80px">
        <div class="row">
            <div class="col-md-1"></div>
            <div class="col-md-10">
                <div class="row" style="margin-top: -30px">
                    <div class="col-md-1"></div>
                    <div class="col-md-1" style="margin-top: 30px">
                        <a href="#" target="_blank" title="The Nanosynthesis Consortium">
                            <img width=300 src="./album/nano.jpg" alt="logo" style="margin-top: -60px !important;" />
                        </a>
                    </div>
                    <div class="col-md-2"></div>
                    <div class="col-sm-1 title" style="border-left: 3px rgba(192, 192, 192, 0.17) solid;">
                        <a class="button" href="index.html">团队首页 <br> <i>Home</i></a>
                    </div>
                    <div class="col-md-1 title"><a class="button" href="chy.html">成员名单 <br> <i>Members</i></a></div>
                    <div class="col-md-1 title"><a class="button" href="publication.html" target="_blank">学术成果 <br>
                            <i>Publication</i></a></div>
                    <div class="col-md-1 title"><a class="button" href="album.html">相册 <br> <i>Album</i></a></div>
                    <div class="col-md-1 title"><a class="button" href="contact.html">联系方式 <br> <i>Contact</i></a></div>
                </div>
            </div>
            <div class="col-md-1"></div>
        </div>
    </div>

    <div class="container" style="margin-top: 50px; border-right: 2px solid silver; border-left: 2px silver solid; box-shadow: #9d9d9d 1px 1px 5px 1px; margin-bottom: 50px; padding: 60px 100px;">
        <div class="lang-switch">
            {lang_switch}
        </div>
        <div class="retro-title">{heading}</div>
        <div class="retro-body">
"""

TAIL = """        </div>
    </div>
</body>

</html>
"""


def render_items(items):
    out = []
    for it in items:
        if it["type"] == "para":
            text = html.escape(it["text"])
            text = text.replace("\n", "<br>")
            out.append(f'            <p>{text}</p>')
        else:  # img
            src = it["src"]
            out.append(
                f'            <div class="img_box"><img class="img-thumbnail img-rounded" src="{src}" alt="figure"></div>'
            )
    return "\n".join(out)


def main():
    config = {
        "zh": {
            "title": "建组二十年回顾",
            "lang": "zh-CN",
            "heading": "建组二十年回顾",
            "body_font": 'font-family: "Songti SC", "STSong", "SimSun", "Source Han Serif SC", "Noto Serif CJK SC", serif;',
            "text_align": "text-align: justify;",
            "lang_switch": '<a href="20years-retrospective-en.html">English Version</a>',
        },
        "en": {
            "title": "20-Year Group Retrospective",
            "lang": "en",
            "heading": "20-Year Group Retrospective",
            "body_font": 'font-family: Georgia, "Times New Roman", "Source Han Serif", serif;',
            "text_align": "text-align: left;",
            "lang_switch": '<a href="20years-retrospective-zh.html">中文版</a>',
        },
    }

    for lang, cfg in config.items():
        json_path = os.path.join(ROOT, f"20years/extract_{lang}.json")
        with open(json_path, "r", encoding="utf-8") as f:
            items = json.load(f)
        body = render_items(items)
        html_doc = (
            HEAD.format(**cfg)
            + body
            + TAIL
        )
        out_path = os.path.join(ROOT, f"20years-retrospective-{lang}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html_doc)
        print(f"Wrote {out_path} ({len(items)} items)")


if __name__ == "__main__":
    main()
