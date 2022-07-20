#from crypt import methods
#from dataclasses import dataclass
from flask import Flask, Blueprint, flash, redirect,render_template, request, session, url_for 
from flask_login import login_required ,current_user
from .models import Note
from . import UPLOAD_FOLDER, db
from werkzeug.utils import secure_filename
import os
import uuid as uuid

views = Blueprint('views', __name__)

app = Flask(__name__)
#---------------- IMPORTANT -- for path ------------
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
#ALLOWED_EXTENSIONS = set(['jpg','png','jpeg','gif'])
#---------------------------------------------------

@views.route('/notes',methods=['GET','POST'])
@login_required
def notes():
    if request.method =='POST':
        note = request.form.get('note')
        pics = request.files['pic']
        if pics :
            #grab image name
            secured_name = secure_filename(pics.filename)
            pic_name = str(uuid.uuid1()) + "_" + secured_name
            #save image to images folder
            pics.save(os.path.join(basedir,app.config['UPLOAD_FOLDER'],pic_name))
        else:
            pic_name = ''

        if len(note) < 1:
            flash('enter a note')
        else:
            new_note = Note(data=note,pic=pic_name,user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()

    return render_template('notes.html',user=current_user)


@views.route('/delete/<int:id>')
def delete(id):
    delete_id = Note.query.get(id)

    db.session.delete(delete_id)
    db.session.commit()
    return redirect(url_for('views.notes'))

    
