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
    # LineStyle → opaque red + width=3
    for ls in root.findall('.//kml:LineStyle', KML_NS):
        c = ls.find('kml:color', KML_NS)
        if c is not None: c.text = 'ff0000ff'
        w = ls.find('kml:width', KML_NS)
        if w is not None: w.text = '3'
    # PolyStyle → outline only
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

def batch_process(files, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    for in_path in files:
        name = os.path.basename(in_path)
        out_path = os.path.join(output_folder, name)
        try:
            style_file(in_path, out_path)
        except Exception as e:
            print(f"Error processing {name}: {e}")

def main():
    root = tk.Tk()
    root.withdraw()

    # 1) выбор нескольких KML-файлов
    files = filedialog.askopenfilenames(
        title="Выберите KML-файлы",
        filetypes=[("KML файлы", "*.kml")],
    )
    if not files:
        return

    # 2) выбор выходной папки
    out_dir = filedialog.askdirectory(title="Куда сохранять стилизованные файлы")
    if not out_dir:
        return

    # 3) обработка
    batch_process(files, out_dir)
    messagebox.showinfo("Готово", f"Обработано файлов: {len(files)}")

if __name__ == '__main__':
    main()
