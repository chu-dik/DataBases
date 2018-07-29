import requests
import html2text
import bs4
import sqlite3





login = ###
password = ###

session = requests.Session()

url = "https://www.piugame.com/bbs/piu.login_check.php" # Ваш URL с формами логина

data= {'mb_id': login, 'mb_password': password}
session.post(url, data) # Отправляем данные в POST, в session записываются наши куки

url2 = "http://www.piugame.com/piu.prime2/mydata/recentPlay.php"
r = session.get(url2) # Все! Вы получили Response. Поскольку в session записались куки авторизации - при вызове метода get() с этой сессии в Request отправляются ваши куки.



playersPage = bs4.BeautifulSoup(r.text, 'html.parser')
print(playersPage.prettify())

songsName = playersPage.find_all('span', attrs={'class':'recentSongT f600 mb30'})
#for song in songsName:
#    print(song.text)

resLvl = playersPage.find_all('div', attrs={'class':'stepBallMiniLevel'})
#for member in resLvl:
#    print(member)

results2 = list()
for lvl in resLvl:
    ress = list(map(str, str(lvl).split('"')))
    ress1 = (list(map(str, ress[1].split())))
    results2.append(ress1[1:])
    
#print(results2)

for i in range(len(results2)):
    print(songsName[i].text, results2[i][0], results2[i][1])
    
#urlMore = 'http://www.piugame.com/piu.prime2/mydata/recentPlayMore.php'

#######working with db
    
conn = sqlite3.connect('PumpBot.sqlite')
cur = conn.cursor()

req = "INSERT INTO Players (pl_id, pl_login, pl_password\
) VALUES ('2', '" + login + "' ,'" + password + "')"

cur.execute(req)
conn.commit()

cur.execute('SELECT * FROM Players')
row = cur.fetchone()   #Что это вообще делает?

while row is not None:
    print("pl_id:"+str(row[0])+" Логин: "+row[2]+" | Пароль: "+row[3])
    row = cur.fetchone()

cur.close()
conn.close()
