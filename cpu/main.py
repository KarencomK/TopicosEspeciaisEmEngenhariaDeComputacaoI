from conexao import criar_conexao, fechar_conexao
import sys
import psutil
import platform
from datetime import datetime
#Biblioteca run a cada hora
import schedule
import time

def insere_cpu(con, Nucleos_Fisicos, Nucleos_Totais, CPU_Freq_MAX_Mhz, CPU_Freq_MIN_Mhz, CPU_Freq_Atual_Mhz, CORE_0, CORE_1, CORE_2, CORE_3, CORE_4,CORE_5,CORE_6,CORE_7, CPU_Total_Usado_Porcentagem):

    cursor=con.cursor()
    sql= "insert into cpu (Nucleos_Fisicos, Nucleos_Totais, CPU_Freq_MAX_Mhz, CPU_Freq_MIN_Mhz, CPU_Freq_Atual_Mhz, CORE_0, CORE_1, CORE_2, CORE_3, CORE_4,CORE_5,CORE_6,CORE_7, CPU_Total_Usado_Porcentagem) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    valores = (Nucleos_Fisicos, Nucleos_Totais, CPU_Freq_MAX_Mhz, CPU_Freq_MIN_Mhz, CPU_Freq_Atual_Mhz, CORE_0, CORE_1, CORE_2, CORE_3, CORE_4,CORE_5,CORE_6,CORE_7, CPU_Total_Usado_Porcentagem)
    cursor.execute(sql, valores)
    cursor.close()
    con.commit()

def main():
    con = criar_conexao("localhost", "root", "", "pythonbd")
    #converte para a  porcentagem.
    def get_size(bytes, suffix="B"):
        """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor

# number of cores
    print("Núcleos físicos:", psutil.cpu_count(logical=False))
    print("Núcleos totais:", psutil.cpu_count(logical=True))
# CPU frequencies

    print(f"Max Frequencia: ", psutil.cpu_freq()[2])
    print(f"Min Frequencia:", psutil.cpu_freq()[1])
    print(f"frequencia usada:", psutil.cpu_freq()[0])
# CPU usage
    print(f"CORE 0: ",psutil.cpu_percent(percpu=True, interval=1)[0])
    print(f"CORE 1: ",psutil.cpu_percent(percpu=True, interval=1)[1])
    print(f"CORE 2: ",psutil.cpu_percent(percpu=True, interval=1)[2])
    print(f"CORE 3: ",psutil.cpu_percent(percpu=True, interval=1)[3])
    print(f"CORE 4: ",psutil.cpu_percent(percpu=True, interval=1)[4])
    print(f"CORE 5: ",psutil.cpu_percent(percpu=True, interval=1)[5])
    print(f"CORE 6: ",psutil.cpu_percent(percpu=True, interval=1)[6])
    print(f"CORE 7: ",psutil.cpu_percent(percpu=True, interval=1)[7])
    print(f"Porcentagem total de CPU usada: ", psutil.cpu_percent())

    insere_cpu(con, psutil.cpu_count(logical=False), psutil.cpu_count(logical=True),psutil.cpu_freq()[2], psutil.cpu_freq()[1] ,psutil.cpu_freq()[0], psutil.cpu_percent(percpu=True, interval=1)[0], psutil.cpu_percent(percpu=True, interval=1)[1], psutil.cpu_percent(percpu=True, interval=1)[2], psutil.cpu_percent(percpu=True, interval=1)[3], psutil.cpu_percent(percpu=True, interval=1)[4], psutil.cpu_percent(percpu=True, interval=1)[5], psutil.cpu_percent(percpu=True, interval=1)[6], psutil.cpu_percent(percpu=True, interval=1)[7],  psutil.cpu_percent() )
    fechar_conexao(con)

schedule.every().hour.do(main)
while True:
    schedule.run_pending()
    time.sleep(1)
if __name__ == '__main__':
    main()

