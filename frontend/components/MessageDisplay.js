import React, { useState, useEffect } from 'react';

const MessageDisplay = ({ eventId }) => {
    const [messages, setMessages] = useState([]);

    useEffect(() => {
        fetch(`/events/${eventId}/messages`)
            .then(response => response.json())
            .then(data => setMessages(data))
            .catch(error => console.error('Error fetching messages:', error));
    }, [eventId]);

    return (
        <div>
            {messages.map(msg => (
                <div key={msg.id}>
                    <p>{msg.sender_id}: {msg.content}</p>
                    <small>{new Date(msg.timestamp).toLocaleString()}</small>
                </div>
            ))}
        </div>
    );
};

export default MessageDisplay;
