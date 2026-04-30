from ..Routers.todos import get_db, get_current_user
from fastapi import status
from ..models import Todos
from .utils import *
from ..Routers.auth import create_access_token
from datetime import timedelta

        
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


## Real all Todos test
def test_read_all_authenticated(test_todo):
    response = client.get('/todos')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete':False,
                                'title': 'Learn to code!', 
                                'description': 'Need to learn everyday!',
                                'id': 1,
                                'priority':5,
                                'owner_id': 1}]


def test_todo_page_with_valid_cookie(test_todo):
    token = create_access_token('Srikumar', 1, 'admin', timedelta(minutes=20))
    response = client.get('/todos/todo-page', cookies={'access_token': token})

    assert response.status_code == status.HTTP_200_OK
    assert 'Learn to code!' in response.text


def test_add_todo_page_with_valid_cookie():
    token = create_access_token('Srikumar', 1, 'admin', timedelta(minutes=20))
    response = client.get('/todos/add-todo-page', cookies={'access_token': token})

    assert response.status_code == status.HTTP_200_OK
    assert 'Make a new todo' in response.text


def test_edit_todo_page_with_valid_cookie(test_todo):
    token = create_access_token('Srikumar', 1, 'admin', timedelta(minutes=20))
    response = client.get('/todos/edit-todo-page/1', cookies={'access_token': token})

    assert response.status_code == status.HTTP_200_OK
    assert 'Learn to code!' in response.text


def test_read_one_authenticated(test_todo):
    response = client.get('/todos/todo/1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'complete':False,
                                'title': 'Learn to code!', 
                                'description': 'Need to learn everyday!',
                                'id': 1,
                                'priority':5,
                                'owner_id': 1}

def test_read_one_authenticated_not_found():
    response = client.get('/todos/todo/999')
    assert response.status_code == 404
    assert response.json() =={'detail':'Todo not found'}
    
def test_create_todo(test_todo):
    request_data ={
        'title':'New Todo!',
        'description':'New todo description',
        'priority': 5,
        'complete': False
    }
    response = client.post('/todos/todo/', json = request_data)
    assert response.status_code == 201
    
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')
    
# test update Todo
def test_update_todo(test_todo):
    request_data = {
        'title':'Change the title of the todo already saved',
        'description': 'Need to learn everyday!',
        'priority':5,
        'complete': False
    }
    
    response = client.put('/todos/todo/1', json = request_data)
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos). filter(Todos.id == 1).first()
    assert model.title == 'Change the title of the todo already saved'
    
## Test Update todo not found
def test_update_todo_not_found(test_todo):
    request_data = {
        'title':'Change the title of the todo already saved',
        'description': 'Need to learn everyday!',
        'priority':5,
        'complete': False
    }
    
    response = client.put('/todos/todo/999', json = request_data)
    assert response.status_code == 404
    assert response.json() == {'detail':'Todo not found'}
    
    
## Todo testing delete code    
def test_delete_todo(test_todo):
    response = client.delete('/todos/todo/1')
    assert response.status_code == 204
    db =  TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id==1).first()
    assert model is None
    

def test_delete_todo_not_found():
    response = client.delete('/todos/todo/999')
    assert response.status_code == 404
    assert response.json() =={'detail':'Todo not found'}
