import sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
from DB import funcionesdb as fdb
import datetime

def userSelected():
    return (V_Login.cbusuario.currentText ())

def vendedorSelected():
    return (V_VentanaModif.listavendedor.currentText ())

def listadoVentasSelectedRow():
    if V_ListadoVentas.tbventas.selectedItems():
        V_ListadoVentas.btnEliminarReg.setEnabled(True)
        V_ListadoVentas.btnModificarReg.setEnabled ( True )
        print('fila venta seleccionada')
        listaitems = []
        for items in V_ListadoVentas.tbventas.selectedItems():
           listaitems.append(items.text())
        print ( listaitems )
        return listaitems

def ventanaAltaSelectedRow():
    V_VentanaAlta.btnAlta.setEnabled(True)
    print ( 'fila alta seleccionada' )
    listaitems = []
    for items in V_VentanaAlta.tbproductos.selectedItems():
        listaitems.append(items.text())
    print(listaitems)
    return listaitems

def ventanaModifSelectedRow():
    print ( 'fila modificar seleccionada' )
    listaitems = []
    for items in  V_VentanaModif.tbproductos.selectedItems():
        listaitems.append(items.text())
    print(listaitems)
    return listaitems

def mostrarVentanaAlta():
    return V_VentanaAlta.show ()

def mostrarVentanaModif():
    return V_VentanaModif.show()

def btnlogingetdata():


            #DATOS INGRESADOS
            inputPass = V_Login.inputpassword.text()
            print('Usuario seleccionado: '+userSelected())
            print('Constrasena ingresada: '+inputPass)

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
                print('contrasena de la base: '+ passDB)
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

def updateVentas():
    ventas = fdb.consultagral (
        "select USUARIO,DESCRIPCION,PRECIO,FECHA,ID_VENTA FROM practicaDB.ventas inner join practicaDB.usuarios on practicaDB.ventas.ID_USUARIO = practicaDB.usuarios.ID_USUARIO inner join practicaDB.productos on practicaDB.ventas.ID_PRODUCTO = practicaDB.productos.ID_PRODUCTO;" )
    print ( ventas )
    # Generar y poblar tabla
    for columna in range ( 5 ):
        for fila in range ( len ( ventas ) ):
            V_ListadoVentas.tbventas.setRowCount ( len ( ventas ) )
            # print('ventas'+ str(len(ventas)))

            V_ListadoVentas.tbventas.setItem ( fila, columna,QtWidgets.QTableWidgetItem ( str ( ventas[fila][columna] ) ) )

#ventanas

#Ventana Login
class Login (QDialog):
    def __init__(self):
        super(Login,self).__init__()
        uic.loadUi('Login.ui',self)

        usuarios = fdb.consultagral('Select * from usuarios') #upgrade select usuario sacar el [1] para llevarla a global
        cantusuarios = len(usuarios)
        for usuario in range(cantusuarios):
            item = usuarios[usuario][1]
            self.cbusuario.addItem(str(item))

        self.btnLogin.clicked.connect(btnlogingetdata)

#Ventana Listado de Ventas
class ListadoVentas (QDialog):
    def __init__(self):
        super(ListadoVentas,self).__init__()
        uic.loadUi('ListadoVentas.ui',self)

        # TRAER DATOS DE USUARIO LOGUEADO

        # updateVentas()

        ventas = fdb.consultagral("select USUARIO,DESCRIPCION,PRECIO,FECHA,ID_VENTA FROM practicaDB.ventas inner join practicaDB.usuarios on practicaDB.ventas.ID_USUARIO = practicaDB.usuarios.ID_USUARIO inner join practicaDB.productos on practicaDB.ventas.ID_PRODUCTO = practicaDB.productos.ID_PRODUCTO;")
        print ( ventas )
        #Generar y poblar tabla
        for columna in range (5):
            for fila in range( len ( ventas ) ):
                self.tbventas.setRowCount( len ( ventas ) )


                self.tbventas.setItem ( fila, columna, QtWidgets.QTableWidgetItem ( str(ventas[fila][columna] )) )

        def eliminarVenta():
            idVenta = int(listadoVentasSelectedRow()[4])
            print(idVenta)
            fdb.consultaModif ("DELETE FROM practicaDB.ventas WHERE ID_VENTA = "+str(idVenta))
            print("DELETE FROM practicaDB.ventas WHERE ID_VENTA = "+str(idVenta))
            V_ListadoVentas.setVisible(False)
            updateVentas ()
            V_ListadoVentas.tbventas.clearSelection()
            V_ListadoVentas.btnEliminarReg.setEnabled(False)
            V_ListadoVentas.btnModificarReg.setEnabled (False)
            V_ListadoVentas.setVisible(True)
            if ventanaAltaSelectedRow():
                V_ListadoVentas.btnEliminarReg.setEnabled ( True )
                V_ListadoVentas.btnModificarReg.setEnabled ( True )

        def mensajeAdvertenciaBorrado():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Eliminar registro")
            msg.setText("Está seguro que desea eliminar este registro?")
            si = msg.addButton('Porsupu', QtWidgets.QMessageBox.YesRole)
            no = msg.addButton('Nopo', QtWidgets.QMessageBox.NoRole)
            x = msg.exec_()




        self.tbventas.clicked.connect(listadoVentasSelectedRow)
        self.btnalta.clicked.connect (mostrarVentanaAlta)
        self.btnEliminarReg.clicked.connect(mensajeAdvertenciaBorrado) #cambiar este para poner mensaje de advertencia
        self.btnModificarReg.clicked.connect(mostrarVentanaModif)

#Ventana Alta de Ventas
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
                for fila in range ( len ( producto ) ):
                    self.tbproductos.setRowCount ( len ( producto ) )
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
        self.tbproductos.clicked.connect ( ventanaAltaSelectedRow )

        def altaVenta():
            idUser = str(fdb.consultagral ( 'SELECT ID_USUARIO FROM practicaDB.usuarios where USUARIO = "'+ userSelected()+'"')[0][0])
            idProducto = str(fdb.consultagral ( 'SELECT ID_PRODUCTO FROM practicaDB.productos where DESCRIPCION ="'+ ventanaAltaSelectedRow()[0]+'"')[0][0])
            setAlta = str(fdb.consultaModif('INSERT INTO practicaDB.ventas (ID_USUARIO,ID_PRODUCTO, FECHA) VALUES ('+idUser+','+idProducto+',"'+fechaHora()+'")'))
            print('INSERT INTO practicaDB.ventas (ID_USUARIO,ID_PRODUCTO, FECHA) VALUES ('+idUser+','+idProducto+',"'+fechaHora()+'")')
            V_VentanaAlta.hide()
            V_ListadoVentas.hide()
            updateVentas()
            V_ListadoVentas.show()
            return setAlta
        self.btnAlta.clicked.connect(altaVenta)

#Ventana Modificacion
class VentanaModif (QDialog):
    def __init__(self):
        super(VentanaModif, self).__init__()
        uic.loadUi('VentanaModif.ui',self)

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
                    self.tbproductos.setRowCount ( 8 )
                    self.tbproductos.setItem ( fila, columna,QtWidgets.QTableWidgetItem ( str ( producto[fila][columna] ) ) )
        # FECHA Y HORA
        def fechaHora():
            dia = datetime.datetime.now ().strftime ( '%d' )
            mes = datetime.datetime.now ().strftime ( '%m' )
            year = datetime.datetime.now ().strftime ( '%Y' )
            hora = datetime.datetime.now ().strftime ( '%X' )
            fyHora = dia + '/' + mes + '/' + year + ' ' + hora
            return fyHora

        self.lblfecha.setText("No se puede modificar la fecha")

        # MODIF DE VENTA
        self.tbproductos.clicked.connect ( ventanaModifSelectedRow )

        def modifVenta():
            if self.listavendedor.currentText() == 'USUARIO':
                self.lblerror.setText('Seleccione usuario')
            elif not self.tbproductos.selectedItems():
                self.lblerror.setText('Seleccione producto')
            else:
                self.lblerror.setText('Funciona OK')

                idUser = str(fdb.consultagral('SELECT ID_USUARIO FROM practicaDB.usuarios where USUARIO = "' + self.listavendedor.currentText() + '"')[0][0])
                idProducto = str(fdb.consultagral('SELECT ID_PRODUCTO FROM practicaDB.productos where DESCRIPCION ="' + ventanaModifSelectedRow()[0] + '"')[0][0])
                idVenta = str(fdb.consultagral('SELECT ID_VENTA FROM practicaDB.ventas where ID_VENTA = ' +listadoVentasSelectedRow()[4])[0][0])
                updateItem = str(fdb.consultaModif('UPDATE practicaDB.ventas SET ID_USUARIO = '+idUser+', ID_PRODUCTO = '+idProducto+' where ID_VENTA = '+idVenta))
                print('UPDATE practicaDB.ventas SET ID_USUARIO = '+idUser+', ID_PRODUCTO = '+idProducto+' where ID_VENTA = '+idVenta)

                V_VentanaModif.hide()
                V_ListadoVentas.hide()
                updateVentas()
                V_ListadoVentas.show()
            return updateItem

        self.btnAlta.clicked.connect(modifVenta)

#Llamada a ventanas
app = QApplication(sys.argv)
V_Login = Login()
V_VentanaAlta = VentanaAlta()
V_ListadoVentas = ListadoVentas()
V_VentanaModif = VentanaModif()

# muestra ventanas
V_Login.show()
#V_ListadoVentas.show()
#V_VentanaAlta.show()

app.exec()