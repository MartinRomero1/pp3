import sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from DB import funcionesdb as fdb


#ventanas

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

        #verificar usuario

        def userSelected():
            return V_Login.cbusuario.currentText()

        def btnlogingetdata():

            #DATOS INGRESADOS
            inputPass = V_Login.inputpassword.text()
            print(userSelected())
            print(inputPass)

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

        self.btnLogin.clicked.connect(btnlogingetdata)


#Listado de Ventas
class ListadoVentas (QDialog):
    def __init__(self):
        super(ListadoVentas,self).__init__()
        uic.loadUi('ListadoVentas.ui',self)

        # TRAER DATOS DE USUARIO LOGUEADO
        #self.lbluser.setText(V_Login.)


        ventas = fdb.consultagral("SELECT USUARIO, DESCRIPCION, PRECIO, FECHA FROM practicaDB.usuarios inner join practicaDB.ventas on practicaDB.usuarios.ID_USUARIO = practicaDB.ventas.ID_USUARIO inner join practicaDB.productos on practicaDB.productos.ID_PRODUCTO = practicaDB.ventas.ID_VENTA")

        #Generar y poblar tabla
        for columna in range (4):
            for fila in range (2):
                self.tbventas.setRowCount(10)
                self.tbventas.setItem ( fila, columna, QtWidgets.QTableWidgetItem ( str(ventas[fila][columna] )) )

        def mostrarVentanaAlta():
            return V_VentanaAlta.show ()

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


#Llamada a ventanas
app = QApplication(sys.argv)
V_Login = Login()
V_VentanaAlta = VentanaAlta()
V_ListadoVentas = ListadoVentas()



#muestra ventanas
V_Login.show()
#V_ListadoVentas.show()
#V_VentanaAlta.show()



app.exec()