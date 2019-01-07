# coding = utf-8

import json
import requests
import datetime

class NGAJsonParser(object):
    def __init__(self):
        self.thread_dict = {
            "-7": "maelstrom",
            "436": "it",
            "334": "hardware",
            "498": "secondhand",
            "422": "hearthstone",
            "7": "14t",
            "310": "forward",
            "182": "mage",
            "414": "game",
            "-8961121": "jx3",
            "-2371813": "eve"
        }
        self.freegame_url = "https://bbs.nga.cn/thread.php?stid=12002550&lite=js"
        self.thread_url = "https://bbs.nga.cn/thread.php?fid={fid}&page={page}&lite=js"
        self.subject_url = "https://bbs.nga.cn/read.php?tid={tid}&_ff={fid}&page={page}&lite=js"
        self._load_cookies()
        self.JSON_STRAT_INDEX = 33
        pass

    def _load_cookies(self):
        with open("config.json", "r") as f:
            self.cookies = json.load(f)

    def _content_to_json(self, response):
        # window.script_muti_get_var_store={"d
        try:
            json_dict = json.loads(response.content.decode("gbk")[self.JSON_STRAT_INDEX:])
        except:
            json_dict = eval(response.content.decode("gbk")[self.JSON_STRAT_INDEX:])
        return json_dict

    def _timestamp_to_str(self, timestamp):
        dt = datetime.datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M")

    def view_thread(self, thread_id, page):
        url = self.thread_url.format(fid=thread_id, page=page)
        r = requests.get(url, headers=self.cookies)
        response_dict = self._content_to_json(r)
        
        response_data = response_dict["data"]
        subjects = response_data["__T"]
        for index in subjects:
            print("tid = {}".format(subjects[index]["tid"]))
            print("fid = {}".format(subjects[index]["fid"]))
            print("author = {}".format(subjects[index]["author"]))
            print("subject = {}".format(subjects[index]["subject"]))
            print("postdate = {}".format(self._timestamp_to_str(subjects[index]["postdate"]))) # timestamp
            print("replies = {}".format(subjects[index]["replies"]))
            print("------------------------------------------")
        pass

    def view_subject(self, thread_id, subject_id, page):
        ## main 
        main_url = self.subject_url.format(fid=thread_id, tid=subject_id, page=1)
        main_r = requests.get(main_url, headers=self.cookies)
        main_response_dict = self._content_to_json(main_r)
        
        main_response_data = main_response_dict["data"]
        main_data = main_response_data["__R"]["0"]
        
        print("subject = {}".format(main_data["subject"]))
        # print("authorid = {}".format(replies[index]["authorid"]))
        print("main_content = {}".format(main_data["content"]))
        print("postdate = {}".format(main_data["postdate"]))
        print("##############################################")

        ## replies
        url = self.subject_url.format(fid=thread_id, tid=subject_id, page=page)
        r = requests.get(url, headers=self.cookies)
        response_dict = self._content_to_json(r)

        response_data = response_dict["data"]
        replies = response_data["__R"]
        for index in replies:
            print("tid = {}".format(replies[index]["tid"]))
            print("fid = {}".format(replies[index]["fid"]))
            # print("authorid = {}".format(replies[index]["authorid"]))
            print("content = {}".format(replies[index]["content"]))
            print("postdate = {}".format(replies[index]["postdate"]))
            print("------------------------------------------")


if __name__ == "__main__":
    parser = NGAJsonParser()
    parser.view_thread(7, 1)
    parser.view_subject(7, 16053030, 1)
