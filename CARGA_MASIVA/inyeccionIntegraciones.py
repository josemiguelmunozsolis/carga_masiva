#Estas funciones reciben 4 parámetros (precios y fechas), retornando "trozo de json" para agregar a put, por lo mismo es importante validar datos antes de retornar, además se debe separar integrations de la ficha de Centry
import pandas as pd
import numpy as np
import requests
import json

excel_entrante = pd.read_excel('precios.xlsx', na_filter=False)
df = pd.DataFrame(excel_entrante)
access_token = ""


def extraerMKPDesdeExcel(marketplace, nombre_col_pn, nombre_col_po, nombre_col_fi, nombre_col_ff):
  df = pd.DataFrame(excel_entrante)
  #ELECCIÓN DEFINE SI SE AGREGARÁ EL CAMPO AL JSON
  eleccion_pn = 0
  eleccion_po = 0
  eleccion_fi = 0
  eleccion_ff = 0
  columnas = []
  col_to_extract = []
  id_producto = "Id Producto Centry (USO EXCLUSIVO SOPORTE)"
  id_variante = "Id Variante Centry (USO EXCLUSIVO SOPORTE)"

  col_to_extract.append(id_producto)
  col_to_extract.append(id_variante)

  for col_name in df.columns: 
    columnas.append(col_name)


  if nombre_col_pn in columnas:
     eleccion_pn = 1
  col_to_extract.append(nombre_col_pn)
  
  if nombre_col_po in columnas:
    eleccion_po = 1
  col_to_extract.append(nombre_col_po)

  if nombre_col_fi in columnas:
    eleccion_fi = 1
  col_to_extract.append(nombre_col_fi)
  

  if nombre_col_ff in columnas:
    eleccion_ff = 1
  col_to_extract.append(nombre_col_ff)
  
  df = pd.DataFrame(excel_entrante,columns=col_to_extract)
  
  df = df.replace({np.nan: ''})

  
  print(df.values)
  for fila in df.values:

    if fila[0] != None: #VALIDACION DE ID_PRODUCTO
        #print(fila[4])
        retorno = armarJSON(marketplace, [fila[2], str("precionormal"), int(eleccion_pn)], [fila[3], str("preciooferta"), int(eleccion_po)], [fila[4], str("salestartdate"), int(eleccion_fi)], [fila[5], str("saleenddate"), int(eleccion_ff)])
        print (type(retorno))
  return (retorno)



def inyeccionMKP(body, id_producto):


  url = "https://www.centry.cl/conexion/v1/products/"+id_producto+".json"

  payload = json.dumps({
    "integrations": {
      "ripley": {
        "price": "",
        "preciooferta": "",
        "salestartdate": "",
        "saleenddate": ""
      }
    }
  })
  headers = {
    'Authorization': 'Bearer '+access_token,
    'Content-Type': 'application/json'
  }

  response = requests.request("PUT", url, headers=headers, data=payload)

  print(response.text)
















def priceToJSON(precio, nombre, activar):
    
    if activar == 1:
        if precio == None or precio == str(""):
            return '"'+str(nombre)+'" : null'

        if type(precio) == int and precio > 0:
            return '"'+str(nombre)+'" : '+ str(precio)
        else:
            print("¡Error función priceToJSON!")
            print(precio,nombre,activar)
    else:
        return str("")



  
def dateToJSON(fecha, nombre, activar):
  
  if activar == 1:
    if fecha == None or fecha == str(""):
      return '"'+str(nombre)+'" : null'
    if fecha:
      return '"'+str(nombre)+'" : '+str(fecha)
  
  else:
    return str("")
  

  
#funciones que se añadiran a json integrations

def armarJSON(marketplace, precio_normal, precio_oferta, inicio_oferta, fin_oferta): #precios y fechas llegan con el segundo valor como tupla "activar"
  
  codigo = ""

  (price, nombre_pn, activar_pn) = precio_normal
  (preciooferta, nombre_po, activar_po) = precio_oferta
  (salestartdate, nombre_fi, activar_fi ) = inicio_oferta
  (saleenddate, nombre_ff, activar_ff ) = fin_oferta

  #VALIDAR TODOS LOS CASOS POSIBLES, PRIMERO CONSIDERANDO RETORNAR UN JSON VACÍO SI NO SE INYECTARÁ NADA
  if activar_pn and activar_po and activar_fi and activar_ff == 0:
    return (codigo)
  
  else:
    if activar_pn == 1:
      codigo = agregarCodigo(priceToJSON(price, nombre_pn, activar_pn), codigo)
    if activar_po == 1:
      codigo = agregarCodigo(priceToJSON(preciooferta, nombre_po, activar_po), codigo)
    if activar_fi == 1:
      codigo = agregarCodigo(dateToJSON(salestartdate, nombre_fi, activar_fi), codigo)
    if activar_ff == 1:
      codigo = agregarCodigo(dateToJSON(saleenddate, nombre_ff, activar_ff), codigo)

    if codigo != "":
      codigo = '"'+marketplace+'"'+": { "+codigo+" } "
      return codigo
    else:
      return codigo
      

    
def agregarCodigo(textToAdd, codigo):
  coma = " , "
  if codigo == "" or None: 
    codigo = textToAdd
  else:
    codigo = str(codigo) + str(coma)+str(textToAdd)
    
  return codigo



a = extraerMKPDesdeExcel("ripley", "Ripley Precio Normal / Ripley", "Ripley Precio Oferta / Ripley", "Ripley Fecha Inicio Oferta / Ripley", "Ripley Fecha Término Oferta / Ripley")


#print (a)