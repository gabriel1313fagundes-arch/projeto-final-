import sqlite3
 
banco = sqlite3.connect("clima.db")
cursor = banco.cursor()

def conectar_banco():
        
    try:    
        

        # Cria a tabela principal das consultas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS consultas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cidade TEXT NOT NULL,
                estado TEXT,
                uf TEXT,
                periodo TEXT,
                total_mm REAL,
                normal_mm REAL,
                resumo TEXT,
                evento TEXT,
                data_consulta TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        banco.commit()
        return banco

    except sqlite3.Error as erro:
     print("Erro ao conectar ao banco:", erro)
     return None


    finally:
       banco.close()



def salvar_consulta(resultado, evento=""):

    banco = conectar_banco()

    if banco is None:
        return

    try:
        cursor = banco.cursor()

        local = resultado["local"]
        analise = resultado["analise"]

        # Salva os dados principais da consulta
        cursor.execute("""
            INSERT INTO consultas
            (cidade, estado, uf, periodo, total_mm,
             normal_mm, resumo, evento)

            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            local.get("cidade"),
            local.get("estado"),
            local.get("uf"),
            analise.get("periodo"),
            analise.get("total_mm"),
            analise.get("normal_mm"),
            resultado.get("resumo"),
            evento
        ))

        id_consulta = cursor.lastrowid

        # Salva os dados diários de chuva
        for item in resultado["previsao"]:

            cursor.execute("""
                INSERT INTO previsoes
                (id_consulta, dia, chuva_mm)

                VALUES (?, ?, ?)
            """, (
                id_consulta,
                item.get("dia"),
                item.get("chuva_mm")
            ))

        # Salva os alertas encontrados
        for item in resultado["alertas"]:

            cursor.execute("""
                INSERT INTO alertas
                (id_consulta, nivel, mensagem)

                VALUES (?, ?, ?)
            """, (
                id_consulta,
                item.get("nivel"),
                item.get("mensagem")
            ))

        banco.commit()

        print("Consulta climática salva com sucesso!")

    except sqlite3.Error as erro:
        print("Erro ao salvar os dados:", erro)

    finally:
        banco.close()
        print("Banco de dados fechado!")
