import urllib.request
import regex as re
import json

#  ooe : 교육기관 코드 sc : 학교코드 stc : 학교유형코드(1 : 유치원 2 : 초등학교 3: 중학교 4 : 고등학교)
# d : 일 m : 월(01 등 2자리수로 표기할 것) y : 년

# https://stu.${region.url}/sts_sci_md00_001.do" + "?schulCode=${code}" + "&schulCrseScCode=${type.id}" + "&schulKndScCode=0${type.id}" + "&schYm=${year}${String.format("%02d", month)}&"

# 원봉중 20년도 3월 5일자 급식 url ex) https://stu.cbe.go.kr/sts_sci_md00_001.do?schulCode=M100000907&schulCrseScCode=3&schulKndScCode=03&schYm=2003

def get_meal(office_of_education, school_code, school_type_code, date, month, year):
    
    url = "https://stu." + office_of_education + ".go.kr/sts_sci_md00_001.do?schulCode=" + school_code + "&schulCrseScCode=" + school_type_code + "&schulKndScCode=0" + school_type_code + "&ay=" + year + "&mm=" + month 
    print(url)
    try:
        tmp = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'})
        body = urllib.request.urlopen(tmp).read().decode()
        meal_list = body.split('<tbody>')[1].split("</tbody>")[0].split("<td>")
        text_for_search = "<div>" + str(date) + "<br />"
        result = ""
        for tmp in meal_list:
            if text_for_search in tmp:
                result = result+tmp
        result = re.split("\[\D{2}\]", result)
        if len(result) == 4:
            for i in range(0, 4):
                result[i] = re.sub('<(/?[^>]+)>|\r|\n|\t', " ", result[i])
                result[i] = re.sub('(\d{1,2}\.)', " ", result[i])
                result[i] = re.sub(' {2,}', " ", result[i])
                result[i] = re.sub('&amp;', "&", result[i])
        else: 
            result.insert(1, "")
            for i in range(0, len(result)):
                result[i] = re.sub('<(/?[^>]+)>|\r|\n|\t', " ", result[i])
                result[i] = re.sub('(\d{1,2}\.)', " ", result[i])
                result[i] = re.sub(' {2,}', " ", result[i])
                result[i] = re.sub('&amp;', "&", result[i])
            result.append("")
            result.append("")
            
        if result[1] is None or result[1] == "":
            breakfast = []
        else:
            breakfast = result[1].strip().split(" ")
        if result[1] is None or result[2] == "":
            lunch = []
        else:
            lunch = result[2].strip().split(" ")
        if result[3] is None or result[3] == "":
            dinner = []
        else:
            dinner = result[3].strip().split(" ")
        FinalData = {"breakfast":breakfast,"lunch":lunch,"dinner":dinner}
        return FinalData
    except Exception as e:
        print("{a}: {b}".format(a=type(e).__name__, b=e))
        return {
            "status": "error"
        }


def get_meal_month(ooe, school_code, school_type_code, month, year): #날짜별로 분리는 되는데 존나 애매하네
    url = "https://stu." + ooe + ".go.kr/sts_sci_md00_001.do?schulCode=" + school_code + "&schulCrseScCode=" + school_type_code + "&schulKndScCode=" + school_type_code + "&ay=" + year + "&mm=" + month 
    try:
        tmp = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'})
        body = urllib.request.urlopen(tmp).read().decode()
        meal_list = body.split('<tbody>')[1].split("</tbody>")[0].split("<td>")
        result = ""
        for tmp in meal_list: # tmp 재활용
            if "[중식]" in tmp:  # zㅣ존 킹갓 in 쓰세요 씨바거
                tmp = re.sub('\r|\n|\t|<div>|</div>|</td>|<br />|<.{2,}>', " ", tmp)        #        얘는 html 태그 제거
                tmp = re.sub('(\d{1,2}\.)', " ", tmp)        #        얘는 알레르기 정보 제거
                tmp = re.sub(' {2,}', " ", tmp)        #        얘는 공백 과다 제거
                tmp = re.sub('&amp;', '&', tmp)
                result = result+tmp
        result = re.split("( \d{1,2} )", result)
        del result[0]
        for i in range(0, len(result)):
            result[i] = result[i].strip()
        a = result
        b = list()
        l = list()
        d = list()
        date = list()
        for i in range(0, len(a)):
            if not i % 2 == 0:
                date.append(a[i-1])
                q = re.findall('\[\D{2}\]', a[i])
                c = re.split('\[\D{2}\]', a[i])
                c[0] = a[i-1]
                for j in range(0, len(q)):
                    if q[j] == '[조식]':
                        b.append(c[j+1].strip().split(" "))
                    if q[j] == '[중식]':
                        l.append(c[j+1].strip().split(" "))
                    if q[j] == '[석식]':
                        d.append(c[j+1].strip().split(" "))
        tmp = {}
        for j in range(0, len(b)):
            b[j].insert(0, date[j])
        for j in range(0, len(l)):
            l[j].insert(0, date[j])
        for j in range(0, len(d)):
            d[j].insert(0, date[j])
        tmp['breakfast'] = b
        tmp['lunch'] = l
        tmp['dinner'] = d
        return(tmp)
    except Exception as e:
        print("{a}: {b}".format(a=type(e).__name__, b=e)) # :D thankyou
        return {
            "status": "error"
        }

    #http://restapi.run.goorm.io/api/meal?token=superuser&office_of_education=cbe&school_type_code=3&school_code=M100000907&year=2019&month=06&date=21
    #암튼 최선이였음 you_must_do_this('암튼 유,초,중,고 별 분류코드 예외 처리 꼭해야됨')        전부다 string으로 넣어야됨. 안그럼 에러남 