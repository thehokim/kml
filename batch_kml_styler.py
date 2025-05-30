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
    # LineStyle → красная линия, ширина 3
    for ls in root.findall('.//kml:LineStyle', KML_NS):
        c = ls.find('kml:color', KML_NS)
        if c is not None: c.text = 'ff0000ff'
        w = ls.find('kml:width', KML_NS)
        if w is not None: w.text = '3'
    # PolyStyle → только контур (outline=1, fill=0)
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

def batch_process(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    kmz = [f for f in os.listdir(input_folder) if f.lower().endswith('.kml')]
    for fname in kmz:
        src = os.path.join(input_folder,   fname)
        dst = os.path.join(output_folder,  fname)
        try:
            style_file(src, dst)
        except Exception as e:
            print(f"Ошибка при обработке {fname}: {e}")
    return len(kmz)

def main():
    root = tk.Tk()
    root.withdraw()  # прячем главное окно

    # 1) Выбор папки с исходными KML
    in_dir = filedialog.askdirectory(title="Выберите папку с KML-файлами")
    if not in_dir:
        return

    # 2) Выбор папки для результатов
    out_dir = filedialog.askdirectory(title="Куда сохранять обработанные файлы")
    if not out_dir:
        return

    # 3) Обработка всех KML из in_dir
    count = batch_process(in_dir, out_dir)
    messagebox.showinfo("Готово", f"Обработано {count} файлов.")

if __name__ == '__main__':
    main()
