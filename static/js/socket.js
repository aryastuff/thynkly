// Socket.IO client for real-time features
let socket;

function initializeSocket() {
    // Only initialize if we're on a page that needs Socket.IO
    if (typeof io === 'undefined') {
        console.log('Socket.IO not loaded');
        return;
    }
    
    socket = io();
    
    // Connection events
    socket.on('connect', function() {
        console.log('Connected to server');
    });
    
    socket.on('disconnect', function() {
        console.log('Disconnected from server');
    });
    
    socket.on('connect_error', function(error) {
        console.error('Connection error:', error);
        showNotification('Connection error. Please refresh the page.', 'error');
    });
    
    // Handle reconnection
    socket.on('reconnect', function() {
        console.log('Reconnected to server');
        showNotification('Connection restored!', 'success');
    });
    
    socket.on('reconnect_error', function(error) {
        console.error('Reconnection error:', error);
    });
    
    // Custom events for notifications
    socket.on('collaboration_request', function(data) {
        showNotification(`New collaboration request from ${data.sender_name}!`, 'info');
        updateNotificationBadge();
    });
    
    socket.on('request_approved', function(data) {
        showNotification(`${data.recipient_name} approved your collaboration request!`, 'success');
    });
    
    socket.on('request_declined', function(data) {
        showNotification(`${data.recipient_name} declined your collaboration request.`, 'warning');
    });
    
    return socket;
}

function updateNotificationBadge() {
    // Update notification badge count (if implemented)
    const badge = document.querySelector('.notification-badge');
    if (badge) {
        const currentCount = parseInt(badge.textContent) || 0;
        badge.textContent = currentCount + 1;
        badge.style.display = 'inline';
    }
}

function joinRoom(roomName) {
    if (socket) {
        socket.emit('join', { room: roomName });
    }
}

function leaveRoom(roomName) {
    if (socket) {
        socket.emit('leave', { room: roomName });
    }
}

function sendMessage(recipientId, content, room) {
    if (socket) {
        socket.emit('send_message', {
            recipient_id: recipientId,
            content: content,
            room: room
        });
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Only initialize socket on pages that need it
    const needsSocket = document.querySelector('.chat-main') || 
                       document.querySelector('.notifications-page') ||
                       document.querySelector('.dashboard-page');
    
    if (needsSocket) {
        initializeSocket();
    }
});

// Handle page visibility changes
document.addEventListener('visibilitychange', function() {
    if (socket) {
        if (document.hidden) {
            // Page is hidden, reduce socket activity
            console.log('Page hidden, reducing socket activity');
        } else {
            // Page is visible, resume normal socket activity
            console.log('Page visible, resuming socket activity');
        }
    }
});

// Clean up socket connection when leaving page
window.addEventListener('beforeunload', function() {
    if (socket) {
        socket.disconnect();
    }
});
