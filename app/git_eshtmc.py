import os
import subprocess
from config import Message

class Eshtmc():

    def __init__(self, repository_url):
        self.repository_url = repository_url
        self.path = "./eshtmc.github.io"

    def git_operation(self, operation):
        pass

    def git_clone(self):
        if not os.path.exists(self.path):
            cmd = "git clone " + self.repository_url
            result = subprocess.call(cmd, shell=True)
            return result

    def git_add(self):
        cmd = "git add ."
        result = subprocess.call(cmd, shell=True, cwd=self.path)
        return result

    def git_commit(self, message=""):
        cmd = "git commit -m '{0}'".format(message)
        result = subprocess.call(cmd, shell=True, cwd=self.path)
        return result

    def git_push(self):
        cmd = "git push origin master"
        result = subprocess.call(cmd, shell=True, cwd=self.path)
        return result


if __name__ == '__main__':
    tm = Eshtmc("git@github.com:eshtmc/eshtmc.github.io.git")
    tm.git_clone()
    tm.git_add()
    tm.git_commit(Message)
    tm.git_push()