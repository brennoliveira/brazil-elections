from pathlib import Path
import duckdb


BASE_DIR = Path(__file__).resolve().parents[2]

FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "tse"
    / "2022"
    / "president"
    / "municipality_turnout_2022.parquet"
)

con = duckdb.connect()


votes_validation = con.execute(
    """
    SELECT
        municipality_name,

        total_votes,

        valid_votes,

        blank_votes,

        null_votes,

        votes_pending_judicial_decision,

        total_votes
        - (
            valid_votes
            + blank_votes
            + null_votes
            + votes_pending_judicial_decision
        ) AS difference

    FROM read_parquet(?)

    WHERE
        state_code = 'SE'
        AND municipality_name = 'ARACAJU'
        AND election_round = 1
    """,
    [str(FILE)]
).fetchdf()


print(votes_validation)