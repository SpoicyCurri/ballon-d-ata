import pandas as pd
from raceplotly.plots import barplot


def main():
    path = "data/ballon_dor_all_years.csv"
    data = pd.read_csv(path)
    data.loc[(data["player"] == "Luis Suárez") & (data["year"] > 1990), "player"] = "Luis Suárez (modern)"
    data = data.groupby(["year", "player"]).size().reset_index(name='count')
    years = data['year'].unique()
    players = data['player'].unique()
    full_index = pd.MultiIndex.from_product([years, players], names=['year', 'player'])
    data = data.set_index(['year', 'player']).reindex(full_index, fill_value=0).reset_index()
    data = data.sort_values(['player', 'year'], ascending=[True, True])
    data['cumulative_count'] = data.groupby('player')['count'].cumsum()
    first_nom_years = data[data['count'] > 0].groupby('player')['year'].transform('min')
    last_nom_years = data[data['count'] > 0].groupby('player')['year'].transform('max')
    data['first_nomination_year'] = first_nom_years
    data['last_nomination_year'] = last_nom_years
    data['last_nomination_year'] = data['last_nomination_year'].ffill()
    data = data[(data['year'] <= data['last_nomination_year'])]

    my_raceplot = barplot(data,
                        item_column='player',
                        value_column='cumulative_count',
                        time_column='year')

    fig = my_raceplot.plot(title = 'Top 10 Players in Ballon d\'Or from 1956 to 2024',
                    item_label = 'Players',
                    value_label = 'Cumulative Count',
                    frame_duration = 1500)

    fig.write_html("visuals/outputs/bar_chart_race_output.html")

if __name__ == "__main__":
    main()
    