from app import app 
from app.controllers import desafios
from app.controllers import empresas
from app.controllers import usuarios

if __name__ == '__main__':
    app.run(debug=True)