from pathlib import Path
import duckdb

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "tse"
    / "2022"
    / "voting"
    / "votacao_candidato_munzona_2022"
    / "votacao_candidato_munzona_2022_BR.csv"
)

OUTPUT_DIR = (
    BASE_DIR
    / "data"
    / "processed"
    / "tse"
    / "2022"
    / "president"
)

OUTPUT_FILE = OUTPUT_DIR / "president_votes_by_municipality.parquet"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

con = duckdb.connect()

query = """
    SELECT
        ANO_ELEICAO AS election_year,
        NR_TURNO AS election_round,

        SG_UF AS state_code,

        CD_MUNICIPIO AS municipality_code,
        NM_MUNICIPIO AS municipality_name,

        SQ_CANDIDATO AS candidate_sequence,
        NR_CANDIDATO AS candidate_number,

        NM_CANDIDATO AS candidate_name,
        NM_URNA_CANDIDATO AS candidate_ballot_name,

        NR_PARTIDO AS party_number,
        SG_PARTIDO AS party_code,
        NM_PARTIDO AS party_name,

        SUM(QT_VOTOS_NOMINAIS) AS votes

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
    NM_MUNICIPIO,
    SQ_CANDIDATO,
    NR_CANDIDATO,
    NM_CANDIDATO,
    NM_URNA_CANDIDATO,
    NR_PARTIDO,
    SG_PARTIDO,
    NM_PARTIDO
"""

df = con.execute(query, [str(INPUT_FILE)]).fetchdf()

print(df.head())

print()
print(f"Rows: {len(df):,}")

con.execute(
    """
    COPY (
    SELECT * FROM df    
    )
    TO ?
    (FORMAT PARQUET, COMPRESSION ZSTD)    
""",
[str(OUTPUT_FILE)]
)

print()
print(f"Created: {OUTPUT_FILE}")