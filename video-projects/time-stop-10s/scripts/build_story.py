#!/usr/bin/env python3
"""Build the 6m18s Vietnamese time-stop film storyboard for the native H2 Canvas renderer.

This is original source data, not a paid-AI video request. It writes H2's native
story/shots.json format, config.json, and a readable 01-PHIM production script.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

FPS = 30
SHOT_SECONDS = 4.5
WIDTH, HEIGHT = 1920, 1080

def actor(who, x, pose="stand", face="neutral", **kw):
    item = {"who": who, "x": x, "pose": pose, "face": face, "h": kw.pop("h", 0.44)}
    item.update(kw)
    return item

def camera(x0=.5, y0=.54, z0=1.02, x1=None, y1=None, z1=1.10):
    return {"from":[x0,y0,z0],"to":[x0 if x1 is None else x1,y0 if y1 is None else y1,z1],"at":0.0,"dur":SHOT_SECONDS,"ease":"sine"}

def cue(name, at=.25, gain=-7):
    return {"name":name,"at":at,"gain":gain}

SHOTS = []
def add(location, scene, caption, actors=None, set_args=None, cam=None, *,
        freeze=False, timer=None, fx=None, lights=None, sfx=None, text_pos="top",
        transition=None, vignette=.56):
    SHOTS.append({
        "location":location,"scene":scene,"caption":caption,"actors":actors or [],
        "set_args":set_args or {},"cam":cam or camera(),"freeze":freeze,"timer":timer,
        "fx":fx or [],"lights":lights or [],"sfx":sfx or [],"text_pos":text_pos,
        "transition":transition,"vignette":vignette,
    })

# ACT 01 — A normal day, until the impossible offer appears.
add("bedroom","Toàn cảnh phòng ngủ nhỏ lúc bình minh; rèm cửa, bàn học và đồng hồ báo thức cùng hiện trong một khung rộng.","Ngày hôm ấy bắt đầu bình thường như mọi ngày.",
    [actor("hoodie",.34,"sit","sad",hold="phone")],{"clock":"06:10","lamp":False,"laptop":True,"sky":"dawn","stage":True},
    camera(.48,.53,1.0,.55,.48,1.08),sfx=[cue("phone_ring"),cue("tick",1.5)])
add("bedroom","Cận đồng hồ báo thức; kim giây chạy, ánh nắng sớm lướt qua mặt kính.","Thời gian chưa bao giờ chờ ai.",
    [actor("hoodie",.30,"sit","sad",hold="phone",h=.38)],{"clock":"06:10","lamp":False,"sky":"dawn","stage":True},
    camera(.62,.30,1.32,.63,.30,1.50),sfx=[cue("tick"),cue("whoosh_tiny",2.2)])
add("bedroom","Góc qua vai nhìn bài kiểm tra còn dang dở; bút nằm cạnh vở, đèn bàn vẫn sáng.","Bài kiểm tra ngày mai vẫn còn nguyên trên bàn.",
    [actor("hoodie",.36,"type","sad",hold="book")],{"clock":"23:48","lamp":True,"laptop":False,"sky":"night","stage":True},
    camera(.42,.57,1.08,.48,.55,1.18),lights=[{"x":.72,"y":.43,"r":.22,"color":"#ffc36f","a":.28}])
add("classroom","Toàn cảnh lớp học; bảng đầy công thức, những dãy bàn chạy sâu vào hậu cảnh.","Sáng hôm sau, cậu gần như ngủ gục trong lớp.",
    [actor("hoodie",.36,"sit","sad"),actor("friend",.73,"type","neutral",h=.42)],{"sky":"day","board":"KIỂM TRA 15 PHÚT","desks":[.25,.48,.72]},
    camera(.50,.50,1.0,.47,.48,1.08),sfx=[cue("type_key",1.0)])
add("lockers","Hành lang trường học; tủ đồ tạo các lớp chiều sâu, học sinh đi qua thành những bóng nhỏ.","Ai cũng có vẻ đang vội đến một nơi nào đó.",
    [actor("hoodie",.34,"walk","sad",walk={"to":.48,"dur":3.5,"speed":.8}),actor("friend2",.78,"wave","grin")],
    {"board":False},camera(.40,.50,1.0,.57,.50,1.13))
add("kitchen","Căn bếp ấm; mẹ đặt hộp đồ ăn cạnh cặp sách, hơi nước bốc lên dưới đèn vàng.","Mẹ vẫn chuẩn bị bữa sáng như mọi ngày.",
    [actor("mom",.62,"point","grin"),actor("hoodie",.30,"stand","neutral",hold="bag")],{"sky":"dawn","lamp":True},
    camera(.50,.52,1.0,.54,.49,1.08),lights=[{"x":.67,"y":.28,"r":.20,"color":"#ffc36f","a":.34}])
add("phone","Cận điện thoại trên bàn; một thông báo lạ phủ lên màn hình khóa.","Một quảng cáo kỳ lạ xuất hiện trên điện thoại.",
    [actor("hoodie",.68,"phone","neutral",hold="phone",h=.36)],{},camera(.70,.45,1.22,.70,.43,1.46),sfx=[cue("phone_ring"),cue("ui_click",1.0)])
add("city","Toàn cảnh thành phố buổi sáng; các tòa nhà, ban công và cửa sổ xếp thành nhiều lớp.","Ngoài kia, hàng triệu chiếc đồng hồ vẫn đang chạy.",
    [actor("hoodie",.20,"walk","neutral",walk={"to":.78,"dur":4.0,"speed":.9},h=.35)],{"time":"day","birds":True,"lamps":[]},
    camera(.48,.48,1.0,.62,.47,1.06))
add("court","Sân trường nhìn chéo; bảng rổ, vạch sân và ghế dài đặt theo phối cảnh.","Tiếng bóng nảy vang lên từ sân trường.",
    [actor("friend",.72,"cheer","grin",hold="ball"),actor("hoodie",.30,"stand","neutral")],{"hoopX":.78,"benchX":.23},
    camera(.53,.50,1.0,.60,.49,1.10),sfx=[cue("impact_light",.6)])
add("mirror","Cận gương trong nhà vệ sinh; nhân vật nhìn thẳng vào chính mình, ánh đèn lạnh.","Cậu chỉ muốn có thêm một chút thời gian.",
    [actor("hoodie",.50,"headhold","sad")],{"mirrorX":.54},camera(.52,.43,1.16,.52,.43,1.28))
add("street","Góc rộng đầu phố; xe cộ lướt qua, đèn giao thông đổi màu, người đi bộ qua vạch.","Cậu không biết rằng một ngày nữa sẽ thay đổi tất cả.",
    [actor("hoodie",.24,"walk","neutral",walk={"to":.55,"dur":3.8,"speed":.9})],{"busstop":False,"rain":False,"lampX":.8},
    camera(.45,.50,1.0,.60,.48,1.08))
add("black","Màn đen mở ra với một vòng tròn mảnh màu xanh băng và một con số duy nhất.","Nếu có thể dừng thời gian trong đúng mười giây thì sao?",
    [actor("hoodie",.50,"stand","neutral",h=.40)],{},camera(.50,.50,1.0,.50,.50,1.0),
    fx=[{"kind":"pulse","at":.2,"dur":4.0,"color":"#7fd8ff","a":.18}],sfx=[cue("slowmo_ring",.2)],
    transition={"type":"dip","dur":.65},text_pos="bottom")

# ACT 02 — The first accidental freeze.
add("kitchen","Cận chiếc cốc trên mặt bàn; bàn tay nhân vật vừa chạm vào quai cốc.","Mọi chuyện bắt đầu từ một chiếc cốc sắp rơi.",
    [actor("hoodie",.47,"carry","neutral",hold="cup",h=.46)],{"sky":"night","lamp":True},camera(.58,.62,1.18,.58,.58,1.38),sfx=[cue("impact_light",3.1)])
add("kitchen","Chiếc cốc nghiêng ở mép bàn; nhân vật giật mình đưa tay theo phản xạ.","Chiếc cốc trượt khỏi mép bàn.",
    [actor("hoodie",.39,"cheer","sad",h=.46)],{"sky":"night","lamp":True},camera(.55,.57,1.28,.52,.54,1.48),
    fx=[{"kind":"speed","at":.1,"dur":1.0,"x":.6,"y":.6}],sfx=[cue("whoosh_fast",.1)])
add("kitchen","Chiếc cốc dừng giữa không trung; nước và giọt bắn lơ lửng trong ánh đèn vàng.","Rồi cả căn bếp im bặt.",
    [actor("hoodie",.38,"guard","sad")],{"sky":"night","lamp":True},camera(.54,.52,1.32,.52,.50,1.42),
    freeze=True,timer=10,lights=[{"x":.52,"y":.54,"r":.33,"color":"#8bd8ff","a":.28}],sfx=[cue("slowmo_ring",.1)])
add("kitchen","Góc rộng; mẹ đứng yên phía sau, giọt nước đứng trên không, rèm cửa không còn lay.","Không một ai khác có thể cử động.",
    [actor("mom",.72,"point","neutral"),actor("hoodie",.35,"stand","neutral")],{"sky":"night","lamp":True},
    camera(.50,.48,1.0,.53,.47,1.08),freeze=True,timer=9)
add("kitchen","Nhân vật bước qua những giọt nước đông cứng; camera thấp ngang mặt bàn.","Chỉ có cậu vẫn bước được giữa thế giới đứng yên.",
    [actor("hoodie",.32,"walk","neutral",walk={"to":.70,"dur":3.7,"speed":1.2})],{"sky":"night","lamp":True},
    camera(.34,.66,1.05,.66,.58,1.25),freeze=True,timer=8,fx=[{"kind":"dust","at":.1,"dur":4.0,"n":22}])
add("kitchen","Cận đồng hồ trên cổ tay; vòng sáng xanh hiện rõ mười vạch nhỏ.","Trên cổ tay hiện lên con số chín giây.",
    [actor("hoodie",.53,"headhold","neutral",h=.42)],{"sky":"night","lamp":True},camera(.55,.49,1.34,.55,.49,1.52),
    freeze=True,timer=7,sfx=[cue("tick",.2),cue("tick",2.0)])
add("kitchen","Bàn tay chạm vào cốc giữa không trung; nhân vật đỡ lấy đáy cốc.","Cậu kịp giữ chiếc cốc trước khi nó vỡ.",
    [actor("hoodie",.48,"carry","grin",hold="cup")],{"sky":"night","lamp":True},camera(.53,.59,1.2,.57,.55,1.32),
    freeze=True,timer=6,sfx=[cue("ding_soft",2.6)])
add("kitchen","Nhân vật xoay người nhìn mẹ vẫn đứng yên cạnh bàn; ánh xanh phủ nhẹ lên gương mặt.","Nhưng mẹ vẫn bất động như một bức tượng.",
    [actor("hoodie",.35,"headhold","sad"),actor("mom",.76,"stand","neutral")],{"sky":"night","lamp":True},
    camera(.50,.50,1.0,.50,.50,1.08),freeze=True,timer=5)
add("kitchen","Cận vòng sáng; những vạch thời gian cuối cùng co lại.","Ba giây cuối cùng trôi nhanh hơn cậu tưởng.",
    [actor("hoodie",.50,"facepalm","sad")],{"sky":"night","lamp":True},camera(.53,.46,1.25,.53,.46,1.42),
    freeze=True,timer=3,sfx=[cue("tick",.2),cue("riser_2s",1.2)])
add("kitchen","Chiếc cốc trở lại mặt bàn; nước rơi xuống khăn; mọi thứ bắt đầu chuyển động.","Mười giây kết thúc. Thế giới tiếp tục chạy.",
    [actor("hoodie",.42,"stand","neutral"),actor("mom",.74,"talk","grin")],{"sky":"night","lamp":True},camera(.50,.52,1.0,.52,.50,1.08),
    fx=[{"kind":"flash","at":.05,"dur":.25,"a":.28}],sfx=[cue("whoosh_reverse",.1)])
add("face","Cận gương mặt nhân vật; đôi mắt mở lớn, ánh phản chiếu xanh dần biến mất.","Cậu vừa chứng kiến điều không thể giải thích.",
    [actor("hoodie",.50,"stand","sad",h=.60)],{},camera(.5,.46,1.25,.5,.46,1.42),sfx=[cue("heartbeat",.2)])
add("bedroom","Nhân vật đặt chiếc đồng hồ lên bàn; màn hình vẫn sáng với vòng tròn mười giây.","Và cậu biết mình có thể làm điều đó lần nữa.",
    [actor("hoodie",.45,"headhold","neutral",hold="phone")],{"clock":"00:01","lamp":True,"sky":"night","stage":True},
    camera(.51,.52,1.05,.54,.50,1.18),sfx=[cue("ting_idea",2.2)])

# ACT 03 — Learning the rules of a ten-second world.
add("classroom","Đồng hồ treo tường trên bảng lớp; kim giây lướt qua vạch số mười hai.","Cậu bắt đầu thử giới hạn của năng lực.",
    [actor("hoodie",.34,"headhold","neutral")],{"sky":"day","board":"THỜI GIAN = 10 GIÂY","desks":[.24,.5,.76]},camera(.62,.25,1.25,.62,.25,1.42))
add("court","Quả bóng rổ lăn khỏi tay bạn, trượt qua vạch biên hướng về phía đường xe chạy.","Một quả bóng lăn khỏi sân trường.",
    [actor("friend",.40,"guard","sad",hold="ball"),actor("hoodie",.78,"point","neutral")],{"hoopX":.18,"benchX":.75},
    camera(.50,.55,1.02,.60,.55,1.16),fx=[{"kind":"speed","at":.2,"dur":1.4,"dir":1}],sfx=[cue("impact_light",.2)])
add("court","Cận chân quả bóng và vạch biên; nhân vật nhìn theo, chuẩn bị chạy.","Cậu bấm nút đúng lúc.",
    [actor("hoodie",.22,"guard","neutral")],{"hoopX":.18,"benchX":.75},camera(.30,.73,1.25,.49,.70,1.43),sfx=[cue("ui_click",.3)])
add("court","Bóng đứng yên giữa cú nảy; bụi phấn và vài giọt nước treo dưới ánh nắng.","Cả sân bóng đông cứng trong một nhịp.",
    [actor("hoodie",.30,"guard","grin"),actor("friend",.72,"cheer","neutral")],{"hoopX":.18,"benchX":.75},
    camera(.5,.52,1.0,.55,.50,1.08),freeze=True,timer=10)
add("street","Nhân vật chạy từ mép sân ra gần quả bóng; hàng xe và đèn đường đứng yên phía sau.","Cậu chạy qua con đường không còn tiếng động.",
    [actor("hoodie",.20,"guard","neutral",run={"to":.70,"dur":3.8,"speed":1.8})],{"busstop":False,"rain":False,"lampX":.85},
    camera(.24,.57,1.0,.65,.54,1.18),freeze=True,timer=8,fx=[{"kind":"speed","at":.1,"dur":2.5,"dir":1}],sfx=[cue("whoosh_fast",.4)])
add("street","Nhân vật cúi người nhặt quả bóng sát bánh xe đang đứng yên.","Cậu chỉ cần vài bước để cứu quả bóng.",
    [actor("hoodie",.53,"crouch","neutral",hold="ball")],{"busstop":False,"rain":False,"lampX":.85},
    camera(.56,.67,1.3,.56,.62,1.48),freeze=True,timer=6)
add("court","Cận đồng hồ đếm ngược; ánh xanh nhấp nháy trên gương mặt nhân vật.","Sáu giây. Cậu phải quay lại ngay.",
    [actor("hoodie",.40,"guard","sad",hold="ball")],{"hoopX":.18,"benchX":.75},camera(.4,.43,1.26,.4,.43,1.5),
    freeze=True,timer=6,sfx=[cue("tick",.2),cue("tick",1.3)])
add("court","Nhân vật đặt bóng trở lại tay bạn; hai người ở hai phía khung hình.","Cậu trả quả bóng về đúng chỗ.",
    [actor("hoodie",.35,"carry","grin",hold="ball"),actor("friend",.68,"stand","neutral")],{"hoopX":.18,"benchX":.75},
    camera(.50,.52,1.0,.56,.52,1.12),freeze=True,timer=4)
add("court","Bóng trở lại tay người bạn khi thời gian chạy tiếp; bạn ngạc nhiên nhìn xuống tay.","Khi thời gian chạy lại, chẳng ai biết chuyện vừa xảy ra.",
    [actor("friend",.70,"headhold","neutral",hold="ball"),actor("hoodie",.30,"relaxed","grin")],{"hoopX":.18,"benchX":.75},
    camera(.53,.50,1.0,.49,.50,1.08),fx=[{"kind":"flash","at":.05,"dur":.22,"a":.22}],sfx=[cue("whoosh_reverse",.1)])
add("stairs","Nhân vật đi lên cầu thang, nhìn đồng hồ trên cổ tay; bóng đổ dài theo bậc thang.","Cậu ghi nhớ một điều: mười giây là giới hạn.",
    [actor("hoodie",.35,"walk","neutral",walk={"to":.72,"dur":3.8,"speed":.8})],{"top":True,"topColor":"#dca86d"},
    camera(.35,.62,1.05,.60,.52,1.16))
add("phone","Cận màn hình ứng dụng; một vòng tròn mười vạch hiện quanh biểu tượng đồng hồ.","Không thể kéo dài. Không thể tạm dừng bộ đếm.",
    [actor("hoodie",.70,"phone","neutral",hold="phone",h=.38)],{},camera(.68,.47,1.22,.68,.44,1.5),sfx=[cue("ui_click",.6)])
add("bedroom","Nhân vật mở cuốn sổ, viết ba chữ: DỪNG — DI CHUYỂN — TRỞ LẠI.","Cậu bắt đầu viết ra những quy tắc đầu tiên.",
    [actor("hoodie",.46,"type","neutral",hold="book")],{"clock":"22:10","lamp":True,"sky":"night","stage":True},
    camera(.48,.57,1.08,.50,.53,1.18),sfx=[cue("typing_2s",.5)])

# ACT 04 — Using the power to help, not to cheat.
add("lockers","Hành lang đông người; một chồng sách trượt khỏi tay học sinh nhỏ tuổi.","Lần này, cậu dùng năng lực để giúp người khác.",
    [actor("kid",.68,"knees","sad",h=.38),actor("hoodie",.26,"guard","neutral")],{"board":False},
    camera(.51,.52,1.0,.57,.51,1.12),fx=[{"kind":"speed","at":.2,"dur":1.0}],sfx=[cue("impact_light",1.0)])
add("lockers","Những cuốn sách lơ lửng giữa không trung, hành lang bất động.","Mười giây nữa lại mở ra.",
    [actor("hoodie",.30,"stand","neutral"),actor("kid",.70,"knees","neutral")],{"board":False},
    camera(.50,.48,1.0,.52,.48,1.08),freeze=True,timer=10)
add("lockers","Nhân vật chạy dọc hành lang, né những cuốn sách đang treo giữa không trung.","Cậu phải hành động trước khi bộ đếm chạm số không.",
    [actor("hoodie",.20,"guard","neutral",run={"to":.74,"dur":3.8,"speed":1.7})],{"board":False},
    camera(.24,.55,1.0,.64,.50,1.20),freeze=True,timer=8,fx=[{"kind":"speed","at":.2,"dur":2.6}],sfx=[cue("whoosh_fast",.2)])
add("lockers","Bàn tay đặt chồng sách trở lại trên cánh tay đứa trẻ.","Cậu giữ lấy chồng sách trước khi rơi xuống.",
    [actor("hoodie",.55,"kneel","grin"),actor("kid",.70,"stand","neutral")],{"board":False},
    camera(.59,.68,1.28,.59,.62,1.42),freeze=True,timer=5)
add("stairs","Đứa trẻ đứng an toàn ở cuối hành lang; nhân vật lùi lại khỏi cầu thang.","Còn ba giây. Cậu phải rút lui.",
    [actor("hoodie",.28,"guard","sad"),actor("kid",.70,"stand","neutral")],{"top":True},
    camera(.50,.50,1.0,.54,.50,1.08),freeze=True,timer=3,sfx=[cue("tick",.2)])
add("lockers","Sách nằm yên trong tay đứa trẻ; bạn bè nhìn nhau khi thời gian trở lại.","Mọi người chỉ nghĩ đứa trẻ đã may mắn.",
    [actor("kid",.68,"carry","grin",hold="book"),actor("hoodie",.30,"relaxed","neutral")],{"board":False},
    camera(.50,.50,1.0,.53,.49,1.08),fx=[{"kind":"flash","at":.05,"dur":.22,"a":.18}],sfx=[cue("whoosh_reverse",.1)])
add("court","Bạn bè chơi bóng; nhân vật chạy theo đường biên, tiếng cười trở lại.","Cậu bắt đầu tin rằng mười giây có thể tạo khác biệt.",
    [actor("friend",.66,"cheer","grin"),actor("hoodie",.28,"wave","grin")],{"hoopX":.72,"benchX":.2},
    camera(.5,.48,1.0,.56,.45,1.12),sfx=[cue("crowd_cheer",.8)])
add("mirror","Nhân vật nhìn vào gương; vòng sáng xanh tắt dần trên cổ tay.","Nhưng cậu cũng bắt đầu lệ thuộc vào nó.",
    [actor("hoodie",.52,"headhold","sad")],{"mirrorX":.54},camera(.52,.45,1.18,.52,.43,1.32))
add("kitchen","Mẹ loay hoay với túi đồ nặng; nhân vật đứng nhìn từ cửa bếp.","Ở nhà, cậu vẫn chưa biết giúp mẹ bằng cách nào.",
    [actor("mom",.66,"crouch","sad",hold="bag"),actor("hoodie",.28,"stand","sad")],{"sky":"dusk","lamp":True},
    camera(.50,.52,1.0,.54,.50,1.08),lights=[{"x":.72,"y":.30,"r":.22,"color":"#ffc36f","a":.3}])
add("doorway","Nhân vật nhường lối cho mẹ bước qua cửa; hai người nhìn nhau nhưng không nói.","Cậu muốn giúp mẹ, nhưng chưa tìm được lời để nói.",
    [actor("hoodie",.34,"point","sad"),actor("mom",.70,"stand","neutral")],{"doorX":.56,"doorOpen":.75},
    camera(.52,.50,1.0,.52,.50,1.08))
add("bedroom","Đồng hồ báo thức và đồng hồ đếm ngược cùng nằm trên bàn, hai kim chỉ hai nhịp khác nhau.","Cậu hiểu rằng dừng thời gian không thể thay thế sự quan tâm.",
    [actor("hoodie",.42,"headhold","sad")],{"clock":"23:50","lamp":True,"sky":"night","stage":True},
    camera(.56,.48,1.14,.56,.48,1.28),sfx=[cue("heartbeat",.3)])
add("street","Mẹ dắt chiếc xe đạp cũ ra khỏi nhà khi trời bắt đầu đổ mưa.","Tối hôm ấy, mẹ vẫn đạp xe về nhà như mọi ngày.",
    [actor("mom",.66,"stand","neutral",y=.73),actor("hoodie",.28,"wave","neutral")],
    {"busstop":False,"rain":True,"bicycle":True,"bikeX":.67,"lampX":.84},camera(.50,.53,1.0,.54,.51,1.08),sfx=[cue("whoosh_mid",.4)])

# ACT 05 — The storm gathers; the billboard becomes a real threat.
add("bedroom","Cận chiếc đồng hồ; mười vạch sáng lại rồi tắt, như lời nhắc về giới hạn.","Cậu không thể giữ năng lực ấy lâu hơn mười giây.",
    [actor("hoodie",.52,"headhold","neutral")],{"clock":"20:17","lamp":True,"sky":"night","stage":True},
    camera(.54,.48,1.25,.54,.48,1.42),sfx=[cue("tick",.2)])
add("kitchen","Mẹ lau tay, xếp hộp đồ ăn vào giỏ xe; căn bếp vàng ấm đối lập trời mưa ngoài cửa.","Mẹ đã làm việc cả ngày, nhưng vẫn còn chuyến xe cuối.",
    [actor("mom",.62,"carry","sad",hold="bag")],{"sky":"rain","lamp":True},camera(.54,.52,1.0,.57,.49,1.08))
add("mirror","Nhân vật đứng trước gương, nhìn vết xước trên cổ tay do những lần chạy vội.","Cậu biết mình không thể cứu tất cả mọi thứ.",
    [actor("hoodie",.52,"sad","sad")],{"mirrorX":.53},camera(.50,.47,1.12,.50,.44,1.26))
add("city","Toàn cảnh thành phố lúc chập tối; mây mưa phủ lên các dãy nhà và ánh đèn bắt đầu sáng.","Mưa lớn dần trên những con phố.",
    [actor("mom",.78,"walk","neutral",walk={"to":.56,"dur":3.5,"speed":.75},y=.73)],
    {"time":"night","birds":False,"lamps":[.22,.48,.75]},camera(.50,.42,1.0,.58,.48,1.08),sfx=[cue("riser_4s",.2)])
add("street","Mẹ đạp xe qua phố; vệt nước phản chiếu đèn đường dưới bánh xe.","Mẹ đang trên đường về nhà.",
    [actor("mom",.66,"sit","neutral",y=.72,h=.41),actor("ghost",.18,"stand","neutral",h=.30)],
    {"busstop":False,"rain":True,"bicycle":True,"bikeX":.67,"lampX":.78},camera(.38,.52,1.0,.60,.50,1.12))
add("street","Góc cao nhìn xuống mặt đường; biển quảng cáo lớn rung trên khung sắt.","Một tấm biển quảng cáo bắt đầu rung lắc trong gió.",
    [actor("mom",.66,"sit","neutral",y=.72,h=.40)],
    {"busstop":False,"rain":True,"bicycle":True,"bikeX":.67,"billboard":True,"billboardX":.78,"lampX":.9},
    camera(.72,.32,1.2,.74,.34,1.4),sfx=[cue("impact_light",2.8)])
add("street","Cận bu-lông gỉ ở chân biển quảng cáo; nước mưa chảy dọc kim loại.","Một chiếc bu-lông đã bật gần hết ren.",
    [],{"busstop":False,"rain":True,"bicycle":True,"bikeX":.67,"billboard":True,"billboardX":.78,"lampX":.9},
    camera(.78,.33,1.42,.78,.33,1.62),sfx=[cue("tick",.6)])
add("street","Biển quảng cáo nghiêng thêm; xe đạp của mẹ vẫn tiến gần dưới khung sắt.","Mẹ không nhìn thấy nguy hiểm phía trên.",
    [actor("mom",.64,"sit","neutral",y=.72,h=.40)],
    {"busstop":False,"rain":True,"bicycle":True,"bikeX":.67,"billboard":True,"billboardX":.78,"billboardTilt":.22,"lampX":.9},
    camera(.54,.48,1.0,.62,.48,1.12),sfx=[cue("riser_2s",.3)])
add("street","Bánh trước xe đạp cắt qua vũng nước; phía trên, khung biển kêu răng rắc trong gió.","Mẹ không nghe thấy tiếng kim loại đang rạn.",
    [actor("mom",.63,"sit","neutral",y=.72,h=.40)],
    {"busstop":False,"rain":True,"bicycle":True,"bikeX":.66,"billboard":True,"billboardX":.79,"billboardTilt":.18,"lampX":.9},
    camera(.64,.68,1.28,.66,.61,1.46),sfx=[cue("impact_heavy",2.5)])
add("street","Cận gương mặt mẹ; ánh đèn đường phản chiếu trên giọt mưa, mắt vẫn nhìn đường.","Mẹ chỉ còn cách tấm biển vài mét.",
    [actor("mom",.53,"guard","neutral",y=.72,h=.47)],
    {"busstop":False,"rain":True,"bicycle":True,"bikeX":.67,"billboard":True,"billboardX":.78,"billboardTilt":.25,"lampX":.9},
    camera(.52,.40,1.28,.52,.40,1.48))
add("street","Nhân vật chính đứng bên kia đường, nhận ra tấm biển đang đổ về phía mẹ.","Cậu nhìn thấy tất cả. Và cậu biết phải làm gì.",
    [actor("hoodie",.27,"guard","sad"),actor("mom",.70,"sit","neutral",y=.72,h=.38)],
    {"busstop":False,"rain":True,"bicycle":True,"bikeX":.68,"billboard":True,"billboardX":.80,"billboardTilt":.30,"lampX":.9},
    camera(.48,.52,1.0,.56,.48,1.12),sfx=[cue("heartbeat",.1)])
add("street","Cận cổ tay; ngón tay bấm lên mặt đồng hồ đúng khi khung biển bật khỏi chốt.","Cậu kích hoạt mười giây cuối cùng.",
    [actor("hoodie",.32,"phone","sad",hold="phone",h=.42)],
    {"busstop":False,"rain":False,"bicycle":True,"bikeX":.68,"billboard":True,"billboardX":.80,"billboardTilt":.30,"lampX":.9},
    camera(.37,.48,1.30,.37,.48,1.56),freeze=True,timer=10,sfx=[cue("slowmo_ring",.1),cue("heartbeat",.2)])

# ACT 06 — The rescue: anticipation, run, contact, impact, recovery.
add("street","Toàn cảnh phố mưa bất động; giọt nước treo giữa không trung, biển quảng cáo nghiêng trên mẹ.","Mọi thứ đứng yên. Chỉ còn cậu có thể di chuyển.",
    [actor("hoodie",.24,"guard","neutral"),actor("mom",.70,"sit","neutral",y=.72,h=.40)],
    {"busstop":False,"rain":False,"bicycle":True,"bikeX":.68,"billboard":True,"billboardX":.80,"billboardTilt":.32,"lampX":.9},
    camera(.50,.48,1.0,.54,.46,1.10),freeze=True,timer=10)
add("street","Cận giày nhân vật đạp mạnh xuống vũng nước; các gợn sóng bị đóng băng giữa không trung.","Cậu lao đi ngay lập tức.",
    [actor("hoodie",.18,"guard","neutral",run={"to":.66,"dur":3.8,"speed":1.9},h=.46)],
    {"busstop":False,"rain":False,"bicycle":True,"bikeX":.68,"billboard":True,"billboardX":.80,"billboardTilt":.32,"lampX":.9},
    camera(.20,.72,1.0,.58,.66,1.22),freeze=True,timer=9,fx=[{"kind":"speed","at":.2,"dur":2.8,"dir":1}],sfx=[cue("whoosh_fast",.2)])
add("street","Tracking ngang: nhân vật chạy qua các vệt mưa đứng yên, mẹ vẫn bất động trên xe.","Tám giây. Cậu phải đến được chỗ mẹ.",
    [actor("hoodie",.24,"guard","neutral",run={"to":.70,"dur":3.4,"speed":1.8},h=.46)],
    {"busstop":False,"rain":False,"bicycle":True,"bikeX":.70,"billboard":True,"billboardX":.80,"billboardTilt":.32,"lampX":.9},
    camera(.30,.53,1.0,.64,.52,1.18),freeze=True,timer=8,fx=[{"kind":"speed","at":.1,"dur":3.0,"dir":1}])
add("street","Cận bàn tay nhân vật vươn về tay lái; khoảng cách chỉ còn một gang tay.","Cậu với tới tay lái.",
    [actor("hoodie",.52,"point","neutral",h=.50),actor("mom",.70,"sit","neutral",y=.72,h=.38)],
    {"busstop":False,"rain":False,"bicycle":True,"bikeX":.70,"billboard":True,"billboardX":.80,"billboardTilt":.32,"lampX":.9},
    camera(.60,.62,1.28,.64,.59,1.50),freeze=True,timer=7)
add("street","Nhân vật kéo xe đạp lệch khỏi đường rơi của tấm biển; thân người nghiêng về phía sau.","Cậu kéo mẹ khỏi vị trí nguy hiểm.",
    [actor("hoodie",.43,"guard","sad",run={"to":.28,"dur":1.8,"speed":1.1},h=.49),actor("mom",.62,"sit","neutral",y=.72,h=.40)],
    {"busstop":False,"rain":False,"bicycle":True,"bikeX":.64,"billboard":True,"billboardX":.80,"billboardTilt":.32,"lampX":.9},
    camera(.52,.54,1.08,.50,.53,1.28),freeze=True,timer=6,fx=[{"kind":"speed","at":.5,"dur":1.5,"dir":-1}],sfx=[cue("impact_light",1.6)])
add("street","Góc thấp bánh xe trượt qua vạch đường; mẹ và nhân vật đã lệch khỏi vùng nguy hiểm.","Năm giây. Họ vẫn chưa đủ xa.",
    [actor("hoodie",.36,"crouch","sad",h=.48),actor("mom",.58,"kneel","neutral",y=.72,h=.40)],
    {"busstop":False,"rain":False,"bicycle":True,"bikeX":.58,"billboard":True,"billboardX":.80,"billboardTilt":.32,"lampX":.9},
    camera(.48,.67,1.18,.50,.62,1.38),freeze=True,timer=5)
add("street","Nhân vật đỡ mẹ đứng dậy, một tay giữ vai, tay kia kéo xe đạp ra sau.","Cậu đỡ mẹ lùi thêm vài bước.",
    [actor("hoodie",.40,"carry","neutral",h=.49),actor("mom",.58,"kneel","sad",y=.72,h=.42)],
    {"busstop":False,"rain":False,"bicycle":True,"bikeX":.62,"billboard":True,"billboardX":.80,"billboardTilt":.32,"lampX":.9},
    camera(.48,.52,1.0,.52,.51,1.14),freeze=True,timer=4)
add("street","Nhân vật đẩy xe đạp vào sát lề, đặt mẹ phía sau cột đèn chắc chắn.","Cậu đưa mẹ đến nơi an toàn.",
    [actor("hoodie",.38,"guard","neutral",run={"to":.27,"dur":2.8,"speed":1.1},h=.47),actor("mom",.58,"stand","neutral",h=.41)],
    {"busstop":False,"rain":False,"bicycle":True,"bikeX":.33,"billboard":True,"billboardX":.80,"billboardTilt":.32,"lampX":.9},
    camera(.46,.50,1.0,.42,.48,1.12),freeze=True,timer=2)
add("street","Tấm biển đã rời khỏi điểm giữ; nhân vật cúi người che cho mẹ, chiếc xe nằm ngoài vùng rơi.","Một giây nữa thôi.",
    [actor("hoodie",.42,"crouch","sad",h=.47),actor("mom",.54,"kneel","sad",h=.41)],
    {"busstop":False,"rain":False,"bicycle":True,"bikeX":.34,"billboard":True,"billboardX":.80,"billboardTilt":.32,"lampX":.9},
    camera(.49,.54,1.10,.49,.52,1.32),freeze=True,timer=1,sfx=[cue("heartbeat",.1)])
add("street","Thời gian bật lại; biển quảng cáo đổ xuống mặt đường trống, nước bắn tung tóe.","Thời gian trở lại. Tấm biển đập xuống phía sau họ.",
    [actor("hoodie",.42,"knees","sad",h=.47),actor("mom",.54,"knees","sad",h=.42)],
    {"busstop":False,"rain":True,"bicycle":True,"bikeX":.30,"billboard":True,"billboardX":.80,"billboardFall":True,"billboardTilt":0.0,"lampX":.9},
    camera(.55,.48,1.0,.62,.46,1.18),fx=[{"kind":"flash","at":.1,"dur":.25,"a":.62},{"kind":"speed","at":.1,"dur":1.5}],
    sfx=[cue("impact_heavy",.15),cue("whoosh_reverse",.2)])
add("street","Mẹ và con trai ngồi trên vỉa hè ướt; chiếc xe nằm cạnh, mưa vẫn rơi.","Mẹ nhìn cậu, vừa sợ hãi vừa không hiểu chuyện gì.",
    [actor("mom",.56,"sit","sad",h=.44),actor("hoodie",.40,"kneel","sad",h=.45)],
    {"busstop":False,"rain":True,"bicycle":True,"bikeX":.77,"billboard":True,"billboardX":.80,"billboardFall":True,"lampX":.9},
    camera(.50,.56,1.1,.50,.52,1.24),sfx=[cue("thud_soft",.4)])
add("street","Hai người ôm nhau dưới ánh đèn vàng; mưa tạo thành lớp hậu cảnh mờ.","Cậu không còn quan tâm chiếc đồng hồ nữa.",
    [actor("hoodie",.43,"carry","sad",h=.49),actor("mom",.56,"carry","sad",h=.46)],
    {"busstop":False,"rain":True,"bicycle":True,"bikeX":.78,"billboard":True,"billboardX":.80,"billboardFall":True,"lampX":.9},
    camera(.50,.48,1.06,.50,.46,1.22),lights=[{"x":.76,"y":.28,"r":.30,"color":"#ffc36f","a":.38}],sfx=[cue("ding_soft",2.6)])

# ACT 07 — A different way to spend the next second.
add("kitchen","Sáng hôm sau; mẹ sửa lại quai túi, nhân vật đặt bữa sáng lên bàn.","Sáng hôm sau, mọi thứ vẫn tiếp tục.",
    [actor("mom",.63,"stand","grin"),actor("hoodie",.36,"carry","grin",hold="cup")],{"sky":"dawn","lamp":False},
    camera(.50,.52,1.0,.54,.50,1.08))
add("street","Xe đạp được dựng cạnh tường; nhân vật kiểm tra phanh và siết lại chiếc ốc lỏng.","Cậu giúp mẹ sửa lại chiếc xe đạp cũ.",
    [actor("hoodie",.43,"crouch","neutral"),actor("mom",.70,"stand","grin")],
    {"busstop":False,"rain":False,"bicycle":True,"bikeX":.60,"lampX":.84},camera(.50,.62,1.08,.53,.59,1.24),sfx=[cue("impact_light",1.8)])
add("doorway","Mẹ đứng ở cửa; nhân vật trao chiếc áo mưa đã gấp gọn, ánh sáng ấm chiếu từ trong nhà.","Cậu không cần năng lực để quan tâm đến mẹ.",
    [actor("hoodie",.37,"carry","grin",hold="umbrella"),actor("mom",.68,"point","grin")],{"doorX":.55,"doorOpen":.8},
    camera(.50,.50,1.0,.53,.48,1.10))
add("classroom","Nhân vật giơ tay phát biểu; bạn cùng lớp quay lại nhìn, bảng học sáng phía sau.","Cậu học cách dùng thời gian thật của mình.",
    [actor("hoodie",.37,"point","grin"),actor("friend",.73,"point","neutral")],{"sky":"day","board":"HÔM NAY","desks":[.25,.5,.75]},
    camera(.50,.49,1.0,.54,.46,1.1))
add("court","Bạn bè chơi bóng; nhân vật chạy theo đường biên, tiếng cười trở lại.","Cậu chạy, chơi và cười cùng bạn bè.",
    [actor("hoodie",.27,"guard","grin",run={"to":.72,"dur":3.5,"speed":1.25}),actor("friend",.76,"cheer","grin",hold="ball")],
    {"hoopX":.74,"benchX":.2},camera(.34,.50,1.0,.62,.46,1.15),fx=[{"kind":"speed","at":.2,"dur":1.4}],sfx=[cue("crowd_cheer",.6)])
add("bedroom","Đồng hồ nằm im trên bàn; nhân vật đi ngang qua mà không nhấn nút.","Chiếc đồng hồ vẫn ở đó, nhưng cậu không còn vội vã.",
    [actor("hoodie",.34,"walk","neutral",walk={"to":.74,"dur":3.8,"speed":.75})],{"clock":"21:30","lamp":True,"sky":"night","stage":True},
    camera(.5,.5,1.0,.54,.48,1.08))
add("bedroom","Cận bàn tay đóng ngăn kéo, chiếc đồng hồ được đặt lại bên trong.","Cậu để mười giây ấy ngủ yên.",
    [actor("hoodie",.50,"carry","neutral")],{"clock":"21:31","lamp":True,"sky":"night","stage":True},
    camera(.53,.61,1.24,.53,.57,1.42),sfx=[cue("ui_click",.8)])
add("city","Thành phố nhìn từ trên cao; đèn xe tạo thành những vệt sáng dài, cửa sổ ấm dần.","Thế giới vẫn chuyển động, dù không ai điều khiển nó.",
    [],{"time":"dusk","birds":False,"lamps":[.2,.45,.7,.9]},camera(.5,.43,1.0,.54,.50,1.06))
add("hill","Nhân vật và mẹ đứng trên con dốc nhìn xuống thành phố; đường chân trời rực màu bình minh.","Điều quý giá không phải là dừng được thời gian.",
    [actor("hoodie",.43,"relaxed","grin"),actor("mom",.58,"relaxed","grin")],{},camera(.50,.46,1.0,.52,.43,1.08),
    lights=[{"x":.75,"y":.28,"r":.38,"color":"#ffc36f","a":.26}])
add("street","Hai mẹ con dắt xe đi trên con phố vừa tạnh mưa; vũng nước phản chiếu ánh sáng đầu ngày.","Mà là chọn điều mình làm trong từng giây đang có.",
    [actor("hoodie",.42,"walk","grin",walk={"to":.62,"dur":3.8,"speed":.72}),actor("mom",.60,"walk","grin",walk={"to":.76,"dur":3.8,"speed":.68})],
    {"busstop":False,"rain":False,"bicycle":True,"bikeX":.70,"lampX":.84},camera(.38,.51,1.0,.58,.48,1.12))
add("hill","Toàn cảnh thành phố trong nắng sớm; hai nhân vật nhỏ ở mép đồi, đường phố bên dưới vẫn nhộn nhịp.","Mười giây không thể thay thế một cuộc đời.",
    [actor("hoodie",.43,"stand","neutral",h=.36),actor("mom",.56,"stand","neutral",h=.36)],{},camera(.50,.48,1.0,.5,.46,1.0))
add("black","Thẻ kết nền than chì; vòng sáng xanh nhỏ co lại thành một chấm rồi tắt.","HÃY SỐNG TRỌN VẸN TỪNG GIÂY.",
    [],{},camera(.5,.5,1,.5,.5,1),fx=[{"kind":"pulse","at":.2,"dur":3.8,"color":"#8bd8ff","a":.14}],
    sfx=[cue("ding_soft",2.4)],transition={"type":"dip","dur":.7},text_pos="bottom")

def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def build(project_dir: Path):
    if len(SHOTS) != 84:
        raise RuntimeError(f"Expected 84 shots, got {len(SHOTS)}")
    duration = round(len(SHOTS) * SHOT_SECONDS, 3)
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "story").mkdir(exist_ok=True)
    (project_dir / "build").mkdir(exist_ok=True)
    (project_dir / "out").mkdir(exist_ok=True)
    config = {
        "title":"time-stop-10s","aspect":"16:9","resolution":"1080p","fps":FPS,
        "style":"flat","pack":"dem","lang":"vi","accent":"teal","captions":False,
        "bars":"scope","fadeIn":0.45,"fadeOut":0.65,
        "music":{"enabled":True,"gainDb":-13},"sfx":{"enabled":True,"gainDb":-4},
        "loudness":-14,"duration":duration,
    }
    write_json(project_dir / "config.json", config)
    shots = []
    script_lines = [
        "TITLE: NẾU BẠN CÓ THỂ DỪNG THỜI GIAN TRONG 10 GIÂY?",
        "ACCENT: teal","",
        "# Phim hoạt hình gốc, 16:9, 1080p, 30fps, 7 hồi / 84 shot.",
        "# Nhạc/SFX tạo bằng H2 kit; không dùng dịch vụ tạo video trả phí.","",
    ]
    set_counts = {}
    freeze_count = 0
    for index, item in enumerate(SHOTS):
        start = round(index * SHOT_SECONDS, 3)
        end = round(start + SHOT_SECONDS, 3)
        shot_id = f"s{index + 1:03d}"
        set_name = item["location"]
        set_counts[set_name] = set_counts.get(set_name, 0) + 1
        args = {
            "set":set_name,"setArgs":dict(item["set_args"]),"actors":item["actors"],
            "texts":[{
                "kind":"narr","t":item["caption"],"at":0.28,"dur":4.02,
                "pos":item["text_pos"],"size":54,"type":True,"maxW":0.84,
            }],
            "cam":item["cam"],"fx":list(item["fx"]),"lights":list(item["lights"]),
            "vignette":item["vignette"],
        }
        if item["freeze"]:
            freeze_count += 1
            args["fx"].append({"kind":"freeze","at":0.10,"dur":4.25,"x":0.50,"y":0.48,"color":"#8bd8ff","intensity":1.0})
            args["setArgs"]["rain"] = False
        if item["timer"] is not None:
            args["hud"] = {"rows":[{"label":"GIÂY CÒN","n":int(item["timer"]),"color":"#a8e5ff"}]}
        transition = item["transition"] or ({"type":"dip","dur":0.48} if index in (12,24,36,48,60,72) else {"type":"cut"})
        shots.append({
            "id":shot_id,"start":start,"end":end,"scene":item["scene"],"line":item["caption"],
            "tpl":"scene","args":args,"in":transition,"sfx":item["sfx"],"notes":item["scene"],
        })
        script_lines.append(f"[{shot_id.upper()}] {SHOT_SECONDS:.1f}s | CẢNH: {item['scene']} | SET: {set_name} | HÀNH ĐỘNG: {item['caption']}")
    music = [
        {"start":0,"end":54,"bed":"curious","gainDb":0},
        {"start":54,"end":108,"bed":"mystery","gainDb":-1},
        {"start":108,"end":162,"bed":"tension","gainDb":-1},
        {"start":162,"end":216,"bed":"triumph","gainDb":-1},
        {"start":216,"end":270,"bed":"tension","gainDb":-2},
        {"start":270,"end":324,"bed":"emotional","gainDb":0},
        {"start":324,"end":378,"bed":"emotional","gainDb":-1},
    ]
    story = {
        "title":"Nếu Bạn Có Thể Dừng Thời Gian Trong 10 Giây?",
        "duration":duration,"fps":FPS,"resolution":[WIDTH,HEIGHT],"shots":shots,"music":music,"sfx":[],
        "production":{"engine":"H2 Canvas/Chromium + FFmpeg","paid_video_services":False,
                      "shot_count":len(shots),"time_freeze_fx_count":freeze_count,"set_variety":set_counts,"fps":FPS},
    }
    write_json(project_dir / "story" / "shots.json", story)
    write_json(project_dir / "story" / "shot-plan.json", {
        "title":story["title"],"durationSeconds":duration,"fps":FPS,
        "acts":[
            {"name":"01 — Một ngày bình thường","shots":"s001–s012"},
            {"name":"02 — Lần dừng đầu tiên","shots":"s013–s024"},
            {"name":"03 — Quy tắc mười giây","shots":"s025–s036"},
            {"name":"04 — Dùng năng lực để giúp người","shots":"s037–s048"},
            {"name":"05 — Cơn mưa và hiểm họa","shots":"s049–s060"},
            {"name":"06 — Cứu mẹ trong mười giây","shots":"s061–s072"},
            {"name":"07 — Sống trọn vẹn","shots":"s073–s084"},
        ],
        "shots":[{"id":s["id"],"start":s["start"],"end":s["end"],"set":s["args"]["set"],"line":s["line"],"scene":s["scene"],
                  "freeze":any(f.get("kind")=="freeze" for f in s["args"]["fx"])} for s in shots],
    })
    (project_dir / "01-PHIM-time-stop-10s.txt").write_text("\n".join(script_lines)+"\n",encoding="utf-8")
    bible = """# Story & Art Bible — 10 Giây Dừng Thời Gian

## Premise
Một học sinh có thể đóng băng thế giới trong đúng 10 giây. Lúc đầu cậu dùng năng lực để giải quyết những phiền toái nhỏ. Khi mẹ gặp nguy hiểm dưới một tấm biển quảng cáo trong cơn mưa, cậu phải dùng toàn bộ mười giây để cứu người mình yêu thương.

## Cast lock
- Protagonist: hoodie, cream head, dark limbs, muted teal clothing; keep scale, face and silhouette consistent.
- Mother: mom; warm muted purple shirt, bun hair, calm body language.
- School friend: friend; appears in school beats.
- Child: kid; small silhouette for the corridor rescue.
- No photoreal humans. The world and staging carry the detail.

## Visual grammar
- 16:9 cinematic scope, 1920×1080, 30fps.
- Dark plum/charcoal architecture; warm amber practicals; restrained cyan time-freeze energy.
- Alternate wide establishing, medium action, low tracking, hand/prop inserts, face reaction and emotional holds.
- Freeze FX is an original H2 Canvas overlay: concentric time rings, suspended rain/particles and fine refractive filaments.
- Street set adds a bicycle and a tilting billboard for the rescue sequence.
- Every action should imply anticipation → movement → contact → follow-through → recovery.
- Captions are short, placed in safe top/bottom lanes; no giant HUDs across the acting.

## Audio
- No synthetic narrator is generated by default.
- Original procedural music beds and H2-generated SFX only; use intentional silence in the rescue aftermath.
"""
    (project_dir / "story" / "bible.md").write_text(bible,encoding="utf-8")
    if len(shots)!=84 or round(shots[-1]["end"],3)!=duration:
        raise RuntimeError("Story duration/count invariant failed")
    if freeze_count<14:
        raise RuntimeError(f"Expected multiple freeze-action shots, got {freeze_count}")
    if max(set_counts.values())>20:
        raise RuntimeError("One setting dominates the film; increase location variety")
    previous=0
    for shot in shots:
        a=round(shot["start"]*FPS); b=round(shot["end"]*FPS)
        if a!=previous or b<=a:
            raise RuntimeError(f"Frame gap/overlap in {shot['id']}: {a}..{b}, expected {previous}")
        previous=b
    print(json.dumps({"status":"story-built","shots":len(shots),"duration_seconds":duration,"fps":FPS,
                      "frames":int(duration*FPS),"time_freeze_shots":freeze_count,"sets":set_counts,
                      "project_dir":str(project_dir)},ensure_ascii=False,indent=2))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--project-dir",required=True)
    args=ap.parse_args()
    build(Path(args.project_dir))

if __name__=="__main__":
    main()
