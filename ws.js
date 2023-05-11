const Websocket = require('ws');
const { EventEmitter } = require('events');

EventEmitter.setMaxListeners(1500)


const app = (require('express'))();

class SocketListener extends EventEmitter {
    constructor() {
        super();

        this.server = new Websocket.Server({
            port: 4968
        });

        this.server.on('error', (err) => {
            console.log('WebSocket server error:', err);
        });

        this.server.on('listening', () => {
            console.log('WebSocket server started');
        });

        this.client = undefined;
    }

    async start() {
        this.server.on("connection", (socket) => {
            this.client = socket;
            this.client.on('message', (data) => this.emit('resolve', data));

            this.emit('ready');
            console.log(`Browser connected`);
        });
    }

    send(data) {
        this.client.send(data);
    }
}

const Client = new SocketListener();
app.get('/n', async (req, res) => {
    await Client.send(req.query.req);
    Client.once('resolve', async (data) => {
        res.send(JSON.parse(data));
    });
});

app.listen(3030, async () => {
    console.log(`Api Online`);
    await Client.start();
});