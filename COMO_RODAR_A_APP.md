# Como Rodar a App TurnOverRH

## 🔧 Setup Inicial (apenas 1 vez)

Faça isso uma única vez quando pegar o projeto.

### 1. Criar os bancos de dados

Abra um terminal (cmd ou PowerShell) e rode:

```bash
createdb turnover -U postgres
createdb mlflow   -U postgres
psql turnover -U postgres -f sql/01_criar_tabelas.sql
psql turnover -U postgres -c "\dt"
```

Tem que aparecer 4 tabelas:
- `treino_v1`
- `validacao_congelada`
- `validacao_atual`
- `predicoes`

### 2. Instalar dependências Python

```bash
pip install -r requirements.txt
```

### 3. Popular os dados de treino

```bash
python preparar_dados.py
```

Resposta esperada:
```
treino_v1            19200 linhas
validacao_congelada   4800 linhas
```

### 4. Registrar o modelo no MLflow

```bash
python onboard_v1.py
```

Resposta esperada:
```
versao  1  ->  @champion
baseline na validacao congelada:
  accuracy                    0.7XXX
  f1                          0.5XXX
  ...
```

**Pronto! Setup terminado.**

---

## 🚀 Iniciar a App (toda vez que quer rodar)

### Passo 1: Abra o Terminal 1

Navegue até a pasta do projeto:

```bash
cd "C:\Users\leticiasilva-ieg\OneDrive - Instituto Germinare\Área de Trabalho\3°H - 2026\Ciências de Dados\TurnOverRH-main"
```

Suba o MLflow (deixa rodando):

```bash
python -m mlflow server --host 127.0.0.1 --port 5000 --backend-store-uri postgresql://postgres:lelelovebts12@127.0.0.1:5432/mlflow --default-artifact-root ./mlruns
```

Você vai ver:
```
[2026-09-25 ...] INFO mlflow.server: MLflow server started on http://127.0.0.1:5000
```

✅ **Deixe esse terminal aberto.**

### Passo 2: Abra o Terminal 2

Na mesma pasta, rode a API:

```bash
python -m uvicorn app.main:app --reload --port 8000
```

Você vai ver:
```
Uvicorn running on http://127.0.0.1:8000
```

✅ **Deixe esse terminal aberto.**

### Passo 3: Acesse a App

Abra o navegador (Chrome, Firefox, Edge) em:

```
http://127.0.0.1:8000
```

Pronto! A interface está rodando.

---

## 📊 Onde acessar cada serviço

| Serviço | URL | Para quê |
|---------|-----|----------|
| **App Principal** | http://127.0.0.1:8000 | Formulário para prever, enviar lotes, ver colaboradores |
| **MLflow** | http://127.0.0.1:5000 | Histórico de treinos, versões do modelo, @champion |
| **Saúde da API** | http://127.0.0.1:8000/saude | Confirmar que o modelo está carregado |

---

## ✅ Rotina Padrão na App

### Prever um colaborador novo
1. Clica em **"Novo Colaborador"**
2. Preenche os campos (ou deixa 0)
3. Clica **"Prever"**
4. Vê: probabilidade, classe, faixa (ok / atenção / alerta)

### Enviar um lote (CSV)
1. Clica em **"Enviar Lote"**
2. Seleciona um CSV com colunas assim:
   ```
   id_pessoa;abs_eventos;abs_qtd_total;horas_previstas_total;...
   001;0;0;0;...
   002;5;10;20;...
   ```
3. Clica **"Upload"**
4. Vê o resumo: quantos mandou, quanto em risco

### Ver histórico
1. Abra **"Colaboradores"** — lista de quem já foi avaliado
2. Abra **"Lotes"** — histórico de tudo que foi enviado
3. Abra **MLflow** (terminal 1 URL) — métricas, versões, audit trail

---

## 🔴 Erros Comuns

### "Nenhuma conexão pôde ser feita porque a máquina de destino as recusou"
**Causa:** MLflow não está rodando no terminal 1.
**Solução:** Verifique se o terminal 1 tem a mensagem `MLflow server started on http://127.0.0.1:5000`

### "ConnectionRefusedError" ou "psycopg2 error"
**Causa:** Postgres não está rodando ou credenciais erradas.
**Solução:** 
- Verifique se o Postgres está ligado
- Confirme as credenciais em `.env` (user, senha, host, port)

### "Table does not exist"
**Causa:** As tabelas não foram criadas.
**Solução:** 
```bash
psql turnover -U postgres -f sql/01_criar_tabelas.sql
```

### "uvicorn: não é reconhecido"
**Causa:** Instalação errada no PowerShell.
**Solução:** Use `python -m uvicorn` em vez de apenas `uvicorn`

### "ModuleNotFoundError: No module named 'mlflow'"
**Causa:** As dependências não foram instaladas.
**Solução:**
```bash
pip install -r requirements.txt
```

---

## 🛑 Parar a App

1. **Terminal 1 (MLflow):** Ctrl + C
2. **Terminal 2 (API):** Ctrl + C

Pronto, está offline.

---

## 📝 Arquivo de Configuração

Se precisar mudar host/porta do Postgres ou MLflow, edite `.env`:

```env
PG_HOST=127.0.0.1
PG_PORT=5432
PG_USER=postgres
PG_SENHA=lelelovebts12
PG_DB_APP=turnover
PG_DB_MLFLOW=mlflow

MLFLOW_URI=http://127.0.0.1:5000
```

---

## 📚 Próximos Passos (Aulas 2, 3, 4)

Quando chegar novo lote rotulado:

```bash
# Aula 2: Retreinar
python treinar.py --incorporar lote_aula2 --gabarito gabarito_aula2.csv --motivo data_drift

# Aula 3: Decidir promover
python promover.py --versao 2

# Aula 4: Monitorar
python monitorar.py --lote lote_aula2 --gabarito gabarito_aula2.csv
```

Mas por enquanto, a app está **pronta para usar**. 🎉
