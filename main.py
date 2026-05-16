from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================
# CONEXIÓN A MONGODB ATLAS
# ==========================

uri = "mongodb+srv://parranderos-user:Samunico05*@fundamentosbd.keysn4i.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri)

# Base de datos en Atlas
db = client["parranderos"]


# ==========================
# RUTA PRINCIPAL
# ==========================

@app.get("/")
def inicio():
    return {"estado": "API funcionando correctamente"}


@app.get("/ping")
def ping():
    try:
        client.admin.command("ping")
        return {"mensaje": "Conexión a MongoDB Atlas exitosa"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==========================
# ENDPOINTS DEL VIDEO
# PROVEEDORES
# ==========================

@app.get("/proveedores")
def get_proveedores():
    return list(db["proveedores"].find({}, {"_id": 0}))


@app.get("/proveedores/{bebida_id}")
def get_proveedor_bebida(bebida_id: int):
    proveedor = db["proveedores"].find_one(
        {"bebidas_suministradas": bebida_id},
        {"_id": 0}
    )
    return proveedor or {}


@app.post("/proveedores")
def post_proveedor(datos: dict):
    datos["fecha_registro"] = datetime.now().isoformat()
    db["proveedores"].insert_one(datos)
    return {"mensaje": "Proveedor registrado"}


@app.put("/proveedores/{nombre}")
def update_proveedor(nombre: str, datos: dict):
    resultado = db["proveedores"].replace_one(
        {"nombre": nombre},
        datos
    )
    return {"mensaje": "Proveedor actualizado correctamente"}

@app.patch("/proveedores/{nombre}")
def patch_proveedor(nombre: str, datos: dict):
    resultado = db["proveedores"].update_one(
        {"nombre": nombre},
        {"$set": datos}
    )
    return {"mensaje": "Campos actualizados correctamente"}

@app.delete("/proveedores/{nombre}")
def delete_proveedor(nombre: str):
    resultado = db["proveedores"].delete_one({"nombre": nombre})
    return {"mensaje": f"Proveedor {nombre} eliminado"}


# ==========================
# ENDPOINTS DEL TALLER / TODO
# COMENTARIOS DE BARES
# ==========================

@app.get("/bares/{bar_id}/comentarios")
def get_comentarios(bar_id: int):
    comentarios = list(
        db["comentarios_bares"].find(
            {"bar_id": bar_id},
            {"_id": 0}
        )
    )
    return comentarios


@app.post("/bares/{bar_id}/comentarios")
def post_comentario(bar_id: int, datos: dict):
    datos["bar_id"] = bar_id
    datos["date"] = datetime.now().isoformat()

    db["comentarios_bares"].insert_one(datos)

    return {"mensaje": "Comentario registrado correctamente"}


# ==========================
# ENDPOINTS DEL TALLER / TODO
# EVENTOS DE BARES
# ==========================

@app.get("/bares/{bar_id}/eventos")
def get_eventos(bar_id: int):
    eventos = list(
        db["eventos"].find(
            {"bar_id": bar_id},
            {"_id": 0}
        )
    )
    return eventos


@app.post("/bares/{bar_id}/eventos")
def post_evento(bar_id: int, datos: dict):
    datos["bar_id"] = bar_id
    datos["fecha_creacion"] = datetime.now().isoformat()

    db["eventos"].insert_one(datos)

    return {"mensaje": "Evento registrado correctamente"}