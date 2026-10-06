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
    / "president_votes_by_municipality.parquet"
)


con = duckdb.connect()


# result = con.execute(
#     """
#     SELECT
#         state_code,
#         municipality_name,
#         candidate_ballot_name,
#         party_code,
#         votes

#     FROM read_parquet(?)

#     WHERE
#         election_round = 1
#         AND state_code = 'SE'
#         AND municipality_name = 'ARACAJU'

#     ORDER BY votes DESC
#     """,
#     [str(FILE)],
# ).fetchdf()


# print(result)

# municipalities = con.execute(
#     """
#     SELECT
#         COUNT(DISTINCT municipality_code)
#     FROM read_parquet(?)

#     WHERE election_round = 1
#     """,
#     [str(FILE)],
# ).fetchone()[0]


# print(
#     f"Municipalities: {municipalities:,}"
# )

# states = con.execute(
#     """
#     SELECT
#         state_code,
#         COUNT(DISTINCT municipality_code) AS municipalities

#     FROM read_parquet(?)

#     WHERE election_round = 1

#     GROUP BY state_code

#     ORDER BY state_code
#     """,
#     [str(FILE)],
# ).fetchdf()


# print(states)

national = con.execute(
    """
    SELECT
        candidate_ballot_name,
        party_code,
        SUM(votes) AS votes

    FROM read_parquet(?)

    WHERE election_round = 1

    GROUP BY
        candidate_ballot_name,
        party_code

    ORDER BY votes DESC
    """,
    [str(FILE)],
).fetchdf()


print(national)