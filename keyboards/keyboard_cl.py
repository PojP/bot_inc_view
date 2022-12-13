from tkinter.tix import Tree
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

none_kb=ReplyKeyboardRemove()
keyboard_cl_gender = ReplyKeyboardMarkup(
    keyboard=[
    [
        KeyboardButton(text="Male 👨"),
        KeyboardButton(text="Female 👩")
    ]
    ]
    ,resize_keyboard=True)
keyboard_cl_interests= ReplyKeyboardMarkup(
    keyboard=[
    [
        KeyboardButton(text="Flood 👋"),
        KeyboardButton(text="Investments 💰")
    ],
    [
        KeyboardButton(text="Meetings ❤️")
    ]
    ],resize_keyboard=True
)
keyboard_cl_registration=ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Registration")
        ]
    ]
    ,resize_keyboard=True)
keyboard_cl_start=ReplyKeyboardMarkup(keyboard=[[
    KeyboardButton(text="Search 🔎")],
    [
        KeyboardButton(text="Interests 💡"),
        KeyboardButton(text="Settings ⚙️"),
    ]
],resize_keyboard=True)

keyboard_cl_settings=ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Age 📈"),
        KeyboardButton(text="Gender 👤")
    ],
    [
        KeyboardButton(text="Cancel 🚫")
    ]
], resize_keyboard=True)

keyboard_cl_settings_gender=ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Male 👨"),
        KeyboardButton(text="Female 👩")
    ],
    [
        KeyboardButton(text="Cancel 🚫")
    ]
], resize_keyboard=True)

keyboard_cl_settings_age=ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Cancel 🚫")
    ]
], resize_keyboard=True)

keyboard_cl_edit_interests=ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Flood 👋"),
        KeyboardButton(text="Investments 💰")
    ],
    [
        KeyboardButton(text="Meetings ❤️")
    ],
    [
        KeyboardButton(text="Cancel 🚫")
    ]
], resize_keyboard=True)

keyboard_cl_chatting=ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Next ➡️"),
        KeyboardButton(text="Stop ❌")
    ]
], resize_keyboard=True)
share_button= InlineKeyboardMarkup(row_width=1,inline_keyboard=[
    [
        InlineKeyboardButton(text="Share contact data", callback_data="share_contact")
    ],
    [
        InlineKeyboardButton(text="Don't share contact data", callback_data="dont_share_contact")
    ]
])
