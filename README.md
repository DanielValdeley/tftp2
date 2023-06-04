# PTC

### Projeto TFTP2

O projeto tftp2 é uma versão incrementada do protocolo [TFTP](https://github.com/mmsobral-croom/projeto-1-um-protocolo-de-transferencia-de-arquivos-ptc-daniel). Com a adição de novas funcionalidades.

### Entrega

- [Cliente TFTP2](/tftp2/client_tftp2.py) - Cliente do protocolo TFTP2

- [Cliente Teste](/tftp2/client_test.py) - Programa de teste

- [*Protocol Buffers*](/tftp2/tftp2.proto) - Mensagens do protocolo (arquivo de especificação) 

- [TFTP2](/tftp2/tftp2.py) - Implementação do protocolo 

### Disponibilizado pelo professor

- [Servidor]() - Servidor tftp (também atende o tftp2) linkado estaticamente

### Como testar as funcionalidades

>A fim de facilitar a instalação do aplicativo, foi criado um [Dockerfile](/Dockerfile) contendo as bibliotecas necessárias. Esse Dockerfile utiliza como base uma imagem do Ubuntu 22.04 e instala as dependências. As bibliotecas instaladas incluem build-essential, protobuf-compiler, libprotobuf-dev, python3-pip, python3-protobuf e tmux.

1. Gerar a imagem a partir do Dockerfile

```shell
    docker build -t ptc/tftp2 .
```

2. Executar o contêiner a partir da imagem criada
```shell
    docker run -it --rm -v `pwd`:/ptc  --name tftp2 ptc/tftp2
```

3. Dentro do contêiner execute o Servidor TFTP
   
   - Entre no diretório `ptc/tftp2`
   
   - Formato do comando de execução

    ```shell
        ./tftp_server base_dir port  
    ```
    - Exemplo de uso
    ```shell
        ./tftp_server $(pwd)/pasta 6969 
    ```


2. Dentro do contêiner execute o Cliente TFTP2

   - Formato do comando de execução

    ```shell
        Uso: python3 client_test.py file_name [recv=1/send=2 | list=3/mkdir=4/move=5] [octet=1/netascii=2] IP PORT new_filename
    ```

   - Exemplo de uso
   
      - RECV
         ```shell
             python3 client_test.py arquivo 1 1 127.0.0.1 6969
         ```
  
     - SEND
        ```shell
            python3 client_test.py arquivo 2 1 127.0.0.1 6969
        ```
     
     - LIST
        ```shell
            python3 client_test.py . 3 1 127.0.0.1 6969
        ```

     - MKDIR
        ```shell
            python3 client_test.py nova-pasta-criada 4 1 127.0.0.1 6969
        ```

     - MOVE
        ```shell
            python3 client_test.py arquivo 5 1 127.0.0.1 6969 novo-nome-arquivo
        ```
### Especificação do protocolo TFTP2

#### Serviço oferecido + novas funcionalidades

  - envia e recebe arquivos
  - lista pastas, obtem uma listagem de arquivos com respectivos atributos (nome, tamanho)
  - criar pastas
  - renomear ou remover arquivos

#### Conjunto de mensagens do protocolo

O protocolo TFTP define cinco tipos de mensagens:

- Read request (RRQ) - solicita a leitura de um arquivo
- Write request (WRQ) - solicita a escrita de um arquivo
- Data (DATA) - representa os dados do arquivo
- Acknowledgment (ACK) - representa a mensagem de confirmação
- Error (ERROR) - representa uma mensagem de erro

A nova versão do TFTP contém destas novas mensagens abaixo:


- LIST: fazer listagem de uma pasta. Seu formato deve ser: caminho (string)
    - Resposta de LIST: contém a listagem da pasta. Seu formato é dado por uma lista de Elementos. Cada Elemento é um valor de um destes dois tipos:
        - Arquivo: representa um arquivo, e é formado por: nome (string), tamanho(int 32 bits)
        - Pasta: representa uma pasta, sendo formado por: nome(string)
    - Resposta de LIST pode também ser uma mensagem Error

- MKDIR: cria uma pasta. Seu formato deve ser: caminho (string)
    - Resposta de MKDIR: deve ser:
        - Sucesso: mensagem Ack com número de bloco 0
        - Erro: mensagem Err com um código de erro e ErrMsg contendo uma breve descrição

- MOVE: renomeia ou remove arquivos. Seu formato deve ser:  nome_original (string), novo_nome (string)
    - Se novo_nome for vazio, o arquivo deve ser removido
    - Resposta de MOVE: deve ser uma mensagem:
        - Sucesso: mensagem Ack com número de bloco 0
        - Erro: mensagem Err com um código de erro e ErrMsg contendo uma breve descrição

