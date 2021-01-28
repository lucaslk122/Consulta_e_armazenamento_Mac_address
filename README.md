# Mac_address
 
Esse programa tem como objetivo a conexão via ssh com dispositivos switchs, a conexão é feita passando como parametro uma lista com os ips dos switchs, usuario e senha.
Feito o acesso, os dados são tratados para serem armazenados em um banco de dados não relacional, no caso, o mongoDB.
Tmbém é possivel utilizar switchs nexus, como o comando show mac address-table é o mesmo para switchs cisco de ios mais atual, a unica diferença está no fato dele possuir informações a mais, tais como age, secure e NTFY, tais campos são removidos através de uma condição básica de existencia.
