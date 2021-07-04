from csv import reader
from json import load
import xml.etree.ElementTree as ET


class Reader:

    def __init__(self, path):
        self.path = path


    def read_csv(self):

        """
        :return: list as [[(x11,x12),(x21,x22)...(xN1,xN2)],[]...[]]
        """

        with open(self.path, encoding="utf-8") as r_file:
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

        with open(self.path, encoding="utf-8") as r_file:
            reader_object = load(r_file)
            final_list = []
            for item in reader_object['fields']:
                turple_list = [(key, value) for key, value in item.items()]
                final_list.append(turple_list)
            return final_list


    def read_xml(self):

        """
        :return: list as [[(x11,x12),(x21,x22)...(xN1,xN2)],[]...[]]
        """

        with open(self.path, encoding='utf-8') as r_file:
            root = ET.parse(r_file).getroot()
            final_list = []
            for item in root:
                tuple_list = [(sub_item.attrib['name'], sub_item[0].text) for sub_item in item]
                final_list.append(tuple_list)
            return final_list

class Sorter:

    @staticmethod
    def sort_list_by_tuple(tuple_list):
        pass



if __name__ == "__main__":
    csv = Reader('csv_data_1.csv')
    print(csv.read_csv())
    json = Reader('json_data.json')
    print(json.read_json())
    xml = Reader('xml_data.xml')
    print(xml.read_xml())