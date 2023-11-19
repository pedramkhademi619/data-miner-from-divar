import mysql.connector

db = mysql.connector.connect(user = 'root',
                             passwd = '13808472aA@#',
                             host = '127.0.0.1',
                             database = 'information')
cursor = db.cursor()

cursor.execute('SELECT milage FROM CAR')
milage = list(map(lambda x: int(x[0]),cursor.fetchall()))


cursor.execute('SELECT model FROM CAR')
model = list(map(lambda x: int(x[0]),cursor.fetchall()))
n = len(milage)

bool = True
k = 0
while bool:
    if k < len(milage):
        if milage[k] < 10000 and model[k] < 1400:
            milage.remove(milage[k])
            model.remove(model[k])
        elif 1402 <= model[k] <= 1975 or model[k] <= 1365:
            milage.remove(milage[k])
            model.remove(model[k])
        elif 1975 < model[k] < 2022:
            model[k] -= 621
            k += 1
        else:
            k += 1
    else:
        break



    


def sumsq(x):
    s = 0
    for i in x:
        s += i**2
    return s
def multiply(x, y):
    lst = []
    l = range(len(x))
    for i in l:
            lst.append(x[i] * y[i])
    return lst

def predict(mdl):
    '''This function takes the year of production from you and predicts its function.'''
    global model
    global milage
    a = (n * sum(multiply(model, milage)) - sum(model) * sum(milage)) / (n * sumsq(model) - sum(model) ** 2)
    b = (sum(model) * sum(multiply(model, milage)) - sumsq(model) * sum(milage)) / (sum(model) ** 2 - n * sumsq(model))
    predicted_milage = a * mdl + b
    return int(predicted_milage)


