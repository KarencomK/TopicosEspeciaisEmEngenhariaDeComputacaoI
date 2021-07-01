#!/usr/bin/env python
import PySimpleGUI as sg
import psutil


GRAPH_WIDTH = 120       # each individual graph size in pixels
GRAPH_HEIGHT = 40
TRANSPARENCY = .8       # how transparent the window looks. 0 = invisible, 1 = normal window
NUM_COLS = 4
POLL_FREQUENCY = 1500    # how often to update graphs in milliseconds
ALPHA = .7
colors = ('#23a0a0', '#56d856', '#be45be', '#5681d8', '#d34545', '#BE7C29', '#d34545')
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

# DashGraph does the drawing of each graph
class DashGraph(object):
    def __init__(self, graph_elem, text_elem, starting_count, color):
        self.graph_current_item = 0
        self.graph_elem = graph_elem        # type: sg.Graph
        self.text_elem = text_elem
        self.prev_value = starting_count
        self.max_sent = 1
        self.color = color
        self.line_list = []                 # list of currently visible lines. Used to delete oild figures
        
    def graph_percentage_abs(self, value):
        self.line_list.append(self.graph_elem.draw_line(            # draw a line and add to list of lines
                (self.graph_current_item, 0),
                (self.graph_current_item, value),
                color=self.color))
        if self.graph_current_item >= GRAPH_WIDTH:
            self.graph_elem.move(-1,0)
            self.graph_elem.delete_figure(self.line_list[0])        # delete the oldest line
            self.line_list = self.line_list[1:]                     # remove line id from list of lines
        else:
            self.graph_current_item += 1

    def text_display(self, text):
        self.text_elem.update(text)

class DashGraph1(object):
    def __init__(self, graph_elem, starting_count, color):
        self.graph_current_item = 0
        self.graph_elem = graph_elem            # type:sg.Graph
        self.prev_value = starting_count
        self.max_sent = 1
        self.color = color
        self.graph_lines = []                # list of currently visible lines. Used to delete oild figures

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

    def graph_percentage_abs1(self, value):
        self.graph_elem.draw_line((self.graph_current_item, 0), (self.graph_current_item, value), color=self.color)
        if self.graph_current_item >= GRAPH_WIDTH:
            self.graph_elem.move(-1, 0)
        else:
            self.graph_current_item += 1
def main():
    # A couple of "User defined elements" that combine several elements and enable bulk edits
    def Txt(text, **kwargs):
        return(sg.Text(text, font=('Helvetica 8'), **kwargs))

    def GraphColumn(name, key):
        return sg.Column([[Txt(name, size=(18,1), key=key+'TXT_'), ],
                    [sg.Graph((GRAPH_WIDTH, GRAPH_HEIGHT), (0, 0), (GRAPH_WIDTH, 100), background_color='pink', key=key+'GRAPH_')]], pad=(2, 2))

    num_cores = len(psutil.cpu_percent(percpu=True))        # get the number of cores in the CPU

    sg.theme('MyColors')
    sg.set_options(element_padding=(0,0), margins=(1,1), border_width=0)

    layout = [[sg.Text('Gráfico em Tempo Real '+' '*18)],
            [GraphColumn('CPU Total Usado', '_CPU_')],]

    # add on the graphs
    for rows in range(num_cores//NUM_COLS+1):
        # for cols in range(min(num_cores-rows*NUM_COLS, NUM_COLS)):
        layout += [[GraphColumn('CPU '+str(rows*NUM_COLS+cols), '_CPU_'+str(rows*NUM_COLS+cols)) for cols in range(min(num_cores-rows*NUM_COLS, NUM_COLS))]]

    # ----------------  Create Window  ----------------
    window = sg.Window('Gráfico', layout, finalize=True)
   # cpu_usage_graph = DashGraph(window['_CPU_GRAPH_'], 0, '#d34545')
    # setup graphs & initial values
    graphs = [DashGraph(window['_CPU_'+str(i)+'GRAPH_'],
                                window['_CPU_'+str(i) + 'TXT_'],
                                0, colors[i%6]) for i in range(num_cores)]
    cpu_usage_graph = DashGraph1(window['_CPU_GRAPH_'], 0, '#d34545')

    # ----------------  main loop  ----------------
    while True :
        # --------- Read and update window once every Polling Frequency --------
        event, values = window.read(timeout=1500)
        if event in (None, 'Exit'):         # Be nice and give an exit
            break
        stats = psutil.cpu_percent(percpu=True)
        # update each graph
        for i, util in enumerate(stats):
            graphs[i].graph_percentage_abs(util)
            graphs[i].text_display('{} CPU {:2.0f}'.format(i, util))
        cpu = psutil.cpu_percent(0)
        cpu_usage_graph.graph_percentage_abs1(cpu)
        window['_CPU_TXT_'].update('{0:2.0f}% CPU Used'.format(cpu))

    window.close()

if __name__ == "__main__":
    main()