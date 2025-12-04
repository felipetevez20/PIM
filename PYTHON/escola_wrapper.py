import os
import ctypes

BASE_DIR = os.path.dirname(__file__)

DLL_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "c", "escola.dll"))
DATA_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "data"))

lib = ctypes.CDLL(DLL_PATH)

lib.init_db.argtypes = [ctypes.c_char_p]
lib.init_db.restype = None

lib.login.argtypes = [
    ctypes.c_char_p,  # usuário
    ctypes.c_char_p,  # senha
    ctypes.c_char_p,  # buffer do tipo
    ctypes.c_int      # tamanho do buffer
]
lib.login.restype = ctypes.c_int

lib.cadastrar_usuario.argtypes = [
    ctypes.c_char_p,  # nome
    ctypes.c_char_p,  # tipo (aluno/professor/diretor)
    ctypes.c_char_p   # senha
]
lib.cadastrar_usuario.restype = ctypes.c_int

lib.registrar_falta.argtypes = [
    ctypes.c_char_p,  # aluno
    ctypes.c_char_p,  # matéria
    ctypes.c_char_p   # data 
]
lib.registrar_falta.restype = ctypes.c_int

lib.contar_faltas.argtypes = [ctypes.c_char_p]
lib.contar_faltas.restype = ctypes.c_int

# notas “3 campos”
lib.salvar_notas3.argtypes = [
    ctypes.c_char_p,  # aluno
    ctypes.c_char_p,  # matéria
    ctypes.c_float,   # prova1
    ctypes.c_float,   # prova2
    ctypes.c_float    # trabalho
]
lib.salvar_notas3.restype = ctypes.c_int

lib.obter_notas3.argtypes = [
    ctypes.c_char_p,  # aluno
    ctypes.c_char_p,  # buffer
    ctypes.c_int      # tamanho do buffer
]
lib.obter_notas3.restype = ctypes.c_int

# matéria do professor
lib.obter_materia_professor.argtypes = [
    ctypes.c_char_p,  # professor
    ctypes.c_char_p,  # buffer
    ctypes.c_int      # tamanho
]
lib.obter_materia_professor.restype = ctypes.c_int

lib.atribuir_materia_professor.argtypes = [
    ctypes.c_char_p,  # professor
    ctypes.c_char_p   # matéria
]
lib.atribuir_materia_professor.restype = ctypes.c_int

lib.init_db(DATA_PATH.encode("utf-8"))

def login(usuario: str, senha: str):
    
    tipo_buf = ctypes.create_string_buffer(32)
    ok = lib.login(
        usuario.encode("utf-8"),
        senha.encode("utf-8"),
        tipo_buf,
        32
    )
    if not ok:
        return False, ""
    return True, tipo_buf.value.decode("utf-8")


def cadastrar_usuario(nome: str, tipo: str, senha: str) -> bool:
    return bool(lib.cadastrar_usuario(
        nome.encode("utf-8"),
        tipo.encode("utf-8"),
        senha.encode("utf-8")
    ))


def registrar_falta(aluno: str, materia: str, data_yyyymmdd: str) -> bool:
    return bool(lib.registrar_falta(
        aluno.encode("utf-8"),
        materia.encode("utf-8"),
        data_yyyymmdd.encode("utf-8")
    ))


def contar_faltas(aluno: str) -> int:
    return int(lib.contar_faltas(aluno.encode("utf-8")))


def salvar_notas3(aluno: str, materia: str, p1: float, p2: float, trab: float) -> bool:
    return bool(lib.salvar_notas3(
        aluno.encode("utf-8"),
        materia.encode("utf-8"),
        float(p1),
        float(p2),
        float(trab)
    ))


def obter_notas3(aluno: str):
    
    buf = ctypes.create_string_buffer(8192)
    n = lib.obter_notas3(aluno.encode("utf-8"), buf, 8192)

    if n <= 0:
        return []

    linhas = buf.value.decode(errors="ignore").strip().splitlines()
    out = []
    for ln in linhas:
        partes = ln.split(";")
        if len(partes) == 6:
            mat, p1, p2, tr, md, st = partes
            out.append((mat, p1, p2, tr, md, st))
    return out


def obter_materia_professor(professor: str) -> str:
    buf = ctypes.create_string_buffer(256)
    ok = lib.obter_materia_professor(professor.encode("utf-8"), buf, 256)
    if not ok or not buf.value:
        return ""
    return buf.value.decode("utf-8")


def atribuir_materia_professor(professor: str, materia: str) -> bool:
    return bool(lib.atribuir_materia_professor(
        professor.encode("utf-8"),
        materia.encode("utf-8")
    ))


def listar_alunos():
    
    try:
        func = lib.listar_alunos
    except AttributeError:
        
        return []

    func.argtypes = [ctypes.c_char_p, ctypes.c_int]
    func.restype = ctypes.c_int

    buf = ctypes.create_string_buffer(8192)
    n = func(buf, 8192)
    if n <= 0:
        return []

    texto = buf.value.decode(errors="ignore").strip()
    return [linha for linha in texto.splitlines() if linha.strip()]
