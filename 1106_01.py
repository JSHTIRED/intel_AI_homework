from factory_controller  import FactoryController


def controlqq(A,ctrl):
    if A =='1':
        FactoryController.system_start(ctrl)
        print('1')
    elif A == '2':
        FactoryController.system_stop(ctrl)
        print('2')
    elif A == '3':
        FactoryController.red=True
    elif A == '4':
        FactoryController.orange=True
        print('4')
    elif A == '5':
        FactoryController.green=True
        print('5')
    elif A == '6':
        FactoryController.conveyor
        print('6')
    elif A == '7':
        FactoryController.push_actuator
        print('7')
    elif A == '8':
        FactoryController.push_actuator
        print('8')
    else:
        print('error, range: 1~8')


try:
  with FactoryController('/dev/ttyACM0') as ctrl:
    B = input("put in number: ")
    print(B)
    controlqq(B, ctrl)
except Exception as e:
  print("An error occ:urred:", str(e))
ctrl.close()
