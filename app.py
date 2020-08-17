# 1. import dependencies
from flask import Flask,jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from scipy import stats 

#setup the database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect the database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the tables
Measurement = Base.classes.measurement
Stations=Base.classes.station

# create the app
app = Flask(__name__)


# 3.define home route and what we want to show when route is ran
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/<start_date><br/>"
        f"/api/v1.0/start_end/<start_date>-<end_date>"
    )

# 4. Define what to do when a user hits the /precipitation route
@app.route("/api/v1.0/precipitation")

#define a function
def precipitation():
    print("Server received request for 'Precipitation' page...")
    
    #create a link from Python to the Dataase
    session=Session(engine)

    #Query the date and percipitation values from the measurement table
    results = session.query(Measurement.date, Measurement.prcp)

    session.close()
    
    #create a dictionary from the row data and append to the list 
    prcp_vals=[]
    for date,prcp in results:
        prcp_dict={}
        prcp_dict['date']=date
        prcp_dict['prcp']=prcp

        prcp_vals.append(prcp_dict)

    #return a jsonified version of the reults
    return jsonify(prcp_vals)


# 4. Define what to do when a user hits the /stations route
@app.route("/api/v1.0/stations")

def stations():
    print("Server received request for 'Stations' page...")
    
    #create a link from Python to the Dataase
    session=Session(engine)

    #Query the station label from the stations table
    results = session.query(Stations.station)

    session.close()

    #create a blank stations list
    stations_list=[]

    #iterate through results
    for station in results:

        #append the station to the station list
        stations_list.append(station[0])

    #return a jsonified version of the reults
    return jsonify(stations_list)
            

# 4. Define what to do when a user hits the /tobs route
@app.route("/api/v1.0/tobs")

def tobs():
    print("Server received request for 'Temperature observations' page...")
    
    #create a link from Python to the Dataase
    session=Session(engine)

    #Query the dates and temperature observations of the most active station for the last year of data.
    results = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.date <= '2017-08-23').\
            filter(Measurement.date >= '2016-08-23').\
            filter(Measurement.tobs != 'None').\
            filter(Measurement.station=='USC00519281').all()

    session.close()

    #results=np.ravel(results)
    #append the temp obervations to a list
    tobs_list=[]
    for date,tobs in results:
        tobs_dict={}
        tobs_dict['date']=date
        tobs_dict['tobs']=tobs

        tobs_list.append( tobs_dict)

    #Return a JSON list of temperature observations (TOBS) for the previous year.
    return jsonify(tobs_list)


@app.route("/api/v1.0/start/<start_date>")

def start(start_date):

    #create a link from Python to the Dataase
    session=Session(engine)

    #Query the dates and temperature observations of the most active station for the last year of data.
    results = session.query(Measurement.tobs).\
            filter(Measurement.date >= start_date).\
            filter(Measurement.tobs != 'None' and Measurement.tobs !='bb').all()

    session.close()

    #append the temp obervations to a list
    results=np.ravel(results)
    tobs_list=[]
    i=[]
    for tobs in results:
        tobs_dict={}
        #tobs_dict['date']=date
        #tobs_dict['tobs']=tobs

        tobs_list.append(tobs)

    tobs_dict['min']=stats.tmin(tobs_list)
    tobs_dict['avg']=stats.tmean(tobs_list)
    tobs_dict['max']=stats.tmax(tobs_list)

    i.append(tobs_dict)

    #Return a JSON list of temperature observations (TOBS) for the previous year.
    return jsonify(i)

@app.route("/api/v1.0/start_end/<start_date>-<end_date>")
def start_end (start_date,end_date):

    #create a link from Python to the Dataase
    session=Session(engine)

    #Query the dates and temperature observations of the most active station for the last year of data.
    results = session.query(Measurement.tobs).\
            filter(Measurement.date >= start_date).\
            filter(Measurement.date <= end_date).\
            filter(Measurement.tobs != 'None' and Measurement.tobs !='bb').all()

    session.close()

    #append the temp obervations to a list
    results=np.ravel(results)
    tobs_list=[]
    i=[]
    for tobs in results:
        tobs_dict={}

        tobs_list.append(tobs)

    #assign key:value pairs for minimum, average, and max
    tobs_dict['min']=stats.tmin(tobs_list)
    tobs_dict['avg']=stats.tmean(tobs_list)
    tobs_dict['max']=stats.tmax(tobs_list)

    i.append(tobs_dict)

    #Return a JSON list of temperature observations (TOBS) for the previous year.
    return jsonify(i)

if __name__ == "__main__":
    app.run(debug=True)