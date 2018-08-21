from crontab import CronTab

gardener_tab = CronTab(user='pi')

class GardenerTab:
    @staticmethod
    def create(params):
        job = gardener_tab.new(command="echo 'HelloWorld'", comment="gardener")
        crontab.write()

    @staticmethod
    def all():
        return [job for job in gardener_tab if job.comment == "gardener"]

    @staticmethod
    def remove_all():
        jobs = GardenerTab.all()
        for job in jobs:
            gardener_tab.remove(job)
        gardener_tab.write()
