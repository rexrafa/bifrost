#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import click
import yaml
import time
import pprint

from tmux_ssh import tmux
from aws_search import list_instances
from aws_search_sr import list_instances_sr
from ssh_command import connect_ssh



with open(os.environ['HEIMDALL_CONFIG'], 'r') as stream:
    heimdall = yaml.load(stream)

@click.group()
def cli():
    pass


@click.command()
@click.option('--reino','-r', help='Cliente a ser executado ')
@click.option('--env','-e', help='ambiente do cliente exp: hmg, prd')
@click.option('--host','-h', help='hosts a serem acessados')
@click.option('--public','-p',default=False ,help='Retornar IP publico caso a maquina tenha, defaul=false')
@click.option('--group','-g',default=False ,help='Cria um grupo com todos os panes do tmux, defaul=false')
@click.option('--user','-u',default=False ,help='Passar um usuario para conexâo, por default pega do heimdall.yml')
@click.option('--key','-k',default=False ,help='Passar key ssh para conexâo, por default pega do heimdall.yml')
def open(reino, env, host, public, group, user, key):
    if reino in heimdall["reinos"] and env in heimdall["reinos"][reino]:
        click.echo('Vamos acessar o reino %s no env %s as maquinas de %s' %(reino, env, host))
# Verificar se existe instancias com o nome pesquisado
        region = heimdall["reinos"][reino][env]["aws"]["region"]

        if heimdall["reinos"][reino][env]["aws"]["sr"]:
            arn = heimdall["reinos"][reino][env]["aws"]["arn"]
            name = heimdall["reinos"][reino][env]["aws"]["name"]
            lista = list_instances_sr(host, region, public, arn, name)
        else:
            lista = list_instances(host, region, public)
        if len(lista) > 0:
            if user == False:
                user = heimdall["reinos"][reino][env]['user']
            if key == False:
                key = heimdall["reinos"][reino][env]['key']
            terminal = heimdall["bifrost"]["terminal"]
            tmux(lista, user, key, terminal, group=group)

    else:
        click.echo('Heimdall não conseguiu conectar no reino escolhido')


@click.command()
@click.option('--reino','-r', help='Mostra os ambientes disponiveis dentro do reino ')
@click.option('--env','-e',default=False ,help='Mostra a lista de hosts disponiveis')
@click.option('--host','-h',default=False ,help='Mostra detalhes do host especifico')
@click.option('--public','-p',default=False ,help='Retornar IP publico caso a maquina tenha, defaul=false')
def describe(reino, env, host, public):
    if reino in heimdall["reinos"] and env == False and host == False:
       for key in heimdall["reinos"][reino]:
           click.echo(key)

    elif reino in heimdall["reinos"] and env and host == False:
       for key in heimdall["reinos"][reino][env]:
           pprint.pprint(heimdall["reinos"][reino][env][key])

    elif reino in heimdall["reinos"] and env and host:
       click.echo(host)
       region = heimdall["reinos"][reino][env]["aws"]["region"]
       if heimdall["reinos"][reino][env]["aws"]["sr"]:
            arn = heimdall["reinos"][reino][env]["aws"]["arn"]
            name = heimdall["reinos"][reino][env]["aws"]["name"]
            lista = list_instances_sr(host, region, public, arn, name)
       else:
            lista = list_instances(host, region, public)
       if len(lista) > 0:
         for ip in range(len(lista)):
             for k, v in lista[ip].items():
                print("%s -- %s"%(k, v))
       else:
            click.echo("Heimdall nâo conseguiu localizar nenhuma maquina")
    else:
        click.echo("Ops algo estranho aconteceu")


@click.command()
def reinos():
    for key in heimdall["reinos"]:
        click.echo(key)


@click.command()
@click.option('--reino','-r', help='Cliente a ser executado ')
@click.option('--env','-e', help='ambiente do cliente exp: hmg, prd')
@click.option('--host','-h', help='hosts a serem acessados')
@click.option('--shell','-s', help='commando a ser executado, precisa estar entre " " ')
@click.option('--public','-p',default=False ,help='Retornar IP publico caso a maquina tenha, defaul=false')
@click.option('--delay','-d',default=0 ,help='Delay entre a execucao de uma maquina para outra em segundos')
def command(reino, env, host, shell,public, delay):
    if reino in heimdall["reinos"] and env in heimdall["reinos"][reino]:
# Verificar se existe instancias com o nome pesquisado
        region = heimdall["reinos"][reino][env]["aws"]["region"]
        if heimdall["reinos"][reino][env]["aws"]["sr"]:
             arn = heimdall["reinos"][reino][env]["aws"]["arn"]
             name = heimdall["reinos"][reino][env]["aws"]["name"]
             lista = list_instances_sr(host, region, public, arn, name)
        else:
             lista = list_instances(host, region, public)
# recebido os valores do Yaml. Não passei os valores direto na chamada da funçaõ pois ia ficar muito grande.
        if len(lista) > 0:
            user = heimdall["reinos"][reino][env]['user']
            key = heimdall["reinos"][reino][env]['key']

            for ip in range(len(lista)):
                for __, value in lista[ip].items():
                    ec2 = value
                click.echo("############ executando o comando na maquina %s  ############" %ec2)
                try:
                    result = connect_ssh(ec2, user, key, shell)               
                    for stdout in range(len(result)):
                        click.echo(result[stdout])
                    if ip < (len(lista) - 1):
                        time.sleep(delay)
                except Exception as e:
                    click.echo("Erro ao conectar no host %s" %e)              
    else:
        click.echo('Heimdall não conseguiu conectar no reino escolhido')


# CLI opcoes
cli.add_command(open)
cli.add_command(command)
cli.add_command(describe)
cli.add_command(reinos)

if __name__ == '__main__':
    cli()
