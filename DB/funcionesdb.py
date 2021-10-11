import mysql.connector
from datetime import date

# 'Mavericks123!' desktop
# '' netbook

dbconn= {
   'host' : 'localhost',
   'user' : 'root',
   'password' : '',
   'database' : 'practicaDB'
}

def consultagral(sql):
   conexion = mysql.connector.connect ( **dbconn )
   cursor = conexion.cursor ()
   cursor.execute(sql)
   resultado = cursor.fetchall()
   return resultado

def consultaModif(sql):
   conexion = mysql.connector.connect ( **dbconn )
   cursor = conexion.cursor ()
   cursor.execute(sql)
   conexion.commit()
   resultado = cursor.fetchall()
   return resultado

#consulta listaventas

# SELECT USUARIO, DESCRIPCION, PRECIO, FECHA FROM practicaDB.usuarios
# inner join practicaDB.ventas
# on practicaDB.usuarios.ID_USUARIO = practicaDB.ventas.ID_USUARIO
# inner join practicaDB.productos
# on practicaDB.productos.ID_PRODUCTO = practicaDB.ventas.ID_VENTA
