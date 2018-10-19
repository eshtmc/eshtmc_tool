#!/usr/bin/env python

from bs4 import BeautifulSoup
import json
import os
from config import *

class Agenda:
    def __init__(self, md_path):
        self.md_path = md_path
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
            "role_takers": ROLE_TAKERS,
            "speakers": {
                "TT": TableTopic,
                "perpared_speackers": PERPARED_SPEACKERS,
            }
        }

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

        for i in range(len(self.md_type_data["speakers"]["perpared_speackers"])):
            if self.md_type_data["speakers"]["perpared_speackers"][i]["project_rank"].strip() != "":
                add_content = add_content + "`{0}` {1}-{2}   \n".format(self.md_type_data["speakers"]["perpared_speackers"][i]["project_rank"].strip(),
                                                                     self.md_type_data["speakers"]["perpared_speackers"][i]["people_name"],
                                                                     self.md_type_data["speakers"]["perpared_speackers"][i]["project_name"])
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
                add_content = add_content + "{0} {1}    \n".format(self.transform_str(key), value)

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
                add_content = add_content + "`{0}` {1}   \n".format(key, value)

        print(add_content)
        with open(os.path.join(self.md_path, "role-takers.md"), "a+") as f:
            f.writelines("\n" + add_content)

    def save_attendance(self):
        soup = BeautifulSoup(open(os.path.join(self.md_path, "attendance.html")), "html.parser")
        temp_n = len(soup.find_all('tr'))
        temp_head = []
        name = []
        data = [[] for i in range(temp_n - 1)]
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

        #         print("-----")
        # print(temp_head)
        # print(data)

        for i in data:
            sum = 0
            for j in i[1:]:
                if j != 0:
                    sum += int(j)
            print(i[0:1], sum, i)

        #  TODO up date the temp_head and data
        if self.md_type_data["date"] not in temp_head and temp_head != []:              # new record
            temp_head.append(self.md_type_data["date"])
            data[temp_n - 2].append(0)
            print(temp_head)
            print(self.md_type_data["attendance"]["name"].split(","))
            temp_attendance_name_list = self.md_type_data["attendance"]["name"]. split(",")
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
                    temp_list.append(str(a_name))
                    for j in range(len(temp_head)-2):                        #don't need to include "name" and "1"
                        temp_list.append(0)
                        pass
                    temp_list.append(1)                                       # flag 1 , meaning the attended
                    data[len(data)-1][len(temp_head) - 1] += 1                # total + 1
                    data.insert(temp_n-2+i, temp_list)
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
        print(HTML_ATTENDANCE_head+html_content+HTML_ATTENDANCE_end)
        with open(os.path.join(self.md_path, "attendance.html"), "w") as f:
            f.writelines(HTML_ATTENDANCE_head+html_content+HTML_ATTENDANCE_end)
            print("write....")

    def create_new_record(self):
        print(os.path.exists(self.md_path))
        if not os.path.exists(self.md_path):
            os.makedirs(self.md_path)
            with open("eshtmc.github.io/index.md", "a+") as f:
                f.writelines("\n" + INDEX_ADD)
        temp = "#### [Home](https://eshtmc.github.io/)    \n"
        if not os.path.exists(os.path.join(self.md_path, "attendance.html")):
            with open(os.path.join(self.md_path, "attendance.html"), "w") as f:
                f.writelines(HTML_ATTENDANCE_head+New_Table+HTML_ATTENDANCE_end)
        if not os.path.exists(os.path.join(self.md_path, "best-awards.md")):
            with open(os.path.join(self.md_path, "best-awards.md"), "w") as f:
                f.writelines(temp)
        if not os.path.exists(os.path.join(self.md_path, "role-takers.md")):
            with open(os.path.join(self.md_path, "role-takers.md"), "w") as f:
                f.writelines(temp)
        if not os.path.exists(os.path.join(self.md_path, "speakers.md")):
            with open(os.path.join(self.md_path, "speakers.md"), "w") as f:
                f.writelines(temp)


if __name__ == '__main__':
    ag = Agenda(md_path_dir)
    ag.create_new_record()
    ag.save_json()
    ag.save_speakers()
    ag.save_best_awards()
    ag.save_role_takers()
    ag.save_attendance()
