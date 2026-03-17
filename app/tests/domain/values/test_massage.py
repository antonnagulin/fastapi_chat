from datetime import datetime

import pytest
from domain.entities.massages import Chat, Massage
from domain.exeptions.massages import TitleToLongExeption
from domain.values.massages import Text, Title


def test_create_massage_sucsess_short_text():
    text = Text("Hello word")
    massage = Massage(text=text)

    assert massage.text == text
    assert massage.created_at.date() == datetime.today().date()


def test_create_massage_sucsess_long_text():
    text = Text("a" * 400)
    massage = Massage(text=text)

    assert massage.text == text
    assert massage.created_at.date() == datetime.today().date()


def test_create_chat_sucsess():
    title = Title("title")
    chat = Chat(title=title)

    assert chat.title == title
    assert not chat.massage
    assert chat.created_at.date() == datetime.today().date()


def test_create_chat_title_to_long():
    with pytest.raises(TitleToLongExeption):
        Title("title" * 200)


def test_add_chat_to_massage():
    text = Text("Hello word")
    massage = Massage(text=text)

    title = Title("title")
    chat = Chat(title=title)

    chat.add_massage(massage)

    assert massage in chat.massage
