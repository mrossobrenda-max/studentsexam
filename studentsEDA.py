#%%
import pandas as pd
df = pd.read_csv(r"C:\Users\BRENDA\Downloads\student_exam_scores.csv")
df.info()
df.describe()
print("Average exam score", df['exam_score'].mean())
print("Median exam score", df['exam_score'].median())
print("Most exam score", df['exam_score'].mode())
print("STD for exam score", df['exam_score'].std())
std = df['exam_score'].std()
avg = df['exam_score'].mean()
cv = (std/avg)*100
print("CV",cv)
print("Average previous_scores", df['previous_scores'].mean())
print("Median previous score", df['previous_scores'].median())
print("Most scored mark from previous exam", df['previous_scores'].mode())
print("Previous STD score", df['previous_scores'].std())
pstd = df['previous_scores'].std()
pavg = df['previous_scores'].mean()
pcv = (pstd/pavg)*100
print("Previous CV",pcv)
#visualize examscore distribution
import seaborn as sns
import matplotlib.pyplot as plt
sns.histplot(x = df['exam_score'], bins=20)
plt.title("Student Exam Performance")
plt.xlabel("Attendance %")
plt.ylabel("Students count")
plt.show()
#topscores
topscore = df['previous_scores'].value_counts().head(5)
sns.barplot(x=topscore.index,y=topscore,palette ="mako",hue=topscore.index,legend=False)
plt.title("Top Scores in the Previous exam")
plt.xlabel("Top scores")
plt.ylabel("students count")
plt.show()
#top scores in the current exam
currtopscore =df['exam_score'].value_counts().head(5)
sns.barplot(x=currtopscore.index,y=currtopscore,palette ="mako",hue = currtopscore.index,legend=False)
plt.title("Top Scores in the Final exam")
plt.xlabel("Top scores")
plt.ylabel("students count")
plt.show()
#check correlation
corr = df[['hours_studied','sleep_hours','attendance_percent','previous_scores','exam_score']].corr()
sns.heatmap(corr,annot=True,cmap="coolwarm")
plt.title("Correlation Matrix")
plt.show()
#piechart to compare the average scores for both exams
labels = ['Previous Average Score','Final Average Score']
colors = ['#66b3ff', '#ff9999']
scores = [pavg,avg]
plt.figure(figsize=(6,6))
plt.pie(scores,labels = labels, colors = colors,autopct='%1.2f%%',startangle = 90)
plt.axis('equal') #ensures the pie is a circle shape
plt.title('Results Comparison')
#regplot to show the strong correlation btn hours studied and exam scores
data = df.sort_values(by='hours_studied')
plt.figure(figsize=(10,6))
sns.regplot(x=data['hours_studied'],y=data['exam_score'],scatter_kws={'alpha':0.6}, line_kws={'color':'teal'},ci=None)
plt.title("How the number of hours studied relate with the student exam scores")
plt.xlabel("Hours Studied")
plt.ylabel("Exam_scores")
plt.tight_layout()
plt.show()
#lineplot for showin the correlation btn attendance percent and previous scores
df_sort = df.sort_values(by='attendance_percent')
sns.regplot(x='attendance_percent',y='previous_scores', data=df_sort,line_kws={'color':'teal'},scatter=False,ci=None)
plt.title("Attendance % vs Previous Exam Scores")
plt.xlabel('attendance%')
plt.ylabel('previous_scores')
plt.show()
#modelling
from sklearn.model_selection import train_test_split
x = df[['hours_studied','sleep_hours','attendance_percent','previous_scores']]
y=df[['exam_score']]
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=1)
print("x_train", x_train.shape)
print("x_test", x_test.shape)
print("y_train",y_train.shape)
print("y_test", y_test.shape)
#initiate the model/build it
from sklearn.linear_model import LinearRegression
lr= LinearRegression()
#train the model
lr.fit(x_train,y_train)
#prediction
ypred = lr.predict(x_test)
#evaluate the model
from sklearn.metrics import mean_absolute_error, mean_squared_error,r2_score
mae = mean_absolute_error(y_test,ypred)
mse = mean_squared_error(y_test,ypred)
r2 = r2_score(y_test,ypred)
print("MAE", mae)
print("MSE", mse)
print("r2", r2)
#%%
