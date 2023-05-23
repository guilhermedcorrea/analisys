#iniciando o app

#python3 -m venv venv
#venv\bin\activate
#pip install -r requirements.txt

# export a variavel 
#export FLASK_APP="app:create_app()"


#Migrações banco de dados

<br>flask db init<br/>
<br>flask db migrate -m "Initial migration."<br/>
<br>flask db upgrade<br/>


#Deploy App
# GUNICORN
#gunicorn --bind 0.0.0.0:5000 'app:create_app()'

# seleciona quantidade de workers respeitando a regra (2*CPU)+1 workers 2 x a quantidade de cores da maquina e +1

#gunicorn -w 4 -b 0.0.0.0 'app:create_app()'


#checar configurações Nginx



```Python
def celery_init_app(app) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app
```
</br>Função MakeCelery -  cria e retorna um Celeryobjeto para a Factory Application.<br>


```Python
@dataclass
class Variaveis(Sequence):
    venda_id: int
    variavel: str
    _data = {}
    _index = 0
    _next_index = 0

    def __len__(self) -> int:
        return self._index

```
</br>Recebe e Itera pelas variaveis passadas pelo parametro do endpoint. Retorna para a Factory e faz as chamadas das funções correspondentes<br>

```Python
class UploadFiles:
    def __init__(self,file_name):
        self.file_name = file_name
        self.path='/home/guilherme/analytics/app/uploads'
        self.databases='/home/guilherme/analytics/app/databases'
        self.name = str(datetime.now()).split(" ")[0]
        
    def csv_reader(self):
        with open(self.file_name,newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(
                csvfile, delimiter=";", skipinitialspace=True)
            rows = [{**item} for item in reader]
            data = pd.DataFrame(rows)
         
            
            data.to_csv(os.path.join(self.path,f'excelfile-{self.name}.csv'))
```
</br>Recebe o Path e o nome do arquivo, faz a leitura e salva.<br>


```Python

    def reader_files(self):
        self.csv_reader()
        files = os.listdir(self.path)
        cont = len(files)
        i = 0
        while i < cont:
            os.path.join(self.path,files[i])
           
            df = pd.read_csv(os.path.join(self.path,files[i]),sep=",",encoding='utf-8')
            dicts = df.to_dict('records')
           
            print(dicts)
            
            
            i+=1
```
</br>Faz a leitura de tods os arquivos dentro da pasta e no final deleta tods.<br>




```Python
def create_app():
    app = Flask(__name__)
    
    app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://localhost",
        result_backend="redis://localhost",
        task_ignore_result=True,),)
            
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SECRET_KEY'] = secrets.token_hex()
    app.config['SQLALCHEMY_POOL_SIZE'] = 370
    app.config['SQLALCHEMY_MAX_OVERFLOW'] = 0
    app.config['MAX_CONTENT_LENGTH'] = 2 * 7024 * 7024
    app.config['UPLOAD_EXTENSIONS'] = ['.csv', '.xlsx', '.xls']
    app.config['UPLOAD_PATH'] = r'/home/guilherme/analytics/app/uploads'
    app.config['DEBUG'] = True

    from .admin.Admin import Admin
   
    with app.app_context():
        db.init_app(app)
       
        migrate.init_app(app, db)
        app.register_blueprint(Admin)
        celery_init_app(app)
    return app

```
</br>Faz a chamada de todas as funções de dentro do aplicativo. blueprints, database etc<br>