#!/usr/bin/env python

from bs4 import BeautifulSoup
import xlrd
import json
import os
execl_path = "data.xlsx"
md_path_dir = "../education/meetings/2018.10-2018.03/"
MEETING_COUNT = 103
MEETING_THEME = "Balance"
MEETING_DATE = "2018.08.24"
TableTopic = "A,B,C,D"
BestTableTopicSpeech = "A"
BestPreparedSpeech = "D"
BestEvaluator = "E"
AttendanceName = "Siyuan Jia,A"


template_attendance_for_create_html = """<h1>Attendance</h1>
<table class="table table-condensed table-bordered">
<tr><th>Name</th></tr>
<tr><th>Davis Zhang</th></tr>
<tr><th>Jason Xu</th></tr>
<tr><th>Jony Zheng</th></tr>
<tr><th>Kuan Li</th></tr>
<tr><th>Michelle Wang</th></tr>
<tr><th>Yayun Sun</th></tr>
<tr><th>Dongchen Tang</th></tr>
<tr><th>Michelle Hua</th></tr>
<tr><th>Jane Gong</th></tr>
<tr><th>Taowen Zhang</th></tr>
<tr><th>Eve Zhang</th></tr>
<tr><th>Yi Fang</th></tr>
<tr><th>Hongyu Qi</th></tr>
<tr><th>Qingzhen Deng</th></tr>
<tr><th>Jun Liu</th></tr>
<tr><th>Siyuan Jia</th></tr>
<tr><th>Minming Lu</th></tr>
<tr><th>Michelle Jin</th></tr>
<tr><th>Alice Huang</th></tr>
<tr><th>Xin Feng</th></tr>
<tr><th>Sarah Zhang</th></tr>
<tr><th>Haoming Zheng</th></tr>
<tr><th>Wujie Zhang</th></tr>
<tr><th>Yao Fang</th></tr>
<tr><th>Mingyu Li</th></tr>
<tr><th>Elvis Jiang</th></tr>
<tr><th>Total</th></tr>
</table>      
"""



class Agenda:
    def __init__(self, md_path, execl_path):
        self.md_path = md_path
        self.execl_path = execl_path
        self.create_new_record()
        self.md_type_data = {
            "date": MEETING_DATE,
            "count": MEETING_COUNT,
            "theme": MEETING_THEME,
            "attendance": {
                "name": AttendanceName
            },
            "best_awards": {
                "BTTS": BestTableTopicSpeech,
                "BPS": BestPreparedSpeech,
                "BE": BestEvaluator
            },
            "role_takers": {
                "TMD": "",
                "TTM": "",
                "GE": "",
                "IE": "",
                "Grammarian": "",
                "Timer": "",
                "Ah-counter": ""
            },
            "speakers": {
                "TT": TableTopic,
                "project_rank": [],
                "people_name": [],
                "project_name": []
            }
        }

    def get_data(self):
        data = xlrd.open_workbook(self.execl_path)
        table = data.sheets()[0]
        nrows = table.nrows
        for i in range(nrows):
            if i == 0:
                continue
            # print (table.row_values(i)[:4])
            # print(table.row_values(0)[0], table.row_values(0)[1], table.row_values(0)[2])
            # print(table.row_values(i)[1], "------", table.row_values(i)[2], "-----------------", i)
            if table.row_values(i)[2] == "":                                    # nothing
                continue
            if table.row_values(i)[2].find("[") == -1:
                continue
            if table.row_values(i)[2].split("[")[1].find(",") != -1:            # title cc/cl
                if table.row_values(i)[2].split(':')[0] == "Speaker":
                    if table.row_values(i)[1].find('-') == -1:                  # sharing Session

                        print(table.row_values(i)[1].split('(')[0], "--1--",
                              table.row_values(i)[2].split("[")[1].split(",")[0])
                    else:
                        print(table.row_values(i)[1].split('(')[0], "--2--",
                              table.row_values(i)[1].split(')')[1].split('-')[1],
                              table.row_values(i)[2].split("[")[1].split(",")[0])

                        self.md_type_data["speakers"]["project_rank"].append(table.row_values(i)[1].split('(')[0])
                        self.md_type_data["speakers"]["project_name"].append(table.row_values(i)[1].split(')')[1].split('-')[1])
                        self.md_type_data["speakers"]["people_name"].append(table.row_values(i)[2].split("[")[1].split(",")[0])
                else:
                    print(table.row_values(i)[2].split(':')[0], "--3--", table.row_values(i)[2].split("[")[1].split(",")[0])
                    if table.row_values(i)[2].split(':')[0] in self.md_type_data["role_takers"].keys():
                        if table.row_values(i)[2].split(':')[0] == "IE":
                            self.md_type_data["role_takers"][table.row_values(i)[2].split(':')[0]] += \
                                table.row_values(i)[2].split("[")[1].split(",")[0] + ","
                        else:
                            self.md_type_data["role_takers"][table.row_values(i)[2].split(':')[0]] = table.row_values(i)[2].split("[")[1].split(",")[0]
            else:
                if table.row_values(i)[2].split(':')[0] == "Speaker":
                    if table.row_values(i)[1].find('-') == -1:
                        print(table.row_values(i)[1].split('(')[0], "--4--",
                              table.row_values(i)[2].split("[")[1].split("]")[0])
                    else:
                        print(table.row_values(i)[1].split('(')[0], "--5--",
                              table.row_values(i)[1].split(')')[1].split('-')[1],
                              table.row_values(i)[2].split("[")[1].split("]")[0])
                        self.md_type_data["speakers"]["project_rank"].append(table.row_values(i)[1].split('(')[0])
                        self.md_type_data["speakers"]["project_name"].append(table.row_values(i)[1].split(')')[1].split('-')[1])
                        self.md_type_data["speakers"]["people_name"].append(table.row_values(i)[2].split("[")[1].split("]")[0])
                else:
                    print(table.row_values(i)[2].split(':')[0], "--6--", table.row_values(i)[2].split("[")[1].split("]")[0])
                    if table.row_values(i)[2].split(':')[0] in self.md_type_data["role_takers"].keys():
                        if table.row_values(i)[2].split(':')[0] == "IE":
                            self.md_type_data["role_takers"][table.row_values(i)[2].split(':')[0]] += \
                                table.row_values(i)[2].split("[")[1].split("]")[0] + ","
                        else:
                            self.md_type_data["role_takers"][table.row_values(i)[2].split(':')[0]] = table.row_values(i)[2].split("[")[1].split("]")[0]

    def save_json(self):
        print(json.dumps(self.md_type_data, indent=4))

    def save_speakers(self):
        """"
 ### 103, Balance (2018-08-10)
`TT`  Eve Zhang, Jenny Yu, Jun Liu, Dongchen Tang
`CC7` Siyuan Jia -  kubernetes say hello
`P2` Elvis Jiang - Be like a man
        """
        add_content = "### {0}, {1} ({2})   \n`TT` {3}  \n".format(self.md_type_data["count"], self.md_type_data["theme"],
                                                             self.md_type_data["date"],
                                                             self.md_type_data["speakers"]["TT"])

        for i in range(len(self.md_type_data["speakers"]["project_rank"])):
            add_content = add_content + "`{0}` {1}-{2}   \n".format(self.md_type_data["speakers"]["project_rank"][i].strip(),
                                                                 self.md_type_data["speakers"]["people_name"][i],
                                                                 self.md_type_data["speakers"]["project_name"][i])

        print(add_content)
        with open(os.path.join(self.md_path, "speakers.md"), "a+") as f:
            f.writelines("\n" + add_content)

    def transform_str(self, key):

        return {
            "BTTS": "`Best Table Topic Speech`",
            "BPS": "`Best Prepared Speech`",
            "BE": "`Best Evaluator`"
        }.get(key)

    def save_best_awards(self):
        """"
 ### 101, Self-discipline (2018-07-13)
`Best Table Topic Speech` Nrapendra singh
`Best Prepared Speech` Sarah Zhang
`Best Evaluator` Jony
        """
        add_content = "### {0}, {1} ({2})   \n".format(self.md_type_data["count"], self.md_type_data["theme"],
                                                             self.md_type_data["date"])
        for key, value in self.md_type_data["best_awards"].items():
            if value != "":
                add_content = add_content + "{0} {1} \n".format(self.transform_str(key), value)

        print(add_content)
        with open(os.path.join(self.md_path, "best-awards.md"), "a+") as f:
            f.writelines("\n" + add_content )


    def save_role_takers(self):
        """
### 102, Music (2018-07-27)
`TMD` Michelle Jin
`TTM` Dongchen Tang
`GE` Sarah Zhang
`IE` Jun Liu, Taowen Zhang
`Grammarian` Xin Feng
`Timer` Wujie Zhang
`Ah-Counter` Nrapendra Singh
        """
        add_content = "### {0}, {1} ({2})   \n".format(self.md_type_data["count"], self.md_type_data["theme"],
                                                             self.md_type_data["date"])
        for key, value in self.md_type_data["role_takers"].items():
            if value != "":
                add_content = add_content + "`{0}` {1} \n".format(key, value)

        print(add_content)
        with open(os.path.join(self.md_path, "role-takers.md"), "a+") as f:
            f.writelines("\n" + add_content)

    def save_attendance(self):
        soup = BeautifulSoup(open(os.path.join(self.md_path, "attendance.html")), "html.parser")
        # print(soup.prettify())
        # print(soup.table.contents)
        temp_n = len(soup.find_all('tr'))
        temp_head = []
        name = []
        data = [[] for i in range( temp_n -1)]
        for i, child_tr in enumerate(soup.find_all('tr')):
            # print("!!")
            # print(child_tr)
            for j, child_th in enumerate(child_tr.find_all('th')):
                if i == 0:
                    temp_head.append(child_th.string)
                else:
                    data[i-1].append(child_th.string)
                    if j == 0:
                        name.append(child_th.string)

                # print(child_th.string)
                #
                # print("-----")
        print(temp_head)
        print(data)

        #  TODO up date the temp_head and data
        if self.md_type_data["date"] not in temp_head:              # new record
            temp_head.append(self.md_type_data["date"])
            data[temp_n - 2].append(0)
            print(temp_head)
            print(self.md_type_data["attendance"]["name"].split(","))
            temp_attendance_name_list = self.md_type_data["attendance"]["name"].split(",")
            print(data[:temp_n-1])
            for k, value in enumerate(data[:temp_n-2]):
                # print(k, value)
                if value[0] in temp_attendance_name_list:
                    data[k].append(1)
                    data[temp_n-2][len(temp_head)-1] += 1
                    temp_attendance_name_list.remove(value[0])
                else:
                    data[k].append(0)

            print(data[:temp_n - 1])
            for i, a_name in enumerate(temp_attendance_name_list):
                if a_name != "":
                    print(i, a_name)
                    temp_list = []
                    for j in range(len(temp_head)-2):                        #don't need to include "name" and "1"
                        temp_list.append(0)
                        pass
                    temp_list.append(1)                                       # flag 1 , meaning the attended
                    data[len(data)-1][len(temp_head) - 1] += 1                # total + 1
                    data.insert(temp_n-2+i, list(a_name.strip()) + temp_list)
        else:                                                        # update the record
            pass                                                     # Avoid unnecessary changes not supported it

        # print(temp_head)
        # print(data)

        html_content = """<h1>Attendance</h1>
<table class="table table-condensed table-bordered">
"""
        for i in range(len(data) + 1):
            html_content += "<tr>"
            if i == 0:
                content = temp_head
            else:
                content = data[i-1]
            for j, value in enumerate(content):
                html_content += "<th>{0}</th>".format(value)
            html_content += "</tr>\n"
        html_content += "</table>\n"
        print(html_content)
        with open(os.path.join(self.md_path, "attendance.html"), "w") as f:
            f.writelines(html_content)

    def create_new_record(self):
        print(os.path.exists(self.md_path))
        if not os.path.exists(self.md_path):
            os.makedirs(self.md_path)
        if not os.path.exists(os.path.join(self.md_path, "attendance.html")):
            with open(os.path.join(self.md_path, "attendance.html"), "w") as f:
                f.writelines(template_attendance_for_create_html)

if __name__ == '__main__':
    ag = Agenda(md_path_dir, execl_path)
    ag.get_data()
    # ag.save_json()
    ag.save_speakers()
    ag.save_best_awards()
    ag.save_role_takers()
    ag.save_attendance()
    # ag.create_new_record()