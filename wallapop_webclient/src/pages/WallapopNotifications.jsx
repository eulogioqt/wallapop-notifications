import React, { useEffect, useState, useRef } from 'react';

const WallapopNotifications = () => {
    const [ws, setWs] = useState(undefined);
    const [messages, setMessages] = useState([]);
    const messageInputRef = useRef(null);
    const messagesDivRef = useRef(null);
    const connectedDivRef = useRef(null);

    useEffect(() => {
        connect();

        // Limpiar la conexión al desmontar el componente
        return () => {
            if (ws) {
                ws.close();
            }
        };
    }, []);

    const connect = () => {
        const serverIp = window.location.hostname;
        console.log("Conectado mediante Servidor Web: " + (serverIp !== undefined && serverIp.length > 0));

        const websocket = new WebSocket(`ws://${serverIp}:8765`);

        websocket.onopen = () => {
            console.log('Conectado al servidor WebSocket');
            addMessage("CONEXIÓN ESTABLECIDA", "green");
            scrollToBottom();
            connectedDivRef.current.style.backgroundColor = "green";
        };

        websocket.onmessage = (event) => {
            addMessage(`Servidor: ${event.data}`);
            scrollToBottom();
        };

        websocket.onclose = () => {
            console.log('Desconectado del servidor WebSocket');
            setWs(undefined);
            if (connectedDivRef.current.style.backgroundColor === "green") {
                addMessage("CONEXIÓN PERDIDA", "red");
                scrollToBottom();
            }
            connectedDivRef.current.style.backgroundColor = "red";
            setTimeout(connect, 5000); // Reintentar conexión después de 5 segundos
        };

        setWs(websocket);
    };

    const addMessage = (text, color = "black") => {
        setMessages((prevMessages) => [...prevMessages, { text, color }]);
    };

    const sendMessage = () => {
        if (ws === undefined || ws.readyState !== WebSocket.OPEN) {
            console.log("No estás conectado al servidor");
            return;
        }

        const message = messageInputRef.current.value;

        if (message) {
            ws.send(message);
            addMessage(`Tú: ${message}`);
            messageInputRef.current.value = '';
            scrollToBottom(); // Llama a la función para desplazar hacia abajo
        }
    };

    const scrollToBottom = () => {
        messagesDivRef.current.scrollTop = messagesDivRef.current.scrollHeight;
    };

    return (
        <div>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <div style={{ marginRight: '16px' }}>
                    <h1>Wallapop Notifications</h1>
                </div>
                <div ref={connectedDivRef} style={{ width: '32px', height: '32px', borderRadius: '100%', backgroundColor: 'black' }} />
            </div>

            <div>
                <input type="text" ref={messageInputRef} placeholder="Escribe un mensaje" />
                <button onClick={sendMessage}>Enviar</button>
            </div>

            <div
                ref={messagesDivRef}
                style={{ marginTop: '20px', border: '1px solid #000', padding: '10px', height: '200px', overflowY: 'scroll' }}
            >
                {messages.map((msg, index) => (
                    <div key={index} style={{ color: msg.color }}>
                        {msg.text}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default WallapopNotifications;
