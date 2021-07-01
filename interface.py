import PySimpleGUI as sg
import back
import grafico_memoria
import grafico_cpu
import grafico_bateria
##########################################################################
#layout janelas e estilo
sg.LOOK_AND_FEEL_TABLE['MyColors'] = {'BACKGROUND': '#f9f3f3',
                                  'TEXT': '#f25287',
                                  'INPUT': '#f1d1d0',
                                  'TEXT_INPUT': '#f25287',
                                  'SCROLL': '#f7d9d9',
                                  'BUTTON': ('#f7d9d9', '#f25287', ),
                                  'PROGRESS': sg.DEFAULT_PROGRESS_BAR_COLOR,
                                  'BORDER': 0, 'SLIDER_DEPTH': 0,
                                  'PROGRESS_DEPTH': 0,
                                  'ACCENT1': '#f7d9d9',
                                  'ACCENT2': '#FF5C93',
                                  'ACCENT3': '#C5003C'}
##############################################################################

bateria = back.read_bateria_porcentagem
cpu = back.read_cpu
memoria = back.read_memoria

def janela_layout ():
    sg.change_look_and_feel('MyColors')
    layout = [
    [sg.Text('Escolha a Opção de Monitoramento:')],
    [sg.Button('Bateria'), sg.Button('  CPU  '), sg.Button('Memória')],
    ]
    return sg.Window('Inicio', layout= layout, finalize=True)

headings = ['Porcentagem Bateria','Tempo' ,'Data']
data=[[]]
def janela_bateria():
    sg.change_look_and_feel('MyColors')
    layout=[
        [sg.Text('Dados de Monitoramento da Bateria', font=("Franklin Gothic Book", 20)) ],
        [sg.Text('')],
        [sg.Checkbox('Diário', key='diario'), sg.Checkbox('Semanal', key='semanal'), sg.Checkbox('Quinzenal', key='quinzenal'), sg.Checkbox('Mensal', key='mensal'),sg.Button('Selecionar'), sg.Text(''), sg.Button('Plotar Gráfico da Bateria')],
        #[sg.Button('Dados Diários'),sg.Text(''),sg.Button('Dados Semanais'),sg.Text(''), sg.Button('Dados Quinzenais'),sg.Text(''), sg.Button('Dados Mensais')],
        [sg.Text('')],
        [sg.Table(values=data, headings=headings, auto_size_columns = False , col_widths = [ 20 , 20 , 20 ], key='-TABLE-')],
        [sg.Button('Voltar')]
    ]
    return sg.Window('janela bateria', layout= layout, finalize=True)

headings1 = ['Porcentagem CPU','CORE_0', 'CORE_1', 'CORE_2', 'CORE_3', 'CORE_4', 'CORE_5', 'CORE_6', 'CORE_7','Data']
data1=[[]]
def janela_CPU():
    sg.change_look_and_feel('MyColors')
    layout=[
        [sg.Text('Dados do Monitoramento da CPU', font=("Franklin Gothic Book", 20)) ],
        [sg.Text('')],
        [sg.Checkbox('Diário', key='diario'), sg.Checkbox('Semanal', key='semanal'), sg.Checkbox('Quinzenal', key='quinzenal'), sg.Checkbox('Mensal', key='mensal'),sg.Button('Selecionar'), sg.Text(''), sg.Button('Plotar Gráfico da CPU')],
        [sg.Text('')],
        [sg.Table(values=data1, headings=headings1, auto_size_columns = False , col_widths = [ 15 , 10 , 10, 10 , 10 , 10, 10 , 10 , 10,20 ], key='-TABLEI-')],
        [sg.Button('Voltar')]
    ]
    return sg.Window('janela cpu', layout= layout, finalize=True)

headings2 = ['Disco Read', 'Disco Write', 'Porcentagem Usada ','Data']
data2=[[]]
def janela_memoria():
    sg.change_look_and_feel('MyColors')
    layout=[
        [sg.Text('Dados do Monitoramento da Memoria', font=("Franklin Gothic Book", 20))],
        [sg.Checkbox('Diário', key='diario'), sg.Checkbox('Semanal', key='semanal'), sg.Checkbox('Quinzenal', key='quinzenal'), sg.Checkbox('Mensal', key='mensal'),sg.Button('Selecionar'),sg.Text(''), sg.Button('Plotar Gráfico da Memória')],
        [sg.Text('')],
        [sg.Table(values=data2, headings=headings2, auto_size_columns = False , col_widths = [ 20 , 20 , 20, 20 ], key='-TABLEII-')],
        [sg.Button('Voltar')]
    ]
    return sg.Window('janela memoria', layout=layout, finalize=True)

#Janela inicial
janela1, janela2, janela3, janela4 = janela_layout(), None, None, None

#Leitura de Eventos
while True :
    window, event, values = sg.read_all_windows()
#Janela fechada
    if window == janela1 and event == sg.WIN_CLOSED:
        break
    if window == janela1 and event == 'Bateria':
        janela2 = janela_bateria()
        janela1.hide()
    if window == janela2 and event == 'Voltar':
        janela2.hide()
        janela1.un_hide()
    if window == janela1 and event == '  CPU  ':
        janela3 = janela_CPU()
        janela1.hide()
    if window == janela3 and event == 'Voltar':
        janela3.hide()
        janela1.un_hide()
    if window == janela1 and event == 'Memória':
        janela4 = janela_memoria()
        janela1.hide()
    if window == janela4 and event == 'Voltar':
        janela4.hide()
        janela1.un_hide()
        #SELECT DOS DADOS DA TABELA 
        #BATERIA
    if window == janela2 and  event == 'Selecionar':
        if values['diario'] == True:
            bateria=back.read_bateria_porcentagem_diario()
            window.find_element('-TABLE-').update(bateria)
    if window == janela2 and  event == 'Selecionar':
        if values['semanal'] == True:
            bateria=back.read_bateria_porcentagem()
            window.find_element('-TABLE-').update(bateria)    
    if window == janela2 and  event == 'Selecionar':
        if values['quinzenal'] == True:
            bateria=back.read_bateria_porcentagem_quinzenal()
            window.find_element('-TABLE-').update(bateria)    
    if window == janela2 and  event == 'Selecionar':
        if values['mensal'] == True:
            bateria=back.read_bateria_porcentagem_mensal()
            window.find_element('-TABLE-').update(bateria)   
    #CPU
    if window == janela3 and  event == 'Selecionar':
        if values['diario'] == True:
            cpu=back.read_cpu_diario()
            window.find_element('-TABLEI-').update(cpu)   
    if window == janela3 and  event == 'Selecionar':
        if values['semanal'] == True:
            cpu=back.read_cpu()
            window.find_element('-TABLEI-').update(cpu)
    if window == janela3 and  event == 'Selecionar':
        if values['quinzenal'] == True:
            cpu=back.read_cpu_quinzenal()
            window.find_element('-TABLEI-').update(cpu)
    if window == janela3 and  event == 'Selecionar':
        if values['mensal'] == True:
            cpu=back.read_cpu_mensal()
            window.find_element('-TABLEI-').update(cpu)   
        #MEMORIA
    if window == janela4 and  event == 'Selecionar':
        if values['diario'] == True:
            memoria=back.read_memoria_diario()
            window.find_element('-TABLEII-').update(memoria)
    if window == janela4 and  event == 'Selecionar':
        if values['semanal'] == True:
            memoria=back.read_memoria()
            window.find_element('-TABLEII-').update(memoria)
    if window == janela4 and  event == 'Selecionar':
        if values['quinzenal'] == True:
            memoria=back.read_memoria_quinzenal()
            window.find_element('-TABLEII-').update(memoria)
    if window == janela4 and  event == 'Selecionar':
        if values['mensal'] == True:
            memoria=back.read_memoria_mensal()
            window.find_element('-TABLEII-').update(memoria)        
        #PLOTA OS GRAFICOS
    if event == 'Plotar Gráfico da Memória':
        plotmemoria=grafico_memoria.main()
    if event == 'Plotar Gráfico da CPU':
        plotcpu=grafico_cpu.main()
    if event == 'Plotar Gráfico da Bateria':
        plotbateria=grafico_bateria.main()