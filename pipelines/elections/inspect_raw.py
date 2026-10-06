from pathlib import Path
import duckdb

BASE_DIR = Path(__file__).resolve().parents[2]

file_path = (
    BASE_DIR
    / "data"
    / "raw"
    / "tse"
    / "2022"
    / "voting"
    / "votacao_candidato_munzona_2022"
    / "votacao_candidato_munzona_2022_BR.csv"
)

con = duckdb.connect()

# result = con.execute(
#     """
#     SELECT *
#     FROM read_csv(
#         ?,
#         delim=';',
#         header=true,
#         encoding='latin-1'
#     )
#     LIMIT 10
# """,
# [str(file_path)]
# ).fetchdf()

# print(result)

# # Total of rows
# total = con.execute(
#     """
#     SELECT COUNT(*)
#     FROM read_csv(
#         ?,
#         delim=';',
#         header=true,
#         encoding='latin-1'
#     )
# """,
# [str(file_path)]
# ).fetchone()[0]

# print(f"Total rows: {total}")

# # Total of columns
# columns = con.execute(
#     """
#     DESCRIBE
#     SELECT *
#     FROM read_csv(
#         ?,
#         delim=';',
#         header=true,
#         encoding='latin-1'
#     )
# """,
#  [str(file_path)]
# ).fetchall()

# for column in columns:
#     print(column[0], "-", column[1])

# # Cargos
# cargos = con.execute(
#     """
#     SELECT
#         CD_CARGO,
#         DS_CARGO,
#         COUNT(*) AS rows
#     FROM read_csv(
#         ?,
#         delim=';',
#         header=true,
#         encoding='latin-1'
#     )
#     GROUP BY
#         CD_CARGO,
#         DS_CARGO
#     ORDER BY
#         CD_CARGO
#     """,
#     [str(file_path)],
# ).fetchdf()

# print(cargos)

# # Turnos
# turnos = con.execute(
#     """
#     SELECT
#         NR_TURNO,
#         COUNT(*) AS rows
#     FROM read_csv(
#         ?,
#         delim=';',
#         header=true,
#         encoding='latin-1'
#     )
#     GROUP BY NR_TURNO
#     ORDER BY NR_TURNO
#     """,
#     [str(file_path)],
# ).fetchdf()

# print(turnos)

# President
# presidente = con.execute(
#     """
#     SELECT
#         NR_TURNO,
#         SG_UF,
#         CD_MUNICIPIO,
#         NM_MUNICIPIO,
#         NR_ZONA,

#         SQ_CANDIDATO,
#         NR_CANDIDATO,
#         NM_URNA_CANDIDATO,

#         SG_PARTIDO,

#         QT_VOTOS_NOMINAIS,
#         QT_VOTOS_NOMINAIS_VALIDOS

#     FROM read_csv(
#         ?,
#         delim=';',
#         header=true,
#         encoding='latin-1'
#     )

#     WHERE UPPER(DS_CARGO) = 'PRESIDENTE'

#     LIMIT 20
#     """,
#     [str(file_path)],
# ).fetchdf()

# print(presidente)

# resultado_municipio = con.execute(
#     """
#     SELECT
#         NR_TURNO,

#         SG_UF,
#         CD_MUNICIPIO,
#         NM_MUNICIPIO,

#         SQ_CANDIDATO,
#         NR_CANDIDATO,
#         NM_URNA_CANDIDATO,

#         SG_PARTIDO,

#         SUM(QT_VOTOS_NOMINAIS) AS votos

#     FROM read_csv(
#         ?,
#         delim=';',
#         header=true,
#         encoding='latin-1'
#     )

#     WHERE
#         UPPER(DS_CARGO) = 'PRESIDENTE'

#     GROUP BY
#         NR_TURNO,

#         SG_UF,
#         CD_MUNICIPIO,
#         NM_MUNICIPIO,

#         SQ_CANDIDATO,
#         NR_CANDIDATO,
#         NM_URNA_CANDIDATO,

#         SG_PARTIDO

#     ORDER BY
#         NM_MUNICIPIO,
#         votos DESC
#     """,
#     [str(file_path)],
# ).fetchdf()

# print(resultado_municipio.head(30))

