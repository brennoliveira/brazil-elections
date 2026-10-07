from pathlib import Path
import duckdb


BASE_DIR = Path(__file__).resolve().parents[3]

VOTES_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "tse"
    / "2022"
    / "president"
    / "president_votes_by_municipality.parquet"
)

TURNOUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "tse"
    / "2022"
    / "president"
    / "municipality_turnout_2022.parquet"
)

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "tse"
    / "2022"
    / "president"
    / "president_municipality_results_2022.parquet"
)


con = duckdb.connect()


query = """
SELECT
    v.election_year,
    v.election_round,

    v.state_code,

    v.municipality_code AS tse_municipality_code,
    v.municipality_name,

    v.candidate_number,
    v.candidate_name,
    v.candidate_ballot_name,

    v.party_number,
    v.party_code,
    v.party_name,

    v.votes,

    t.eligible_voters,
    t.turnout,
    t.abstentions,

    t.total_votes,
    t.valid_votes,
    t.blank_votes,
    t.null_votes,

    t.votes_pending_judicial_decision,

    CASE
        WHEN t.valid_votes > 0
        THEN v.votes::DOUBLE / t.valid_votes
        ELSE NULL
    END AS vote_share,

    CASE
        WHEN t.eligible_voters > 0
        THEN t.turnout::DOUBLE / t.eligible_voters
        ELSE NULL
    END AS turnout_rate,

    CASE
        WHEN t.eligible_voters > 0
        THEN t.abstentions::DOUBLE / t.eligible_voters
        ELSE NULL
    END AS abstention_rate,

    CASE
        WHEN t.turnout > 0
        THEN t.blank_votes::DOUBLE / t.turnout
        ELSE NULL
    END AS blank_vote_rate,

    CASE
        WHEN t.turnout > 0
        THEN t.null_votes::DOUBLE / t.turnout
        ELSE NULL
    END AS null_vote_rate

FROM read_parquet(?) v

LEFT JOIN read_parquet(?) t

    ON v.election_year = t.election_year
    AND v.election_round = t.election_round
    AND v.state_code = t.state_code
    AND v.municipality_code = t.tse_municipality_code
"""


df = con.execute(
    query,
    [
        str(VOTES_FILE),
        str(TURNOUT_FILE),
    ],
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
    [str(OUTPUT_FILE)],
)


print()
print(f"Arquivo criado: {OUTPUT_FILE}")