#!/usr/bin/env python

from bs4 import BeautifulSoup
import json
import os
from config import Config

class Agenda:
    def __init__(self, config):
        self.config = config
        self.create_new_record()
        self.md_type_data = {
            "date": self.config.MEETING_DATE,
            "count": self.config.MEETING_COUNT,
            "theme": self.config.MEETING_THEME,
            "attendance": {
                "name": self.config.AttendanceName
            },
            "best_awards": {
                "BTTS": self.config.BestTableTopicSpeech,
                "BPS": self.config.BestPreparedSpeech,
                "BE": self.config.BestEvaluator
            },
            "role_takers": self.config.ROLE_TAKERS,
            "speakers": {
                "TT": self.config.TableTopic,
                "perpared_speackers": self.config.PERPARED_SPEACKERS,
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
        with open(os.path.join(self.config.md_path_dir, "speakers.md"), "a+") as f:
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
        with open(os.path.join(self.config.md_path_dir, "best-awards.md"), "a+") as f:
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
        with open(os.path.join(self.config.md_path_dir, "role-takers.md"), "a+") as f:
            f.writelines("\n" + add_content)

    def save_attendance(self):
        soup = BeautifulSoup(open(os.path.join(self.config.md_path_dir, "attendance.html")), "html.parser")
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
        print(self.config.HTML_ATTENDANCE_head+html_content+self.config.HTML_ATTENDANCE_end)
        with open(os.path.join(self.config.md_path_dir, "attendance.html"), "w") as f:
            f.writelines(self.config.HTML_ATTENDANCE_head+html_content+self.config.HTML_ATTENDANCE_end)
            print("write....")

    def create_new_record(self):
        print(os.path.exists(self.config.md_path_dir))
        if not os.path.exists(self.config.md_path_dir):
            os.makedirs(self.config.md_path_dir)
            with open("eshtmc.github.io/index.md", "a+") as f:
                f.writelines("\n" + self.config.INDEX_ADD)
        temp = "#### [Home](https://eshtmc.github.io/)    \n"
        if not os.path.exists(os.path.join(self.config.md_path_dir, "attendance.html")):
            with open(os.path.join(self.config.md_path_dir, "attendance.html"), "w") as f:
                f.writelines(self.config.HTML_ATTENDANCE_head+self.config.New_Table+self.config.HTML_ATTENDANCE_end)
        if not os.path.exists(os.path.join(self.config.md_path_dir, "best-awards.md")):
            with open(os.path.join(self.config.md_path_dir, "best-awards.md"), "w") as f:
                f.writelines(temp)
        if not os.path.exists(os.path.join(self.config.md_path_dir, "role-takers.md")):
            with open(os.path.join(self.config.md_path_dir, "role-takers.md"), "w") as f:
                f.writelines(temp)
        if not os.path.exists(os.path.join(self.config.md_path_dir, "speakers.md")):
            with open(os.path.join(self.config.md_path_dir, "speakers.md"), "w") as f:
                f.writelines(temp)


if __name__ == '__main__':
    ag = Agenda(Config)
    ag.create_new_record()
    ag.save_json()
    ag.save_speakers()
    ag.save_best_awards()
    ag.save_role_takers()
    ag.save_attendance()
