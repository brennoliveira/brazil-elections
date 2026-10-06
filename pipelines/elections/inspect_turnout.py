from pathlib import Path
import duckdb


BASE_DIR = Path(__file__).resolve().parents[2]

FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "tse"
    / "2022"
    / "turnout"
    / "detalhe_votacao_munzona_2022_.csv"
    / "detalhe_votacao_munzona_2022_BR.csv"
)

con = duckdb.connect()


schema = con.execute(
    """
    DESCRIBE
    SELECT *
    FROM read_csv(
        ?,
        delim=';',
        header=true,
        encoding='latin-1'
    )
    """,
    [str(FILE)],
).fetchdf()

print(schema)