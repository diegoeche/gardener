from crontab import CronTab

gardener_tab = CronTab(user='pi')

COMMANDS = {
    "0": "python /home/pi/gardener/irrigate.py 0",
    "1": "python /home/pi/gardener/irrigate.py 1",
    "2": "python /home/pi/gardener/irrigate.py 2",
    "3": "python /home/pi/gardener/irrigate.py 3",
    "4": "python /home/pi/gardener/irrigate.py 4",
    "5": "python /home/pi/gardener/irrigate.py 5"
}

class GardenerTab:
    @staticmethod
    def create(params):
        title = params["title"]
        frequency = params["frequency"]
        amount = params["amount"]
        commandId = params["command"]

        comment = ",".join(["gardener", title, commandId, amount])

        command = "%s %s" % (COMMANDS[params["command"]], amount)

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
