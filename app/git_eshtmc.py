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
            self.git_config()
            return result

    def git_config(self):
        cmd1 = "git config --local --add user.name {0}".format("eshtmc")
        cmd2 = "git config --local --add user.email {0}".format("github@eshtmc.com")
        subprocess.call(cmd1, shell=True, cwd=self.config.repository_save_path)
        subprocess.call(cmd2, shell=True, cwd=self.config.repository_save_path)

    def git_pull(self):
        cmd = "git pull --rebase"
        result = subprocess.call(cmd, shell=True, cwd=self.config.repository_save_path)
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
        self.git_pull()
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
