from Dispatcher import Dispatcher
from CalculationUnit import CalculationUnit
from MyProcess import MyProcess
from Table import Table


dispatcher = Dispatcher()
unite1 = CalculationUnit("127.0.0.1", 4898)
#unite2 = CalculationUnit("127.0.0.1", 4899)
processMultiplyArray = MyProcess()

unite1.attach_process(processMultiplyArray)
#unite2.attach_process(processMultiplyArray)

#  unite2 = CalculationUnit("192.168.1.12", 4898)
#  unite1.attach_process(processMultiplyArray)

dispatcher.add_calculation_unit(unite1)
#dispatcher.add_calculation_unit(unite2)

def endTask(resultat):
    print(resultat.to_string())

t1 = Table(1, 64)
for i in range(0, 64):
    t1.append(i)

if dispatcher.prepare():
    print("YES")
    dispatcher.distribute_data(t1)
    dispatcher.setResponseCallback(endTask)
    dispatcher.run()
    #  dispatcher.emit()
    #  dispatcher.join()
