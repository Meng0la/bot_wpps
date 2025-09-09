const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const sqlite3 = require('sqlite3').verbose();

const client = new Client({
    authStrategy: new LocalAuth()
});

const db = new sqlite3.Database('./pecas_empilhadeira_pronto.db');

const estado = {};

client.on('qr', (qr) => {
    qrcode.generate(qr, { small: true });
});

client.on('ready', () => {
    console.log('✅ BOT está pronto e rodando!');
});

client.on('message', async msg => {
    const chatId = msg.from;
    const texto = msg.body.trim().toLowerCase();

    if (!estado[chatId]) {
        estado[chatId] = { etapa: 'marca' };
        msg.reply('👋 Qual a marca da empilhadeira?\n1 - Yale\n2 - Hyster\n3 - Hangcha');
        return;
    }

    const user = estado[chatId];

    if (user.etapa === 'marca') {
        const marcas = ['Yale', 'Hyster', 'Hangcha'];
        const escolha = parseInt(texto);
        if (escolha >= 1 && escolha <= marcas.length) {
            user.marca = marcas[escolha - 1];
            user.etapa = 'energia';
            msg.reply('🔋 Qual o tipo de energia?\n1 - GLP\n2 - Diesel\n3 - Elétrica');
        } else {
            msg.reply('❌ Opção inválida. Escolha:\n1 - Yale\n2 - Hyster\n3 - Hangcha');
        }
        return;
    }

    if (user.etapa === 'energia') {
        const energias = ['GLP', 'Diesel', 'Elétrica'];
        const escolha = parseInt(texto);
        if (escolha >= 1 && escolha <= energias.length) {
            user.energia = energias[escolha - 1];
            user.etapa = 'modelo';
            msg.reply('📦 Informe o modelo da empilhadeira (Ex.: 70VX, GDP50VX...)');
        } else {
            msg.reply('❌ Opção inválida. Digite:\n1 - GLP\n2 - Diesel\n3 - Elétrica');
        }
        return;
    }

    if (user.etapa === 'modelo') {
        user.modelo = msg.body.trim().toUpperCase();
        user.etapa = 'versao';
        msg.reply('🔢 Qual a versão do equipamento?\nEx.: A975, B975, C813...');
        return;
    }

    if (user.etapa === 'versao') {
        user.versao = msg.body.trim().toUpperCase();
        user.etapa = 'motor';
        msg.reply('⚙️ Qual o motor? (Ex.: Kubota 3.8L, GM, PSI...)');
        return;
    }

    if (user.etapa === 'motor') {
        user.motor = msg.body.trim();
        user.etapa = 'tipopeca';
        msg.reply('🔧 Qual o tipo de peça?\n1 - Motor\n2 - Hidráulico\n3 - Elétrico\n4 - Filtros\n5 - Freios\n6 - Transmissão\n7 - Estrutura\n8 - Acessórios');
        return;
    }

    if (user.etapa === 'tipopeca') {
        const tipos = ['Motor', 'Hidráulico', 'Elétrico', 'Filtros', 'Freios', 'Transmissão', 'Estrutura', 'Acessórios'];
        const escolha = parseInt(texto);

        if (escolha >= 1 && escolha <= tipos.length) {
            user.tipopeca = tipos[escolha - 1];

            db.all(`SELECT nome_peca, codigo_peca, observacoes FROM pecas 
                WHERE marca_empilhadeira = ? 
                AND tipo_energia = ? 
                AND modelo = ? 
                AND versao_equipamento = ?
                AND motor = ? 
                AND tipo_peca = ?`,
                [user.marca, user.energia, user.modelo, user.versao, user.motor, user.tipopeca],
                (err, rows) => {
                    if (err) {
                        msg.reply('❌ Erro na consulta ao banco.');
                        console.error(err);
                        return;
                    }

                    if (rows.length === 0) {
                        msg.reply('❌ Nenhuma peça encontrada com essas informações.');
                    } else {
                        let resposta = `✅ Peças encontradas para ${user.modelo} versão ${user.versao} motor ${user.motor}:\n`;
                        rows.forEach(row => {
                            resposta += `\n📦 *${row.nome_peca}*\n🔧 Código: *${row.codigo_peca}*\nℹ️ ${row.observacoes || 'Sem observações'}\n`;
                        });
                        msg.reply(resposta);
                    }

                    user.etapa = 'menu'; // Vai para o menu
                    msg.reply('\nDeseja:\n1 - Consultar outro tipo de peça nesse mesmo equipamento\n2 - Consultar outro equipamento\n3 - Encerrar');
                }
            );
        } else {
            msg.reply('❌ Opção inválida. Escolha:\n1 - Motor\n2 - Hidráulico\n3 - Elétrico\n4 - Filtros\n5 - Freios\n6 - Transmissão\n7 - Estrutura\n8 - Acessórios');
        }
        return;
    }

    if (user.etapa === 'menu') {
        const escolha = parseInt(texto);
        if (escolha === 1) {
            user.etapa = 'tipopeca';
            msg.reply('🔧 Qual o tipo de peça?\n1 - Motor\n2 - Hidráulico\n3 - Elétrico\n4 - Filtros\n5 - Freios\n6 - Transmissão\n7 - Estrutura\n8 - Acessórios');
        } else if (escolha === 2) {
            estado[chatId] = { etapa: 'marca' };
            msg.reply('👋 Vamos começar de novo!\nQual a marca da empilhadeira?\n1 - Yale\n2 - Hyster\n3 - Hangcha');
        } else if (escolha === 3) {
            delete estado[chatId];
            msg.reply('👍 Consulta encerrada. Quando precisar, é só chamar!');
        } else {
            msg.reply('❌ Opção inválida. Digite:\n1 - Consultar outro tipo de peça\n2 - Consultar outro equipamento\n3 - Encerrar');
        }
        return;
    }
});

client.initialize();
