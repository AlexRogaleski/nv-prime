import fileinput
import sys

filename = "/etc/X11/xorg.conf.d/nvidia.conf"
# filename = "nvidia.conf"
text_to_search_yes = "Option \"PrimaryGPU\" \"yes\""
text_to_search_no = "Option \"PrimaryGPU\" \"no\""
replacement_text_yes = "Option \"PrimaryGPU\" \"yes\""
replacement_text_no = "Option \"PrimaryGPU\" \"no\""

def status():
    global filename
    global text_to_search_yes

    dgpu_ativa = 0

    with open(filename) as f:
        if text_to_search_yes in f.read():
            dgpu_ativa = 1

    if(dgpu_ativa == 1):
        print('Gráfico NVIDIA Ativo!')
    else:
        print('Gráfico Híbrido Ativo!')

def change():
   
    global filename
    global text_to_search_yes
    global text_to_search_no
    global replacement_text_yes
    global replacement_text_no

    dgpu_ativa = 1

    with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
        for line in file:
            
            if(line.find(text_to_search_yes) != -1):
                dgpu_ativa = 0
                print(line.replace(text_to_search_yes, replacement_text_no), end='')
            else:
                print(line.replace(text_to_search_no, replacement_text_yes), end='')

    if(dgpu_ativa == 1):
        print('dGPU (Discreta - NVIDIA) definida como padrão! Encerre a sessão para aplicar as mudanças!')
    else:
        print('iGPU (Interna - INTEL) definida como padrão! Encerre a sessão para aplicar as mudanças!')

if(len(sys.argv) > 1):
    if(sys.argv[1] == '-c' or sys.argv[1] == '--change'):
        change()
    elif(sys.argv[1] == '-s' or sys.argv[1] == '--status'):
        status()
    elif(sys.argv[1] == '-h' or sys.argv[1] == '--help'):
        print('uso: nv-prime -c')
        print('')
        print('Argumentos')
        print('  -c, --change    Alterna entre "gráfico híbrido", que usa a iGPU (Intel) por padrão e a dGPU (NVIDIA) para aplicativos específicos. E "gráfico NVIDIA" onde a dGPU é ativada por padrão para todo o processamento.')
        print('  -s, --status    Informa o modo gráfico ativo.')
        print('  -h, --help      Mostra esta ajuda.')
else:
    print('nv-prime: falta de argumentos')
    print('Tente "nv-prime --help" para mais informações.')
