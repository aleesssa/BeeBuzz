from models.chat_message import ChatMessage
from models.user import User
from models.request import Request
from extensions import db, socketio

# Message from system
def system_update(message, request_id):
    system_user = User.query.filter_by(email='system@beebuzz.app').first()
    request = Request.query.filter_by(id=request_id).first()
    system_message = ChatMessage(
        sender_id = system_user.id,
        recipient_id = request.client_id,
        request_id = request_id,
        message = message
    )
    
    data = {
        'sender_id' : system_user.id,
        'sender_name' : 'BeeBuzz System',
        'message' : message,
    }
    
    # Save to db
    db.session.add(system_message)
    db.session.commit()
    
    # Real-time update
    socketio.emit('receive_message', data, room=request_id) 
    
    