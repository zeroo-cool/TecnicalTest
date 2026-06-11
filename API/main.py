from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from datetime import date
from pydantic import BaseModel
from database import get_db

# Llamada a la API 
app = FastAPI(
    title="Servicio Ventas",
    description="Endpoints para proyecciones de ventas",
    version="1.0.0"
)

# Clases Modelos (Corregido: Total ahora es float para soportar los decimales del SUM)
class ventasTotales(BaseModel):
    Mes: str
    IdCliente: str        
    NombreCliente: str
    Total: float

class montoPendienteCobro(BaseModel):
    Total: float 
    
class montoDeudores(BaseModel):
    IdCliente: str        
    NombreCliente: str
    Total: float


class rankingBestClient(BaseModel):
    IdCliente: str
    NombreCliente: str
    Total: float
    
class DeudoresResponse(BaseModel):
    monto_total_pendiente: float 
    top_deudores: List[rankingBestClient]  
    

class tendenciaVentas(BaseModel):
    Mes: str
    TotalMensual: float
    
@app.get("/", tags=["Test"])
def root():
    return {"status": "Online", "message": "API funcionando perfectamente"}


@app.get("/Ventas/TendenciaHistorica", response_model=List[tendenciaVentas], tags=["Visualizacion"])
def obtener_tendencia_historica(db: Session = Depends(get_db)):
    
    query = text("EXEC [ventas_db].[dbo].[obtenerTendenciaVentas]")
    
    try:
        resultado = db.execute(query).fetchall()
        
        if not resultado:
            raise HTTPException(status_code=404, detail="No hay registros cronológicos.")
            
        respuesta_limpia = [
            {
                "Mes": str(row[0]).strip(),
                "TotalMensual": float(row[1])
            }
            for row in resultado
        ]
        return respuesta_limpia
        
    except Exception as e:
        print(f"❌ Error al consultar tendencia: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@app.get("/Ventas/TotalesByMes", response_model=List[ventasTotales], tags=["ventasTotales"])
def ventasByMes(db: Session = Depends(get_db)):
    query = text("EXEC [ventas_db].[dbo].[ventasTotalesCliente]")
    
    try:
        resultado = db.execute(query).fetchall()
        
        if not resultado:
            raise HTTPException(status_code=404, detail="No hay datos de ventas")
            
        respuesta_limpia = [
            {
                "Mes": str(row[0]).strip(),
                "IdCliente": str(row[1]).strip(),
                "NombreCliente": str(row[2]).strip(),
                "Total": float(row[3])  
            }
            for row in resultado
        ]
        
        return respuesta_limpia
        
    except Exception as e:
        print(f"Error en el proceso del endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
        
@app.get("/Ventas/TopCincoClientes", response_model=List[rankingBestClient], tags=["rankingBestClient"])
def topCincoClientes(db: Session = Depends(get_db)):
    query = text("EXECUTE [dbo].[rankigBestClient]")
    
    try:
        resultado = db.execute(query).fetchall()
        
        if not resultado:
            raise HTTPException(status_code=404, detail="No hay datos")
            
        respuesta_limpia = [
            {
                "IdCliente": str(row[0]).strip(),
                "NombreCliente": str(row[1]).strip(),
                "Total":  float(row[2]) 
            }
            for row in resultado
        ]
        
        return respuesta_limpia
        
    except Exception as e:
        print(f"Error en el proceso del endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
        
@app.get("/Ventas/MontoDeudores", response_model=DeudoresResponse, tags=["Visualizacion"])
def obtener_monto_y_deudores(db: Session = Depends(get_db)):
    
    query_total = text("EXEC [ventas_db].[dbo].[montoPendienteCobro]")
    query_ranking = text("EXECUTE [ventas_db].[dbo].[montoTotaldeudores]")
    
    try:
        # 1. Ejecutar y obtener el Monto Total Pendiente (Devuelve 1 fila con 1 valor)
        res_total = db.execute(query_total).fetchone()
        monto_acumulado = float(res_total[0]) if res_total and res_total[0] is not None else 0.0
        
        # 2. Ejecutar y obtener la lista de los deudores (Devuelve múltiples filas)
        res_ranking = db.execute(query_ranking).fetchall()
        
        # 3. Mapear la lista de deudores usando tu estructura 'rankingBestClient'
        lista_deudores = [
            {
                "IdCliente": str(row[0]).strip(),
                "NombreCliente": str(row[1]).strip(),
                "Total": float(row[2])
            }
            for row in res_ranking
        ]
        
      
        return {
            "monto_total_pendiente": monto_acumulado,
            "top_deudores": lista_deudores
        }
        
    except Exception as e:
        print(f"Error al consultar deudores: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
        
