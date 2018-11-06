#!/usr/bin/python
# -*- coding: utf-8 -*-

import libtmux
import os
from datetime import datetime

# Variaveis estaticas
timenow = datetime.now().strftime('-%M-%S')
tmux_session = "bifrost%s"%(timenow)

### Issue consigo abrir akeyas 6 sessoes, devido ao espaco da tela. tentei dividir com horizontal também, porém cosegui akeyas 7 telas
def tmux(hosts, user, key, terminal, screen=False, group=False):
# Abre um terminator e cria uma sessao do temux, depois atacha a sessao
    if terminal:
        start_tmux = "%s -x tmux new-session -s bifrost%s"%(terminal, timenow)
    else:
        start_tmux = "/bin/xterm -e \"tmux new-session -s bifrost%s\""%(timenow)
    os.system(start_tmux)
    server = libtmux.Server()
    try:
        session = server.find_where({ "session_name": tmux_session })
    except Exception as e:
        print("Erro ao procurar a sessão do Tmux  %s" %e)
        session = False

# Foi preciso separa com o if pois a primeira execucao do tmux eu preciso atachar a existente e depois vou criando as demais
    if session:
        for host in range(len(hosts)):
            if host == 0:
                for __, value in hosts[host].items():
                    ec2 = value
                cmd = "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i %s %s@%s" %(key, user, ec2)
                window = session.attached_window
                current = window.attached_pane
                current.send_keys(cmd)
            elif host < (len(hosts) -1 ):
                for __, value in hosts[host].items():
                    ec2 = value
                cmd = "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i %s %s@%s" %(key, user, ec2)
                window = session.attached_window
                pane = window.split_window(attach=False, vertical=screen)
                pane.send_keys(cmd)
            else:
                for __, value in hosts[host].items():
                    ec2 = value
                cmd = "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i %s %s@%s" %(key, user, ec2)
                window = session.attached_window
                pane = window.split_window(attach=False, vertical=screen)
                pane.send_keys(cmd)
                if group:
                    window.set_window_option("synchronize-panes", "on")
