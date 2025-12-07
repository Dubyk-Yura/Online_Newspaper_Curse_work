from core.interfaces import IObserver
from typing import List


class NewsPublisher:
    """
    Class that handles notification broadcasts.
    """
    _instance = None

    def __init__(self):
        self._subscribers: List[IObserver] = []

    @staticmethod
    def get_instance():
        if NewsPublisher._instance is None:
            NewsPublisher._instance = NewsPublisher()
        return NewsPublisher._instance

    def subscribe(self, user: IObserver):
        if user not in self._subscribers:
            self._subscribers.append(user)

    def unsubscribe(self, user: IObserver):
        if user in self._subscribers:
            self._subscribers.remove(user)

    def notify_all(self, news_item_title: str):
        message = f"BREAKING: New content published: {news_item_title}"
        print("Starting Notification Broadcast")

        for subscriber in self._subscribers:
            subscriber.update(message)