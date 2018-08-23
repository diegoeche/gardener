from crontab import CronTab

gardener_tab = CronTab(user='pi')

COMMANDS = {
    "1": "echo 'Hello World! 1'",
    "2": "echo 'Hello World! 2'",
    "3": "echo 'Hello World! 3'",
}

class GardenerTab:
    @staticmethod
    def create(params):
        title = params["title"]
        frequency = params["frequency"]
        comment = "gardener,%s" % title
        command = COMMANDS[params["command"]]

        job = gardener_tab.new(command=command, comment=comment)
        job.setall(frequency)
        gardener_tab.write()

    @staticmethod
    def all():
        return [job for job in gardener_tab if job.comment.split(",")[0] == "gardener"]

    @staticmethod
    def remove_all():
        jobs = GardenerTab.all()
        for job in jobs:
            gardener_tab.remove(job)
        gardener_tab.write()

    @staticmethod
    def remove_by_id(id):
        jobs = GardenerTab.all()
        gardener_tab.remove(jobs[id])
        gardener_tab.write()
