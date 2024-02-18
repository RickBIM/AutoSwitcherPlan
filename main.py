import wmi
import subprocess

class PowerPlanManage():
    def __init__(self):
        self.power_plan_order = open("power_plan_order.txt", "r")
        self.power_plan_priorit = {}
        self.apps_plan = open("apps_list.txt", "r")
        for line in self.power_plan_order:
            self.power_plan_priorit[line[0:line.find(":")]] = line[line.find(":")+1:line.find("\n")]


    # Defina o plano de energia desejado
    def get_guid_power_plan(self, name):
        get_power_plan_list = f'powercfg /LIST'
        power_plan_list = subprocess.run(get_power_plan_list, shell=True, check=True, stdout=subprocess.PIPE).stdout.decode('utf-8').splitlines()
        power_plan_dict = {}
        for i, line in enumerate(power_plan_list):
            if i == 0 or i == 1 or i == 2:
                continue
            line = line.replace("GUID do Esquema de Energia: ", "")
            GUID = line[0:line.find(" ")]
            _name = line[line.find("(") + 1:line.find(")")]
            power_plan_dict[_name] = GUID
        GUID = power_plan_dict[name]
        return GUID

    

    def get_plan(self):
        # Iterating through all the running processes
        running_process = set()
        # Initializing the wmi constructor
        f = wmi.WMI()
        for process in f.Win32_Process():
            running_process.add(process.Name)

        priorits = set()
        for line in self.apps_plan:
            if line[0:line.find(":")] in running_process:
                plan = line[line.find(":")+1:line.find("\n")]
                priorit = self.power_plan_priorit[plan]
                priorits.add(priorit)
        try:
            plan_priorit = max(list(priorits))
        except:
            return "Economia de energia"
        for key, value in self.power_plan_priorit.items():
            if value == plan_priorit:
                return key
        return "Economia de energia"
        # Comando para definir o plano de energia

    def set_power_plan(self):
        subprocess.run(f'powercfg /setactive {self.get_guid_power_plan(self.get_plan())}', shell=True, check=True)

if __name__ == '__main__':
    power_manage = PowerPlanManage()
    power_manage.set_power_plan()