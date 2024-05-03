import React, { useState } from 'react';

const MessageInput = ({ eventId }) => {
    const [content, setContent] = useState('');

    const sendMessage = (e) => {
        e.preventDefault();
        fetch(`/events/${eventId}/messages`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ content, sender_id: 1 }) // Assuming sender_id is 1 for now
        })
        .then(response => response.json())
        .then(data => {
            console.log('Message sent:', data);
            setContent('');
        })
        .catch(error => console.error('Error sending message:', error));
    };

    return (
        <form onSubmit={sendMessage}>
            <textarea value={content} onChange={(e) => setContent(e.target.value)} />
            <button type="submit">Send Message</button>
        </form>
    );
};

export default MessageInput;
