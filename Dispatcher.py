from CalculationUnit import CalculationUnit
from Server import ServerDispatcher
from Process import Process
from Table import Table

class Dispatcher:
    def __init__(self):
        self.dict_of_calculation_unit = dict()
        self.server = None
        self.resultat = None
        self.callback = None
        self.nbResponseRequired = None

    def add_calculation_unit(self, *listof_calculation_unit):
        """
        :param listof_calculation_unit: Une liste d'unités de calcul
        :type listof_calculation_unit: list(CalculationUnit)
        :return:
        """
        for calculUnit in listof_calculation_unit:
            self.dict_of_calculation_unit[calculUnit.get_address()] = calculUnit

    def setResponseCallback(self, mth):
        self.callback = mth

    def prepare(self):
        self.server = ServerDispatcher(self, 8111, 8192, len(list(self.dict_of_calculation_unit.keys())))
        self.server.start()

        for key in self.dict_of_calculation_unit.keys():
            calculation_unit = self.dict_of_calculation_unit[key]
            if not self.server.connect(calculation_unit):
                self.server.stop_server()
                return False
            else:
                code = calculation_unit.get_code_process()
                self.server.send(calculation_unit, "CODE-" + str(calculation_unit.get_process().__class__.__name__))
                self.server.send(calculation_unit, code)
                self.server.send(calculation_unit, "ENDCODE")

        return True

    def run(self):
        for calculation_unit in list(self.dict_of_calculation_unit.values()):
            self.server.send(calculation_unit, "RUN")

    def join(self, index, resultat):
        self.resultat.get_node(index).set_data(resultat)
        self.nbResponseRequired -= 1
        print(self.nbResponseRequired)
        if self.nbResponseRequired == 0:
            self.callback(self.resultat)

    def distribute_data(self, data):
        """

        :param data:
        :type data: Table
        :return:
        """

        self.nbResponseRequired = data.N
        self.resultat = Table(data.N, data.size)

        i = 0
        for calculation_unit in list(self.dict_of_calculation_unit.values()):
            calculation_unit.set_node_index(i)
            self.server.send(calculation_unit, "DATA")
            self.server.send(calculation_unit, str(data.get_node(i).get_data()))
            self.server.send(calculation_unit, "ENDDATA")
            i += 1
