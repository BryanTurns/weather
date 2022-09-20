import sqlite3
import matplotlib.pyplot as plt
import numpy 
from datetime import datetime, timedelta
from sklearn.metrics import r2_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pandas as pd




def main():
    data = gatherDataLegacy()
    df = pd.DataFrame(list(zip(data["datetime"], data["timeofday"], data["timeofyear"], data["humidity"], data["pressure"], data["gas"], data["temperature"],  data["lux"], data["uv"], data["prevTemp3"], data["prevPressure3"])), columns=["Time Stamp", "Time of Day", "Time of Year", "Humidity", "Pressure", "Gas", "Temperature", "Lux", "UV", "3 Hour Past Temp", "3 Hour Past Pressure"])

    df = df[df["3 Hour Past Temp"].notna()]
    # df = df[df["6 Hour Past Temp"].notna()]
    x = [df["3 Hour Past Temp"], df["Time of Day"]]
    y = df["Temperature"]
    print(df)
    # pd.set_option("display.max_rows", None)
    # print(df[["Temperature", "3 Hour Past Temp", "Time of Day"]])

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(x[1], x[0], y)
    ax.set_xlabel("Time of Day")
    ax.set_ylabel("3 Hour Past Temp")
    ax.set_zlabel("Actual Temperature (C)")
    plt.show()
    # plt.scatter(x[2], y)
    
    polyRegression(x, y, 5, plt)

    

def gatherDataLegacy():
    connection = sqlite3.connect("./api/test.db")
    cursor = connection.cursor() 
    data = {
        "datetime": [],
        "timeofday": [],
        "humidity": [],
        "pressure": [],
        "gas": [],
        "temperature": [],
        "timeofyear": [],
        "lux": [],
        "uv": [],
        "prevTemp3": [],
        "prevTemp6": [],
        "prevPressure3": []

    }
    rows = cursor.execute("SELECT * FROM weather").fetchall()
    for row in rows:
        if True:
            data["datetime"].append(datetime.strptime(row[4], '%m/%d/%Y %H:%M:%S')) 
            
            setPrevData(3, data, "prevTemp3", "temperature")
            setPrevData(3, data, "prevPressure3", "pressure")

            data["temperature"].append(row[1])
            data["pressure"].append(row[0])
            data["humidity"].append(row[2])
            data["gas"].append(row[3])
            data["timeofday"].append(data["datetime"][-1].hour  + data["datetime"][-1].minute/60)
            tmp = ((((data["datetime"][-1].month * 30.44) + data["datetime"][-1].day) * 24 + data["datetime"][-1].hour) * 60 + data["datetime"][-1].minute) / 100000
            data["timeofyear"].append(tmp)
            data["lux"].append(row[6])
            data["uv"].append(row[5])

    return data

def gatherData():
    # rows[i][0] = pressure
    # rows[i][1] = temperature
    # rows[i][2] = humidity
    # rows[i][3] = gas (volatile natural particles or smth)
    # rows[i][4] = datetime (formatted string '%m/%d/%Y %H:%M:%S')
    # rows[i][5] = UV
    # rows[i][6] = lux
    connection = sqlite3.connect("./api/test.db")
    cursor = connection.cursor() 
    rows = cursor.execute("SELECT * FROM weather").fetchall()

    data = []
    for row in rows:
        data.append([])
        for value in row:
            data[-1].append(value)
        datetime = datetime.strptime(data[-1][4], '%m/%d/%Y %H:%M:%S')
        data[-1].append(datetime.hour + datetime.minute/60)
    
def setPrevData(hours, data, previousCategory, dataCategory):
    lowbound = data["datetime"][-1]
    highbound = data["datetime"][-1]
    data[previousCategory].append(None)
    i = len(data[dataCategory])-1
    if i < 0:
        return
    lowbound += timedelta(hours=-hours, minutes=-10)
    highbound += timedelta(hours=-hours, minutes=10)
    while i >= 0:

        
        if data["datetime"][i] < highbound and data["datetime"][i] > lowbound:
            data[previousCategory][-1] = data[dataCategory][i]
            break
        i -= 1


def polyRegression(x, y, n, plt):
    X = numpy.asarray(x)
    X = X.transpose()
    y = numpy.asarray(y)
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)
    reg = LinearRegression()
    reg.fit(x_train, y_train)
    y_pred = reg.predict(x_test)
    # plt.plot(x_test[:, 0], y_pred, color="green")
    print("R2 Score Linear: " + str(r2_score(y_test, y_pred)))


    poly = PolynomialFeatures(degree=n)
    x_poly = poly.fit_transform(x_train)
    poly.fit(x_train, y_train)
    model = LinearRegression()
    model.fit(x_poly, y_train)
    
    y_pred = model.predict(poly.fit_transform(x_test))
    print("R2 Score Polynomial: " + str(r2_score(y_test, y_pred)))

    while True:
        time = input("Current Time (1-24): ")
        time = float(time) + 3
        prevTemp3 = input("Current Temperature: ")
        prevTemp3 = (float(prevTemp3)-32)/1.8
        customTest = numpy.asarray([float(prevTemp3), float(time)]).reshape(-1, 1).transpose()
        print("Predicted Temp in Three Hours: " + str((model.predict(poly.fit_transform(customTest))[0]*1.8) + 32))


def cleanForCollumn(collumn):
    
    
    return cleanData


def datetime_to_float(d):
    epoch = datetime.datetime.utcfromtimestamp(0)
    total_seconds =  (d - epoch).total_seconds()
    # total_seconds will be in decimals (millisecond precision)
    return total_seconds


if __name__ == "__main__":
    main()