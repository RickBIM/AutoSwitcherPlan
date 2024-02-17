import wmi
import subprocess
 
# # Initializing the wmi constructor
# f = wmi.WMI()
 
# # Iterating through all the running processes
# running_process = set()
# for process in f.Win32_Process():
#     ...
#     # Displaying the P_ID and P_Name of the process
#     running_process.add(process.Name)
# [print(item) for item in running_process]



# Defina o plano de energia desejado
def get_guid_power_plan(name):
    get_power_plan_list = f'powercfg /LIST'
    power_plan_list = subprocess.run(get_power_plan_list, shell=True, check=True, stdout=subprocess.PIPE).stdout.decode('utf-8').splitlines()
    power_plan_dict = {}
    for i, line in enumerate(power_plan_list):
        if i == 0 or i == 1 or i == 2:
            continue
        line = line.replace("GUID do Esquema de Energia: ", "")
        GUID = line[0:line.find(" ")]
        name = line[line.find("(") + 1:line.find(")")]
        power_plan_dict[name] = GUID
    # [print(item + " : " + power_plan_dict[item]) for item in power_plan_dict]

    GUID = power_plan_dict[name]
    return GUID

file = open("power_plan_order.txt", "r")
[print(line.replace("\n", "")) for line in file]

# Comando para definir o plano de energia
set_power_plan = f'powercfg /setactive {get_guid_power_plan("Economia de energia")}'

# Execute o comando no terminal
subprocess.run(set_power_plan, shell=True, check=True)
