import pandas as pd
from collections import defaultdict
from collections.abc import MutableSet


def process_raw(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, MutableSet]]:
    """
    Sanitize raw dataframe and cache a set of unique element in some columns

    Parameters:
        df: raw dataframe

    Returns:
        pd.DataFrame: processed dataframe
        Dict[str, MutableSet]: a dictionary of set of unique element in some columns
    """

    # create new column to store sanitized data
    df = df.assign(
        genres_n="", creators_n="", publishers_n="", franchises_n="", regions_n=""
    )

    def data_sanitizer():
        """
        Return a function that contains logic to sanitize the dataframe

        Parameters:
            None

        Returns:
            function: a function sanitizing one row dataframe
        """
        def helper(row: pd.core.series.Series) -> pd.core.series.Series:
            """
            A function containing logic to santize one dataframe row,
            while building up a set of unique element in some columns

            Parameters:
            row (pd.core.series.Series): a dataframe row

            Returns:
            pd.core.series.Series: a dataframe row
            """
            helper.dataset_dict["media_types"].add(row["media_type"])

            if row["genres"].strip() != "{}":
                # remove leading and tailing {}
                row["genres_n"] = row["genres"][1:-1]
                helper.dataset_dict["genres"].update(row["genres_n"].split(","))

            if row["created_by"].strip() != "{}":
                # remove leading and tailing {}
                row["creators_n"] = row["created_by"][1:-1]
                helper.dataset_dict["creators"].update(row["creators_n"].split(","))

            if row["published_by"].strip() != "{}":
                # remove leading and tailing {}
                row["publishers_n"] = row["published_by"][1:-1]
                helper.dataset_dict["publishers"].update(row["publishers_n"].split(","))

            if row["franchises"].strip() != "{}":
                # remove leading and tailing {}
                row["franchises_n"] = row["franchises"][1:-1]
                helper.dataset_dict["franchises"].update(row["franchises_n"].split(","))

            if not pd.isna(row["regions"]) and row["regions"].strip() != "":
                # remove leading and tailing {}
                row["regions_n"] = row["regions"][1:-1]
                regions = row["regions_n"].split(",")
                # remvoe leading white space
                regions = map(lambda s: s.strip(), regions)
                helper.dataset_dict["regions"].update(regions)

            return row

        helper.dataset_dict = defaultdict(lambda: set())

        return helper

    sanitizer = data_sanitizer()
    df = df.apply(sanitizer, axis=1)
    df = df.drop(["genres", "created_by", "published_by", "franchises", "regions"], axis=1)

    return df, dict(sanitizer.dataset_dict)
