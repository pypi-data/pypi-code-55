"""
Learning to use this lib what sends windows notification
"""
from win10toast import ToastNotifier

toast = ToastNotifier()
toast.show_toast("Notification", "Lorem Ipsum", icon_path=None, duration=20)
