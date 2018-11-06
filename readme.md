# Bifrost

Bifrost é um CLI com o intuito de facilitar o acesso as maquinas escalaveis da AWS. Ele verifica quais as maquinas estão rodando com o TAG Name definida no seu YML de config e utiliza o SSH para abrir de forma rapida sessão com as maquinas. 

Principais funções
  - Acesso remoto a diversos hosts de forma dinamica.
  - Executar comando remoto nos hosts com opção de definir delay de execução.
  - Conseguir visualizar os IPs da maquinas rodando na AWS.

### Tech

Bifrost é um projeto OpenSource que utiliza as tecnologias abaixo:

* [Python](https://www.python.org/) - O projeto é escrito em Python 3
* [Click](http://click.pocoo.org/5/) - Lib Python que facilita a criação de CLI
* [boto 3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) - Lib para consumir a API da AWS.
* [libtmux](https://libtmux.git-pull.com/en/latest/) - Lib Python na qual é utilizada para interagir com o TMUX
* [paramiko](https://docs.paramiko.org/en/2.4/) - Lib Python para executar conexões remotas e executar comandos.

### Instalação

Bifrost precisa do Python 2.7 +.

Instalar o Tmux.

```sh
$ sudo apt-get install tmux
$ sudo yum install tmux
$ sudo pacman -S tmux
```

Instalar dependencias Python(Vamos utilizar o PIP)

```sh
$ Sudo pip install -r requirements.txt
```
Criar um alias no bashrc com  caminho do bifrost.py ou adicionar no PATH a pasta do Bifrost, garantir o arquivo bifrost.py tenha permissão de execução

### Configuração Heimdall
O Bifrost precisa do arquivo heindall.yml, pois o mesmo contem suas configs, exporte o caminho do arquivo com a seguinte variavel de ambiente HEIMDALL_CONFIG.
Exemplo de arquivo:
```sh
bifrost:
  terminal: /bin/terminator
reinos: # Você pode ter varios clientes.
  conta1:   
    prd:
      aws:
        sr: True # Deixe falso se não for usar switch role ai não precisa dos campos arn e name
        region: sa-east-1
        arn: arn:aws:iam::id:role/rivendel-servicos
        name: cliente-prd
      key: key.pem
      user: ec2-user
    hmg:
      aws:
        sr: False # exeplo sem switch role
        region: sa-east-1
      key: key.pem
      user: ec2-user
  conta2:
    prd:
      aws:
        sr: False
        region: us-east-1
      key:
      user: ec2-user
    hmg:
      aws:
        sr: False
        region: us-east-1
      key:
      user: ec2-user
```

### Exemplos
```sh
$ bifrost command --reino cliente --env prd --host "api" --shell "pwd" --delay 3
$ bifrost open --reino cliente --env hmg --host "api" --group true
$ bifrost open --reino cliente --env prd --host "api" --user root --key key.pem
$ bifrost open --reino cliente --env hmg --host "api" --public true --group true #Conecta com o IP publico da maquina caso ela tenha
$ bifrost describe -r cliente -e prd -h "*api*"
```

License
----

MIT

**Free Software, Hell Yeah!**
