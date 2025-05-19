from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import pandas as pd
import sqlite3
import jwt
from passlib.context import CryptContext

app = FastAPI()

DB_PATH = "dados.db"
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Modelos
class User(BaseModel):
    username: str
    password: str

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ExtratoModel(BaseModel):
    DataDebito: str
    DataLancamento: str
    MeioPagamento: Optional[str] = None
    Lancamento: Optional[str] = None
    Ref1: Optional[str] = None
    Ref2: Optional[str] = None
    ref3: Optional[str] = None
    PagoRecebido: Optional[str] = None
    ValorPrincipal: Optional[float] = None
    ClasseSugerida: Optional[str] = None
    Accurace: Optional[int] = None
    Classe: Optional[str] = None
    Origem: Optional[str] = None

class ClassificacaoModel(BaseModel):
    Tipo: str
    Subtipo: Optional[str] = None
    Referencia: Optional[str] = None

# Inicializa o banco de dados
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            hashed_password TEXT
        )""")
        conn.execute("""
        CREATE TABLE IF NOT EXISTS Extrato (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            DataDebito TEXT,
            DataLancamento TEXT,
            MeioPagamento TEXT,
            Lancamento TEXT,
            Ref1 TEXT,
            Ref2 TEXT,
            ref3 TEXT,
            PagoRecebido TEXT,
            ValorPrincipal REAL,
            ClasseSugerida TEXT,
            Accurace INTEGER,
            Classe TEXT,
            Origem TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )""")
        conn.execute("""
        CREATE TABLE IF NOT EXISTS Classificacao (
            IDClass INTEGER PRIMARY KEY AUTOINCREMENT,
            Tipo TEXT,
            Subtipo TEXT,
            Referencia TEXT
        )""")

init_db()

# Utilitários

def get_user(username: str):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        if row:
            return {"id": row[0], "username": row[1], "hashed_password": row[2]}
        return None

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user or not verify_password(password, user["hashed_password"]):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Credenciais inválidas")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    user = get_user(username)
    if user is None:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    return user

# Autenticação
@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/register")
def register(user: User):
    hashed_password = get_password_hash(user.password)
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("INSERT INTO users (username, hashed_password) VALUES (?, ?)", (user.username, hashed_password))
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    return {"message": "Usuário registrado com sucesso"}

# Utilitários para Extrato

def fetch_df(query, params=()):
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(query, conn, params=params)

def execute_query(query, params):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(query, params)
        conn.commit()

# ROTAS DE EXTRATO

@app.post("/extrato")
def incluir_extrato(item: ExtratoModel, current_user: dict = Depends(get_current_user)):
    # Converte todos os campos "Nenhum" para None
    data = {k: (None if v == "Nenhum" else v) for k, v in item.dict().items()}
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO Extrato (user_id, DataDebito, DataLancamento, MeioPagamento, Lancamento, 
                     Ref1, Ref2, ref3, PagoRecebido, ValorPrincipal, ClasseSugerida, Accurace, Classe, Origem)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (current_user["id"], *data.values()))
    return {"message": "Registro incluído"}

@app.get("/extrato")
def listar_extratos(current_user: dict = Depends(get_current_user)):
    df = fetch_df("SELECT * FROM Extrato WHERE user_id = ?", (current_user["id"],))
    return df.to_dict(orient="records")

# ROTAS DE CLASSIFICACAO
@app.post("/classificacao")
def incluir_classificacao(item: ClassificacaoModel):
    execute_query("INSERT INTO Classificacao (Tipo, Subtipo, Referencia) VALUES (?, ?, ?)", tuple(item.dict().values()))
    return {"message": "Classificação incluída"}

@app.get("/classificacao")
def listar_classificacoes():
    df = fetch_df("SELECT * FROM Classificacao")
    return df.to_dict(orient="records")