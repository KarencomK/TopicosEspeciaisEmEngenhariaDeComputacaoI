#!/usr/bin/env python
import PySimpleGUI as sg
import psutil

GRAPH_WIDTH, GRAPH_HEIGHT = 120, 40       # each individual graph size in pixels
ALPHA = .7

class DashGraph(object):
    def __init__(self, graph_elem, starting_count, color):
        self.graph_current_item = 0
        self.graph_elem = graph_elem            # type:sg.Graph
        self.prev_value = starting_count
        self.max_sent = 1
        self.color = color
        self.graph_lines = []

    def graph_value(self, current_value):
        delta = current_value - self.prev_value
        self.prev_value = current_value
        self.max_sent = max(self.max_sent, delta)
        percent_sent = 100 * delta / self.max_sent
        line_id = self.graph_elem.draw_line((self.graph_current_item, 0), (self.graph_current_item, percent_sent), color=self.color)
        self.graph_lines.append(line_id)
        if self.graph_current_item >= GRAPH_WIDTH:
            self.graph_elem.delete_figure(self.graph_lines.pop(0))
            self.graph_elem.move(-1, 0)
        else:
            self.graph_current_item += 1
        return delta

    def graph_percentage_abs(self, value):
        self.graph_elem.draw_line((self.graph_current_item, 0), (self.graph_current_item, value), color=self.color)
        if self.graph_current_item >= GRAPH_WIDTH:
            self.graph_elem.move(-1, 0)
        else:
            self.graph_current_item += 1


def human_size(bytes, units=(' bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB')):
    """ Returns a human readable string reprentation of bytes"""
    return str(bytes) + units[0] if bytes < 1024 else human_size(bytes >> 10, units[1:])

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


def main():
    # ----------------  Create Window  ----------------
    sg.theme('MyColors')
    sg.set_options(element_padding=(0, 0), margins=(1, 1), border_width=0)

    def GraphColumn(name, key):
        layout = [
            [sg.Text(name, size=(18,1), font=('Helvetica 8'), key=key+'TXT_')],
            [sg.Graph((GRAPH_WIDTH, GRAPH_HEIGHT),
                      (0, 0),
                      (GRAPH_WIDTH, 100),
                      background_color='pink',
                      key=key+'GRAPH_')]]
        return sg.Col(layout, pad=(2, 2))

    layout = [
        [sg.Text('Gráfico em Tempo Real '+' '*18)],
        [GraphColumn('Bateria Procentagem', '_BATERI_READ_')]]

    window = sg.Window('Gráfico', layout, finalize=True)

    battery = psutil.sensors_battery()
    bat_porcent_graph = DashGraph(window['_BATERI_READ_GRAPH_'],  battery.percent, '#00FFFF')

    # print(psutil.cpu_percent(percpu=True))
    # ----------------  main loop  ----------------
    while True :
        # --------- Read and update window once a second--------
        event, values = window.read(timeout=1000)
        # Be nice and give an exit, expecially since there is no titlebar
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        bat = psutil.sensors_battery().percent
       
        bat_porcent_graph.graph_percentage_abs(bat)
        window['_BATERI_READ_TXT_'].update('{}% Bateria Restante'.format(bat))


if __name__ == "__main__":
    main()