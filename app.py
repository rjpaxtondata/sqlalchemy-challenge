import numpy as np
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

#########create home route##############
@app.route("/")
def welcome():
    #"List all available routes."
    return (
        f"Available routes:<br/>"
        f"#############################<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/yyyy-mm-dd<br/>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd"

    )
#########create Precipitation route##############
@app.route("/api/v1.0/precipitation")
def precipitation():
    #Calculate data for last 12 months
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    #create our session (link) from Python to the DB
    session = Session(engine)
    #Query Percipatation and date
    results = session.query(Measurement.date, Measurement.prcp).\
            filter (Measurement.date >= prev_year).all()
    
    #close out the session
    session.close()
    
    #Create a dictionary from the row data and append to a list of dates and precipitations
    data_prec = []

    for date, prcp in results:
        prcp_dict= {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp

        data_prec.append(prcp_dict)
    
    return jsonify(data_prec)

#########create station route##############

@app.route("/api/v1.0/stations")
def stations():

#create our session (link) from Python to the DB
    session = Session(engine)
    #Query Percipatation and date
    results = session.query(Station.station, Station.name).all()
    
    #close out the session
    session.close()

    station_list = []

    for station, name in results:
        stat_name={}
        stat_name["station"] = station
        stat_name["name"] = name

        station_list.append(stat_name)
    
    return jsonify(station_list)

#########code to return just 1 variable of station
# def stations():
# 	results = session.query(Station.station).all()
# 	# Unravel results into one-dimensional array with:
# 		# `function np.ravel()`, `parameter = results`
# 	# Convert results array into a list with `list()`
# 	stations = list(np.ravel(results))
# 	return jsonify(stations=stations) 

#########create temp route for most active station##############
@app.route("/api/v1.0/tobs")
def temp():
    #create our session (link) from Python to the DB
    session = Session(engine)
    #create variable to focus on last 12 months
    lastyear = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    latestdate = dt.datetime.strptime(lastyear, '%Y-%m-%d')
    querydate = dt.date(latestdate.year -1, latestdate.month, latestdate.day)

    sel = [Measurement.date, Measurement.tobs]
    
    results = session.query(*sel).filter(Measurement.date >= querydate).all()
    
        #close out the session
    session.close()
    temps = list(np.ravel(results))
    return jsonify(stations=temps)

#########create temp route for most active station##############
@app.route("/api/v1.0/<start_date>")
def start_temp(start_date):
    #create our session (link) from Python to the DB
    session = Session(engine)
    
    
    #return min, max, average temp for a specific date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).all()

    #close out the session
    session.close()
    
    #create a dictionary with values

    start_values = []

    for min, avg, max in results:
        startdate_value = {}
        startdate_value["min_temp"] = min
        startdate_value["avg_temp"] = avg
        startdate_value["max_temp"] = max

        start_values.append(startdate_value)
    
    return jsonify(start_values)

#########create temp route for most active station##############
@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end_temp(start_date, end_date):

    session = Session(engine)
    
    
    #return min, max, average temp for a specific date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    #close out the session
    session.close()
    
    #create a dictionary with values for state to end date
    range_values = []

    for min, avg, max in results:
        start_end_values ={}
        start_end_values["min_temp"] = min
        start_end_values["avg_temp"] = avg
        start_end_values["max_temp"] = max
        range_values.append(start_end_values)
    
    return jsonify(range_values)

if __name__ == '__main__':
    app.run(debug=True)