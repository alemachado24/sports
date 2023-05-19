import pandas as pd
import numpy as np
import streamlit as st
import json
from urllib.request import urlopen
import plotly.express as px

#cd Desktop/AleClasses/sports
#streamlit run sports.py

st.set_page_config(page_title="Sports %", page_icon="🏅",layout="wide",)

st.title("Sports Forecast 🏅")

# st.image("https://wallpapercave.com/dwp2x/83KPCfi.jpg",width=1500)

page_bg_img = """
<style>
body {
background-image: url("https://wallpapercave.com/dwp2x/83KPCfi.jpg");
background-size: cover;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

st.caption("This app shows fiverhityeight predictions for multiple spots gathered in one page")
st.caption("")
st.caption("Sports shown: MLB, NBA, NFL, NHL & Soccer")

#sidebar
selected_year = st.selectbox('Year', list(reversed(range(2020,2024))))

###################################### MLB STARTS ##############################################

team_names = ['Dodgers','Astros','Braves','Yankees','Mets','Padres','Blue Jays','Guardians','Rays','Brewers','Cardinals','Twins','Phillies','Angels','Mariners','Giants','Rangers','Red Sox','White Sox','Marlins','Cubs','Orioles','Diamondbacks','Reds','Pirates','Rockies','Tigers','Royals','Athletics','Nationals']

team_names.sort()
  
    
# store the URL in url as 
# parameter for urlopen
url = f'https://projects.fivethirtyeight.com/{selected_year}-mlb-predictions/data.json'
  
# store the response of URL
response = urlopen(url)
  
# storing the JSON response 
# from url in data
data_json = json.loads(response.read())

data = []
for row in data_json['games']:
    data.append(row)

# print(url)
df = pd.json_normalize(data)

df_final=df.drop(['id','datetime','neutral','pitcher1_id','pitcher2_id','pitcher1',
                  'pitcher2','playoff','rating1','rating2','rating1_post',
                  'rating2_post','dist_adj1','dist_adj2','rest_adj1','rest_adj2',
                 'pitcher_adj1','pitcher_adj2','opener1','opener2','hfa_adj',
                 'favorite','underdog','favprob','dogprob'], axis=1)

first_column = df_final.pop('date')
  
# first_column) function
df_final.insert(1, 'Date', first_column)
# df_final['team1'] = df_final['team1'].str.replace(df_final['team1'],selected_team_full[0])

df_final['prob2'] = df_final['prob2']*100
df_final['prob1'] = df_final['prob1']*100

df_final['team1'] = df_final['team1'] .map({'HOU': 'Astros', 'LAD': 'Dodgers','ATL': 'Braves', 'NYY': 'Yankees',
                                            'NYM': 'Mets', 'SD': 'Padres','TOR': 'Blue Jays', 'CLE': 'Guardians',
                                            'TB': 'Rays', 'MIL': 'Brewers','STL': 'Cardinals', 'MIN': 'Twins',
                                            'PHI': 'Phillies', 'LAA': 'Angels','SEA': 'Mariners', 'SF': 'Giants',
                                            'TEX': 'Rangers', 'BOS': 'Red Sox','CHW': 'White Sox', 'MIA': 'Marlins',
                                            'CHC': 'Cubs', 'BAL': 'Orioles','ARI': 'Diamondbacks', 'CIN': 'Reds',
                                            'PIT': 'Pirates', 'COL': 'Rockies','DET': 'Tigers', 'KC': 'Royals',
                                            'OAK': 'Athletics', 'WSH': 'Nationals'})

df_final['team2'] = df_final['team2'] .map({'HOU': 'Astros', 'LAD': 'Dodgers','ATL': 'Braves', 'NYY': 'Yankees',
                                            'NYM': 'Mets', 'SD': 'Padres','TOR': 'Blue Jays', 'CLE': 'Guardians',
                                            'TB': 'Rays', 'MIL': 'Brewers','STL': 'Cardinals', 'MIN': 'Twins',
                                            'PHI': 'Phillies', 'LAA': 'Angels','SEA': 'Mariners', 'SF': 'Giants',
                                            'TEX': 'Rangers', 'BOS': 'Red Sox','CHW': 'White Sox', 'MIA': 'Marlins',
                                            'CHC': 'Cubs', 'BAL': 'Orioles','ARI': 'Diamondbacks', 'CIN': 'Reds',
                                            'PIT': 'Pirates', 'COL': 'Rockies','DET': 'Tigers', 'KC': 'Royals',
                                            'OAK': 'Athletics', 'WSH': 'Nationals'})

# df2 = df_final.reset_index(drop=True)

# st.write(df2)

upcoming_games = df_final.loc[df_final['status']=='pre']
past_games = df_final.loc[df_final['status']=='post']

# st.dataframe(upcoming_games)

upcoming_games=upcoming_games.drop(['status','score1','score2'], axis=1)




def highlight_green(val):
    '''
    highlight the maximum in a Series yellow.
    '''
    color = 'lightgreen' if str(val) > str(65) else 'white'
    return 'background-color: %s' % color
upcoming_games_color = upcoming_games.style.format(precision=0).applymap(highlight_green, subset=['prob1','prob2'])


predicted = np.where((((past_games['score1']>past_games['score2']) & (past_games['prob1']>past_games['prob2'])) | ((past_games['score1']<past_games['score2']) & (past_games['prob1']<past_games['prob2']))) , 'Predicted', 'Turnaround')

new_analysis = np.where((past_games['score1']>past_games['score2']) , 'W', 'L')

column_results=pd.DataFrame(new_analysis, columns=['Results'])
column_predicted=pd.DataFrame(predicted, columns=['Predicted'])

combined_list = pd.concat([past_games,column_results,column_predicted], axis=1)
combined_list=combined_list.drop(['status'], axis=1)
combined_list2=combined_list.sort_values(by=['Date'],ascending=False)

groupped_scores = combined_list.groupby(['prob1','Results','Predicted']).size()

st.title("MLB Forecast ⚾️")

option1, option2 = st.columns(2)
with option1:
    st.header('Upcoming Games')
    list_dates =  upcoming_games['Date'].sort_values(ascending=True).unique()
    dates = st.selectbox('Date', list_dates)
    try:
        try:
            filtered_dates = upcoming_games[(upcoming_games['Date']==dates)]
            upcoming_games_color2 = filtered_dates.style.format(precision=0).applymap(highlight_green, subset=['prob1','prob2'])
    #         st.write(upcoming_games_color2.hide(axis=0).to_html(), unsafe_allow_html=True)
            st.dataframe(upcoming_games_color2)
        except:
            st.dataframe(upcoming_games_color)
    except:
        st.warning('Check later for Upcoming Games')
with option2:
    st.header('Past Games')
    selected_team_full = st.multiselect('',team_names,default = team_names[5])
    try:
        try:
            filtered_both_teams = combined_list2[(combined_list2['team1']==selected_team_full[0]) | (combined_list2['team2']==selected_team_full[0])]
            filtered_both_teams2= filtered_both_teams.style.hide_index().format(precision=0)
    #         st.write(filtered_both_teams2.hide(axis=0).to_html(), unsafe_allow_html=True)
            st.dataframe(filtered_both_teams2)
        except:
            combined_list22= combined_list2.style.hide_index().format(precision=0)
            st.dataframe(combined_list22)
    except:
        st.warning('Check later for Upcoming Games')


###################################### MLB ENDS ##############################################

###################################### NBA STARTS ##############################################

st.title("NBA Forecast 🏀")

team_names_nba = ['Boston Celtics','Brooklyn Nets','Philadelphia 76ers','New York Knicks','Toronto Raptors','Milwaukee Bucks','Cleveland Cavaliers','Indiana Pacers','Chicago Bulls','Detroit Pistons','Atlanta Hawks','Miami Heat','Washington Wizards','Orlando Magic','Charlotte Hornets','Denver Nuggets','Portland Trail Blazers','Utah Jazz','Minnesota Timberwolves','Oklahoma City Thunder','Phoenix Suns','Los Angeles Clippers','Sacramento Kings','Golden State Warriors','Los Angeles Lakers','Memphis Grizzlies','New Orleans Pelicans','Dallas Mavericks','Houston Rockets','San Antonio Spurs']

team_names_nba.sort()
  
    
# store the URL in url as 
# parameter for urlopen
url_nba = f'https://projects.fivethirtyeight.com/{selected_year}-nba-predictions/data.json'
  
# store the response of URL
response_nba = urlopen(url_nba)
  
# storing the JSON response 
# from url in data
data_json_nba = json.loads(response_nba.read())

data_nba = []
for row in data_json_nba['games']:
    data_nba.append(row)

# print(url)
df_nba = pd.json_normalize(data_nba)

df_final_nba=df_nba.drop(['id','nba_id','neutral','playoff','winner', 'elo_spread','elo_prob1','elo_prob2','rating1','rating2','elo1','elo2','carmelo_scaled_quality','carmelo_scaled_swing',           'carmelo_scaled_total','elo_scaled_quality','elo_scaled_swing','elo_scaled_total','altitude_adj','dist_adj1','dist_adj2','back_to_back_adj1','back_to_back_adj2','cur_rating1','cur_rating2','elo1_pre','elo2_pre','elo1_post','elo2_post','rating1_pre','rating2_pre','hfa','favorite','underdog','favprob','dogprob','favorites.carmelo','favorites.elo'], axis=1)

# st.dataframe(df_final_nba)

# first_column = df_final.pop('date')
  
# # first_column) function
# df_final.insert(1, 'Date', first_column)
# # df_final['team1'] = df_final['team1'].str.replace(df_final['team1'],selected_team_full[0])

df_final_nba['rating_prob2'] = df_final_nba['rating_prob2']*100
df_final_nba['rating_prob1'] = df_final_nba['rating_prob1']*100

df_final_nba['team1'] = df_final_nba['team1'] .map({'BOS': 'Boston Celtics', 'BKN': 'Brooklyn Nets','PHI': 'Philadelphia 76ers', 'NY': 'New York Knicks',
                                            'TOR': 'Toronto Raptors', 'MIL': 'Milwaukee Bucks','CLE': 'Cleveland Cavaliers', 'IND': 'Indiana Pacers',
                                            'CHI': 'Chicago Bulls', 'DET': 'Detroit Pistons','ATL': 'Atlanta Hawks', 'MIA': 'Miami Heat',
                                            'WSH': 'Washington Wizards', 'ORL': 'Orlando Magic','CHA': 'Charlotte Hornets', 'DEN': 'Denver Nuggets',
                                            'POR': 'Portland Trail Blazers', 'UTA': 'Utah Jazz','MIN': 'Minnesota Timberwolves', 'OKC': 'Oklahoma City Thunder',
                                            'PHX': 'Phoenix Suns', 'LAC': 'Los Angeles Clippers','SAC': 'Sacramento Kings', 'GS': 'Golden State Warriors',
                                            'LAL': 'Los Angeles Lakers', 'MEM': 'Memphis Grizzlies','NO': 'New Orleans Pelicans', 'DAL': 'Dallas Mavericks',
                                            'HOU': 'Houston Rockets', 'SA': 'San Antonio Spurs'})

df_final_nba['team2'] = df_final_nba['team2'] .map({'BOS': 'Boston Celtics', 'BKN': 'Brooklyn Nets','PHI': 'Philadelphia 76ers', 'NY': 'New York Knicks',
                                            'TOR': 'Toronto Raptors', 'MIL': 'Milwaukee Bucks','CLE': 'Cleveland Cavaliers', 'IND': 'Indiana Pacers',
                                            'CHI': 'Chicago Bulls', 'DET': 'Detroit Pistons','ATL': 'Atlanta Hawks', 'MIA': 'Miami Heat',
                                            'WSH': 'Washington Wizards', 'ORL': 'Orlando Magic','CHA': 'Charlotte Hornets', 'DEN': 'Denver Nuggets',
                                            'POR': 'Portland Trail Blazers', 'UTA': 'Utah Jazz','MIN': 'Minnesota Timberwolves', 'OKC': 'Oklahoma City Thunder',
                                            'PHX': 'Phoenix Suns', 'LAC': 'Los Angeles Clippers','SAC': 'Sacramento Kings', 'GS': 'Golden State Warriors',
                                            'LAL': 'Los Angeles Lakers', 'MEM': 'Memphis Grizzlies','NO': 'New Orleans Pelicans', 'DAL': 'Dallas Mavericks',
                                            'HOU': 'Houston Rockets', 'SA': 'San Antonio Spurs'})

# df2 = df_final.reset_index(drop=True)

# # st.write(df2)

upcoming_games_nba = df_final_nba.loc[df_final_nba['status']=='pre']
past_games_nba = df_final_nba.loc[df_final_nba['status']=='post']

# # st.dataframe(upcoming_games)

upcoming_games_nba=upcoming_games_nba.drop(['status','score1','score2'], axis=1)




def highlight_green_nba(val):
    '''
    highlight the maximum in a Series yellow.
    '''
    color = 'lightgreen' if str(val) > str(65) else 'white'
    return 'background-color: %s' % color
upcoming_games_color_nba = upcoming_games_nba.style.format(precision=0).applymap(highlight_green, subset=['rating_prob1','rating_prob2'])


predicted_nba = np.where((((past_games_nba['score1']>past_games_nba['score2']) & (past_games_nba['rating_prob1']>past_games_nba['rating_prob2'])) | ((past_games_nba['score1']<past_games_nba['score2']) & (past_games_nba['rating_prob1']<past_games_nba['rating_prob2']))) , 'Predicted', 'Turnaround')

new_analysis_nba = np.where((past_games_nba['score1']>past_games_nba['score2']) , 'W', 'L')

column_results_nba=pd.DataFrame(new_analysis_nba, columns=['Results'])
column_predicted_nba=pd.DataFrame(predicted_nba, columns=['Predicted'])

combined_list_nba = pd.concat([past_games_nba,column_results_nba,column_predicted_nba], axis=1)
combined_list_nba=combined_list_nba.drop(['status'], axis=1)
combined_list2_nba=combined_list_nba.sort_values(by=['date'],ascending=False)

# groupped_scores = combined_list.groupby(['prob1','Results','Predicted']).size()


option1_nba, option2_nba = st.columns(2)
with option1_nba:
    st.header('Upcoming Games')
    list_dates_nba =  upcoming_games_nba['date'].sort_values(ascending=True).unique()
    dates_nba = st.selectbox('date', list_dates_nba)
    try:
        try:
            filtered_dates_nba = upcoming_games_nba[(upcoming_games_nba['date']==dates_nba)]
            upcoming_games_color2_nba = filtered_dates_nba.style.format(precision=3).applymap(highlight_green_nba, subset=['rating_prob1','rating_prob2'])
    #         st.write(upcoming_games_color2.hide(axis=0).to_html(), unsafe_allow_html=True)
            st.dataframe(upcoming_games_color2_nba)
        except:
            st.dataframe(upcoming_games_color_nba)
    except:
        st.warning('Check later for Upcoming Games')
with option2_nba:
    st.header('Past Games')
    selected_team_full_nba = st.multiselect('',team_names_nba,default = team_names_nba[5])
    try:
        try:
            filtered_both_teams_nba = combined_list2_nba[(combined_list2_nba['team1']==selected_team_full_nba[0]) | (combined_list2_nba['team2']==selected_team_full_nba[0])]
            filtered_both_teams2_nba= filtered_both_teams_nba.style.hide_index().format(precision=0)
    #         st.write(filtered_both_teams2.hide(axis=0).to_html(), unsafe_allow_html=True)
            st.dataframe(filtered_both_teams2_nba)
        except:
            combined_list22_nba= combined_list2_nba.style.hide_index().format(precision=0)
            st.dataframe(combined_list22_nba)
    #         st.write(combined_list22.hide(axis=0).to_html(), unsafe_allow_html=True)
    except:
        st.warning('Check later for Past Games')


###################################### NBA ENDS ##############################################

###################################### NFL STARTS ##############################################

st.title("NFL Forecast 🏈")

# team_names_nhl = ['Boston Celtics','Brooklyn Nets','Philadelphia 76ers','New York Knicks','Toronto Raptors','Milwaukee Bucks','Cleveland Cavaliers','Indiana Pacers','Chicago Bulls','Detroit Pistons','Atlanta Hawks','Miami Heat','Washington Wizards','Orlando Magic','Charlotte Hornets','Denver Nuggets','Portland Trail Blazers','Utah Jazz','Minnesota Timberwolves','Oklahoma City Thunder','Phoenix Suns','Los Angeles Clippers','Sacramento Kings','Golden State Warriors','Los Angeles Lakers','Memphis Grizzlies','New Orleans Pelicans','Dallas Mavericks','Houston Rockets','San Antonio Spurs']

# team_names_nhl.sort()
  
    
# store the URL in url as 
# parameter for urlopen
url_nfl = f'https://projects.fivethirtyeight.com/2022-nfl-predictions/data.json'
  
# store the response of URL
response_nfl = urlopen(url_nfl)
  
# storing the JSON response 
# from url in data
data_json_nfl = json.loads(response_nfl.read())

data_nfl = []
for row in data_json_nfl['games']:
    data_nfl.append(row)

# print(url)
df_nfl = pd.json_normalize(data_nfl)

df_final_nfl=df_nfl.drop(["id","datetime","week","neutral","playoff","overtime","elo1_pre","elo2_pre","elo_prob1","elo_prob2","elo1_post","elo2_post","rating1_pre","rating2_pre","rating_spread","rating_prob1","rating_prob2","rating1_post","rating2_post","bettable","outcome","qb_adj1","qb_adj2","rest_adj1","rest_adj2","dist_adj","rating1_top_qb","rating2_top_qb","rating1_current_qb","rating2_current_qb","rating_scaled_quality","rating_scaled_swing","rating_scaled_total","elo_scaled_quality","elo_scaled_swing","elo_scaled_total","seed_lock1","seed_lock2","seed_lock_adj","forfeit","hfa","favorite","underdog","favprob","dogprob","favorites.rating","favorites.elo"
], axis=1)



# # first_column_nhl = df_final_nhl.pop('date')
  
# # # first_column) function
# # df_final_nhl.insert(0, 'date', first_column_nhl)
# # # # # df_final['team1'] = df_final['team1'].str.replace(df_final['team1'],selected_team_full[0])


df_final_nfl['prob2'] = df_final_nfl['prob2']*100
df_final_nfl['prob1'] = df_final_nfl['prob1']*100


# st.dataframe(df_final_nfl)

# # df_final_nba['team1'] = df_final_nba['team1'] .map({'BOS': 'Boston Celtics', 'BKN': 'Brooklyn Nets','PHI': 'Philadelphia 76ers', 'NY': 'New York Knicks',
# #                                             'TOR': 'Toronto Raptors', 'MIL': 'Milwaukee Bucks','CLE': 'Cleveland Cavaliers', 'IND': 'Indiana Pacers',
# #                                             'CHI': 'Chicago Bulls', 'DET': 'Detroit Pistons','ATL': 'Atlanta Hawks', 'MIA': 'Miami Heat',
# #                                             'WSH': 'Washington Wizards', 'ORL': 'Orlando Magic','CHA': 'Charlotte Hornets', 'DEN': 'Denver Nuggets',
# #                                             'POR': 'Portland Trail Blazers', 'UTA': 'Utah Jazz','MIN': 'Minnesota Timberwolves', 'OKC': 'Oklahoma City Thunder',
# #                                             'PHX': 'Phoenix Suns', 'LAC': 'Los Angeles Clippers','SAC': 'Sacramento Kings', 'GS': 'Golden State Warriors',
# #                                             'LAL': 'Los Angeles Lakers', 'MEM': 'Memphis Grizzlies','NO': 'New Orleans Pelicans', 'DAL': 'Dallas Mavericks',
# #                                             'HOU': 'Houston Rockets', 'SA': 'San Antonio Spurs'})

# # df_final_nba['team2'] = df_final_nba['team2'] .map({'BOS': 'Boston Celtics', 'BKN': 'Brooklyn Nets','PHI': 'Philadelphia 76ers', 'NY': 'New York Knicks',
# #                                             'TOR': 'Toronto Raptors', 'MIL': 'Milwaukee Bucks','CLE': 'Cleveland Cavaliers', 'IND': 'Indiana Pacers',
# #                                             'CHI': 'Chicago Bulls', 'DET': 'Detroit Pistons','ATL': 'Atlanta Hawks', 'MIA': 'Miami Heat',
# #                                             'WSH': 'Washington Wizards', 'ORL': 'Orlando Magic','CHA': 'Charlotte Hornets', 'DEN': 'Denver Nuggets',
# #                                             'POR': 'Portland Trail Blazers', 'UTA': 'Utah Jazz','MIN': 'Minnesota Timberwolves', 'OKC': 'Oklahoma City Thunder',
# #                                             'PHX': 'Phoenix Suns', 'LAC': 'Los Angeles Clippers','SAC': 'Sacramento Kings', 'GS': 'Golden State Warriors',
# #                                             'LAL': 'Los Angeles Lakers', 'MEM': 'Memphis Grizzlies','NO': 'New Orleans Pelicans', 'DAL': 'Dallas Mavericks',
# #                                             'HOU': 'Houston Rockets', 'SA': 'San Antonio Spurs'})

# # # df2 = df_final.reset_index(drop=True)

# # # # st.write(df2)

# upcoming_games_soccer = df_final_soccer.loc[df_final_soccer['status']=='pre']
past_games_nfl = df_final_nfl.loc[df_final_nfl['status']=='post']

# # # # # st.dataframe(upcoming_games)

# upcoming_games_soccer=upcoming_games_soccer.drop(['status'], axis=1)




# def highlight_green_soccer(val):
#     '''
#     highlight the maximum in a Series yellow.
#     '''
#     color = 'lightgreen' if str(val) > str(65) else 'white'
#     return 'background-color: %s' % color
# upcoming_games_color_soccer = upcoming_games_soccer.style.format(precision=0).applymap(highlight_green, subset=['prob1','prob2','probtie'])


predicted_nfl = np.where((((past_games_nfl['score1']>past_games_nfl['score2']) & (past_games_nfl['prob1']>past_games_nfl['prob2'])) | ((past_games_nfl['score1']<past_games_nfl['score2']) & (past_games_nfl['prob1']<past_games_nfl['prob2']))) , 'Predicted', 'Turnaround')

new_analysis_nfl = np.where((past_games_nfl['score1']>past_games_nfl['score2']) , 'W', 'L')

column_results_nfl=pd.DataFrame(new_analysis_nfl, columns=['Results'])
column_predicted_nfl=pd.DataFrame(predicted_nfl, columns=['Predicted'])

combined_list_nfl = pd.concat([past_games_nfl,column_results_nfl,column_predicted_nfl], axis=1)
combined_list_nfl=combined_list_nfl.drop(['status'], axis=1)
combined_list2_nfl=combined_list_nfl.sort_values(by=['date'],ascending=False)

# # # # groupped_scores = combined_list.groupby(['prob1','Results','Predicted']).size()


option1_nfl, option2_nfl = st.columns(2)
with option1_nfl:
    st.header('Upcoming Games')
#     list_dates_soccer =  upcoming_games_soccer['datetime'].sort_values(ascending=True).unique()
#     dates_soccer = st.selectbox('datetime', list_dates_soccer)
#     try:
#         filtered_dates_soccer = upcoming_games_soccer[(upcoming_games_soccer['datetime']==dates_soccer)]
#         upcoming_games_color2_soccer = filtered_dates_soccer.style.format(precision=3).applymap(highlight_green_soccer, subset=['prob1','prob2','probtie'])
# #         st.write(upcoming_games_color2.hide(axis=0).to_html(), unsafe_allow_html=True)
#         st.dataframe(upcoming_games_color2_soccer)
#     except:
#         st.dataframe(upcoming_games_color_soccer)
with option2_nfl:
    st.header('Past Games')
    try:
        st.dataframe(combined_list2_nfl)
    except:
        st.warning('Check later for Past Games')
# # #     selected_team_full_nba = st.multiselect('',team_names_nba,default = team_names_nba[5])
# # #     try:
# # #         filtered_both_teams_nba = combined_list2_nba[(combined_list2_nba['team1']==selected_team_full_nba[0]) | (combined_list2_nba['team2']==selected_team_full_nba[0])]
# # #         filtered_both_teams2_nba= filtered_both_teams_nba.style.hide_index().format(precision=0)
# # # #         st.write(filtered_both_teams2.hide(axis=0).to_html(), unsafe_allow_html=True)
# # #         st.dataframe(filtered_both_teams2_nba)
# # #     except:
# # #         combined_list22_nba= combined_list2_nba.style.hide_index().format(precision=0)
# # #         st.dataframe(combined_list22_nba)
# # # #         st.write(combined_list22.hide(axis=0).to_html(), unsafe_allow_html=True)


###################################### NFL ENDS ##############################################




###################################### NHL STARTS ##############################################

st.title("NHL Forecast 🏑")

# team_names_nhl = ['Boston Celtics','Brooklyn Nets','Philadelphia 76ers','New York Knicks','Toronto Raptors','Milwaukee Bucks','Cleveland Cavaliers','Indiana Pacers','Chicago Bulls','Detroit Pistons','Atlanta Hawks','Miami Heat','Washington Wizards','Orlando Magic','Charlotte Hornets','Denver Nuggets','Portland Trail Blazers','Utah Jazz','Minnesota Timberwolves','Oklahoma City Thunder','Phoenix Suns','Los Angeles Clippers','Sacramento Kings','Golden State Warriors','Los Angeles Lakers','Memphis Grizzlies','New Orleans Pelicans','Dallas Mavericks','Houston Rockets','San Antonio Spurs']

# team_names_nhl.sort()
  
    
# store the URL in url as 
# parameter for urlopen
url_nhl = f'https://projects.fivethirtyeight.com/{selected_year}-nhl-predictions/data.json'
  
# store the response of URL
response_nhl = urlopen(url_nhl)
  
# storing the JSON response 
# from url in data
data_json_nhl = json.loads(response_nhl.read())

data_nhl = []
for row in data_json_nhl['games']:
    data_nhl.append(row)

# print(url)
df_nhl = pd.json_normalize(data_nhl)

df_final_nhl=df_nhl.drop(['id','season','datetime','playoff','neutral','points1','points2', 'ot','elo1_pre','elo2_pre','elo1_post','elo2_post','leverage1','leverage2','quality','importance','game_rating'], axis=1)



first_column_nhl = df_final_nhl.pop('date')
  
# first_column) function
df_final_nhl.insert(0, 'date', first_column_nhl)
# # # df_final['team1'] = df_final['team1'].str.replace(df_final['team1'],selected_team_full[0])


df_final_nhl['prob2'] = df_final_nhl['prob2']*100
df_final_nhl['prob1'] = df_final_nhl['prob1']*100
df_final_nhl['otprob'] = df_final_nhl['otprob']*100

# st.dataframe(df_final_nhl)

# df_final_nba['team1'] = df_final_nba['team1'] .map({'BOS': 'Boston Celtics', 'BKN': 'Brooklyn Nets','PHI': 'Philadelphia 76ers', 'NY': 'New York Knicks',
#                                             'TOR': 'Toronto Raptors', 'MIL': 'Milwaukee Bucks','CLE': 'Cleveland Cavaliers', 'IND': 'Indiana Pacers',
#                                             'CHI': 'Chicago Bulls', 'DET': 'Detroit Pistons','ATL': 'Atlanta Hawks', 'MIA': 'Miami Heat',
#                                             'WSH': 'Washington Wizards', 'ORL': 'Orlando Magic','CHA': 'Charlotte Hornets', 'DEN': 'Denver Nuggets',
#                                             'POR': 'Portland Trail Blazers', 'UTA': 'Utah Jazz','MIN': 'Minnesota Timberwolves', 'OKC': 'Oklahoma City Thunder',
#                                             'PHX': 'Phoenix Suns', 'LAC': 'Los Angeles Clippers','SAC': 'Sacramento Kings', 'GS': 'Golden State Warriors',
#                                             'LAL': 'Los Angeles Lakers', 'MEM': 'Memphis Grizzlies','NO': 'New Orleans Pelicans', 'DAL': 'Dallas Mavericks',
#                                             'HOU': 'Houston Rockets', 'SA': 'San Antonio Spurs'})

# df_final_nba['team2'] = df_final_nba['team2'] .map({'BOS': 'Boston Celtics', 'BKN': 'Brooklyn Nets','PHI': 'Philadelphia 76ers', 'NY': 'New York Knicks',
#                                             'TOR': 'Toronto Raptors', 'MIL': 'Milwaukee Bucks','CLE': 'Cleveland Cavaliers', 'IND': 'Indiana Pacers',
#                                             'CHI': 'Chicago Bulls', 'DET': 'Detroit Pistons','ATL': 'Atlanta Hawks', 'MIA': 'Miami Heat',
#                                             'WSH': 'Washington Wizards', 'ORL': 'Orlando Magic','CHA': 'Charlotte Hornets', 'DEN': 'Denver Nuggets',
#                                             'POR': 'Portland Trail Blazers', 'UTA': 'Utah Jazz','MIN': 'Minnesota Timberwolves', 'OKC': 'Oklahoma City Thunder',
#                                             'PHX': 'Phoenix Suns', 'LAC': 'Los Angeles Clippers','SAC': 'Sacramento Kings', 'GS': 'Golden State Warriors',
#                                             'LAL': 'Los Angeles Lakers', 'MEM': 'Memphis Grizzlies','NO': 'New Orleans Pelicans', 'DAL': 'Dallas Mavericks',
#                                             'HOU': 'Houston Rockets', 'SA': 'San Antonio Spurs'})

# # df2 = df_final.reset_index(drop=True)

# # # st.write(df2)

upcoming_games_nhl = df_final_nhl.loc[df_final_nhl['status']=='pre']
past_games_nhl = df_final_nhl.loc[df_final_nhl['status']=='post']

# # # st.dataframe(upcoming_games)

upcoming_games_nhl=upcoming_games_nhl.drop(['status','score1','score2'], axis=1)




def highlight_green_nhl(val):
    '''
    highlight the maximum in a Series yellow.
    '''
    color = 'lightgreen' if str(val) > str(65) else 'white'
    return 'background-color: %s' % color
upcoming_games_color_nhl = upcoming_games_nhl.style.format(precision=0).applymap(highlight_green, subset=['prob1','prob2'])


predicted_nhl = np.where((((past_games_nhl['score1']>past_games_nhl['score2']) & (past_games_nhl['prob1']>past_games_nhl['prob2'])) | ((past_games_nhl['score1']<past_games_nhl['score2']) & (past_games_nhl['prob1']<past_games_nhl['prob2']))) , 'Predicted', 'Turnaround')

new_analysis_nhl = np.where((past_games_nhl['score1']>past_games_nhl['score2']) , 'W', 'L')

column_results_nhl=pd.DataFrame(new_analysis_nhl, columns=['Results'])
column_predicted_nhl=pd.DataFrame(predicted_nhl, columns=['Predicted'])

combined_list_nhl = pd.concat([past_games_nhl,column_results_nhl,column_predicted_nhl], axis=1)
combined_list_nhl=combined_list_nhl.drop(['status'], axis=1)
combined_list2_nhl=combined_list_nhl.sort_values(by=['date'],ascending=False)

# # groupped_scores = combined_list.groupby(['prob1','Results','Predicted']).size()


option1_nhl, option2_nhl = st.columns(2)
with option1_nhl:
    st.header('Upcoming Games')
    list_dates_nhl =  upcoming_games_nhl['date'].sort_values(ascending=True).unique()
    dates_nhl = st.selectbox('date', list_dates_nhl)
    try:
        try:
            filtered_dates_nhl = upcoming_games_nhl[(upcoming_games_nhl['date']==dates_nhl)]
            upcoming_games_color2_nhl = filtered_dates_nhl.style.format(precision=3).applymap(highlight_green_nhl, subset=['prob1','prob2'])
    #         st.write(upcoming_games_color2.hide(axis=0).to_html(), unsafe_allow_html=True)
            st.dataframe(upcoming_games_color2_nhl)
        except:
            st.dataframe(upcoming_games_color_nhl)
    except:
        st.warning('Check later for Upcoming Games') 
with option2_nhl:
    st.header('Past Games')
    try:
        st.dataframe(combined_list2_nhl)
    except:
        st.warning('Check later for Past Games')
#     selected_team_full_nba = st.multiselect('',team_names_nba,default = team_names_nba[5])
#     try:
#         filtered_both_teams_nba = combined_list2_nba[(combined_list2_nba['team1']==selected_team_full_nba[0]) | (combined_list2_nba['team2']==selected_team_full_nba[0])]
#         filtered_both_teams2_nba= filtered_both_teams_nba.style.hide_index().format(precision=0)
# #         st.write(filtered_both_teams2.hide(axis=0).to_html(), unsafe_allow_html=True)
#         st.dataframe(filtered_both_teams2_nba)
#     except:
#         combined_list22_nba= combined_list2_nba.style.hide_index().format(precision=0)
#         st.dataframe(combined_list22_nba)
# #         st.write(combined_list22.hide(axis=0).to_html(), unsafe_allow_html=True)


###################################### NHL ENDS ##############################################

###################################### SOCCER STARTS ##############################################

st.title("Soccer Forecast ⚽️")

# team_names_nhl = ['Boston Celtics','Brooklyn Nets','Philadelphia 76ers','New York Knicks','Toronto Raptors','Milwaukee Bucks','Cleveland Cavaliers','Indiana Pacers','Chicago Bulls','Detroit Pistons','Atlanta Hawks','Miami Heat','Washington Wizards','Orlando Magic','Charlotte Hornets','Denver Nuggets','Portland Trail Blazers','Utah Jazz','Minnesota Timberwolves','Oklahoma City Thunder','Phoenix Suns','Los Angeles Clippers','Sacramento Kings','Golden State Warriors','Los Angeles Lakers','Memphis Grizzlies','New Orleans Pelicans','Dallas Mavericks','Houston Rockets','San Antonio Spurs']

# team_names_nhl.sort()
  
    
# store the URL in url as 
# parameter for urlopen
url_soccer = f'https://projects.fivethirtyeight.com/soccer-predictions/data.json'
  
# store the response of URL
response_soccer = urlopen(url_soccer)
  
# storing the JSON response 
# from url in data
data_json_soccer = json.loads(response_soccer.read())

data_soccer = []
for row in data_json_soccer['matches']:
    data_soccer.append(row)

# print(url)
df_soccer = pd.json_normalize(data_soccer)

df_final_soccer=df_soccer.drop(['id','league_id','leg','team1_id','team2_id','team1_code','team2_code', 'round','matchday','quality','leverage'], axis=1)



# first_column_nhl = df_final_nhl.pop('date')
  
# # first_column) function
# df_final_nhl.insert(0, 'date', first_column_nhl)
# # # # df_final['team1'] = df_final['team1'].str.replace(df_final['team1'],selected_team_full[0])


df_final_soccer['prob2'] = df_final_soccer['prob2']*100
df_final_soccer['prob1'] = df_final_soccer['prob1']*100
df_final_soccer['probtie'] = df_final_soccer['probtie']*100

df_final_soccer['datetime'] = pd.to_datetime(df_final_soccer['datetime']).dt.date

# df['Date'] = pd.to_datetime(df["InsertedDateTime"]).dt.date
# .date()

# st.dataframe(df_final_soccer)

# # df_final_nba['team1'] = df_final_nba['team1'] .map({'BOS': 'Boston Celtics', 'BKN': 'Brooklyn Nets','PHI': 'Philadelphia 76ers', 'NY': 'New York Knicks',
# #                                             'TOR': 'Toronto Raptors', 'MIL': 'Milwaukee Bucks','CLE': 'Cleveland Cavaliers', 'IND': 'Indiana Pacers',
# #                                             'CHI': 'Chicago Bulls', 'DET': 'Detroit Pistons','ATL': 'Atlanta Hawks', 'MIA': 'Miami Heat',
# #                                             'WSH': 'Washington Wizards', 'ORL': 'Orlando Magic','CHA': 'Charlotte Hornets', 'DEN': 'Denver Nuggets',
# #                                             'POR': 'Portland Trail Blazers', 'UTA': 'Utah Jazz','MIN': 'Minnesota Timberwolves', 'OKC': 'Oklahoma City Thunder',
# #                                             'PHX': 'Phoenix Suns', 'LAC': 'Los Angeles Clippers','SAC': 'Sacramento Kings', 'GS': 'Golden State Warriors',
# #                                             'LAL': 'Los Angeles Lakers', 'MEM': 'Memphis Grizzlies','NO': 'New Orleans Pelicans', 'DAL': 'Dallas Mavericks',
# #                                             'HOU': 'Houston Rockets', 'SA': 'San Antonio Spurs'})

# # df_final_nba['team2'] = df_final_nba['team2'] .map({'BOS': 'Boston Celtics', 'BKN': 'Brooklyn Nets','PHI': 'Philadelphia 76ers', 'NY': 'New York Knicks',
# #                                             'TOR': 'Toronto Raptors', 'MIL': 'Milwaukee Bucks','CLE': 'Cleveland Cavaliers', 'IND': 'Indiana Pacers',
# #                                             'CHI': 'Chicago Bulls', 'DET': 'Detroit Pistons','ATL': 'Atlanta Hawks', 'MIA': 'Miami Heat',
# #                                             'WSH': 'Washington Wizards', 'ORL': 'Orlando Magic','CHA': 'Charlotte Hornets', 'DEN': 'Denver Nuggets',
# #                                             'POR': 'Portland Trail Blazers', 'UTA': 'Utah Jazz','MIN': 'Minnesota Timberwolves', 'OKC': 'Oklahoma City Thunder',
# #                                             'PHX': 'Phoenix Suns', 'LAC': 'Los Angeles Clippers','SAC': 'Sacramento Kings', 'GS': 'Golden State Warriors',
# #                                             'LAL': 'Los Angeles Lakers', 'MEM': 'Memphis Grizzlies','NO': 'New Orleans Pelicans', 'DAL': 'Dallas Mavericks',
# #                                             'HOU': 'Houston Rockets', 'SA': 'San Antonio Spurs'})

# # # df2 = df_final.reset_index(drop=True)

# # # # st.write(df2)

upcoming_games_soccer = df_final_soccer.loc[df_final_soccer['status']=='pre']
past_games_soccer = df_final_soccer.loc[df_final_soccer['status']=='post']

# # # # st.dataframe(upcoming_games)

upcoming_games_soccer=upcoming_games_soccer.drop(['status','group'], axis=1)




def highlight_green_soccer(val):
    '''
    highlight the maximum in a Series yellow.
    '''
    color = 'lightgreen' if str(val) > str(65) else 'white'
    return 'background-color: %s' % color
upcoming_games_color_soccer = upcoming_games_soccer.style.format(precision=0).applymap(highlight_green, subset=['prob1','prob2','probtie'])


# predicted_nhl = np.where((((past_games_nhl['score1']>past_games_nhl['score2']) & (past_games_nhl['prob1']>past_games_nhl['prob2'])) | ((past_games_nhl['score1']<past_games_nhl['score2']) & (past_games_nhl['prob1']<past_games_nhl['prob2']))) , 'Predicted', 'Turnaround')

# new_analysis_nhl = np.where((past_games_nhl['score1']>past_games_nhl['score2']) , 'W', 'L')

# column_results_nhl=pd.DataFrame(new_analysis_nhl, columns=['Results'])
# column_predicted_nhl=pd.DataFrame(predicted_nhl, columns=['Predicted'])

# combined_list_nhl = pd.concat([past_games_nhl,column_results_nhl,column_predicted_nhl], axis=1)
# combined_list_nhl=combined_list_nhl.drop(['status'], axis=1)
# combined_list2_nhl=combined_list_nhl.sort_values(by=['date'],ascending=False)

# # # groupped_scores = combined_list.groupby(['prob1','Results','Predicted']).size()


option1_soccer, option2_soccer = st.columns(2)
with option1_soccer:
    st.header('Upcoming Games')
    list_dates_soccer =  upcoming_games_soccer['datetime'].sort_values(ascending=True).unique()
    dates_soccer = st.selectbox('datetime', list_dates_soccer)
    try:
        try:
            filtered_dates_soccer = upcoming_games_soccer[(upcoming_games_soccer['datetime']==dates_soccer)]
            upcoming_games_color2_soccer = filtered_dates_soccer.style.format(precision=3).applymap(highlight_green_soccer, subset=['prob1','prob2','probtie'])
    #         st.write(upcoming_games_color2.hide(axis=0).to_html(), unsafe_allow_html=True)
            st.dataframe(upcoming_games_color2_soccer)
        except:
            st.dataframe(upcoming_games_color_soccer)
    except:
        st.warning('Check later for Upcoming Games')
# with option2_nhl:
#     st.header('Past Games')
#     st.dataframe(combined_list2_nhl)
# #     selected_team_full_nba = st.multiselect('',team_names_nba,default = team_names_nba[5])
# #     try:
# #         filtered_both_teams_nba = combined_list2_nba[(combined_list2_nba['team1']==selected_team_full_nba[0]) | (combined_list2_nba['team2']==selected_team_full_nba[0])]
# #         filtered_both_teams2_nba= filtered_both_teams_nba.style.hide_index().format(precision=0)
# # #         st.write(filtered_both_teams2.hide(axis=0).to_html(), unsafe_allow_html=True)
# #         st.dataframe(filtered_both_teams2_nba)
# #     except:
# #         combined_list22_nba= combined_list2_nba.style.hide_index().format(precision=0)
# #         st.dataframe(combined_list22_nba)
# # #         st.write(combined_list22.hide(axis=0).to_html(), unsafe_allow_html=True)


###################################### SOCCER ENDS ##############################################
st.caption("Data Source: fivethirtyeight Website")# and pro-basketball-reference

