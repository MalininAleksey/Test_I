from csv import reader, writer, DictWriter
from json import load
import xml.etree.ElementTree as ET
from pprint import pprint


class Reader:

    def __init__(self, file_name):
        self.file_name = file_name

    def read_file(self):
        if ".csv" in self.file_name:
            return self.read_csv()
        elif ".xml" in self.file_name:
            return self.read_xml()
        elif ".json" in self.file_name:
            return self.read_json()

    def read_csv(self):

        """
        :return: list as [[(x11,x12),(x21,x22)...(xN1,xN2)],[]...[]]
        """

        with open(self.file_name, encoding="utf-8") as r_file:
            reader_object = reader(r_file, delimiter=",")
            count = 0
            final_list = []
            for row in reader_object:
                if count == 0:
                    title = row
                else:
                    content = row
                    tuple_list = [(title[i], v) for i, v in enumerate(content)]
                    final_list.append(tuple_list)
                count += 1
            return final_list


    def read_json(self):

        """
        :return: list as [[(x11,x12),(x21,x22)...(xN1,xN2)],[]...[]]
        """

        with open(self.file_name, encoding="utf-8") as r_file:
            reader_object = load(r_file)
            final_list = []
            for item in reader_object['fields']:
                turple_list = [(key, str(value)) for key, value in item.items()]
                final_list.append(turple_list)
            return final_list


    def read_xml(self):

        """
        :return: list as [[(x11,x12),(x21,x22)...(xN1,xN2)],[]...[]]
        """

        with open(self.file_name, encoding='utf-8') as r_file:
            root = ET.parse(r_file).getroot()
            final_list = []
            for item in root:
                tuple_list = [(sub_item.attrib['name'], sub_item[0].text) for sub_item in item]
                final_list.append(tuple_list)
            return final_list


class DataWorker:

    @staticmethod
    def sort_list_by_tuple(tuple_list):
        for item in tuple_list:
            item.sort(key=lambda element: (element[0][0], int(element[0][1:(len(element[0]))])), reverse=False)
        return tuple_list

    @staticmethod
    def unite_data(*args):
        title_list = []
        content = []
        for item in args:
            for sub_item in item:
                for sub_sub_item in sub_item:
                    title_list.append([element[0] for element in sub_sub_item])
                    content.append([element[1] for element in sub_sub_item])
        title = min(title_list, key=len)
        cut_content = [item[:len(title)] for item in content]
        return title, cut_content

    @staticmethod
    def sort_by_param_name(param_name, list):
        index = list[0].index(param_name)
        sorted_list = [(item[index], item) for item in list[1]]
        sorted_list.sort(key=lambda element: element[0])
        final_content_list = [item[1] for item in sorted_list]
        return [list[0]] + final_content_list


class Writer:

    def __init__(self, data):
        self.data = data

    def write_in_tsv(self, file_name):
        with open(file_name, 'w', encoding='utf-8', newline='') as wr_file:
            tsv_writer = writer(wr_file, delimiter='\t')
            for item in self.data:
                tsv_writer.writerow(item)







if __name__ == "__main__":
    input_data = ['csv_data_1.csv', 'csv_data_2.csv', 'json_data.json', 'xml_data.xml']
    #Читаем данные из файлов и сразу сортируем по именам заголовков
    collect_data = [DataWorker.sort_list_by_tuple(Reader(item).read_file()) for item in input_data]
    pprint(collect_data)
    #Объединяем все в единый список
    unite_data = DataWorker.unite_data(collect_data)
    pprint(unite_data)
    #Сортируем по содержимое по выбранному заголовку
    sorted_data = DataWorker.sort_by_param_name('D1', unite_data)
    #Записываем в файл
    Writer(sorted_data).write_in_tsv('test_3.tsv')