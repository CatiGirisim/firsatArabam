
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import db_connection
import time
connection, cursor = db_connection.connect_db()
cursor.execute("SELECT * FROM firsatarabam.public.sahibinden_raw_data")
selected = cursor.fetchall()
print(len(selected))
time.sleep(99999)
text = []
for i in selected:
    for j in i[15].split():
        text.append(j)
connection.close()

print("tot words: ", len(text))
text_list = "-".join(text)
words = WordCloud(background_color='black').generate(text_list)

plt.figure(figsize=(10, 6))
plt.imshow(words, interpolation='bilinear')
plt.axis("off")
plt.show()
