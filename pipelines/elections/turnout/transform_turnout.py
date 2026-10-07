from pathlib import Path
import duckdb

BASE_DIR = Path(__file__).resolve().parents[3]

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "tse"
    / "2022"
    / "turnout"
    / "detalhe_votacao_munzona_2022"
    / "detalhe_votacao_munzona_2022_BR.csv"
)

OUTPUT_DIR = BASE_DIR / "data" / "processed" / "tse" / "2022" / "president"

OUTPUT_FILE = ( OUTPUT_DIR / "municipality_turnout_2022.parquet" )

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


con = duckdb.connect()

query = """
SELECT
    ANO_ELEICAO AS election_year,
    NR_TURNO AS election_round,

    SG_UF AS state_code,

    CD_MUNICIPIO AS tse_municipality_code,
    NM_MUNICIPIO AS municipality_name,

    SUM(QT_APTOS) AS eligible_voters,
    SUM(QT_COMPARECIMENTO) AS turnout,
    SUM(QT_ABSTENCOES) AS abstentions,

    SUM(QT_VOTOS) AS total_votes,
    SUM(QT_TOTAL_VOTOS_VALIDOS) AS valid_votes,
    SUM(QT_VOTOS_BRANCOS) AS blank_votes,
    SUM(QT_TOTAL_VOTOS_NULOS) AS null_votes,

    SUM(QT_VOTOS_ANULADOS_APU_SEP)
        AS votes_pending_judicial_decision

FROM read_csv(
    ?,
    delim=';',
    header=true,
    encoding='latin-1'
)

WHERE
    UPPER(TRIM(DS_CARGO)) = 'PRESIDENTE'

GROUP BY
    ANO_ELEICAO,
    NR_TURNO,
    SG_UF,
    CD_MUNICIPIO,
    NM_MUNICIPIO

ORDER BY
    SG_UF,
    NM_MUNICIPIO,
    NR_TURNO
"""

df = con.execute(
    query,
    [str(INPUT_FILE)],
).fetchdf()

print(df.head())

print()
print(f"Linhas geradas: {len(df):,}")

con.execute(
    """
    COPY (
        SELECT * FROM df
    )
    TO ?
    (
        FORMAT PARQUET,
        COMPRESSION ZSTD
    )
    """,
    [str(OUTPUT_FILE)]
)


print()
print(f"Arquivo criado: {OUTPUT_FILE}")

print(
    con.execute(
        """
        SELECT
            DS_CARGO,
            COUNT(*) AS rows
        FROM read_csv(
            ?,
            delim=';',
            header=true,
            encoding='latin-1'
        )
        GROUP BY DS_CARGO
        ORDER BY DS_CARGO
        """,
        [str(INPUT_FILE)],
    ).fetchdf()
)