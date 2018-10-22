import os
import subprocess
from config import Config


class Eshtmc:
    def __init__(self, config):
        self.config = config

    def git_operation(self, operation):
        pass

    def git_clone(self):
        if not os.path.exists(self.config.repository_save_path):
            cmd = "git clone " + self.config.repository_url
            result = subprocess.call(cmd, shell=True)
            return result

    def git_add(self):
        cmd = "git add ."
        result = subprocess.call(cmd, shell=True, cwd=self.config.repository_save_path)
        return result

    def git_commit(self, message=Config.Message):
        cmd = "git commit -m '{0}'".format(message)
        result = subprocess.call(cmd, shell=True, cwd=self.config.repository_save_path)
        return result

    def git_push(self):
        cmd = "git push origin master"
        result = subprocess.call(cmd, shell=True, cwd=self.config.repository_save_path)
        return result


if __name__ == '__main__':
    pass
    # tm = Eshtmc(Config)
    # tm.git_clone()
    # tm.git_add()
    # tm.git_commit()
    # tm.git_push()
