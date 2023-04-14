# TFTP2


1. Gerar a imagem a partir do Dockerfile

```shell
    docker build -t ptc/tftp2 .
```

2. Executar o contêiner a partir da imagem criada
```shell
    docker run -it --rm -v `pwd`:/tftp2  --name tftp2 ptc/tftp2
```

3. Atenção ao executar o Servidor:

```
    $(pwd)/pasta
```
