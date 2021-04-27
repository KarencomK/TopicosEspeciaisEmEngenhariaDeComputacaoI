from conexao import criar_conexao, fechar_conexao
import sys
import psutil
#Biblioteca run a cada hora
import schedule
import time

def insere_bateria(con, Bateria_Porcentagem,	Tempo_Restante, Carregador_Conectado):

    cursor=con.cursor()
    sql= "insert into bateria (Bateria_Porcentagem,	Tempo_Restante, Carregador_Conectado) values(%s, %s, %s)"
    valores=(Bateria_Porcentagem,	Tempo_Restante, Carregador_Conectado)
    cursor.execute(sql, valores)
    cursor.close()
    con.commit()

def main():

    con= criar_conexao("localhost", "root", "", "pythonbd")
    #Bateria
    def secs2hours(secs):
        mm, ss = divmod(secs, 60)
        hh, mm = divmod(mm, 60)
        return "%d:%02d:%02d" % (hh, mm, ss)
    battery = psutil.sensors_battery()
    print("Porcentagem Bateria",battery.percent)
    print("Carregador Conectado:", battery.power_plugged)
    print("tempo de bateria:", secs2hours(battery.secsleft))
    insere_bateria(con, battery.percent, secs2hours(battery.secsleft), battery.power_plugged)
    fechar_conexao(con)

schedule.every().hour.do(main)
while True:
    schedule.run_pending()
    time.sleep(1)
if __name__ == '__main__':
    main()

