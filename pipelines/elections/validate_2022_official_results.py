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
    / "president_municipality_results_2022.parquet"
)

con = duckdb.connect()

candidate_totals = con.execute(
    """
    SELECT
        election_round,
        candidate_number,
        candidate_ballot_name,
        party_code,

        SUM(votes) AS votes

    FROM read_parquet(?)

    GROUP BY
        election_round,
        candidate_number,
        candidate_ballot_name,
        party_code

    ORDER BY
        election_round,
        votes DESC
    """,
    [str(FILE)],
).fetchdf()


print(candidate_totals)

OFFICIAL_FIRST_ROUND = {
    13: 57_259_504,
    22: 51_072_345,
}
for candidate_number, expected_votes in OFFICIAL_FIRST_ROUND.items():

    actual_votes = con.execute(
        """
        SELECT SUM(votes)

        FROM read_parquet(?)

        WHERE
            election_round = 1
            AND candidate_number = ?
        """,
        [
            str(FILE),
            candidate_number,
        ],
    ).fetchone()[0]

    print(
        f"Candidato {candidate_number}: "
        f"esperado={expected_votes:,} "
        f"obtido={actual_votes:,}"
    )

    assert actual_votes == expected_votes

OFFICIAL_SECOND_ROUND = {
    13: 60_345_999,
    22: 58_206_354,
}

for candidate_number, expected_votes in OFFICIAL_SECOND_ROUND.items():

    actual_votes = con.execute(
        """
        SELECT SUM(votes)

        FROM read_parquet(?)

        WHERE
            election_round = 2
            AND candidate_number = ?
        """,
        [
            str(FILE),
            candidate_number,
        ],
    ).fetchone()[0]

    print(
        f"Candidato {candidate_number}: "
        f"esperado={expected_votes:,} "
        f"obtido={actual_votes:,}"
    )

    assert actual_votes == expected_votes



first_round_totals = con.execute(
    """
    WITH municipalities AS (

        SELECT DISTINCT
            election_year,
            election_round,
            state_code,
            tse_municipality_code,

            eligible_voters,
            turnout,
            abstentions,
            total_votes,
            valid_votes,
            blank_votes,
            null_votes

        FROM read_parquet(?)

        WHERE election_round = 1

    )

    SELECT
        SUM(eligible_voters) AS eligible_voters,
        SUM(turnout) AS turnout,
        SUM(abstentions) AS abstentions,
        SUM(valid_votes) AS valid_votes,
        SUM(blank_votes) AS blank_votes,
        SUM(null_votes) AS null_votes

    FROM municipalities
    """,
    [str(FILE)],
).fetchdf()


print(first_round_totals)

EXPECTED_FIRST_ROUND = {
    "eligible_voters": 156_454_011,
    "turnout": 123_682_372,
    "abstentions": 32_770_982,
    "valid_votes": 118_229_719,
    "blank_votes": 1_964_779,
    "null_votes": 3_487_874,
}

row = first_round_totals.iloc[0]

for column, expected in EXPECTED_FIRST_ROUND.items():

    actual = int(row[column])

    print(
        f"{column}: "
        f"esperado={expected:,} "
        f"obtido={actual:,} "
        f"diferença={actual - expected:,}"
    )



states = con.execute(
    """
    SELECT DISTINCT state_code

    FROM read_parquet(?)

    ORDER BY state_code
    """,
    [str(FILE)],
).fetchdf()


print(states)




invalid_electorate = con.execute(
    """
    WITH municipalities AS (

        SELECT DISTINCT
            election_year,
            election_round,
            state_code,
            tse_municipality_code,

            eligible_voters,
            turnout,
            abstentions

        FROM read_parquet(?)

    )

    SELECT *
    FROM municipalities

    WHERE
        eligible_voters
        != turnout + abstentions
    """,
    [str(FILE)],
).fetchdf()


print(
    f"Inconsistências de eleitorado: "
    f"{len(invalid_electorate)}"
)


invalid_vote_share = con.execute(
    """
    SELECT *

    FROM read_parquet(?)

    WHERE
        votes > valid_votes
        OR vote_share < 0
        OR vote_share > 1
    """,
    [str(FILE)],
).fetchdf()


print(
    f"Vote shares inválidos: "
    f"{len(invalid_vote_share)}"
)


invalid_rates = con.execute(
    """
    SELECT *

    FROM read_parquet(?)

    WHERE
        turnout_rate < 0
        OR turnout_rate > 1

        OR abstention_rate < 0
        OR abstention_rate > 1
    """,
    [str(FILE)],
).fetchdf()


print(
    f"Taxas inválidas: {len(invalid_rates)}"
)



vote_share_errors = con.execute(
    """
    SELECT
        election_round,
        state_code,
        tse_municipality_code,
        municipality_name,

        SUM(vote_share) AS vote_share_sum

    FROM read_parquet(?)

    GROUP BY
        election_round,
        state_code,
        tse_municipality_code,
        municipality_name

    HAVING
        ABS(SUM(vote_share) - 1.0) > 0.000001

    ORDER BY
        ABS(SUM(vote_share) - 1.0) DESC
    """,
    [str(FILE)],
).fetchdf()


print(vote_share_errors)



print()
print("====================================")
print(" DATA QUALITY REPORT - TSE 2022")
print("====================================")

# print(
#     f"Duplicated records: {len(duplicates)}"
# )

# print(
#     f"Missing turnout: {missing_turnout}"
# )

print(
    f"Invalid electorate totals: "
    f"{len(invalid_electorate)}"
)

print(
    f"Invalid vote shares: "
    f"{len(invalid_vote_share)}"
)

print(
    f"Invalid rates: "
    f"{len(invalid_rates)}"
)

print("====================================")