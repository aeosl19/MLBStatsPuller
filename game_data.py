import queries
import datetime as dt


# from models import Games

def update_historic_games(toDate):
    updated = queries.check_last_update('games')
    games = pd.DataFrame()

    if updated:
        if updated == yesterday:
            print('Games up to date')
            return

        elif updated.year == yesterday.year:
            games = fetch.get_games(season='{}'.format(updated.year),
                                    fromDate='{}'.format(updated + dt.timedelta(1)),
                                    toDate='{}'.format(yesterday), is_historic=True)

        elif updated.year < yesterday.year:
            for i in range(updated.year, yesterday.year + 1):
                print('from loop, year: {}'.format(i))
                games = games.append(fetch.get_games(season='{}'.format(i),
                                                     fromDate='{}-03-15'.format(i),
                                                     toDate='{}-11-10'.format(i), is_historic=True))

        else:
            games = fetch.get_games(season=updated.year, fromDate='{}'.format(updated + dt.timedelta(1)),
                                    toDate='{}'.format(yesterday), is_historic=True)

    else:
        print('Update is None')
        for i in range(2018, yesterday.year + 1):
            if i == yesterday.year:
                games = games.append(fetch.get_games(season='{}'.format(i),
                                                     fromDate='{}-03-15'.format(i),
                                                     toDate='{}'.format(yesterday), is_historic=True))

            else:
                games = games.append(fetch.get_games(season='{}'.format(i),
                                                     fromDate='{}-03-15'.format(i),
                                                     toDate='{}-11-10'.format(i), is_historic=True))

    try:
        games = utils.clean_historic_game(games)
        queries.insert_data(tablename='games', data=games, replace_add='append')
    except Exception as ex:
        print('Dataframe empty no games has been played:', ex)
