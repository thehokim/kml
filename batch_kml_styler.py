#!/usr/bin/env python3
import os
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog, messagebox

# KML namespace
KML_NS = {'kml': 'http://www.opengis.net/kml/2.2'}
NS_URI = KML_NS['kml']
ET.register_namespace('', NS_URI)

def style_file(in_path, out_path):
    tree = ET.parse(in_path)
    root = tree.getroot()
    # красим линию в красный, ширина 3
    for ls in root.findall('.//kml:LineStyle', KML_NS):
        c = ls.find('kml:color', KML_NS)
        if c is not None: c.text = 'ff0000ff'
        w = ls.find('kml:width', KML_NS)
        if w is not None: w.text = '3'
    # только контур у полигонов
    for ps in root.findall('.//kml:PolyStyle', KML_NS):
        c = ps.find('kml:color', KML_NS)
        if c is not None: c.text = 'ff0000ff'
        fill = ps.find('kml:fill', KML_NS)
        if fill is None:
            ET.SubElement(ps, f'{{{NS_URI}}}fill').text = '0'
        else:
            fill.text = '0'
        outl = ps.find('kml:outline', KML_NS)
        if outl is None:
            ET.SubElement(ps, f'{{{NS_URI}}}outline').text = '1'
        else:
            outl.text = '1'
    tree.write(out_path, encoding='utf-8', xml_declaration=True)

def process_folder(in_folder, out_folder):
    cnt = 0
    for fname in os.listdir(in_folder):
        if fname.lower().endswith('.kml'):
            src = os.path.join(in_folder, fname)
            dst = os.path.join(out_folder,  fname)
            try:
                style_file(src, dst)
                cnt += 1
            except Exception as e:
                print(f"Ошибка в {fname}: {e}")
    return cnt

def main():
    root = tk.Tk()
    root.withdraw()

    # 1) Собираем список входных папок
    input_dirs = []
    while True:
        d = filedialog.askdirectory(title="Выберите папку с KML (Cancel — стоп)")
        if not d:
            break
        input_dirs.append(d)
    if not input_dirs:
        return

    # 2) Папка-назначение
    out_dir = filedialog.askdirectory(title="Куда сохранять обработанные файлы")
    if not out_dir:
        return

    # 3) Стартуем
    total = 0
    for folder in input_dirs:
        total += process_folder(folder, out_dir)

    messagebox.showinfo(
        "Готово",
        f"Обработано всего: {total} файлов\nИз папок:\n" +
        "\n".join(input_dirs)
    )

if __name__ == '__main__':
    main()
