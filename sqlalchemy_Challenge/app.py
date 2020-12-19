import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt

#setting up database
#creating the engine

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#reflecting an existing db in a new modal
Base = automap_base()
#reflecting the tables
Base.prepare(engine, reflect=True)

#saving reference to the table
ME = Base.classes.measurement
SA = Base.classes.station


#creating a session link from Python
session = Session(engine)

#setting up Flask
app = Flask(__name__)

#Flask Routes
@app.route("/")
def welcome():
    """Listing all available api routes"""
    return(
        f"Availabile Routes: <br>"
        f"<br/>"
        f"/api/v1.0/precipitation <br>"
        f"- List of prior year rain totals from all stations <br/>"
        f"<br/>"
        f"/api/v1.0/stations <br>"
        f"- List of Station numbers and names, which in active for the whole prior year <br/>"
        f"<br/>"
        f"/api/v1.0/tobs <br>"
        f"- List of temperatures in prior year from all stations <br/>"
        f"<br/>"
        f"/api/v1.0/<start> and <start>/<end> <br>"
        f"- When given the start date (YYYY-MM-DD), calculates the MIN/AVG/MAX temperature for all dates greater than and equal to the start date<br/>"
        f"<br/>"
        f"- When given the start and the end date (YYYY-MM-DD), calculate the MIN/AVG/MAX temperature for dates between the start and end date inclusive<br/>"
      
    )


@app.route("/api/v1.0/precipitation")
def prcpp():
    
    session = Session(engine)
    
    #querying date and precipitation for the last year of the data
    latest_date = session.query(ME.date).order_by(ME.date.desc()).first()
    date_result = latest_date[0]
    year_ago = dt.datetime.strptime(date_result, "%Y-%m-%d") - dt.timedelta(days=366)
    precipitation_oneyearago = session.query(ME.date,ME.prcp).filter(ME.date>=year_ago).all()

    session.close

    #returning the dict in a jsonified formart
    
    record = []
    for date, rain in precipitation_oneyearago:
        startdict = {}
        startdict['date'] = date
        startdict['rain_level'] = rain
                
        record.append(startdict)
    
    return jsonify(record)



@app.route("/api/v1.0/stations")
def stat():
    
    session = Session(engine)
    
    # Option 1: List of Station numbers and names in use in the last year of the dataset
    # querying date and precipitation for the last year of the data
    latest_date = session.query(ME.date).order_by(ME.date.desc()).first()
    date_result = latest_date[0]
    year_ago = dt.datetime.strptime(date_result, "%Y-%m-%d") - dt.timedelta(days=366)
    
    
    #querying the stations list
    sel = [ME.station, SA.name]
    dupli_station = session.query(*sel).filter(ME.station == SA.station).filter(ME.date >= year_ago).all()
    station_list = list(dict.fromkeys(dupli_station))
    
    session.close

    #returning the list in a jsonified formart
    record = []
    for station, name in station_list:
        startdict = {}
        startdict['station_ID'] = station
        startdict['name'] = name
                
        record.append(startdict)
    
    
    return jsonify(record)


    # # Option 2: Return list of stations of in the whole Area
    # stations =session.query(SA.station,SA.name).all()

    # stations_results = dict(stations)
    # return  jsonify(stations_results)


@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)
    
       
    #query to get dataset for the last year of the data
    latest_date = session.query(ME.date).order_by(ME.date.desc()).first()
    latest_date = latest_date[0]
    year_ago = dt.datetime.strptime(latest_date, "%Y-%m-%d") - dt.timedelta(days=366)
    
    # The station has the highest number of observations
    stations_activelist = session.query(ME.station,func.count(ME.station)).group_by(ME.station).order_by(func.count(ME.station).desc()).filter(ME.date>=year_ago).all()
    station_mostactive = stations_activelist[0][0]
    
    # query to get dates and temperature of the most active station for the last year of the data
    temp_stat = session.query(ME.date, ME.tobs).filter(ME.station == station_mostactive).all()

    session.close
    
    #returning the list in a jsonified formart
    record = []
    for date, tobs in temp_stat:
        startdict = {}
        startdict['date'] = date
        startdict['temp'] = tobs
                
        record.append(startdict)
    
    return jsonify(record)


@app.route("/api/v1.0/<start>") 
def start_range(start):
    
    session = Session(engine)
    
    single_date = session.query(ME.date,func.min(ME.tobs),func.avg(ME.tobs),func.max(ME.tobs)).filter(ME.date >= start).group_by(ME.date).all()
    
    session.close

    record = []
    for date, tmin, tavg, tmax in single_date:
        startdict = {}
        startdict['date'] = date
        startdict['min'] = tmin
        startdict['avg'] = tavg
        startdict['max'] = tmax
        
        record.append(startdict)
    
    return jsonify(record)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    
    session = Session(engine)
    
    range_date = session.query(ME.date,func.min(ME.tobs),func.avg(ME.tobs),func.max(ME.tobs)).filter(ME.date >= start).filter(ME.date <= end).group_by(ME.date).all()
    
    session.close

    record = []
    for date, tmin, tavg, tmax in range_date:
        startdict = {}
        startdict['date'] = date
        startdict['min'] = tmin
        startdict['avg'] = tavg
        startdict['max'] = tmax
        
        record.append(startdict)
    
    return jsonify(record)


if __name__ == '__main__':
    app.run(debug=True)