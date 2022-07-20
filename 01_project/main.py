#----The following code to generate a requirements.txt file:
#----pip install pipreqs
#----pipreqs /path/to/project

from project import create_app

app = create_app()

if __name__ =='__main__':
    app.run(debug = True)