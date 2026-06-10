from plyer import notification

notification.notify(
    title="Medicine Reminder",
    message="Time to take your medicine!",
    timeout=10
)

print("Notification Sent")