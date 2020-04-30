def getLabel(x):
    buttonlabel=""
    if(x != ""):
        if "facebook" in x:
            if "videos" in x:
                buttonlabel = "페이스북 영상"
            else:
                buttonlabel = "페이스북 링크"
        elif "everytime" in x:
            buttonlabel = "에브리타임 링크"
        elif "naver.me" in x:
            buttonlabel = "네이버폼 지원서"
        elif "open.kakao.com" in x:
            buttonlabel = "카톡 오픈채팅"
        elif "google" in x or "goo.gl" in x or "http://bit.ly/2IygLil" or "forms.gle" in x:
            buttonlabel = "구글폼 지원서"
        else:
            buttonlabel = "기타링크"
    return buttonlabel


@csrf_exempt
def club(request):
    category = json.loads(request.body.decode("utf-8"))["userRequest"]["utterance"]
    category_tojson = {
        "연행예술분과" : "performing", 
        "체육분과" : "physical", 
        "평면예술분과" : "drawing", 
        "학술분과" : "studying", 
        "구기체육분과" : "ball", 
        "봉사분과" : "volunteering", 
        "교양분과" : "culture", 
        "종교분과" : "religion", 
        "기타":"others"
        }
    link = "https://raw.githubusercontent.com/jil8885/ERICA_api/master/club.json"
    response = requests.get(link)
    body = response.json()
    result = body[category_tojson[category]]
    json_result = []
    thumbnail = False
    
    for x in result:
        if "photo" in x.keys():
            thumbnail = True
            break
    for x in list(result):
        json_item = {"title" : x["name"], "description" : x["description"]}
        if x["link"] != "":
            label = getLabel(x["link"])
            json_item["buttons"] = [{"action" : "webLink", "label" : label, "webLinkUrl" : x["link"]}]
        if "link2" in x.keys():
            label = getLabel(x["link2"])
            json_item["buttons"].append({"action" : "webLink", "label" : label, "webLinkUrl" : x["link2"]})
        if "link3" in x.keys():
            label = getLabel(x["link3"])
            json_item["buttons"].append({"action" : "webLink", "label" : label, "webLinkUrl" : x["link3"]})
        if "info" in x.keys():
            label = "상세정보 알아보기"
            blockId = "5e71907427fd9f0001351c81"
            json_item["buttons"].append({"action" : "block", "label" : label, "messageText": x["name"], "blockId" : blockId})
        if "photo" in x.keys():
            json_item["thumbnail"] = {}
            json_item["thumbnail"]["imageUrl"] = x["photo"]
            if "width" in x.keys() and "height" in x.keys():
                json_item["thumbnail"]["fixedRatio"] = True
                json_item["thumbnail"]["width"] = x["width"]
                json_item["thumbnail"]["height"] = x["height"]
            
        json_result.append(json_item)
    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "carousel": {
                    "type": "basicCard",
                    "items":json_result
                    }
                }
            ]
        }
    }
    return JsonResponse(responseBody, json_dumps_params = {'ensure_ascii': False})

@csrf_exempt
def circle(request):
    category = json.loads(request.body.decode("utf-8"))["userRequest"]["utterance"]
    category_tojson = {
        "소프트웨어":"software",
        "ICT융합":"ict",
        "소프트웨어융합대학":"soft",
        "전자공":"electric",
        "기계공":"mechanic",
        "로봇공":"robot",
        "공학대학":"engineering",
        "국제문화대학":"gukmun",
        "디자인대학":"design",
        "경상대학":"economy_college",
        "경영학부":"biz",
        "경제학부":"economy"
    }
    link = "https://raw.githubusercontent.com/jil8885/ERICA_api/master/circles.json"
    response = requests.get(link)
    body = response.json()
    result = body[category_tojson[category]]
    json_result = []
    thumbnail = False
    for x in result:
        if "photo" in x.keys():
            thumbnail = True
            break
    for x in result:
        json_item = {"title" : x["name"], "description" : x["description"]}
        if x["link"] != "":
            label = getLabel(x["link"])
            json_item["buttons"] = [{"action" : "webLink", "label" : label, "webLinkUrl" : x["link"]}]
        if "link2" in x.keys():
            label = getLabel(x["link2"])
            json_item["buttons"].append({"action" : "webLink", "label" : label, "webLinkUrl" : x["link2"]})
        if "link3" in x.keys():
            label = getLabel(x["link3"])
            json_item["buttons"].append({"action" : "webLink", "label" : label, "webLinkUrl" : x["link3"]})
        if "info" in x.keys():
            label = "상세정보 알아보기"
            blockId = "5e71907427fd9f0001351c81"
            json_item["buttons"].append({"action" : "block", "label" : label, "messageText": x["name"], "blockId" : blockId})
        if "photo" in x.keys():
            json_item["thumbnail"] = {}
            json_item["thumbnail"]["imageUrl"] = x["photo"]
            if "width" in x.keys() and "height" in x.keys():
                json_item["thumbnail"]["fixedRatio"] = True
                json_item["thumbnail"]["width"] = x["width"]
                json_item["thumbnail"]["height"] = x["height"]
        elif thumbnail:
            json_item["thumbnail"] = {}
            json_item["thumbnail"]["imageUrl"] = "https://raw.githubusercontent.com/jil8885/djangoapp-kakao-i/master/templates/images/default.png"
            json_item["thumbnail"]["fixedRatio"] = True
            json_item["thumbnail"]["width"] = 833
            json_item["thumbnail"]["height"] = 833
        json_result.append(json_item)

    if category == "소프트웨어융합대학":
        quickReplies = [
                {
                    "action" : "block",
                    "label" : "소프트웨어",
                    "messageText" : "소프트웨어",
                    "blockId" : "5e70be9a2d3cd0000121a234"
                },
                {
                    "action" : "block",
                    "label" : "ICT융합",
                    "messageText" : "ICT융합",
                    "blockId" : "5e70be9a2d3cd0000121a234"
                }              
        ]
    elif category == "공학대학":
        quickReplies = [
                {
                    "action" : "block",
                    "label" : "전자공",
                    "messageText" : "전자공",
                    "blockId" : "5e70be9a2d3cd0000121a234"
                },
                {
                    "action" : "block",
                    "label" : "기계공",
                    "messageText" : "기계공",
                    "blockId" : "5e70be9a2d3cd0000121a234"
                },
                {
                    "action" : "block",
                    "label" : "로봇공",
                    "messageText" : "로봇공",
                    "blockId" : "5e70be9a2d3cd0000121a234"
                }              
        ]
    elif category == "경상대학":
        quickReplies = [
                {
                    "action" : "block",
                    "label" : "경제학부",
                    "messageText" : "경제학부",
                    "blockId" : "5e70be9a2d3cd0000121a234"
                },
                {
                    "action" : "block",
                    "label" : "경영학부",
                    "messageText" : "경영학부",
                    "blockId" : "5e70be9a2d3cd0000121a234"
                }           
        ]        
    else:
        quickReplies = []
    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "carousel": {
                    "type": "basicCard",
                    "items":json_result
                    }
                }
            ]
        }
    }
    if quickReplies != []:
        responseBody["template"]["quickReplies"] = quickReplies
    return JsonResponse(responseBody, json_dumps_params = {'ensure_ascii': False})

@csrf_exempt
def info(request):
    name = json.loads(request.body.decode("utf-8"))["userRequest"]["utterance"]
    name_tofolder = {
        "CRUX":"CRUX"
    }
    clubName = name_tofolder[name]
    json_result = []
    if clubName == "CRUX":
        json_result.append({"title" : clubName + "에서는?", "description" : "❗⚠️국제문화대학 신입생 친구들 주목⚠️❗\n\n안녕하세요! [국제문화대학 밴드동아리 CRUX]에서 신입부원을 모집합니다🥳\n\n⬇️모집 대상⬇️\n\n🎤 밴드에 관심이 많으신 분\n🎤 기타,드럼,베이스,키보드 등의 악기 연주를 좋아하시는 분\n🎤 공연을 해보고 싶으신 분\n🎤 국문대 인싸가 되고싶으신 분"})
        json_result.append({"title" : clubName + "에서는?", "description" : "⬇️동아리 활동⬇️\n\n🥁 1년에 2번 정기공연 및 여름방학 홍대공연\n🥁 매주 목요일 정기모임 및 뒤풀이\n🥁 각 세션별 멘토링\n🥁 상상유니브 보컬 클래스\n🥁 매 학기 신나는 MT\n🥁 기타 다양한 외부 행사\n\n기타,드럼,베이스,보컬,키보드 5개 세션의 신입부원을 모집하오니 가입신청을 원하시는 분들은 아래 네이버폼을 작성해 주시면 감사하겠습니다🤩🤩", "buttons":[{"action" : "webLink", "label" : "지원서 링크", "webLinkUrl" : "http://naver.me/xqGnPF58"}]})
        for x in range(1, 9):
            json_result.append({"thumbnail":{"imageUrl" : "https://raw.githubusercontent.com/jil8885/djangoapp-kakao-i/master/templates/images/club/CRUX/CRUX" + str(x) + ".jpeg"}})  
    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "carousel": {
                    "type": "basicCard",
                    "items":json_result
                    }
                }
            ]
        }
    }
    return JsonResponse(responseBody, json_dumps_params = {'ensure_ascii': False})
