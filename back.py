import mysql.connector

def read_bateria_porcentagem():
    con = mysql.connector.connect(host='localhost', database='pythonbd', user='root', password='')
    cursor= con.cursor()
    cursor.execute("SELECT Bateria_Porcentagem, Tempo_Restante, Data FROM bateria WHERE Data BETWEEN CURRENT_DATE()-7 AND CURRENT_DATE()")
    resultado=cursor.fetchall()
    return resultado

def read_bateria_porcentagem_diario():
    con = mysql.connector.connect(host='localhost', database='pythonbd', user='root', password='')
    cursor= con.cursor()
    cursor.execute("SELECT Bateria_Porcentagem, Tempo_Restante, Data FROM bateria WHERE DATE(Data) = CURDATE()")
    resultado=cursor.fetchall()
    return resultado

def read_bateria_porcentagem_quinzenal():
    con = mysql.connector.connect(host='localhost', database='pythonbd', user='root', password='')
    cursor= con.cursor()
    cursor.execute("SELECT Bateria_Porcentagem, Tempo_Restante, Data FROM bateria WHERE Data > now() - INTERVAL 15 day")
    resultado=cursor.fetchall()
    return resultado

def read_bateria_porcentagem_mensal():
    con = mysql.connector.connect(host='localhost', database='pythonbd', user='root', password='')
    cursor= con.cursor()
    cursor.execute("SELECT Bateria_Porcentagem, Tempo_Restante, Data FROM bateria WHERE MONTH(Data) = 6")
    resultado=cursor.fetchall()
    return resultado

def read_cpu_diario():
    con = mysql.connector.connect(host='localhost', database='pythonbd', user='root', password='')
    cursor= con.cursor()
    cursor.execute("SELECT CPU_Total_Usado_Porcentagem, CORE_0, CORE_1, CORE_2, CORE_3, CORE_4, CORE_5, CORE_6, CORE_7, Data FROM cpu WHERE DATE(Data) = CURDATE()")
    resultado1=cursor.fetchall()
    return resultado1

def read_cpu():
    con = mysql.connector.connect(host='localhost', database='pythonbd', user='root', password='')
    cursor= con.cursor()
    cursor.execute("SELECT CPU_Total_Usado_Porcentagem, CORE_0, CORE_1, CORE_2, CORE_3, CORE_4, CORE_5, CORE_6, CORE_7, Data FROM cpu WHERE Data BETWEEN CURRENT_DATE()-7 AND CURRENT_DATE()")
    resultado1=cursor.fetchall()
    return resultado1

def read_cpu_quinzenal():
    con = mysql.connector.connect(host='localhost', database='pythonbd', user='root', password='')
    cursor= con.cursor()
    cursor.execute("SELECT CPU_Total_Usado_Porcentagem, CORE_0, CORE_1, CORE_2, CORE_3, CORE_4, CORE_5, CORE_6, CORE_7, Data FROM cpu WHERE Data > now() - INTERVAL 15 day")
    resultado1=cursor.fetchall()
    return resultado1

def read_cpu_mensal():
    con = mysql.connector.connect(host='localhost', database='pythonbd', user='root', password='')
    cursor= con.cursor()
    cursor.execute("SELECT CPU_Total_Usado_Porcentagem, CORE_0, CORE_1, CORE_2, CORE_3, CORE_4, CORE_5, CORE_6, CORE_7, Data FROM cpu WHERE MONTH(Data) = 6")
    resultado1=cursor.fetchall()
    return resultado1

def read_memoria_diario():
    con = mysql.connector.connect(host='localhost', database='pythonbd', user='root', password='')
    cursor= con.cursor()
    cursor.execute("SELECT Disco_Total_Read_Gb, Disco_Total_Write_Gb, Disco_Porcentagem, Data FROM memoria WHERE DATE(Data) = CURDATE()")
    resultado2=cursor.fetchall()
    return resultado2

def read_memoria():
    con = mysql.connector.connect(host='localhost', database='pythonbd', user='root', password='')
    cursor= con.cursor()
    cursor.execute("SELECT Disco_Total_Read_Gb, Disco_Total_Write_Gb, Disco_Porcentagem, Data FROM memoria WHERE Data BETWEEN CURRENT_DATE()-7 AND CURRENT_DATE()")
    resultado2=cursor.fetchall()
    return resultado2

def read_memoria_quinzenal():
    con = mysql.connector.connect(host='localhost', database='pythonbd', user='root', password='')
    cursor= con.cursor()
    cursor.execute("SELECT Disco_Total_Read_Gb, Disco_Total_Write_Gb, Disco_Porcentagem, Data FROM memoria WHERE Data > now() - INTERVAL 15 day")
    resultado2=cursor.fetchall()
    return resultado2

def read_memoria_mensal():
    con = mysql.connector.connect(host='localhost', database='pythonbd', user='root', password='')
    cursor= con.cursor()
    cursor.execute("SELECT Disco_Total_Read_Gb, Disco_Total_Write_Gb, Disco_Porcentagem, Data FROM memoria WHERE MONTH(Data) = 6")
    resultado2=cursor.fetchall()
    return resultado2