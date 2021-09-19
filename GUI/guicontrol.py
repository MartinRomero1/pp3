import sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from DB import funcionesdb as fdb
import datetime

def userSelected():
    return (V_Login.cbusuario.currentText ())

def selectedRow():
    if V_ListadoVentas.tbventas.selectedItems() and V_ListadoVentas.isActiveWindow():
        V_ListadoVentas.btnEliminarReg.setEnabled(True)
        V_ListadoVentas.btnModificarReg.setEnabled ( True )
        print('fila venta seleccionada')
        for items in V_ListadoVentas.tbventas.selectedItems():
            print(items.text())

    if V_VentanaAlta.tbproductos.selectedItems() and V_VentanaAlta.isActiveWindow():
        V_VentanaAlta.btnAlta.setEnabled(True)
        print ( 'fila alta seleccionada' )
        for items in V_VentanaAlta.tbproductos.selectedItems():
            print(items.text())
    return items.text()

def mostrarVentanaAlta():
    return V_VentanaAlta.show ()

def btnlogingetdata():


            #DATOS INGRESADOS
            inputPass = V_Login.inputpassword.text()
            print(userSelected())
            print(inputPass)

            #pasaje de usuario a ventana ventas

            userAct = userSelected()
            V_ListadoVentas.lbluser.setText(userAct)
            try:
                userAlta = fdb.consultagral('Select ID_USUARIO from usuarios where USUARIO = ' + '"' + userAct + '"')[0][0]
                V_VentanaAlta.listavendedor.setCurrentIndex (userAlta - 1 )  # el -1 es para compensar que no tiene la opcion USUARIO
            except:
                pass

            #TRAE DATOS DE USUARIO DE BD
            try:
                passDB = str(fdb.consultagral('Select CONTRASENA from usuarios where USUARIO = ' + '"' + userSelected() + '"')[0][0])
            except:
                pass

            #VALIDACION DE USUARIO Y CONTRASEÑA

            if userSelected() == 'Usuario':
                V_Login.lblerror.setText('Seleccione usuario')
            elif passDB == inputPass:
                V_Login.lblerror.setText('Correcto')
                V_ListadoVentas.show()
                V_Login.hide()
            else :
                V_Login.lblerror.setText('Usuario o contraseña incorrecta')



# def getUsuarios():
#     usuarios = fdb.consultagral ( 'Select * from usuarios' )
#     cantusuarios = len ( usuarios )
#     for usuario in range ( cantusuarios ):
#         item = usuarios[usuario][1]


#ventana

#Login
class Login (QDialog):
    def __init__(self):
        super(Login,self).__init__()
        uic.loadUi('Login.ui',self)

        usuarios = fdb.consultagral('Select * from usuarios')
        cantusuarios = len(usuarios)
        for usuario in range(cantusuarios):
            item = usuarios[usuario][1]
            self.cbusuario.addItem(str(item))

        self.btnLogin.clicked.connect(btnlogingetdata)


#Listado de Ventas
class ListadoVentas (QDialog):
    def __init__(self):
        super(ListadoVentas,self).__init__()
        uic.loadUi('ListadoVentas.ui',self)

        # TRAER DATOS DE USUARIO LOGUEADO



        ventas = fdb.consultagral("SELECT USUARIO, DESCRIPCION, PRECIO, FECHA, ventas.ID_VENTA FROM practicaDB.usuarios inner join practicaDB.ventas on practicaDB.usuarios.ID_USUARIO = practicaDB.ventas.ID_USUARIO inner join practicaDB.productos on practicaDB.productos.ID_PRODUCTO = practicaDB.ventas.ID_VENTA")

        #Generar y poblar tabla
        for columna in range (5):
            for fila in range(2):
                self.tbventas.setRowCount(10)
                self.tbventas.setItem ( fila, columna, QtWidgets.QTableWidgetItem ( str(ventas[fila][columna] )) )

        #Seleccion fila
        self.tbventas.clicked.connect(selectedRow)

        self.btnalta.clicked.connect (mostrarVentanaAlta)

#Alta de Ventas
class VentanaAlta (QDialog):
    def __init__(self):
        super(VentanaAlta, self).__init__()
        uic.loadUi('VentanaAlta.ui',self)

        #muestra usuarios para alta
        usuarios = fdb.consultagral ( 'Select * from usuarios' )
        cantusuarios = len ( usuarios )
        for usuario in range ( cantusuarios ):
            item = usuarios[usuario][1]
            self.listavendedor.addItem ( str ( item ) )


            producto = fdb.consultagral ("SELECT DESCRIPCION, PRECIO FROM practicaDB.productos")

            # Generar y poblar tabla
            for columna in range ( 2 ):
                for fila in range ( 8 ):
                    self.tbproductos.setRowCount ( 11 )
                    self.tbproductos.setItem ( fila, columna,QtWidgets.QTableWidgetItem ( str ( producto[fila][columna] ) ) )
        # FECHA Y HORA
        def fechaHora():
            dia = datetime.datetime.now ().strftime ( '%d' )
            mes = datetime.datetime.now ().strftime ( '%m' )
            year = datetime.datetime.now ().strftime ( '%Y' )
            hora = datetime.datetime.now ().strftime ( '%X' )
            fyHora = dia + '/' + mes + '/' + year + ' ' + hora
            return fyHora

        self.lblfecha.setText(fechaHora())

        # ALTA DE VENTA
        self.tbproductos.clicked.connect ( selectedRow )

        def altaVenta():
            idUser = fdb.consultagral ( 'SELECT ID_USUARIO FROM practicaDB.usuarios where USUARIO ='+selectedRow[0] )
            idProducto = fdb.consultagral ( 'SELECT ID_PRODUCTO  FROM practicaDB.productos where DESCRIPCION ='+ +selectedRow[1])
            setAlta = fdb.consultagral('INSERT INTO practicaDB.ventas (ID_USUARIO,ID_PRODUCTO, FECHA) VALUES ("'+idUser+'","'+idProducto+'","'+fechaHora()+'")')

        self.btnAlta.clicked.connect(altaVenta)


#Llamada a ventanas
app = QApplication(sys.argv)
V_Login = Login()
V_VentanaAlta = VentanaAlta()
V_ListadoVentas = ListadoVentas()

# muestra ventanas
V_Login.show()
#V_ListadoVentas.show()
#V_VentanaAlta.show()



app.exec()