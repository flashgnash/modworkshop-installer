import requests
import sys
from pzp import pzp

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


headers = {
    "Accept": "Application/json"
}

def get_mods(query):
   
    url = "https://api.modworkshop.net/games/853/mods"
    params = {"query": query, "sort": "score", "limit": 50}
    response = requests.get(url, params=params, headers = headers)
    response.raise_for_status()

    json = response.json()
    
    return json.get("data"),json.get("meta")


def get_mod(id):
    url = f"https://api.modworkshop.net/mods/{id}"

    response = requests.get(url, headers = headers)
    response.raise_for_status()


    json =response.json()

    print(f"Downloading mod  {json.get('id')}: {json.get('name')}")

    if "dependencies" in json:
        deps = json.get("dependencies")

        for dep in deps:
            # print(f"Downloading dependency {dep.get('mod').get('name')}")
            get_mod(dep.get('mod').get('id'))
    return json


def main(search_query=None):

    print(f"{bcolors.WARNING}⚠️this tool is only intended for installing mods, please use the original website{bcolors.OKBLUE} https://modworkshop.net/ {bcolors.WARNING}to discover mods ⚠️{bcolors.ENDC}")
    
    if not search_query:
        search_query = input("Enter search query: ")

    mods, meta = get_mods(search_query)

    total_mods = meta.get('total')



    if not mods:
        print("No mods found.")
        return

    named_mods = {}
    i = 1
    for mod in mods:
        name = mod.get('name','Unknown???')
        named_mods[f"{i}. {name}"] = mod
        i+=1

    if len(mods) < total_mods:
        print("Warning: Not all mods are being retrieved (50 max), please narrow initial search terms.")
    print(f"{len(mods)}/{total_mods} total mods displayed\n------------------")

    chosen_mod_name = pzp(named_mods,fullscreen=False, height=10) 
    chosen_mod = named_mods[chosen_mod_name]
    chosen_mod_id = chosen_mod.get("id")
    
    print(f"You chose: {chosen_mod_name} ({chosen_mod_id})")

    mod_response = get_mod(chosen_mod_id)
    # print(mod_response)


if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else None
    main(query)
