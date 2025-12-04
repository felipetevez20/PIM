#ifndef ESCOLA_H
#define ESCOLA_H

#ifdef _WIN32
  #define EXPORT __declspec(dllexport)
  #define CDECL  __cdecl
#else
  #define EXPORT
  #define CDECL
#endif

// Inicializa o diretório base dos CSV (ex.: "C:\\Users\\Windows\\Desktop\\projetopim\\DATA")
EXPORT void  CDECL init_db(const char* base_dir);

// Login: retorna 1 se ok e escreve "aluno"/"professor"/"diretor" em tipo_out
EXPORT int   CDECL login(const char* usuario, const char* senha,
                         char* tipo_out, int tipo_out_size);

// Diretor
// tipo: "aluno" | "professor" | "diretor"
EXPORT int   CDECL cadastrar_usuario(const char* nome, const char* tipo, const char* senha);

// Professor
EXPORT int   CDECL adicionar_nota(const char* aluno, const char* materia, float nota);
EXPORT int   CDECL registrar_falta(const char* aluno, const char* materia, const char* data_yyyymmdd);

// Aluno
// Escreve linhas "materia;nota\n" em buffer. Retorna quantidade de linhas.
EXPORT int   CDECL obter_notas(const char* aluno, char* buffer, int bufsize);
// Conta faltas do aluno (todas as matérias)
EXPORT int   CDECL contar_faltas(const char* aluno);
EXPORT int   CDECL listar_alunos(char* buffer, int bufsize);
EXPORT int   CDECL atribuir_materia_professor(const char* professor, const char* materia);
EXPORT int   CDECL obter_materia_professor(const char* professor, char* buffer, int bufsize);
EXPORT int   CDECL salvar_notas3(const char* aluno, const char* materia,
                                  float p1, float p2, float trab);
EXPORT int   CDECL obter_notas3(const char* aluno, char* buffer, int bufsize);
#endif