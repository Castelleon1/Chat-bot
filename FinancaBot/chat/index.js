var app = require('express')();
var http = require('http'); 
var server = http.Server(app);
var io = require('socket.io')(server);
var port = process.env.PORT || 3000;

const URL_ROBO = "http://localhost:5000";
const URL_ROBO_RESPOSTA = `${URL_ROBO}/resposta`;
const CONFIANCA_MINIMA = 0.60;

const getResposta = (mensagem) => {
  
  const mensagemCodificada = encodeURIComponent(mensagem);
  const urlCompleta = `${URL_ROBO_RESPOSTA}/${mensagemCodificada}`;

  http.get(urlCompleta, (res) => {
    let retorno = "";

    res.on("data", (pedaco) => {
      retorno += pedaco;
    });

    res.on("end", () => {
      try {

        const jsonRetorno = JSON.parse(retorno);

        if (jsonRetorno.confianca >= CONFIANCA_MINIMA) {
          io.emit("chat message", `🤖 ${jsonRetorno.resposta}`);
        } else {
          io.emit("chat message", `🤖 Não sei responder essa pergunta com certeza. Tente reformular.`);
        }
      } catch (erro) {
        console.error("Erro ao processar JSON do Python:", erro);
        console.error("Resposta crua recebida:", retorno);
        io.emit("chat message", "🤖 Ocorreu um erro interno no cérebro do robô.");
      }
    });

  }).on('error', (e) => {

    console.error(`Erro na conexão com o Python: ${e.message}`);
    io.emit("chat message", "🤖 Erro: Não consegui conectar ao servidor do robô (Python).");
  });
}


app.get('/', function (req, res) {
  res.sendFile(__dirname + '/index.html');
});


io.on('connection', function (socket) {
  console.log('Um usuário conectou');

  socket.on('chat message', function (msg) {
  
    io.emit('chat message', `👤 ${msg}`);
    
    
    getResposta(msg);
  });
  
  socket.on('disconnect', () => {
      console.log('Usuário desconectou');
  });
});


server.listen(port, function () {
  console.log('Servidor Node rodando em http://localhost:' + port);
});