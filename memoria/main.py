from conexao import criar_conexao, fechar_conexao
import sys
import psutil
import platform
from datetime import datetime
# Biblioteca run a cada hora
import schedule
import time


def insere_memoria(con, Virtual_Total_Gb, Virtual_Disponivel_Gb, Virtual_Usada_Gb, Virtual_Porcentagem, Swap_Total_Gb, Swap_Disponivel_Gb, Swap_Usada_Gb, Swap_Porcentagem, Disco, Tipo_Sistema_Arquivos, Disco_Total_Gb, Disco_Usado_Gb, Disco_Disponivel_Gb, Disco_Porcentagem, Disco_Total_Read_Gb, Disco_Total_Write_Gb):

    cursor = con.cursor()
    sql = "insert into memoria (Virtual_Total_Gb, Virtual_Disponivel_Gb, Virtual_Usada_Gb, Virtual_Porcentagem, Swap_Total_Gb, Swap_Disponivel_Gb, Swap_Usada_Gb, Swap_Porcentagem, Disco, Tipo_Sistema_Arquivos, Disco_Total_Gb, Disco_Usado_Gb, Disco_Disponivel_Gb, Disco_Porcentagem, Disco_Total_Read_Gb, Disco_Total_Write_Gb) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    valores = (Virtual_Total_Gb, Virtual_Disponivel_Gb, Virtual_Usada_Gb, Virtual_Porcentagem, Swap_Total_Gb, Swap_Disponivel_Gb, Swap_Usada_Gb, Swap_Porcentagem, Disco, Tipo_Sistema_Arquivos, Disco_Total_Gb, Disco_Usado_Gb, Disco_Disponivel_Gb, Disco_Porcentagem, Disco_Total_Read_Gb, Disco_Total_Write_Gb)
    cursor.execute(sql, valores)
    cursor.close()
    con.commit()


def main():
    con = criar_conexao("localhost", "root", "", "pythonbd")

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

# get the memory details
    svmem = psutil.virtual_memory()
    print(f"Total:", get_size(svmem.total))
    print(f"Available:", get_size(svmem.available))
    print(f"Used:", get_size(svmem.used))
    print(f"Percentage:", svmem.percent)

# get the swap memory details (if exists)
    swap = psutil.swap_memory()
    print(f"Total:", get_size(swap.total))
    print(f"Free:", get_size(swap.free))
    print(f"Used:", get_size(swap.used))
    print(f"Percentage:", swap.percent)

    print("Partitions and Usage:")
# get all disk partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(f"  Mountpoint:", partition.mountpoint)
        print(f"  File system type:", partition.fstype)
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            # this can be catched due to the disk that
            # isn't ready
            continue
    print(f"  Total Size:", get_size(partition_usage.total))
    print(f"  Used: ", get_size(partition_usage.used))
    print(f"  Free: ", get_size(partition_usage.free))
    print(f"  Percentage:", partition_usage.percent)
# get IO statistics since boot
    disk_io = psutil.disk_io_counters()
    print(f"Total read: ", get_size(disk_io.read_bytes))
    print(f"Total write:", get_size(disk_io.write_bytes))

    insere_memoria(con, get_size(svmem.total), get_size(svmem.available), get_size(svmem.used), svmem.percent, get_size(swap.total), get_size(swap.free), get_size(swap.used), swap.percent, partition.mountpoint, partition.fstype, get_size(partition_usage.total), get_size(partition_usage.used), get_size(partition_usage.free), partition_usage.percent, get_size(disk_io.read_bytes), get_size(disk_io.write_bytes))
    fechar_conexao(con)

schedule.every().hour.do(main)
while True:
    schedule.run_pending()
    time.sleep(1)
if __name__ == '__main__':
    main()