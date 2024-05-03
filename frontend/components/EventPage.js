import React from 'react';
import MessageDisplay from '../components/MessageDisplay';
import MessageInput from '../components/MessageInput';

const EventPage = ({ eventId }) => {
    return (
        <div>
            <h1>Event Messages</h1>
            <MessageDisplay eventId={eventId} />
            <MessageInput eventId={eventId} />
        </div>
    );
};

export default EventPage;
