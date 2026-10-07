from pathlib import Path
import duckdb


BASE_DIR = Path(__file__).resolve().parents[3]

FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "tse"
    / "2022"
    / "president"
    / "president_municipality_results_2022.parquet"
)


con = duckdb.connect()


# missing = con.execute(
#     """
#     SELECT COUNT(*)

#     FROM read_parquet(?)

#     WHERE eligible_voters IS NULL
#     """,
#     [str(FILE)],
# ).fetchone()[0]


# print(
#     f"Linhas sem dados de comparecimento: {missing}"
# )

# aracaju = con.execute(
#     """
#     SELECT
#         candidate_ballot_name,
#         party_code,

#         votes,

#         ROUND(vote_share * 100, 2)
#             AS vote_share_percent,

#         eligible_voters,
#         turnout,
#         abstentions,

#         ROUND(turnout_rate * 100, 2)
#             AS turnout_percent,

#         ROUND(abstention_rate * 100, 2)
#             AS abstention_percent,

#         blank_votes,
#         null_votes

#     FROM read_parquet(?)

#     WHERE
#         election_round = 1
#         AND state_code = 'SE'
#         AND municipality_name = 'ARACAJU'

#     ORDER BY votes DESC
#     """,
#     [str(FILE)],
# ).fetchdf()


# print(aracaju)

# vote_share_sum = con.execute(
#     """
#     SELECT
#         state_code,
#         municipality_name,
#         election_round,

#         SUM(vote_share) AS total_vote_share

#     FROM read_parquet(?)

#     WHERE election_round = 1

#     GROUP BY
#         state_code,
#         municipality_name,
#         election_round

#     ORDER BY total_vote_share DESC

#     LIMIT 20
#     """,
#     [str(FILE)],
# ).fetchdf()


# print(vote_share_sum)

# national = con.execute(
#     """
#     SELECT
#         candidate_ballot_name,
#         party_code,

#         SUM(votes) AS votes

#     FROM read_parquet(?)

#     WHERE election_round = 1

#     GROUP BY
#         candidate_ballot_name,
#         party_code

#     ORDER BY votes DESC
#     """,
#     [str(FILE)],
# ).fetchdf()


# print(national)

# duplicates = con.execute(
#     """
#     SELECT
#         election_year,
#         election_round,
#         state_code,
#         tse_municipality_code,
#         candidate_number,

#         COUNT(*) AS occurrences

#     FROM read_parquet(?)

#     GROUP BY
#         election_year,
#         election_round,
#         state_code,
#         tse_municipality_code,
#         candidate_number

#     HAVING COUNT(*) > 1

#     ORDER BY occurrences DESC
#     """,
#     [str(FILE)],
# ).fetchdf()


# print(duplicates)

# winners = con.execute(
#     """
#     WITH ranking AS (

#         SELECT
#             *,

#             ROW_NUMBER() OVER (
#                 PARTITION BY
#                     election_year,
#                     election_round,
#                     state_code,
#                     municipality_code

#                 ORDER BY votes DESC
#             ) AS position

#         FROM read_parquet(?)

#     )

#     SELECT
#         state_code,
#         municipality_code,
#         municipality_name,

#         candidate_ballot_name,
#         party_code,

#         votes,

#         ROUND(vote_share * 100, 2)
#             AS vote_share_percent

#     FROM ranking

#     WHERE
#         election_round = 1
#         AND position = 1

#     ORDER BY
#         state_code,
#         municipality_name
#     """,
#     [str(FILE)],
# ).fetchdf()


# print(winners.head(50))

VOTES_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "tse"
    / "2022"
    / "president"
    / "president_votes_by_municipality.parquet"
)

RESULTS_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "tse"
    / "2022"
    / "president"
    / "president_municipality_results_2022.parquet"
)

before = con.execute(
    """
    SELECT SUM(votes)
    FROM read_parquet(?)
    """,
    [str(VOTES_FILE)],
).fetchone()[0]


after = con.execute(
    """
    SELECT SUM(votes)
    FROM read_parquet(?)
    """,
    [str(RESULTS_FILE)],
).fetchone()[0]


print(f"Antes do JOIN: {before:,}")
print(f"Depois do JOIN: {after:,}")
print(f"Diferença: {after - before:,}")

missing_turnout = con.execute(
    """
    SELECT COUNT(*)

    FROM read_parquet(?)

    WHERE
        eligible_voters IS NULL
        OR turnout IS NULL
        OR valid_votes IS NULL
    """,
    [str(RESULTS_FILE)],
).fetchone()[0]


print(
    f"Linhas sem dados de totalização: {missing_turnout}"
)