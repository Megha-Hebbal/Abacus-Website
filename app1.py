from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func

with open('templates/config.json', 'r') as c:
    params = json.load(c)["params"]

# create the app
app = Flask(__name__)
db = SQLAlchemy()

# configure the SQLite database, relative to the app instance folder
if(params["local_server"]):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['production_uri']


db = SQLAlchemy(app)

class Members(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    designation = db.Column(db.String(50), nullable=False)
    img_id = db.Column(db.String(40), nullable=True)
    year = db.Column(db.String(20), nullable=False)
    quote = db.Column(db.String(300), nullable=True)


@app.route('/add_new_member',methods = ['GET','POST'])
def add_member():
    if(request.method == "POST"):
        membername = request.form.get('membername')
        designation = request.form.get('designation')
        year = request.form.get('year')
        quote = request.form.get('quote')
        
        entry = Members(name=membername, designation=designation, year=year, quote=quote)
        db.session.add(entry)
        db.session.commit()  

        flash('Member added successfully','success')
        return render_template('/admin_login.html')
      
    return render_template('add_new_member.html')

@app.route('/delete_member', methods=['GET','POST'])
def deletemembers():
    if(request.method == 'POST'):
        membername=request.form.get('membername')
        designation=request.form.get('designation')
        year=request.form.get('year')

        try:
            entry = db.session.execute(db.select(Members).filter_by(name=membername, designation=designation, year=year)).scalar_one()

            db.session.delete(entry)
            db.session.commit()
            flash('Member deleted successfully','success')
            return render_template('/admin_login.html')
            
        except Exception as e:
            flash ('Record not found','error')
            return render_template('/admin_login.html')

    return render_template('delete_member.html')

# Attributes for events table
# id (int(11)), name(varchar(50)), description(text), date(datetime(6)), registration_link(varchar(60)) 
class Events(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(300),nullable=False)
    date = db.Column(db.String(20),nullable=False)
    registration_link = db.Column(db.String(50),nullable=True)
    img_id = db.Column(db.String(50),nullable=False)

#---------------------Add New Event--------------------
app.config['SECRET_KEY'] = 'key'


@app.route('/add_new_event',methods = ['GET','POST'])
def add_event():
    if(request.method == "POST"):
        name = request.form.get('eventname')
        description = request.form.get('description')
        date = request.form.get('Date')
        link = request.form.get('link')
        
        entry = Events(name=name, description=description, date=date, registration_link=link)
        db.session.add(entry)
        db.session.commit()  
        flash('Event added successfully!', 'success')

        return render_template('/admin_login.html')

    return render_template('add_new_event.html')

#--------------Modify Events------------------

@app.route('/modify_event', methods=['GET','POST'])
def modifyevent():
    if(request.method == 'POST'):
        oldname=request.form.get('oldeventname')
        newname=request.form.get('eventname')
        description=request.form.get('description')
        date=request.form.get('Date')
        link=request.form.get('link')

        try:
            #Retrieving data from database based on oldname
            event = Events.query.filter_by(name=oldname).first()

            # Update the attributes of the event with new values
            if event:
                event.name = newname
                event.description = description
                event.date = date
                event.link = link

                # Commit the changes to the database
                db.session.commit()
                flash('Event updated successfully!', 'success')
                return render_template('/admin_login.html')
            # else:
            #     flash('Event not found!', 'error')
            
        except Exception as e:
            print ('Record not found')
            return render_template('/admin_login.html')

    return render_template('/modify_event.html')


class Achievements(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100), nullable=False)
    description=db.Column(db.String(1000), nullable= False)
    img_id=db.Column(db.String(40),nullable=True)
    Date=db.Column(db.Date,nullable=False)

@app.route("/add_new_achievement", methods = ['GET','POST'])
def addachievement():
    if(request.method == 'POST'):
        achievementname=request.form.get('achievementname')
        achievementdescription=request.form.get('achievementdescription')
        Date=request.form.get('Date')

        entry=Achievements(name=achievementname, description=achievementdescription, Date=Date)
        db.session.add(entry)
        db.session.commit()
        flash('Achievement added successfully','success')
        return render_template('admin_login.html')

    return render_template('add_new_achievement.html')

@app.route('/modify_achievement',methods=['GET','POST'])
def modifyachievement():
    if(request.method == 'POST'):
        oldachievement=request.form.get('oldachievement')
        newachievement=request.form.get('newachievement')
        adescription=request.form.get('achievementdescription')
        date=request.form.get('Date')

        try:
            #  Fetch record based on old achievement title
            entry = Achievements.query.filter_by(name=oldachievement).first()
            
            # check if entry contains a record
            if entry:
                entry.name=newachievement
                entry.description=adescription
                entry.Date=date

                # Commit changes to the DB
                db.session.commit()
                flash('Successfully modified achievement!','success')
                return render_template('admin_login.html')
            else:
                flash("Achievement not found!",'error')
                return render_template('admin_login.html')
        except Exception as e:
            flash('Achievement not found!','error')
            return render_template('admin_login.html')

    return render_template('modify_achievement.html')



@app.route('/')
def index():
    return render_template('index.html', params=params)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/events')
def events():
    all_events = Events.query.order_by(Events.date.desc()).all()
    return render_template('events.html', all_events = all_events)


@app.route('/achievements')
def achievements():
    Ach=Achievements.query.order_by(Achievements.Date.desc()).with_entities(Achievements.name, Achievements.img_id, Achievements.description,func.date_format(Achievements.Date, "%M, %Y").label("formatted_date")).all()
    return render_template('achievements.html', Ach=Ach)


@app.route('/members')
def members():
    Mem = Members.query.all()
    return render_template('members.html', Mem=Mem)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/login', methods=['GET','POST'])
def login():
    if(request.method=='GET'):
        return render_template('login.html')
    elif(request.method=='POST'):
        return render_template('admin_login.html')


@app.route('/add_new_event')
def add_new_event():
    return render_template('add_new_event.html')


@app.route('/modify_event')
def modify_event():
    return render_template('modify_event.html')


@app.route('/add_new_achievement')
def add_new_achievement():
    return render_template('add_new_achievement.html')


@app.route('/modify_achievement')
def modify_achievement():
    return render_template('modify_achievement.html')


@app.route('/delete_member')
def delete_member():
    return render_template('delete_member.html')



if __name__ == "__main__":
    app.run(debug=True)