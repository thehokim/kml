import os
import xml.etree.ElementTree as ET
import PySimpleGUI as sg

# KML namespace
KML_NS = {'kml': 'http://www.opengis.net/kml/2.2'}
NS_URI = KML_NS['kml']
ET.register_namespace('', NS_URI)

def style_file(in_path, out_path):
    tree = ET.parse(in_path)
    root = tree.getroot()

    # LineStyle → opaque red + width=3
    for ls in root.findall('.//kml:LineStyle', KML_NS):
        c = ls.find('kml:color', KML_NS)
        if c is not None: c.text = 'ff0000ff'
        w = ls.find('kml:width', KML_NS)
        if w is not None: w.text = '3'

    # PolyStyle → outline only
    for ps in root.findall('.//kml:PolyStyle', KML_NS):
        # color (outline)
        c = ps.find('kml:color', KML_NS)
        if c is not None: c.text = 'ff0000ff'
        # fill=0
        fill = ps.find('kml:fill', KML_NS)
        if fill is None:
            ET.SubElement(ps, f'{{{NS_URI}}}fill').text = '0'
        else:
            fill.text = '0'
        # outline=1
        outl = ps.find('kml:outline', KML_NS)
        if outl is None:
            ET.SubElement(ps, f'{{{NS_URI}}}outline').text = '1'
        else:
            outl.text = '1'

    tree.write(out_path, encoding='utf-8', xml_declaration=True)

def batch_process(input_folder, output_folder, window):
    os.makedirs(output_folder, exist_ok=True)
    kmz = [f for f in os.listdir(input_folder) if f.lower().endswith('.kml')]
    total = len(kmz)
    for idx, fname in enumerate(kmz, 1):
        in_f = os.path.join(input_folder, fname)
        out_f = os.path.join(output_folder, fname)
        try:
            style_file(in_f, out_f)
            window['-PROG-'].update(current_count=idx)
        except Exception as e:
            print(f"Error on {fname}: {e}")
    sg.popup(f'Готово!\nОбработано {total} файлов.')

def main():
    sg.theme('DarkGrey13')
    layout = [
        [sg.Text('Input KML folder'), sg.Input(key='-IN-'), sg.FolderBrowse()],
        [sg.Text('Output folder'),    sg.Input(key='-OUT-'), sg.FolderBrowse()],
        [sg.ProgressBar(max_value=1, orientation='h', size=(40, 20),
                        key='-PROG-', expand_x=True,
                        bar_color=('green','gray'))],
        [sg.Button('Process'), sg.Button('Exit')]
    ]
    window = sg.Window('Batch KML Styler', layout, finalize=True)

    while True:
        event, vals = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event == 'Process':
            in_folder = vals['-IN-']
            out_folder = vals['-OUT-']
            if not os.path.isdir(in_folder):
                sg.popup_error('Укажи корректную папку с KML.')
                continue
            files = [f for f in os.listdir(in_folder) if f.lower().endswith('.kml')]
            if not files:
                sg.popup('В папке нет .kml файлов.')
                continue
            window['-PROG-'].update(max=len(files), current_count=0)
            batch_process(in_folder, out_folder, window)

    window.close()

if __name__ == '__main__':
    main()
