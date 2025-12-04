//Bibliotecas
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <windows.h>
#include "escola.h"

//DefiniçãodeMAXPACH
#define MAXPATH 1024

//FunçõesGlobais (definidas por maxpatch)
static char G_USERS[MAXPATH]  = {0};
static char G_NOTAS[MAXPATH]  = {0};
static char G_FALTAS[MAXPATH] = {0};

//Caminho do arquivo
//1. Ela verifica diretório se já contém um separador no final para evitar concatenações incorretas
static void join_path(char* out, const char* dir, const char* file) {
    size_t n = strlen(dir);
    if (n > 0 && (dir[n-1] == '\\' || dir[n-1] == '/')) {
        snprintf(out, MAXPATH, "%s%s", dir, file);
    } else {
        snprintf(out, MAXPATH, "%s\\%s", dir, file);
    }
}

static void trim_crlf(char *s) {
    if (!s) return;
    size_t n = strlen(s);
    while (n > 0 && (s[n-1] == '\n' || s[n-1] == '\r' || s[n-1] == ' ' || s[n-1] == '\t')) {
        s[--n] = '\0';
    }
}

static void ltrim_spaces(char **ps) {
    if (!ps || !*ps) return;
    while (**ps == ' ' || **ps == '\t') {
        (*ps)++;
    }
}

static void trim_spaces(char *s) {
    if (!s) return;

    char *p = s;
    ltrim_spaces(&p);
    if (p != s) {
        memmove(s, p, strlen(p) + 1);
    }
    trim_crlf(s);
}

static int safe_eq(const char* a, const char* b) {
    return a && b && strcmp(a, b) == 0;
}

static void ensure_files_exist(void) {
    FILE *f;
    f = fopen(G_USERS, "a");  if (f) fclose(f);
    f = fopen(G_NOTAS, "a");  if (f) fclose(f);
    f = fopen(G_FALTAS, "a"); if (f) fclose(f);
}

void __cdecl init_db(const char* base_dir) {
    join_path(G_USERS,  base_dir, "users.csv");
    join_path(G_NOTAS,  base_dir, "notas.csv");
    join_path(G_FALTAS, base_dir, "faltas.csv");
    ensure_files_exist();
}

int __cdecl login(const char* usuario, const char* senha, char* tipo_out, int tipo_out_size) {
    ensure_files_exist();
    FILE* f = fopen(G_USERS, "r");
    if (!f) return 0;

    char u2[128], s2[128];
    strncpy(u2, usuario ? usuario : "", sizeof(u2)-1);
    u2[sizeof(u2)-1] = 0;
    trim_spaces(u2);

    strncpy(s2, senha ? senha : "", sizeof(s2)-1);
    s2[sizeof(s2)-1] = 0;
    trim_spaces(s2);

    char linha[512];
    while (fgets(linha, sizeof(linha), f)) {
        char tipo[64] = {0}, nome[128] = {0}, pass[128] = {0}, materia[128] = {0};
        int n = sscanf(linha, "%63[^;];%127[^;];%127[^;];%127[^\n]", tipo, nome, pass, materia);
        if (n >= 3) {
            trim_spaces(tipo);
            trim_spaces(nome);
            trim_spaces(pass);

            if (strcmp(nome, u2) == 0 && strcmp(pass, s2) == 0) {
                if (tipo_out && tipo_out_size > 0) {
                    strncpy(tipo_out, tipo, (size_t)tipo_out_size - 1);
                    tipo_out[tipo_out_size - 1] = '\0';
                }
                fclose(f);
                return 1;
            }
        }
    }
    fclose(f);
    return 0;
}
//CadastroDeUsuarios
//1. ColetaDeDados
int __cdecl cadastrar_usuario(const char* nome, const char* tipo, const char* senha) {
//2. ValidaçãodeDados
    ensure_files_exist();
    if (!nome || !tipo || !senha) return 0;

//LimitaçãoDeCaracteresNome
    char n2[128], t2[64], s2[128];
    strncpy(n2, nome,  sizeof(n2)-1);
    n2[sizeof(n2)-1] = 0;
    trim_spaces(n2);
//LimitaçãoDeCaracteresTipo
    strncpy(t2, tipo,  sizeof(t2)-1);
    t2[sizeof(t2)-1] = 0;
    trim_spaces(t2);
//LimitaçãoDeCaracteresSenha
    strncpy(s2, senha, sizeof(s2)-1);
    s2[sizeof(s2)-1] = 0;
    trim_spaces(s2);
//3. Validação(Tipo)
    if (!(safe_eq(t2, "aluno") || safe_eq(t2, "professor") || safe_eq(t2, "diretor"))) {
        return 0;
    }
//ExecuçãoUsuariosCSV
    FILE* fr = fopen(G_USERS, "r");
    if (fr) {
        char linha[512], t[64], n[128], s[128];
        while (fgets(linha, sizeof(linha), fr)) {
            if (sscanf(linha, "%63[^;];%127[^;];%127[^\n]", t, n, s) == 3) {
                trim_spaces(n);
                if (safe_eq(n, n2)) {
                    fclose(fr);
                    return 0;
                }
            }
        }
        fclose(fr);
    }

    FILE* f = fopen(G_USERS, "a");
    if (!f) return 0;
    fprintf(f, "%s;%s;%s\n", t2, n2, s2);
    fclose(f);
    return 1;
}
//Notas
int __cdecl adicionar_nota(const char* aluno, const char* materia, float nota) {
    ensure_files_exist();
    if (!aluno || !materia) return 0;

    char a2[128], m2[128];
    strncpy(a2, aluno,   sizeof(a2)-1);
    a2[sizeof(a2)-1] = 0;
    trim_spaces(a2);

    strncpy(m2, materia, sizeof(m2)-1);
    m2[sizeof(m2)-1] = 0;
    trim_spaces(m2);

    FILE* f = fopen(G_NOTAS, "a");
    if (!f) return 0;
    fprintf(f, "%s;%s;%.2f\n", a2, m2, nota);
    fclose(f);
    return 1;
}

int __cdecl obter_notas(const char* aluno, char* buffer, int bufsize) {
    ensure_files_exist();
    if (!aluno || !buffer || bufsize <= 0) return 0;

    char a2[128];
    strncpy(a2, aluno, sizeof(a2)-1);
    a2[sizeof(a2)-1] = 0;
    trim_spaces(a2);

    FILE* f = fopen(G_NOTAS, "r");
    if (!f) {
        buffer[0] = '\0';
        return 0;
    }

    buffer[0] = '\0';
    char linha[512], a[128], mat[128], nota[64];
    int count = 0;

    while (fgets(linha, sizeof(linha), f)) {
        if (sscanf(linha, "%127[^;];%127[^;];%63[^\n]", a, mat, nota) == 3) {
            trim_spaces(a);
            trim_spaces(mat);
            trim_spaces(nota);
            if (safe_eq(a, a2)) {
                char out[256];
                snprintf(out, sizeof(out), "%s;%s\n", mat, nota);
                if ((int)(strlen(buffer) + strlen(out) + 1) < bufsize) {
                    strcat(buffer, out);
                    count++;
                } else {
                    break;
                }
            }
        }
    }
    fclose(f);
    return count;
}
//Faltas
int __cdecl registrar_falta(const char* aluno, const char* materia, const char* data_yyyymmdd) {
    ensure_files_exist();
    if (!aluno || !materia || !data_yyyymmdd) return 0;

    char a2[128], m2[128], d2[64];
    strncpy(a2, aluno, sizeof(a2)-1);
    a2[sizeof(a2)-1] = 0;
    trim_spaces(a2);

    strncpy(m2, materia, sizeof(m2)-1);
    m2[sizeof(m2)-1] = 0;
    trim_spaces(m2);

    strncpy(d2, data_yyyymmdd, sizeof(d2)-1);
    d2[sizeof(d2)-1] = 0;
    trim_spaces(d2);

    FILE* f = fopen(G_FALTAS, "a");
    if (!f) return 0;
    fprintf(f, "%s;%s;%s\n", a2, m2, d2);
    fclose(f);
    return 1;
}

int __cdecl contar_faltas(const char* aluno) {
    ensure_files_exist();
    if (!aluno) return 0;

    char a2[128];
    strncpy(a2, aluno, sizeof(a2)-1);
    a2[sizeof(a2)-1] = 0;
    trim_spaces(a2);

    FILE* f = fopen(G_FALTAS, "r");
    if (!f) return 0;

    char linha[512], a[128], mat[128], data[64];
    int total = 0;

    while (fgets(linha, sizeof(linha), f)) {
        if (sscanf(linha, "%127[^;];%127[^;];%63[^\n]", a, mat, data) == 3) {
            trim_spaces(a);
            if (safe_eq(a, a2)) {
                total++;
            }
        }
    }
    fclose(f);
    return total;
}
//ListagemDeAlunos
int __cdecl listar_alunos(char* buffer, int bufsize) {
    ensure_files_exist();
    if (!buffer || bufsize <= 0) return 0;

    FILE* f = fopen(G_USERS, "r");
    if (!f) {
        buffer[0] = '\0';
        return 0;
    }

    buffer[0] = '\0';
    char linha[512], tipo[64], nome[128], pass[128];
    int count = 0;

    while (fgets(linha, sizeof(linha), f)) {
        if (sscanf(linha, "%63[^;];%127[^;];%127[^\n]", tipo, nome, pass) == 3) {
            trim_spaces(tipo);
            trim_spaces(nome);
            if (safe_eq(tipo, "aluno")) {
                size_t need = strlen(nome) + 1;
                if ((int)(strlen(buffer) + need + 1) < bufsize) {
                    strcat(buffer, nome);
                    strcat(buffer, "\n");
                    count++;
                } else {
                    break;
                }
            }
        }
    }
    fclose(f);
    return count;
}
//AtribuiçãoDeMatéria
int __cdecl obter_materia_professor(const char* professor, char* buffer, int bufsize) {
    ensure_files_exist();
    if (!professor || !buffer || bufsize <= 0) return 0;

    FILE* f = fopen(G_USERS, "r");
    if (!f) {
        buffer[0] = '\0';
        return 0;
    }

    char linha[512], tipo[64], nome[128], pass[128], mat[128];
    buffer[0] = '\0';

    while (fgets(linha, sizeof(linha), f)) {
        int n = sscanf(linha, "%63[^;];%127[^;];%127[^;];%127[^\n]", tipo, nome, pass, mat);
        if (n >= 3) {
            trim_spaces(tipo);
            trim_spaces(nome);
            if (safe_eq(tipo, "professor") && safe_eq(nome, professor)) {
                if (n == 4) {
                    trim_spaces(mat);
                    strncpy(buffer, mat, (size_t)bufsize-1);
                    buffer[bufsize-1] = '\0';
                } else {
                    buffer[0] = '\0';
                }
                fclose(f);
                return 1;
            }
        }
    }
    fclose(f);
    return 0;
}

int __cdecl atribuir_materia_professor(const char* professor, const char* materia) {
    ensure_files_exist();
    if (!professor || !materia) return 0;

    char p2[128], m2[128];
    strncpy(p2, professor, sizeof(p2)-1);
    p2[sizeof(p2)-1] = 0;
    trim_spaces(p2);

    strncpy(m2, materia, sizeof(m2)-1);
    m2[sizeof(m2)-1] = 0;
    trim_spaces(m2);

    FILE* fin = fopen(G_USERS, "r");
    if (!fin) return 0;

    char tmpPath[MAXPATH];
    snprintf(tmpPath, MAXPATH, "%s.tmp", G_USERS);
    FILE* fout = fopen(tmpPath, "w");
    if (!fout) {
        fclose(fin);
        return 0;
    }

    char linha[512], tipo[64], nome[128], pass[128], mat[128];
    int updated = 0;

    while (fgets(linha, sizeof(linha), fin)) {
        int n = sscanf(linha, "%63[^;];%127[^;];%127[^;];%127[^\n]", tipo, nome, pass, mat);
        if (n >= 3) {
            trim_spaces(tipo);
            trim_spaces(nome);
            trim_spaces(pass);

            if (safe_eq(tipo, "professor") && safe_eq(nome, p2)) {
                fprintf(fout, "%s;%s;%s;%s\n", tipo, nome, pass, m2);
                updated = 1;
            } else {
                if (n == 4) {
                    trim_spaces(mat);
                    fprintf(fout, "%s;%s;%s;%s\n", tipo, nome, pass, mat);
                } else {
                    fprintf(fout, "%s;%s;%s\n", tipo, nome, pass);
                }
            }
        } else {
            fputs(linha, fout);
        }
    }

    fclose(fin);
    fclose(fout);

    remove(G_USERS);
    rename(tmpPath, G_USERS);

    return updated;
}
//Notas2
static int linha_notas3_parse(const char* linha, char* a, char* m, char* s1, char* s2, char* s3) {
    int n = sscanf(linha, "%127[^;];%127[^;];%31[^;];%31[^;];%31[^\n]", a, m, s1, s2, s3);
    return (n == 5);
}

int __cdecl salvar_notas3(const char* aluno, const char* materia, float p1, float p2, float trab) {
    ensure_files_exist();
    if (!aluno || !materia) return 0;

    char a2[128], m2[128];
    strncpy(a2, aluno, sizeof(a2)-1);
    a2[sizeof(a2)-1] = 0;
    trim_spaces(a2);

    strncpy(m2, materia, sizeof(m2)-1);
    m2[sizeof(m2)-1] = 0;
    trim_spaces(m2);

    FILE* fin = fopen(G_NOTAS, "r");
    char tmpPath[MAXPATH];
    snprintf(tmpPath, MAXPATH, "%s.tmp", G_NOTAS);
    FILE* fout = fopen(tmpPath, "w");
    if (!fout) {
        if (fin) fclose(fin);
        return 0;
    }

    char linha[512], a[128], m[128], s1[32], s2[32], s3[32];
    int updated = 0;

    if (fin) {
        while (fgets(linha, sizeof(linha), fin)) {
            if (linha_notas3_parse(linha, a, m, s1, s2, s3)) {
                trim_spaces(a);
                trim_spaces(m);
                if (safe_eq(a, a2) && safe_eq(m, m2)) {
                    fprintf(fout, "%s;%s;%.2f;%.2f;%.2f\n", a2, m2, p1, p2, trab);
                    updated = 1;
                } else {
                    trim_spaces(s1);
                    trim_spaces(s2);
                    trim_spaces(s3);
                    fprintf(fout, "%s;%s;%s;%s;%s\n", a, m, s1, s2, s3);
                }
            } else {
                
            }
        }
        fclose(fin);
    }

    if (!updated) {
        fprintf(fout, "%s;%s;%.2f;%.2f;%.2f\n", a2, m2, p1, p2, trab);
    }
    fclose(fout);

    remove(G_NOTAS);
    rename(tmpPath, G_NOTAS);

    return 1;
}

int __cdecl obter_notas3(const char* aluno, char* buffer, int bufsize) {
    ensure_files_exist();
    if (!aluno || !buffer || bufsize <= 0) return 0;

    char a2[128];
    strncpy(a2, aluno, sizeof(a2)-1);
    a2[sizeof(a2)-1] = 0;
    trim_spaces(a2);

    FILE* f = fopen(G_NOTAS, "r");
    if (!f) {
        buffer[0] = '\0';
        return 0;
    }

    buffer[0] = '\0';
    char linha[512], a[128], m[128], s1[32], s2[32], s3[32];
    int count = 0;

    while (fgets(linha, sizeof(linha), f)) {
        if (linha_notas3_parse(linha, a, m, s1, s2, s3)) {
            trim_spaces(a);
            trim_spaces(m);
            trim_spaces(s1);
            trim_spaces(s2);
            trim_spaces(s3);

            if (safe_eq(a, a2)) {
                float p1 = (float)atof(s1);
                float p2 = (float)atof(s2);
                float tr = (float)atof(s3);
                float media = (p1 + p2 + tr) / 3.0f;
                const char* status = (media >= 7.0f) ? "Aprovado" : "Reprovado";

                char out[256];
                snprintf(out, sizeof(out), "%s;%.2f;%.2f;%.2f;%.2f;%s\n", m, p1, p2, tr, media, status);
                if ((int)(strlen(buffer) + strlen(out) + 1) < bufsize) {
                    strcat(buffer, out);
                    count++;
                } else {
                    break;
                }
            }
        } else {
            
        }
    }
    fclose(f);
    return count;
}
