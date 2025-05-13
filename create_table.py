import psycopg2
from psycopg2 import sql

# Dados de acesso
HOST = "localhost"
USER = "yourUser"
PASSWORD = "yourPassword"
DB_NAME = "chooseYourDBName"

# Conecta ao banco default para criar o novo banco
def criar_banco():
    conn = psycopg2.connect(host=HOST, user=USER, password=PASSWORD, dbname="postgres")
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")
    exists = cursor.fetchone()

    if not exists:
        print(f"Criando banco de dados '{DB_NAME}'...")
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
    else:
        print(f"Banco de dados '{DB_NAME}' já existe.")

    cursor.close()
    conn.close()

# Cria as tabelas no novo banco
def criar_tabelas():
    conn = psycopg2.connect(host=HOST, user=USER, password=PASSWORD, dbname=DB_NAME)
    cursor = conn.cursor()

    comandos = [
        """
        CREATE TABLE IF NOT EXISTS public.events (
            id serial4 NOT NULL,
            "name" varchar NOT NULL,
            "date" varchar NOT NULL,
            budget int4 NULL,
            CONSTRAINT events_pkey PRIMARY KEY (id)
        );
        CREATE INDEX IF NOT EXISTS ix_events_id ON public.events USING btree (id);
        """,
        """
        CREATE TABLE IF NOT EXISTS public.feedbacks (
            id serial4 NOT NULL,
            "content" text NOT NULL,
            event_id int4 NOT NULL,
            CONSTRAINT feedbacks_pkey PRIMARY KEY (id),
            CONSTRAINT fk_feedback_event FOREIGN KEY (event_id) REFERENCES public.events(id) ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS public.participants (
            id serial4 NOT NULL,
            "name" varchar(255) NOT NULL,
            event_id int4 NOT NULL,
            CONSTRAINT participants_pkey PRIMARY KEY (id),
            CONSTRAINT fk_participant_event FOREIGN KEY (event_id) REFERENCES public.events(id) ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS public.speakers (
            id serial4 NOT NULL,
            "name" varchar(255) NOT NULL,
            description varchar(255) NULL,
            event_id int4 NOT NULL,
            CONSTRAINT speakers_pkey PRIMARY KEY (id),
            CONSTRAINT fk_speaker_event FOREIGN KEY (event_id) REFERENCES public.events(id) ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS public.vendors (
            id serial4 NOT NULL,
            "name" varchar(255) NOT NULL,
            services varchar(255) NULL,
            event_id int4 NOT NULL,
            CONSTRAINT vendors_pkey PRIMARY KEY (id),
            CONSTRAINT fk_vendor_event FOREIGN KEY (event_id) REFERENCES public.events(id) ON DELETE CASCADE
        );
        """
    ]

    for comando in comandos:
        cursor.execute(comando)

    conn.commit()
    cursor.close()
    conn.close()
    print("Tabelas criadas com sucesso!")

if __name__ == "__main__":
    criar_banco()
    criar_tabelas()
