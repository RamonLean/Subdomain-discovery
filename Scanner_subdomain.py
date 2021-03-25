import requests
import argparse
print ("\n\nExemplo de uso:\nScanner_subdominio.py example.com -l lista_subdominios.txt\n\n")

parser = argparse.ArgumentParser()
parser.add_argument("dominio", help="Digite o dominio com ""exemplo.com" "")
parser.add_argument("-l", "--lista", help="Arquivo de texto com a lista a ser testada")

args = parser.parse_args()
dominio = args.dominio
subs_testar= args.lista
try:
    arquivo = open(subs_testar)
    conteudo = arquivo.read()
    subdominos =conteudo.splitlines()
except:
    print("Arquivo não encontrado")
    exit()
descobertos_subs = []
for subdominio in subdominos:
    url = f"http://{subdominio}.{dominio}"
    try:
        requests.get(url,timeout=5)
    except requests.ConnectionError:
        #print(url, "Não existe")
        pass
    except requests.Timeout:
        pass
    else:
        print("[+] Subdomíno descoberto:", url)
        descobertos_subs.append(url)

with open("subs_descobertos.txt", "w") as f:
    for subdominio in descobertos_subs:
        print(subdominio, file=f)
print("Finalizado")
