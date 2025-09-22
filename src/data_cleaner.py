import pandas as pd
import re
from typing import Dict

class DataCleaner:
    def __init__(self, patterns: Dict[str, str], column_mappings: Dict[str, str]):
        self.patterns = patterns
        self.column_mappings = column_mappings
    
    def clean_dataframe(self, df: pd.DataFrame, year: int) -> pd.DataFrame:
        df.columns = self._clean_headers(df.columns.to_list())
        df = self._clean_text_columns(df)
        df = self._clean_numeric_columns(df)
        df = self._clean_rank_column(df, year)
        return df

    def _clean_headers(self, headers: list) -> list:
        cleaned_headers = []
        for header in headers:
            header = header.lower().replace('\n', ' ').strip()
            header = re.sub(r'\[\d+\]$', '', header)
            header = self.column_mappings.get(header, header)
            cleaned_headers.append(header)
        return cleaned_headers
    
    def _clean_text_columns(self, df: pd.DataFrame) -> pd.DataFrame:

        for col in ["club", "player", "nationality"]:
            if col in df.columns:
                df[col] = df[col].str.replace(self.patterns.get("reference_notes", ''), '', regex=True).str.strip()
        return df
    
    def _clean_numeric_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        if "points" in df.columns:
                df["points"] = df["points"].astype(str).str.replace(r'(\d)\s*\[\d+\]$', r'\1', regex=True)
                df["points"] = pd.to_numeric(df["points"], errors="coerce").ffill()
        return df

    def _clean_rank_column(self, df: pd.DataFrame, year: int) -> pd.DataFrame:
        if "rank" in df.columns:
                df["rank"] = df["rank"].replace("MISSING_RANK", pd.NA)
                df["rank"] = df["rank"].ffill()
                df["rank"] = df["rank"].astype(str).str.replace(r'(\d+)[a-zA-Z]{2}$', r'\1', regex=True)
                df["rank"] = df["rank"].str.strip().str.replace(" ", "")
                df["rank"] = df["rank"].astype(float, errors="raise")
        return df

    def clean_multi_year_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.dropna(subset=["nationality", "player", "club"], how="any")
        df = df.rename({"points": "votes", "total": "points"}, axis=1)
        df[["1st", "2nd", "3rd", "4th", "5th"]] = df[["1st", "2nd", "3rd", "4th", "5th"]].apply(pd.to_numeric, errors='coerce')

        # Special calculation for 2005 points
        df_2005_mask = df["year"] == 2005
        df.loc[df_2005_mask, "points"] = (
            df.loc[df_2005_mask, "1st"].astype(float).fillna(0) * 5 +
            df.loc[df_2005_mask, "2nd"].astype(float).fillna(0) * 4 +
            df.loc[df_2005_mask, "3rd"].astype(float).fillna(0) * 3 +
            df.loc[df_2005_mask, "4th"].astype(float).fillna(0) * 2 +
            df.loc[df_2005_mask, "5th"].astype(float).fillna(0) * 1
        )

        # For each year, count non-null ranks and assign count+1 to missing ranks
        for _, group in df.groupby("year"):
            non_null_count = group["rank"].notna().sum()
            missing_mask = group["rank"].isna()
            df.loc[group.index[missing_mask], "rank"] = str(non_null_count + 1)

        df["points"] = df["points"].astype(float).fillna(0).astype(int)
        df["votes"] = df["votes"].astype(float).fillna(0).astype(int)
        df["rank"] = df["rank"].astype(int)
        return df

    def calculate_percentage(self, df: pd.DataFrame) -> pd.DataFrame:
        if "percent" in df.columns:
            df["percent"] = df["percent"].str.replace('%', '', regex=False)
            df["percent"] = df["percent"].astype(float)
        else:
            df["percent"] = pd.NA

        for year in df["year"].unique():
            year_mask = df["year"] == year
            if df.loc[year_mask, "percent"].isnull().all():
                try:
                    total_points = df.loc[year_mask, "points"].astype(float).sum()
                    if total_points > 0:
                        df.loc[year_mask, "percent"] = (
                            (df.loc[year_mask, "points"].astype(float) * 100 / total_points).round(4)
                        )
                except Exception as e:
                    print(f"Error calculating percentage for year {year}: {e}")
                    df.loc[year_mask, "percent"] = pd.NA
        return df