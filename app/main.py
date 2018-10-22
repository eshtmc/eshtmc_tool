from update_data import Agenda
from git_eshtmc import Eshtmc
from config import Config


def main():

    ag = Agenda(Config)
    tm = Eshtmc(Config)

    tm.git_clone()

    # ag.create_new_record()
    # ag.save_json()
    # ag.save_speakers()
    # ag.save_best_awards()
    # ag.save_role_takers()
    ag.save_attendance()


    tm.git_add()
    tm.git_commit()
    tm.git_push()


if __name__ == '__main__':
    main()

