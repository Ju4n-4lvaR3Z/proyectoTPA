import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *

import sys
import os

import time
import datetime as dt
from datetime import timedelta
from PIL import Image, ImageTk
import requests
import json
import calendar

from tkinter import ttk
from tkinter.font import Font


from babel import default_locale
from babel.dates import format_date, parse_date, get_day_names, get_month_names, get_date_format
from tkcalendar.tooltip import TooltipWrapper
import re

from PIL import Image, ImageTk

class DataManager:
    # constructor de la clase
    def __init__(self):
        self.data = {}
        self.colores = {}
        self.color_actual = self.colores.get("Actual", list(self.colores.values())[0] if self.colores else {"principal": "#151515", "subcolores": ["#59595B"], "texto": "white"})

    # funcion para abrir la base de datos del programa
    # def load_data(str) -> str 
    def load_data(self):
        try:
            with open("calendario_data.json", "r") as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = {}
            print("except")
    
    # funcion que guarda los datos en el diccionario
    # def save_data(int,str) -> int, str (guardados en el atributo (dicionario))
    def save_data(self,user, date, data):
        self.data.get("users")[user].get("data")[date] = data
        self.save_data_to_file()
    # guarda los datos del diccionario y los actualiza en la base de datos
    # def save_data_to_file(str) -> str (actualiza datos en la base de datos)
    def save_data_to_file(self):
        with open("calendario_data.json", "w") as file:
            json.dump(self.data, file)
    def get_user(self):
        return self.data.get("sesion").get("actual")[0]
    
    def get_color(self,user):
        color=(self.data.get("users")[int(user)].get("settings").get("color") if user!="N" else "Default")
        for i in range(0,len(self.data.get("colores"))):
            if self.data.get("colores")[i].get("color")==color:
                theme=self.data.get("colores")[i].get("color")
                break
        return self.data.get("colores")[i].get("settings")

    def cambiarColor(self,user,color):
        self.data.get("users")[int(user)].get("settings")["color"]=color
        self.save_data_to_file()
        self.restart()


    def logIn(self,i):
        self.data.get("sesion")["actual"] = f"{i}"
        self.save_data_to_file()
        self.restart()
    def register(self,user,password):
        self.data.get("users").append(
            {
            "id": len(self.data.get("users")),
            "name": f"{user}",
            "contrasena": f"{password}",
            "settings": "Black",
            "data": {
            }
            }
            )
        self.save_data_to_file()
    def restablecer(self,i,password):
        self.data.get("users")[i] = {
            "id": self.data.get("users")[i].get("id"),
            "name": self.data.get("users")[i].get("name"),
            "contrasena": f"{password}",
            "settings": self.data.get("users")[i].get("settings"),
            "data": self.data.get("users")[i].get("data")
            }
        self.save_data_to_file()
    def logOut(self):
        self.data.get("sesion")["actual"] = "N"
        self.save_data_to_file()
        self.restart()
    def restart(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)


# api de calendario, api no creado por nosotros
class Calendar(ttk.Frame):
    """Calendar widget."""
    date = calendar.datetime.date
    datetime = calendar.datetime.datetime
    timedelta = calendar.datetime.timedelta
    strptime = calendar.datetime.datetime.strptime
    strftime = calendar.datetime.datetime.strftime
    
    def __init__(self, master=None, **kw):
        self.arrows={1:ImageTk.PhotoImage(Image.open("img/up-arrow.png").resize((20,20), Image.LANCZOS)),
                     2:ImageTk.PhotoImage(Image.open("img/down-arrow.png").resize((20,20), Image.LANCZOS)),
                     11:ImageTk.PhotoImage(Image.open("img/up-arrow-lock.png").resize((20,20), Image.LANCZOS)),
                     22:ImageTk.PhotoImage(Image.open("img/down-arrow-lock.png").resize((20,20), Image.LANCZOS)),
                     3:ImageTk.PhotoImage(Image.open("img/left-arrow.png").resize((20,20), Image.LANCZOS)),
                     33:ImageTk.PhotoImage(Image.open("img/left-arrow-lock.png").resize((20,20), Image.LANCZOS)),
                     4:ImageTk.PhotoImage(Image.open("img/right-arrow.png").resize((20,20), Image.LANCZOS)),
                     44:ImageTk.PhotoImage(Image.open("img/right-arrow-lock.png").resize((20,20), Image.LANCZOS))}
        """
        Construct a Calendar with parent master.

        Standard Options
        ----------------

        cursor, font, borderwidth, state

        Widget-specific Options
        -----------------------

        year : int
            intinitially displayed year, default is current year.

        month : int
            initially displayed month, default is current month.

        day : int
            initially selected day, if month or year is given but not day, no initial selection, otherwise, default is today.

        firstweekday : "monday" (default) or "sunday"
            first day of the week

        weekenddays : list
            days to be displayed as week-end days given as a list of integers corresponding to the number of the day in the week
            (e.g. [6, 7] for the last two days of the week).

        mindate : None (default), datetime.date or datetime.datetime
            minimum allowed date

        maxdate : None (default), datetime.date or datetime.datetime
            maximum allowed date

        showweeknumbers : bool (default is True)
            whether to display week numbers.

        showothermonthdays : bool (default is True)
            whether to display the last days of the previous month and the first of the next month.

        locale : str
            locale to use, e.g. 'en_US'

        date_pattern : str
            date pattern used to format the date as a string. The default
            pattern used is babel's short date format in the Calendar's locale.

            A valid pattern is a combination of 'y', 'm' and 'd' separated by
            non letter characters to indicate how and in which order the
            year, month and day should be displayed.

                y: 'yy' for the last two digits of the year, any other number of 'y's for
                   the full year with an extra padding of zero if it has less
                   digits than the number of 'y's.
                m: 'm' for the month number without padding, 'mm' for a
                   two-digit month
                d: 'd' for the day of month number without padding, 'dd' for a
                   two-digit day

            Examples for datetime.date(2019, 7, 1):

                'y-mm-dd' → '2019-07-01'
                'm/d/yy' → '7/1/19'

        selectmode : "none" or "day" (default)
            whether the user can change the selected day with a mouse click.

        textvariable : StringVar
            connect the currently selected date to the variable.

        Style Options
        -------------

        background : str
            background color of calendar border and month/year name

        foreground : str
            foreground color of month/year name

        disabledbackground : str
            background color of calendar border and month/year name in disabled state

        disabledforeground : str
            foreground color of month/year name in disabled state

        bordercolor : str
            day border color

        headersbackground : str
            background color of day names and week numbers

        headersforeground : str
            foreground color of day names and week numbers

        selectbackground : str
            background color of selected day

        selectforeground : str
            foreground color of selected day

        disabledselectbackground : str
            background color of selected day in disabled state

        disabledselectforeground : str
            foreground color of selected day in disabled state

        normalbackground : str
            background color of normal week days

        normalforeground : str
            foreground color of normal week days

        weekendbackground : str
            background color of week-end days

        weekendforeground : str
            foreground color of week-end days

        othermonthforeground : str
            foreground color of normal week days belonging to the previous/next month

        othermonthbackground : str
            background color of normal week days belonging to the previous/next month

        othermonthweforeground : str
            foreground color of week-end days belonging to the previous/next month

        othermonthwebackground : str
            background color of week-end days belonging to the previous/next month

        disableddaybackground : str
            background color of days in disabled state

        disableddayforeground : str
            foreground color of days in disabled state

        Tooltip Options (for calevents)
        -------------------------------

        tooltipforeground : str
            tooltip text color

        tooltipbackground : str
            tooltip background color

        tooltipalpha : float
            tooltip opacity between 0 and 1

        tooltipdelay : int
            delay in ms before displaying the tooltip

        Virtual Event
        -------------

        A ``<<CalendarSelected>>`` event is generated each time the user
        selects a day with the mouse.

        A ``<<CalendarMonthChanged>>`` event is generated each time the user
        changes the displayed month.

        Calendar Events
        ---------------

        Special events (e.g. birthdays, ..) can be managed using the
        ``calevent_..`` methods. The way they are displayed in the calendar is
        determined with tags. An id is attributed to each event upon creation
        and can be used to edit the event (ev_id argument).


        """
        data_Manager=DataManager()
        data_Manager.load_data()
        user=data_Manager.get_user()
        self.color=data_Manager.get_color(user)
        curs = kw.pop("cursor", "")
        font = kw.pop("font", "Liberation\ Sans 9")
        classname = kw.pop('class_', "Calendar")
        name = kw.pop('name', None)
        ttk.Frame.__init__(self, master, class_=classname, cursor=curs, name=name)
        self._style_prefixe = str(self)
        ttk.Frame.configure(self, style='main.%s.TFrame' % self._style_prefixe)

        self._textvariable = kw.pop("textvariable", None)

        self._font = Font(self, font)
        prop = self._font.actual()
        prop["size"] += 1
        self._header_font = Font(self, **prop)

        # state
        state = kw.get('state', 'normal')

        try:
            bd = int(kw.pop('borderwidth', 2))
        except ValueError:
            raise ValueError("expected integer for the 'borderwidth' option.")

        firstweekday = kw.pop('firstweekday', 'monday')
        if firstweekday not in ["monday", "sunday"]:
            raise ValueError("'firstweekday' option should be 'monday' or 'sunday'.")
        self._cal = calendar.TextCalendar((firstweekday == 'sunday') * 6)

        weekenddays = kw.pop("weekenddays", None)
        if not weekenddays:
            l = list(self._cal.iterweekdays())
            weekenddays = [l.index(5) + 1, l.index(6) + 1]  # saturday and sunday
        self._check_weekenddays(weekenddays)

        # --- locale
        locale = kw.pop("locale", default_locale())
        if locale is None:
            locale = 'en'
        self._day_names = get_day_names('abbreviated', locale=locale)
        self._month_names = get_month_names('wide', locale=locale)
        date_pattern = self._get_date_pattern(kw.pop("date_pattern", "short"), locale)

        # --- date
        today = self.date.today()

        if self._textvariable is not None:
            # the variable overrides day, month and year keywords
            try:
                self._sel_date = parse_date(self._textvariable.get(), locale)
                month = self._sel_date.month
                year = self._sel_date.year
            except IndexError:
                self._sel_date = None
                self._textvariable.set('')
                month = kw.pop("month", today.month)
                year = kw.pop('year', today.year)
        else:
            if (("month" in kw) or ("year" in kw)) and ("day" not in kw):
                month = kw.pop("month", today.month)
                year = kw.pop('year', today.year)
                self._sel_date = None  # selected day
            else:
                day = kw.pop('day', today.day)
                month = kw.pop("month", today.month)
                year = kw.pop('year', today.year)
                try:
                    self._sel_date = self.date(year, month, day)  # selected day
                except ValueError:
                    self._sel_date = None

        self._date = self.date(year, month, 1)  # (year, month) displayed by the calendar

        # --- date limits
        maxdate = kw.pop('maxdate', None)
        mindate = kw.pop('mindate', None)
        if maxdate is not None:
            if isinstance(maxdate, self.datetime):
                maxdate = maxdate.date()
            elif not isinstance(maxdate, self.date):
                raise TypeError("expected %s for the 'maxdate' option." % self.date)
        if mindate is not None:
            if isinstance(mindate, self.datetime):
                mindate = mindate.date()
            elif not isinstance(mindate, self.date):
                raise TypeError("expected %s for the 'mindate' option." % self.date)
        if (mindate is not None) and (maxdate is not None) and (mindate > maxdate):
            raise ValueError("mindate should be smaller than maxdate.")

        # --- selectmode
        selectmode = kw.pop("selectmode", "day")
        if selectmode not in ("none", "day"):
            raise ValueError("'selectmode' option should be 'none' or 'day'.")
        # --- show week numbers
        showweeknumbers = kw.pop('showweeknumbers', True)

        # --- style
        self.style = ttk.Style(self)
        active_bg = self.style.lookup('TEntry', 'selectbackground', ('focus',))
        dis_active_bg = self.style.lookup('TEntry', 'selectbackground', ('disabled',))
        dis_bg = self.style.lookup('TLabel', 'background', ('disabled',))
        dis_fg = self.style.lookup('TLabel', 'foreground', ('disabled',))

        # --- properties
        options = ['cursor',
                   'font',
                   'borderwidth',
                   'state',
                   'selectmode',
                   'textvariable',
                   'locale',
                   'date_pattern',
                   'maxdate',
                   'mindate',
                   'showweeknumbers',
                   'showothermonthdays',
                   'firstweekday',
                   'weekenddays',
                   'selectbackground',
                   'selectforeground',
                   'disabledselectbackground',
                   'disabledselectforeground',
                   'normalbackground',
                   'normalforeground',
                   'background',
                   'foreground',
                   'disabledbackground',
                   'disabledforeground',
                   'bordercolor',
                   'othermonthforeground',
                   'othermonthbackground',
                   'othermonthweforeground',
                   'othermonthwebackground',
                   'weekendbackground',
                   'weekendforeground',
                   'headersbackground',
                   'headersforeground',
                   'disableddaybackground',
                   'disableddayforeground',
                   'tooltipforeground',
                   'tooltipbackground',
                   'tooltipalpha',
                   'tooltipdelay']

        keys = list(kw.keys())
        for option in keys:
            if option not in options:
                del(kw[option])

        self._properties = {"cursor": curs,
                            "font": font,
                            "borderwidth": bd,
                            "state": state,
                            "locale": locale,
                            "date_pattern": date_pattern,
                            "selectmode": selectmode,
                            'textvariable': self._textvariable,
                            'firstweekday': firstweekday,
                            'weekenddays': weekenddays,
                            'mindate': mindate,
                            'maxdate': maxdate,
                            'showweeknumbers': showweeknumbers,
                            'showothermonthdays': kw.pop('showothermonthdays', True),
                            'selectbackground': self.color.get("selectbackground"),
                            'selectforeground': self.color.get("white"),
                            'disabledselectbackground': dis_active_bg,
                            'disabledselectforeground': self.color.get("white"),
                            'normalbackground': self.color.get("background"),
                            'normalforeground': self.color.get("white"),
                            'background': self.color.get("background"),
                            'foreground': self.color.get("white"),
                            'disabledbackground': 'black',
                            'disabledforeground': self.color.get("disabledforeground"),
                            # 
                            'bordercolor': self.color.get("white"),
                            # 
                            'othermonthforeground': self.color.get("othermonthforeground"),
                            'othermonthbackground': 'black',
                            'othermonthweforeground': self.color.get("othermonthforeground"),
                            'othermonthwebackground': 'black',
                            'weekendbackground': self.color.get("weekendbackground"),
                            'weekendforeground': self.color.get("white"),
                            'headersbackground': 'gray70',
                            'headersforeground': 'black',
                            'disableddaybackground': dis_bg,
                            'disableddayforeground': dis_fg,
                            'tooltipforeground': 'gray90',
                            'tooltipbackground': 'black',
                            'tooltipalpha': 0.8,
                            'tooltipdelay': 2000}
        self._properties.update(kw)

        # --- calevents
        self.calevents = {}  # special events displayed in colors and with tooltips to show content
        self._calevent_dates = {}  # list of event ids for each date
        self._tags = {}  # tags to format event display
        self.tooltip_wrapper = TooltipWrapper(self,
                                              alpha=self._properties['tooltipalpha'],
                                              style=self._style_prefixe + '.tooltip.TLabel',
                                              delay=self._properties['tooltipdelay'])

        # --- init calendar
        # --- *-- header: month - year
        self._header = ttk.Frame(self, style='main.%s.TFrame' % self._style_prefixe)

        f_month = ttk.Frame(self._header,
                            style='main.%s.TFrame' % self._style_prefixe)
        self._l_month = ttk.Button(f_month,
                                   image=self.arrows[3],
                                   command=self._prev_month)
        self._header_month = ttk.Label(f_month, width=10, anchor='center',
                                       style='main.%s.TLabel' % self._style_prefixe, font=self._header_font)
        self._r_month = ttk.Button(f_month,
                                   image=self.arrows[4],
                                   command=self._next_month)
        self._l_month.pack(side='left', fill="y")
        self._header_month.pack(side='left', padx=4)
        self._r_month.pack(side='left', fill="y")

        f_year = ttk.Frame(self._header, style='main.%s.TFrame' % self._style_prefixe)
        self._l_year = ttk.Button(f_year, image=self.arrows[3],
                                  command=self._prev_year)
        self._header_year = ttk.Label(f_year, width=4, anchor='center',
                                      style='main.%s.TLabel' % self._style_prefixe, font=self._header_font)
        self._r_year = ttk.Button(f_year, image=self.arrows[4],
                                  command=self._next_year)
        self._l_year.pack(side='left', fill="y")
        self._header_year.pack(side='left', padx=4)
        self._r_year.pack(side='left', fill="y")

        f_month.pack(side='left', fill='x')
        f_year.pack(side='right')

        # --- *-- calendar
        self._cal_frame = ttk.Frame(self,
                                    style='cal.%s.TFrame' % self._style_prefixe)

        ttk.Label(self._cal_frame,
                  style='headers.%s.TLabel' % self._style_prefixe).grid(row=0,
                                                                        column=0,
                                                                        sticky="eswn")
        # week day names
        self._week_days = []
        for i, day in enumerate(self._cal.iterweekdays()):
            d = self._day_names[day % 7]
            self._cal_frame.columnconfigure(i + 1, weight=1)
            self._week_days.append(ttk.Label(self._cal_frame,
                                             font=self._font,
                                             style='headers.%s.TLabel' % self._style_prefixe,
                                             anchor="center",
                                             text=d, width=4))
            self._week_days[-1].grid(row=0, column=i + 1, sticky="ew", pady=(0, 1))
        self._week_nbs = []  # week numbers
        self._calendar = []  # days
        for i in range(1, 7):
            self._cal_frame.rowconfigure(i, weight=1)
            wlabel = ttk.Label(self._cal_frame, style='headers.%s.TLabel' % self._style_prefixe,
                               font=self._font, padding=2,
                               anchor="e", width=2)
            self._week_nbs.append(wlabel)
            wlabel.grid(row=i, column=0, sticky="esnw", padx=(0, 1))
            if not showweeknumbers:
                wlabel.grid_remove()
            self._calendar.append([])
            for j in range(1, 8):
                label = ttk.Label(self._cal_frame, style='normal.%s.TLabel' % self._style_prefixe,
                                  font=self._font, anchor="center")
                self._calendar[-1].append(label)
                label.grid(row=i, column=j, padx=(0, 1), pady=(0, 1), sticky="nsew")
                if selectmode == "day":
                    label.bind("<1>", self._on_click)

        # --- *-- pack main elements
        self._header.pack(fill="x", padx=2, pady=2)
        self._cal_frame.pack(fill="both", expand=True, padx=bd, pady=bd)

        self.config(state=state)

        # --- bindings
        self.bind('<<ThemeChanged>>', self._setup_style)

        self._setup_style()
        self._display_calendar()
        self._btns_date_range()
        self._check_sel_date()

        if self._textvariable is not None:
            try:
                self._textvariable_trace_id = self._textvariable.trace_add('write', self._textvariable_trace)
            except AttributeError:
                self._textvariable_trace_id = self._textvariable.trace('w', self._textvariable_trace)

    def __getitem__(self, key):
        """Return the resource value for a KEY given as string."""
        try:
            return self._properties[key]
        except KeyError:
            raise AttributeError("Calendar object has no attribute %s." % key)

    def __setitem__(self, key, value):
        if key not in self._properties:
            raise AttributeError("Calendar object has no attribute %s." % key)
        elif key == 'date_pattern':
            date_pattern = self._get_date_pattern(value)
            self._properties[key] = date_pattern
        else:
            if key == "selectmode":
                if value == "none":
                    for week in self._calendar:
                        for day in week:
                            day.unbind("<1>")
                elif value == "day":
                    for week in self._calendar:
                        for day in week:
                            day.bind("<1>", self._on_click)
                else:
                    raise ValueError("'selectmode' option should be 'none' or 'day'.")
            elif key == "locale":
                self._day_names = get_day_names('abbreviated', locale=value)
                self._month_names = get_month_names('wide', locale=value)
                self._properties['date_pattern'] = self._get_date_pattern("short", value)
                for i, l in enumerate(self._week_days):
                    l.configure(text=self._day_names[i])
                self._header_month.configure(text=self._month_names[self._date.month].title())
            elif key == 'textvariable':
                try:
                    if self._textvariable is not None:
                        self._textvariable.trace_remove('write', self._textvariable_trace_id)
                    if value is not None:
                        self._textvariable_trace_id = value.trace_add('write', self._textvariable_trace)
                except AttributeError:
                    if self._textvariable is not None:
                        self._textvariable.trace_vdelete('w', self._textvariable_trace_id)
                    if value is not None:
                        value.trace('w', self._textvariable_trace)
                self._textvariable = value
                value.set(value.get())
            elif key == 'showweeknumbers':
                if value:
                    for wlabel in self._week_nbs:
                        wlabel.grid()
                else:
                    for wlabel in self._week_nbs:
                        wlabel.grid_remove()
            elif key == 'firstweekday':
                if value not in ["monday", "sunday"]:
                    raise ValueError("'firstweekday' option should be 'monday' or 'sunday'.")
                self._cal.firstweekday = (value == 'sunday') * 6
                for label, day in zip(self._week_days, self._cal.iterweekdays()):
                    label.configure(text=self._day_names[day % 7])
            elif key == 'weekenddays':
                self._check_weekenddays(value)
            elif key == 'borderwidth':
                try:
                    bd = int(value)
                    self._cal_frame.pack_configure(padx=bd, pady=bd)
                except ValueError:
                    raise ValueError('expected integer for the borderwidth option.')
            elif key == 'state':
                if value not in ['normal', 'disabled']:
                    raise ValueError("bad state '%s': must be disabled or normal" % value)
                else:
                    state = '!' * (value == 'normal') + 'disabled'
                    self.state((state,))
                    self._header.state((state,))
                    for child in self._header.children.values():
                        child.state((state,))
                    self._header_month.state((state,))
                    self._header_year.state((state,))
                    self._l_year.state((state,))
                    self._r_year.state((state,))
                    self._l_month.state((state,))
                    self._r_month.state((state,))
                    for child in self._cal_frame.children.values():
                        child.state((state,))
            elif key == "maxdate":
                if value is not None:
                    if isinstance(value, self.datetime):
                        value = value.date()
                    elif not isinstance(value, self.date):
                        raise TypeError("expected %s for the 'maxdate' option." % self.date)

                    mindate = self['mindate']
                    if mindate is not None and mindate > value:
                        self._properties['mindate'] = value
                        self._date = self._date.replace(year=value.year, month=value.month)
                    elif self._date > value:
                        self._date = self._date.replace(year=value.year, month=value.month)
                self._r_month.state(['!disabled'])
                self._r_year.state(['!disabled'])
                self._l_month.state(['!disabled'])
                self._l_year.state(['!disabled'])
            elif key == "mindate":
                if value is not None:
                    if isinstance(value, self.datetime):
                        value = value.date()
                    elif not isinstance(value, self.date):
                        raise TypeError("expected %s for the 'mindate' option." % self.date)
                    maxdate = self['maxdate']
                    if maxdate is not None and maxdate < value:
                        self._properties['maxdate'] = value
                        self._date = self._date.replace(year=value.year, month=value.month)
                    elif self._date < value:
                        self._date = self._date.replace(year=value.year, month=value.month)
                self._r_month.state(['!disabled'])
                self._r_year.state(['!disabled'])
                self._l_month.state(['!disabled'])
                self._l_year.state(['!disabled'])
            elif key == "font":
                font = Font(self, value)
                prop = font.actual()
                self._font.configure(**prop)
                prop["size"] += 1
                self._header_font.configure(**prop)
                size = max(prop["size"], 10)
                self.style.configure('R.%s.TButton' % self._style_prefixe, arrowsize=size)
                self.style.configure('L.%s.TButton' % self._style_prefixe, arrowsize=size)
            elif key == "normalbackground":
                self.style.configure('cal.%s.TFrame' % self._style_prefixe, background=value)
                self.style.configure('normal.%s.TLabel' % self._style_prefixe, background=value)
                self.style.configure('normal_om.%s.TLabel' % self._style_prefixe, background=value)
            elif key == "normalforeground":
                self.style.configure('normal.%s.TLabel' % self._style_prefixe, foreground=value)
            elif key == "bordercolor":
                self.style.configure('cal.%s.TFrame' % self._style_prefixe, background=value)
            elif key == "othermonthforeground":
                self.style.configure('normal_om.%s.TLabel' % self._style_prefixe, foreground=value)
            elif key == "othermonthbackground":
                self.style.configure('normal_om.%s.TLabel' % self._style_prefixe, background=value)
            elif key == "othermonthweforeground":
                self.style.configure('we_om.%s.TLabel' % self._style_prefixe, foreground=value)
            elif key == "othermonthwebackground":
                self.style.configure('we_om.%s.TLabel' % self._style_prefixe, background=value)
            elif key == "selectbackground":
                self.style.configure('sel.%s.TLabel' % self._style_prefixe, background=value)
            elif key == "selectforeground":
                self.style.configure('sel.%s.TLabel' % self._style_prefixe, foreground=value)
            elif key == "disabledselectbackground":
                self.style.map('sel.%s.TLabel' % self._style_prefixe, background=[('disabled', value)])
            elif key == "disabledselectforeground":
                self.style.map('sel.%s.TLabel' % self._style_prefixe, foreground=[('disabled', value)])
            elif key == "disableddaybackground":
                self.style.map('%s.TLabel' % self._style_prefixe, background=[('disabled', value)])
            elif key == "disableddayforeground":
                self.style.map('%s.TLabel' % self._style_prefixe, foreground=[('disabled', value)])
            elif key == "weekendbackground":
                self.style.configure('we.%s.TLabel' % self._style_prefixe, background=value)
                self.style.configure('we_om.%s.TLabel' % self._style_prefixe, background=value)
            elif key == "weekendforeground":
                self.style.configure('we.%s.TLabel' % self._style_prefixe, foreground=value)
            elif key == "headersbackground":
                self.style.configure('headers.%s.TLabel' % self._style_prefixe, background=value)
            elif key == "headersforeground":
                self.style.configure('headers.%s.TLabel' % self._style_prefixe, foreground=value)
            elif key == "background":
                self.style.configure('main.%s.TFrame' % self._style_prefixe, background=value)
                self.style.configure('main.%s.TLabel' % self._style_prefixe, background=value)
                self.style.configure('R.%s.TButton' % self._style_prefixe, background=value,
                                     bordercolor=value,
                                     lightcolor=value, darkcolor=value)
                self.style.configure('L.%s.TButton' % self._style_prefixe, background=value,
                                     bordercolor=value,
                                     lightcolor=value, darkcolor=value)
            elif key == "foreground":
                self.style.configure('R.%s.TButton' % self._style_prefixe, arrowcolor=value)
                self.style.configure('L.%s.TButton' % self._style_prefixe, arrowcolor=value)
                self.style.configure('main.%s.TLabel' % self._style_prefixe, foreground=value)
            elif key == "disabledbackground":
                self.style.map('%s.TButton' % self._style_prefixe,
                               background=[('active', '!disabled', self.style.lookup('TEntry', 'selectbackground', ('focus',))),
                                           ('disabled', value)],)
                self.style.map('main.%s.TFrame' % self._style_prefixe,
                               background=[('disabled', value)])
                self.style.map('main.%s.TLabel' % self._style_prefixe,
                               background=[('disabled', value)])
            elif key == "disabledforeground":
                self.style.map('%s.TButton' % self._style_prefixe,
                               arrowcolor=[('disabled', value)])
                self.style.map('main.%s.TLabel' % self._style_prefixe,
                               foreground=[('disabled', value)])
            elif key == "cursor":
                ttk.Frame.configure(self, cursor=value)
            elif key == "tooltipbackground":
                self.style.configure('%s.tooltip.TLabel' % self._style_prefixe,
                                     background=value)
            elif key == "tooltipforeground":
                self.style.configure('%s.tooltip.TLabel' % self._style_prefixe,
                                     foreground=value)
            elif key == "tooltipalpha":
                self.tooltip_wrapper.configure(alpha=value)
            elif key == "tooltipdelay":
                self.tooltip_wrapper.configure(delay=value)
            self._properties[key] = value
            if key in ['showothermonthdays', 'firstweekday', 'weekenddays',
                       'maxdate', 'mindate']:
                self._display_calendar()
                self._check_sel_date()
                self._btns_date_range()

    @staticmethod
    def _check_weekenddays(weekenddays):
        try:
            if len(weekenddays) != 2:
                raise ValueError("weekenddays should be a list of two days.")
            else:
                for d in weekenddays:
                    if d not in range(1, 8):
                        raise ValueError("weekenddays should contain integers between 1 and 7.")
        except TypeError:
            raise TypeError("weekenddays should be a list of two days.")

    def _textvariable_trace(self, *args):
        """Connect StringVar value with selected date."""
        if self._properties.get("selectmode") == "day":
            date = self._textvariable.get()
            if not date:
                self._remove_selection()
                self._sel_date = None
            else:
                try:
                    self._sel_date = self.parse_date(date)
                except Exception:
                    if self._sel_date is None:
                        self._textvariable.set('')
                    else:
                        self._textvariable.set(self.format_date(self._sel_date))
                    raise ValueError("%r is not a valid date." % date)
                else:
                    self._date = self._sel_date.replace(day=1)
                    self._display_calendar()
                    self._display_selection()

    def _setup_style(self, event=None):
        """Configure style."""
        self.style.layout('L.%s.TButton' % self._style_prefixe,
                          [('Button.focus',
                            {'children': [('Button.leftarrow', None)]})])
        self.style.layout('R.%s.TButton' % self._style_prefixe,
                          [('Button.focus',
                            {'children': [('Button.rightarrow', None)]})])
        active_bg = self.style.lookup('TEntry', 'selectbackground', ('focus',))

        sel_bg = self._properties.get('selectbackground')
        sel_fg = self._properties.get('selectforeground')
        dis_sel_bg = self._properties.get('disabledselectbackground')
        dis_sel_fg = self._properties.get('disabledselectforeground')
        dis_day_bg = self._properties.get('disableddaybackground')
        dis_day_fg = self._properties.get('disableddayforeground')
        cal_bg = self._properties.get('normalbackground')
        cal_fg = self._properties.get('normalforeground')
        hd_bg = self._properties.get("headersbackground")
        hd_fg = self._properties.get("headersforeground")
        bg = self._properties.get('background')
        fg = self._properties.get('foreground')
        dis_bg = self._properties.get('disabledbackground')
        dis_fg = self._properties.get('disabledforeground')
        bc = self._properties.get('bordercolor')
        om_fg = self._properties.get('othermonthforeground')
        om_bg = self._properties.get('othermonthbackground')
        omwe_fg = self._properties.get('othermonthweforeground')
        omwe_bg = self._properties.get('othermonthwebackground')
        we_bg = self._properties.get('weekendbackground')
        we_fg = self._properties.get('weekendforeground')

        self.style.configure('main.%s.TFrame' % self._style_prefixe, background=bg)
        self.style.configure('cal.%s.TFrame' % self._style_prefixe, background=bc)
        self.style.configure('main.%s.TLabel' % self._style_prefixe, background=bg, foreground=fg)
        self.style.configure('headers.%s.TLabel' % self._style_prefixe, background=hd_bg,
                             foreground=hd_fg)
        self.style.configure('normal.%s.TLabel' % self._style_prefixe, background=cal_bg,
                             foreground=cal_fg)
        self.style.configure('normal_om.%s.TLabel' % self._style_prefixe, background=om_bg,
                             foreground=om_fg)
        self.style.configure('we_om.%s.TLabel' % self._style_prefixe, background=omwe_bg,
                             foreground=omwe_fg)
        self.style.configure('sel.%s.TLabel' % self._style_prefixe, background=sel_bg,
                             foreground=sel_fg)
        self.style.configure('we.%s.TLabel' % self._style_prefixe, background=we_bg,
                             foreground=we_fg)
        size = max(self._header_font.actual()["size"], 10)
        self.style.configure('%s.TButton' % self._style_prefixe, background=bg,
                             arrowcolor=fg, arrowsize=size, bordercolor=bg,
                             relief="flat", lightcolor=bg, darkcolor=bg)
        self.style.configure('%s.tooltip.TLabel' % self._style_prefixe,
                             background=self._properties['tooltipbackground'],
                             foreground=self._properties['tooltipforeground'])

        self.style.map('%s.TButton' % self._style_prefixe,
                       background=[('active', '!disabled', active_bg), ('disabled', dis_bg)],
                       bordercolor=[('active', active_bg)],
                       relief=[('active', 'flat')],
                       arrowcolor=[('disabled', dis_fg)],
                       darkcolor=[('active', active_bg)],
                       lightcolor=[('active', active_bg)])
        self.style.map('main.%s.TFrame' % self._style_prefixe,
                       background=[('disabled', dis_bg)])
        self.style.map('main.%s.TLabel' % self._style_prefixe,
                       background=[('disabled', dis_bg)],
                       foreground=[('disabled', dis_fg)])
        self.style.map('sel.%s.TLabel' % self._style_prefixe,
                       background=[('disabled', dis_sel_bg)],
                       foreground=[('disabled', dis_sel_fg)])
        self.style.map(self._style_prefixe + '.TLabel',
                       background=[('disabled', dis_day_bg)],
                       foreground=[('disabled', dis_day_fg)])

    # --- display
    def _display_calendar(self):
        """Display the days of the current month (the one in self._date)."""
        year, month = self._date.year, self._date.month

        # update header text (Month, Year)
        header = self._month_names[month]
        self._header_month.configure(text=header.title())
        self._header_year.configure(text=str(year))

        # remove previous tooltips
        self.tooltip_wrapper.remove_all()

        # update calendar shown dates
        if self['showothermonthdays']:
            self._display_days_with_othermonthdays()
        else:
            self._display_days_without_othermonthdays()

        self._display_selection()
        maxdate = self['maxdate']
        mindate = self['mindate']

        if maxdate is not None:
            mi, mj = self._get_day_coords(maxdate)
            if mi is not None:
                for j in range(mj + 1, 7):
                    self._calendar[mi][j].state(['disabled'])
                for i in range(mi + 1, 6):
                    for j in range(7):
                        self._calendar[i][j].state(['disabled'])

        if mindate is not None:
            mi, mj = self._get_day_coords(mindate)
            if mi is not None:
                for j in range(mj):
                    self._calendar[mi][j].state(['disabled'])
                for i in range(mi):
                    for j in range(7):
                        self._calendar[i][j].state(['disabled'])

    def _display_days_without_othermonthdays(self):
        year, month = self._date.year, self._date.month

        cal = self._cal.monthdays2calendar(year, month)
        while len(cal) < 6:
            cal.append([(0, i) for i in range(7)])

        week_days = {i: 'normal.%s.TLabel' % self._style_prefixe for i in range(7)}  # style names depending on the type of day
        week_days[self['weekenddays'][0] - 1] = 'we.%s.TLabel' % self._style_prefixe
        week_days[self['weekenddays'][1] - 1] = 'we.%s.TLabel' % self._style_prefixe
        _, week_nb, d = self._date.isocalendar()
        if d == 7 and self['firstweekday'] == 'sunday':
            week_nb += 1
        modulo = max(week_nb, 52)
        for i_week in range(6):
            if i_week == 0 or cal[i_week][0][0]:
                self._week_nbs[i_week].configure(text=str((week_nb + i_week - 1) % modulo + 1))
            else:
                self._week_nbs[i_week].configure(text='')
            for i_day in range(7):
                day_number, week_day = cal[i_week][i_day]
                style = week_days[i_day]
                label = self._calendar[i_week][i_day]
                label.state(['!disabled'])
                if day_number:
                    txt = str(day_number)
                    label.configure(text=txt, style=style)
                    date = self.date(year, month, day_number)
                    if date in self._calevent_dates:
                        ev_ids = self._calevent_dates[date]
                        i = len(ev_ids) - 1
                        while i >= 0 and not self.calevents[ev_ids[i]]['tags']:
                            i -= 1
                        if i >= 0:
                            tag = self.calevents[ev_ids[i]]['tags'][-1]
                            label.configure(style='tag_%s.%s.TLabel' % (tag, self._style_prefixe))
                        text = '\n'.join(['➢ {}'.format(self.calevents[ev]['text']) for ev in ev_ids])
                        self.tooltip_wrapper.add_tooltip(label, text)
                else:
                    label.configure(text='', style=style)

    def _display_days_with_othermonthdays(self):
        year, month = self._date.year, self._date.month

        cal = self._cal.monthdatescalendar(year, month)

        next_m = month + 1
        y = year
        if next_m == 13:
            next_m = 1
            y += 1
        if len(cal) < 6:
            if cal[-1][-1].month == month:
                i = 0
            else:
                i = 1
            cal.append(self._cal.monthdatescalendar(y, next_m)[i])
            if len(cal) < 6:
                cal.append(self._cal.monthdatescalendar(y, next_m)[i + 1])

        week_days = {i: 'normal' for i in range(7)}  # style names depending on the type of day
        week_days[self['weekenddays'][0] - 1] = 'we'
        week_days[self['weekenddays'][1] - 1] = 'we'
        prev_m = (month - 2) % 12 + 1
        months = {month: '.%s.TLabel' % self._style_prefixe,
                  next_m: '_om.%s.TLabel' % self._style_prefixe,
                  prev_m: '_om.%s.TLabel' % self._style_prefixe}

        week_nb = cal[0][1].isocalendar()[1]
        modulo = max(week_nb, 52)
        for i_week in range(6):
            self._week_nbs[i_week].configure(text=str((week_nb + i_week - 1) % modulo + 1))
            for i_day in range(7):
                style = week_days[i_day] + months[cal[i_week][i_day].month]
                label = self._calendar[i_week][i_day]
                label.state(['!disabled'])
                txt = str(cal[i_week][i_day].day)
                label.configure(text=txt, style=style)
                if cal[i_week][i_day] in self._calevent_dates:
                    date = cal[i_week][i_day]
                    ev_ids = self._calevent_dates[date]
                    i = len(ev_ids) - 1
                    while i >= 0 and not self.calevents[ev_ids[i]]['tags']:
                        i -= 1
                    if i >= 0:
                        tag = self.calevents[ev_ids[i]]['tags'][-1]
                        label.configure(style='tag_%s.%s.TLabel' % (tag, self._style_prefixe))
                    text = '\n'.join(['➢ {}'.format(self.calevents[ev]['text']) for ev in ev_ids])
                    self.tooltip_wrapper.add_tooltip(label, text)

    def _get_day_coords(self, date):
        y1, y2 = date.year, self._date.year
        m1, m2 = date.month, self._date.month
        if y1 == y2 or (y1 - y2 == 1 and m1 == 1 and m2 == 12) or (y2 - y1 == 1 and m2 == 1 and m1 == 12):
            _, w, d = date.isocalendar()
            _, wn, dn = self._date.isocalendar()
            if self['firstweekday'] == 'sunday':
                d %= 7
                if d == 0:
                    w += 1
                if dn == 7:
                    wn += 1
            else:
                d -= 1
            w -= wn
            w %= max(52, wn)
            if 0 <= w < 6:
                return w, d
            else:
                return None, None
        else:
            return None, None

    def _display_selection(self):
        """Highlight selected day."""
        if self._sel_date is not None:
            w, d = self._get_day_coords(self._sel_date)
            if w is not None:
                label = self._calendar[w][d]
                if label.cget('text'):
                    label.configure(style='sel.%s.TLabel' % self._style_prefixe)

    def _reset_day(self, date):
        """Restore usual week day colors."""
        month = date.month
        w, d = self._get_day_coords(date)
        if w is not None:
            self.tooltip_wrapper.remove_tooltip(self._calendar[w][d])
            week_end = [0, 6] if self['firstweekday'] == 'sunday' else [5, 6]
            if month == date.month:
                if d in week_end:
                    self._calendar[w][d].configure(style='we.%s.TLabel' % self._style_prefixe)
                else:
                    self._calendar[w][d].configure(style='normal.%s.TLabel' % self._style_prefixe)
            else:
                if d in week_end:
                    self._calendar[w][d].configure(style='we_om.%s.TLabel' % self._style_prefixe)

                else:
                    self._calendar[w][d].configure(style='normal_om.%s.TLabel' % self._style_prefixe)

    def _remove_selection(self):
        """Remove highlight of selected day."""
        if self._sel_date is not None:
            if self._sel_date in self._calevent_dates:
                self._show_event(self._sel_date)
            else:
                w, d = self._get_day_coords(self._sel_date)
                if w is not None:
                    week_end = [0, 6] if self['firstweekday'] == 'sunday' else [5, 6]
                    if self._sel_date.month == self._date.month:
                        if d in week_end:
                            self._calendar[w][d].configure(style='we.%s.TLabel' % self._style_prefixe)
                        else:
                            self._calendar[w][d].configure(style='normal.%s.TLabel' % self._style_prefixe)
                    else:
                        if d in week_end:
                            self._calendar[w][d].configure(style='we_om.%s.TLabel' % self._style_prefixe)
                        else:
                            self._calendar[w][d].configure(style='normal_om.%s.TLabel' % self._style_prefixe)

    def _show_event(self, date):
        """Display events on date if visible."""
        w, d = self._get_day_coords(date)
        if w is not None:
            label = self._calendar[w][d]
            if not label.cget('text'):
                # this is an other month's day and showothermonth is False
                return
            ev_ids = self._calevent_dates[date]
            i = len(ev_ids) - 1
            while i >= 0 and not self.calevents[ev_ids[i]]['tags']:
                i -= 1
            if i >= 0:
                tag = self.calevents[ev_ids[i]]['tags'][-1]
                label.configure(style='tag_%s.%s.TLabel' % (tag, self._style_prefixe))
            text = '\n'.join(['➢ {}'.format(self.calevents[ev]['text']) for ev in ev_ids])
            self.tooltip_wrapper.remove_tooltip(label)
            self.tooltip_wrapper.add_tooltip(label, text)

    def check_date_range(self, date):
        """
        Ensure that date is in the allowed date range.

            date : datetime.date or datetime.datetime

        Return date if date is in the allowed date range, return the closest
        bound otherwise.
        """
        maxdate = self['maxdate']
        mindate = self['mindate']
        if maxdate is not None and date > maxdate:
            return maxdate
        elif mindate is not None and date < mindate:
            return mindate
        else:
            return date

    def _check_sel_date(self):

        if self._sel_date is not None:
            maxdate = self['maxdate']
            mindate = self['mindate']
            if maxdate is not None and self._sel_date > maxdate:
                self._sel_date = maxdate
                self._display_selection()
            elif mindate is not None and self._sel_date < mindate:
                self._sel_date = mindate
                self._display_selection()

    def _btns_date_range(self):
        """Disable/enable buttons depending on allowed date range."""
        maxdate = self['maxdate']
        mindate = self['mindate']

        if maxdate is not None:
            max_year, max_month = maxdate.year, maxdate.month
            if self._date > maxdate:
                self._date = self._date.replace(year=max_year, month=max_month)
                self._display_calendar()

            dy = max_year - self._date.year
            if dy == 0:
                self._r_year.state(['disabled'])
                if self._date.month == max_month:
                    self._r_month.state(['disabled'])
                else:
                    self._r_month.state(['!disabled'])
            elif dy == 1:
                if self._date.month > max_month:
                    self._r_year.state(['disabled'])
                else:
                    self._r_year.state(['!disabled'])
                    self._r_month.state(['!disabled'])
            else:  # dy > 1
                self._r_year.state(['!disabled'])
                self._r_month.state(['!disabled'])

        if mindate is not None:
            min_year, min_month = mindate.year, mindate.month
            if self._date < mindate:
                self._date = self._date.replace(year=min_year, month=min_month)
                self._display_calendar()

            dy = self._date.year - min_year
            if dy == 0:
                self._l_year.state(['disabled'])
                if self._date.month == min_month:
                    self._l_month.state(['disabled'])
                else:
                    self._l_month.state(['!disabled'])
            elif dy == 1:
                if self._date.month >= min_month:
                    self._l_year.state(['!disabled'])
                    self._l_month.state(['!disabled'])
                else:
                    self._l_year.state(['disabled'])
            else:  # dy > 1
                self._l_year.state(['!disabled'])
                self._l_month.state(['!disabled'])

    # --- callbacks
    def _next_month(self):
        """Display the next month."""
        year, month = self._date.year, self._date.month
        self._date = self._date + \
            self.timedelta(days=calendar.monthrange(year, month)[1])
        self._display_calendar()
        self.event_generate('<<CalendarMonthChanged>>')
        self._btns_date_range()

    def _prev_month(self):
        """Display the previous month."""
        self._date = self._date - self.timedelta(days=1)
        self._date = self._date.replace(day=1)
        self._display_calendar()
        self.event_generate('<<CalendarMonthChanged>>')
        self._btns_date_range()

    def _next_year(self):
        """Display the next year."""
        year = self._date.year
        self._date = self._date.replace(year=year + 1)
        self._display_calendar()
        self.event_generate('<<CalendarMonthChanged>>')
        self._btns_date_range()

    def _prev_year(self):
        """Display the previous year."""
        year = self._date.year
        self._date = self._date.replace(year=year - 1)
        self._display_calendar()
        self.event_generate('<<CalendarMonthChanged>>')
        self._btns_date_range()

    # --- bindings
    def _on_click(self, event):
        """Select the day on which the user clicked."""
        if self._properties['state'] == 'normal':
            label = event.widget
            if "disabled" not in label.state():
                day = label.cget("text")
                style = label.cget("style")
                if style in ['normal_om.%s.TLabel' % self._style_prefixe, 'we_om.%s.TLabel' % self._style_prefixe]:
                    if label in self._calendar[0]:
                        self._prev_month()
                    else:
                        self._next_month()
                if day:
                    day = int(day)
                    year, month = self._date.year, self._date.month
                    self._remove_selection()
                    self._sel_date = self.date(year, month, day)
                    self._display_selection()
                    if self._textvariable is not None:
                        self._textvariable.set(self.format_date(self._sel_date))
                    self.event_generate("<<CalendarSelected>>")

    def _get_date_pattern(self, date_pattern, locale=None):
        """
        Return the babel pattern corresponding to date_pattern.

        If date_pattern is "short", return the pattern correpsonding to the
        locale, else return date_pattern if valid.

        A valid pattern is a sequence of y, m and d
        separated by non letter characters, e.g. yyyy-mm-dd or d/m/yy
        """
        if locale is None:
            locale = self._properties["locale"]
        if date_pattern == "short":
            return get_date_format("short", locale).pattern
        pattern = date_pattern.lower()
        ymd = r"^y+[^a-zA-Z]*m{1,2}[^a-z]*d{1,2}[^mdy]*$"
        mdy = r"^m{1,2}[^a-zA-Z]*d{1,2}[^a-z]*y+[^mdy]*$"
        dmy = r"^d{1,2}[^a-zA-Z]*m{1,2}[^a-z]*y+[^mdy]*$"
        res = ((re.search(ymd, pattern) is not None)
               or (re.search(mdy, pattern) is not None)
               or (re.search(dmy, pattern) is not None))
        if res:
            return pattern.replace('m', 'M')
        raise ValueError("%r is not a valid date pattern" % date_pattern)

    def format_date(self, date=None):
        """Convert date (datetime.date) to a string in the locale."""
        return format_date(date, self._properties['date_pattern'], self._properties['locale'])

    def parse_date(self, date):
        """Parse string date in the locale format and return the corresponding datetime.date."""
        date_format = self._properties['date_pattern'].lower()
        year_idx = date_format.index('y')
        month_idx = date_format.index('m')
        day_idx = date_format.index('d')

        indexes = [(year_idx, 'Y'), (month_idx, 'M'), (day_idx, 'D')]
        indexes.sort()
        indexes = dict([(item[1], idx) for idx, item in enumerate(indexes)])

        numbers = re.findall(r'(\d+)', date)
        year = numbers[indexes['Y']]
        if len(year) == 2:
            year = 2000 + int(year)
        else:
            year = int(year)
        month = int(numbers[indexes['M']])
        day = int(numbers[indexes['D']])
        if month > 12:
            month, day = day, month
        return self.date(year, month, day)

    def see(self, date):
        """
        Display the month in which date is.


            date : datetime.date or datetime.datetime
                date to be made visible
        """
        if isinstance(date, self.datetime):
            date = date.date()
        elif not isinstance(date, self.date):
            raise TypeError("expected %s for the 'date' argument." % self.date)

        self._date = self._date.replace(month=date.month, year=date.year)
        self._display_calendar()
        self._btns_date_range()

    # --- selection handling
    def selection_clear(self):
        """Clear the selection."""
        self._remove_selection()
        self._sel_date = None
        if self._textvariable is not None:
            self._textvariable.set('')

    def selection_get(self):
        """
        Return currently selected date (datetime.date instance).

        Always return None if selectmode == "none".
        """

        if self._properties.get("selectmode") == "day":
            return self._sel_date
        else:
            return None

    def selection_set(self, date):
        """
        Set the selection to date.

            date : datetime.date, datetime.datetime or str
                    date to be made visible. If given as a string, it should be
                    in the format corresponding to the calendar locale.

        Do nothing if selectmode == "none".
        """
        if self._properties.get("selectmode") == "day" and self._properties['state'] == 'normal':
            if date is None:
                self.selection_clear()
            else:
                if isinstance(date, self.datetime):
                    self._sel_date = date.date()
                elif isinstance(date, self.date):
                    self._sel_date = date
                else:
                    try:
                        self._sel_date = self.parse_date(date)
                    except Exception as e:
                        raise ValueError("%r is not a valid date." % date)
                if self['mindate'] is not None and self._sel_date < self['mindate']:
                    self._sel_date = self['mindate']
                elif self['maxdate'] is not None and self._sel_date > self['maxdate']:
                    self._sel_date = self['maxdate']
                if self._textvariable is not None:
                    self._textvariable.set(self.format_date(self._sel_date))

                self._date = self._sel_date.replace(day=1)
                self._display_calendar()
                self._display_selection()
                self._btns_date_range()

    def get_displayed_month(self):
        """Return the currently displayed month in the form of a (month, year) tuple."""
        return self._date.month, self._date.year

    def get_date(self):
        """Return selected date as string."""
        if self._sel_date is not None:
            return self.format_date(self._sel_date)
        else:
            return ""

    # --- events
    def calevent_create(self, date, text, tags=[]):
        """
        Add new event in calendar and return event id.

        Options:

            date : datetime.date or datetime.datetime
                event date

            text : str
                text to put in the tooltip associated to date.

            tags : list
                list of tags to apply to the event. The last tag determines
                the way the event is displayed. If there are several events on
                the same day, the lowest one (on the tooltip list) which has
                tags determines the colors of the day.
        """
        if isinstance(date, Calendar.datetime):
            date = date.date()
        if not isinstance(date, Calendar.date):
            raise TypeError("date option should be a %s instance" % (Calendar.date))
        if self.calevents:
            ev_id = max(self.calevents) + 1
        else:
            ev_id = 0
        if isinstance(tags, str):
            tags_ = [tags]
        else:
            tags_ = list(tags)
        self.calevents[ev_id] = {'date': date, 'text': text, 'tags': tags_}
        for tag in tags_:
            if tag not in self._tags:
                self._tag_initialize(tag)
        if date not in self._calevent_dates:
            self._calevent_dates[date] = [ev_id]
        else:
            self._calevent_dates[date].append(ev_id)
        self._show_event(date)
        return ev_id

    def _calevent_remove(self, ev_id):
        """Remove event ev_id."""
        try:
            date = self.calevents[ev_id]['date']
        except KeyError:
            ValueError("event %s does not exists" % ev_id)
        else:
            del self.calevents[ev_id]
            self._calevent_dates[date].remove(ev_id)
            if not self._calevent_dates[date]:
                del self._calevent_dates[date]
                self._reset_day(date)
            else:
                self._show_event(date)

    def calevent_remove(self, *ev_ids, **kw):
        """
        Remove events from calendar.

        Arguments: event ids to remove or 'all' to remove them all.

        Keyword arguments: tag, date.

            They are taken into account only if no id is given. Remove all events
            with given tag on given date. If only date is given, remove all events
            on date and if only tag is given, remove all events with tag.
        """
        if ev_ids:
            if 'all' in ev_ids:
                ev_ids = self.get_calevents()
            for ev_id in ev_ids:
                self._calevent_remove(ev_id)
        else:
            date = kw.get('date')
            tag = kw.get('tag')
            evs = self.get_calevents(tag=tag, date=date)
            for ev_id in evs:
                self._calevent_remove(ev_id)

    def calevent_cget(self, ev_id, option):
        """Return value of given option for the event ev_id."""
        try:
            ev = self.calevents[ev_id]
        except KeyError:
            raise ValueError("event %s does not exists" % ev_id)
        else:
            try:
                return ev[option]
            except KeyError:
                raise ValueError('unknown option "%s"' % option)

    def calevent_configure(self, ev_id, **kw):
        """
        Configure the event ev_id.

        Keyword options: date, text, tags (see calevent_create options).
        """
        try:
            ev = self.calevents[ev_id]
        except KeyError:
            raise ValueError("event %s does not exists" % ev_id)
        else:
            text = kw.pop('text', None)
            tags = kw.pop('tags', None)
            date = kw.pop('date', None)
            if kw:
                raise KeyError('Invalid keyword option(s) %s, valid options are "text", "tags" and "date".' % (kw.keys(),))
            else:
                if text is not None:
                    ev['text'] = str(text)
                if tags is not None:
                    if isinstance(tags, str):
                        tags_ = [tags]
                    else:
                        tags_ = list(tags)
                    for tag in tags_:
                        if tag not in self._tags:
                            self._tag_initialize(tag)
                    ev['tags'] = tags_
                if date is not None:
                    if isinstance(date, Calendar.datetime):
                        date = date.date()
                    if not isinstance(date, Calendar.date):
                        raise TypeError("date option should be a %s instance" % (Calendar.date))
                    old_date = ev['date']
                    self._calevent_dates[old_date].remove(ev_id)
                    if not self._calevent_dates[old_date]:
                        self._reset_day(old_date)
                    else:
                        self._show_event(old_date)
                    ev['date'] = date
                    if date not in self._calevent_dates:
                        self._calevent_dates[date] = [ev_id]
                    else:
                        self._calevent_dates[date].append(ev_id)
                self._show_event(ev['date'])

    def calevent_raise(self, ev_id, above=None):
        """
        Raise event ev_id in tooltip event list.

            above : str
                put ev_id above given one, if above is None, put it on top
                of tooltip event list.

        The day's colors are determined by the last tag of the lowest event
        which has tags.
        """
        try:
            date = self.calevents[ev_id]['date']
        except KeyError:
            raise ValueError("event %s does not exists" % ev_id)
        else:
            evs = self._calevent_dates[date]
            if above is None:
                evs.remove(ev_id)
                evs.insert(0, ev_id)
            else:
                if above not in evs:
                    raise ValueError("event %s does not exists on %s" % (above, date))
                else:
                    evs.remove(ev_id)
                    index = evs.index(above)
                    evs.insert(index, ev_id)
            self._show_event(date)

    def calevent_lower(self, ev_id, below=None):
        """
        Lower event ev_id in tooltip event list.

            below : str
                put ev_id below given one, if below is None, put it at the
                bottom of tooltip event list.

        The day's colors are determined by the last tag of the lowest event
        which has tags.
        """
        try:
            date = self.calevents[ev_id]['date']
        except KeyError:
            raise ValueError("event %s does not exists" % ev_id)
        else:
            evs = self._calevent_dates[date]
            if below is None:
                evs.remove(ev_id)
                evs.append(ev_id)
            else:
                if below not in evs:
                    raise ValueError("event %s does not exists on %s" % (below, date))
                else:
                    evs.remove(ev_id)
                    index = evs.index(below) + 1
                    evs.insert(index, ev_id)
            self._show_event(date)

    def get_calevents(self, date=None, tag=None):
        """
        Return event ids of events with given tag and on given date.

        If only date is given, return event ids of all events on date.
        If only tag is given, return event ids of all events with tag.
        If both options are None, return all event ids.
        """
        if date is not None:
            if isinstance(date, Calendar.datetime):
                date = date.date()
            if not isinstance(date, Calendar.date):
                raise TypeError("date option should be a %s instance" % (Calendar.date))
            try:
                if tag is not None:
                    return tuple(ev_id for ev_id in self._calevent_dates[date] if tag in self.calevents[ev_id]['tags'])
                else:
                    return tuple(self._calevent_dates[date])
            except KeyError:
                return ()
        elif tag is not None:
            return tuple(ev_id for ev_id, prop in self.calevents.items() if tag in prop['tags'])
        else:
            return tuple(self.calevents.keys())

    def _tag_initialize(self, tag):
        props = dict(foreground='white', background='royal blue')
        self._tags[tag] = props
        self.style.configure('tag_%s.%s.TLabel' % (tag, self._style_prefixe), **props)

    def tag_config(self, tag, **kw):
        """
        Configure tag.

        Keyword options: foreground, background (of the day in the calendar)
        """
        if tag not in self._tags:
            self._tags[tag] = {}
        props = dict(foreground='white', background='royal blue')  # default
        props.update(self._tags[tag])
        props.update(kw)
        self.style.configure('tag_%s.%s.TLabel' % (tag, self._style_prefixe), **props)
        self._tags[tag] = props

    def tag_cget(self, tag, option):
        """Return the value of the tag's option."""
        try:
            prop = self._tags[tag]
        except KeyError:
            raise ValueError('unknow tag "%s"' % tag)
        else:
            try:
                return prop[option]
            except KeyError:
                raise ValueError('unknow option "%s"' % option)

    def tag_names(self):
        """Return tuple of existing tags."""
        return tuple(self._tags.keys())

    def tag_delete(self, tag):
        """
        Delete given tag.

        Delete tag properties and remove tag from all events.
        """
        try:
            del self._tags[tag]
        except KeyError:
            raise ValueError('tag "%s" does not exists' % tag)
        else:
            for props in self.calevents.values():
                if tag in props['tags']:
                    props['tags'].remove(tag)
            self._display_calendar()

    # --- other methods
    def keys(self):
        """Return a list of all resource names of this widget."""
        return list(self._properties.keys())

    def cget(self, key):
        """Return the resource value for a KEY given as string."""
        return self[key]

    def configure(self, cnf={}, **kw):
        """
        Configure resources of a widget.

        The values for resources are specified as keyword
        arguments. To get an overview about
        the allowed keyword arguments call the method :meth:`~Calendar.keys`.
        """
        if not isinstance(cnf, dict):
            raise TypeError("Expected a dictionary or keyword arguments.")
        kwargs = cnf.copy()
        kwargs.update(kw)
        for item, value in kwargs.items():
            self[item] = value

    config = configure

# apis

class getWhether:
    def __init__(self):
        self.data = {}
    def loadData(self):
        with open("whether.json", "r") as file:
            self.data = json.load(file)
        if self.data.get("timelines").get("daily")[0].get("time")!=f"{dt.datetime.now().strftime("%Y-%m-%d")}T10:00:00Z" and self.data.get("timelines").get("daily")[0].get("time")!=f"{dt.datetime.now().strftime("%Y-%m")}-{"0" if (int(dt.datetime.today().strftime("%d"))-1) <10 else ""}{int(dt.datetime.today().strftime("%d"))-1}T10:00:00Z" :
            self.apiCall()
    def save_data_to_file(self,data):
        with open("whether.json", "w") as file:
            json.dump(data, file)
        self.loadData()
    def apiCall(self):
        print("////////////////API call///////////////////")
        api_key="a51S5D6NSdSEfLhIK5t97rShUgKgLb0T"
        # api_key="xcDOEQGB3KiPXjJmIfYGQXhW4bWpQBja"
        url = f"https://api.tomorrow.io/v4/weather/forecast?location=-40.57395%2C%20-73.13348&units=metric&apikey={api_key}"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        js=json.loads(response.text)
        self.save_data_to_file(js)



# kalendario app
class CalendarioApp(tk.Tk):
    def __init__(self,fecha):
        # configucacion
        super().__init__()
        self.title('Kalendario')
        self.geometry('700x700')
        self.minsize(700,700)
        self.maxsize(700,700)
        self.data_Manager=DataManager()
        self.data_Manager.load_data()
        self.user=self.data_Manager.get_user()
        self.color=self.data_Manager.get_color(self.user)
        self.config(background=self.color.get("background"))
        self.iconphoto(False,ImageTk.PhotoImage(file="img/ico.png"))
        # cargamos las imagenes
        self.arrows={1:ImageTk.PhotoImage(Image.open("img/up-arrow.png").resize((20,20), Image.LANCZOS)),
                     2:ImageTk.PhotoImage(Image.open("img/down-arrow.png").resize((20,20), Image.LANCZOS)),
                     11:ImageTk.PhotoImage(Image.open("img/up-arrow-lock.png").resize((20,20), Image.LANCZOS)),
                     22:ImageTk.PhotoImage(Image.open("img/down-arrow-lock.png").resize((20,20), Image.LANCZOS)),
                     3:ImageTk.PhotoImage(Image.open("img/left-arrow.png").resize((20,20), Image.LANCZOS)),
                     33:ImageTk.PhotoImage(Image.open("img/left-arrow-lock.png").resize((20,20), Image.LANCZOS)),
                     4:ImageTk.PhotoImage(Image.open("img/right-arrow.png").resize((20,20), Image.LANCZOS)),
                     44:ImageTk.PhotoImage(Image.open("img/right-arrow-lock.png").resize((20,20), Image.LANCZOS))}
        self.imagenes={1000:ImageTk.PhotoImage(Image.open("img/1000.png").resize((80,80), Image.LANCZOS)),
                       1001:ImageTk.PhotoImage(Image.open("img/1001.png").resize((80,80), Image.LANCZOS)),
                       1100:ImageTk.PhotoImage(Image.open("img/1100.png").resize((80,80), Image.LANCZOS)),
                       1101:ImageTk.PhotoImage(Image.open("img/1101.png").resize((80,80), Image.LANCZOS)),
                       1102:ImageTk.PhotoImage(Image.open("img/1102.png").resize((80,80), Image.LANCZOS)),
                       2000:ImageTk.PhotoImage(Image.open("img/2000.png").resize((80,80), Image.LANCZOS)),
                       2100:ImageTk.PhotoImage(Image.open("img/2100.png").resize((80,80), Image.LANCZOS)),
                       4000:ImageTk.PhotoImage(Image.open("img/4000.png").resize((80,80), Image.LANCZOS)),
                       4001:ImageTk.PhotoImage(Image.open("img/4001.png").resize((80,80), Image.LANCZOS)),
                       4200:ImageTk.PhotoImage(Image.open("img/4200.png").resize((80,80), Image.LANCZOS)),
                       4201:ImageTk.PhotoImage(Image.open("img/4201.png").resize((80,80), Image.LANCZOS)),
                       5000:ImageTk.PhotoImage(Image.open("img/5000.png").resize((80,80), Image.LANCZOS)),
                       5001:ImageTk.PhotoImage(Image.open("img/5001.png").resize((80,80), Image.LANCZOS)),
                       5100:ImageTk.PhotoImage(Image.open("img/5100.png").resize((80,80), Image.LANCZOS)),
                       5101:ImageTk.PhotoImage(Image.open("img/5101.png").resize((80,80), Image.LANCZOS)),
                       6000:ImageTk.PhotoImage(Image.open("img/6000.png").resize((80,80), Image.LANCZOS)),
                       6001:ImageTk.PhotoImage(Image.open("img/6001.png").resize((80,80), Image.LANCZOS)),
                       6200:ImageTk.PhotoImage(Image.open("img/6200.png").resize((80,80), Image.LANCZOS)),
                       6201:ImageTk.PhotoImage(Image.open("img/6201.png").resize((80,80), Image.LANCZOS)),
                       7000:ImageTk.PhotoImage(Image.open("img/7000.png").resize((80,80), Image.LANCZOS)),
                       7101:ImageTk.PhotoImage(Image.open("img/7101.png").resize((80,80), Image.LANCZOS)),
                       7102:ImageTk.PhotoImage(Image.open("img/7102.png").resize((80,80), Image.LANCZOS)),
                       8000:ImageTk.PhotoImage(Image.open("img/8000.png").resize((80,80), Image.LANCZOS)),
                       "LogoG":ImageTk.PhotoImage(Image.open("img/LogoGrande.png").resize((200,100), Image.LANCZOS)),
                       "ico":ImageTk.PhotoImage(Image.open("img/LogoGrande.png").resize((200,100), Image.LANCZOS)),
                       "cancelar":ImageTk.PhotoImage(Image.open("img/cancelar.png").resize((100,20), Image.LANCZOS)),
                       "guardar":ImageTk.PhotoImage(Image.open("img/guardar.png").resize((100,20), Image.LANCZOS)),
                       "settings":ImageTk.PhotoImage(Image.open("img/settings.png").resize((20,20), Image.LANCZOS)),
                       "entrar":ImageTk.PhotoImage(Image.open("img/entrar.png").resize((90,20), Image.LANCZOS)),
                       "registro":ImageTk.PhotoImage(Image.open("img/registro.png").resize((90,20), Image.LANCZOS)),
                       "restablecer":ImageTk.PhotoImage(Image.open("img/restablecer.png").resize((90,20), Image.LANCZOS)),
                       "salir":ImageTk.PhotoImage(Image.open("img/salir.png").resize((90,20), Image.LANCZOS)),
                       "seguro":ImageTk.PhotoImage(Image.open("img/seguro.png").resize((90,20), Image.LANCZOS)),
                       "c-azul-vs":ImageTk.PhotoImage(Image.open("img/c-Azul-Vs.png").resize((30,30), Image.LANCZOS)),
                       "c-default":ImageTk.PhotoImage(Image.open("img/c-Default.png").resize((30,30), Image.LANCZOS)),
                       "c-rojo":ImageTk.PhotoImage(Image.open("img/c-Rojo.png").resize((30,30), Image.LANCZOS)),
                       "c-verde":ImageTk.PhotoImage(Image.open("img/c-Verde.png").resize((30,30), Image.LANCZOS)),
                       "c-purpura":ImageTk.PhotoImage(Image.open("img/c-Purpura.png").resize((30,30), Image.LANCZOS))
                       }
        # parametros del clima
        self.tipo_clima={1000:"Despejado",1001:"Nublado",1100:"Mayormente Despejado",1101:"Parcialmente Nublado",
                         1102:"Mayormente Nublado",2000:"Neblina",2100:"Ligera Neblina",4000:"Llovizna",4200:"Lluvia Ligera",
                         4001:"Lluvia",4201:"Lluvia Intensa",5001:"Neviscas",5100:"Nieve Ligera",5000:"Nieve",
                         5101:"Nieve Ligera",6000:"Llovizna Helada",6001:"Lluvia Helada",6200:"Lluvia Helada Ligera",
                         6201:"lluvia helada Intensa",7102:"Ligera Hielo Granulado",7000:"Hielo Granulado",7101:"Hielo Granulado Intenso",
                         8000:"Tormenta"}
        # controles del calendario

        self.bienvenida= bienvenida(self,fecha)
        # panel del clima
        self.control_clima=seccion_clima(self,fecha)
        self.seccion_calendario=seccion_calendario(self,fecha)
        self.mainloop()

class bienvenida(ttk.Frame):
    def __init__(self, parent,fecha):
        super().__init__(parent)
        ttk.Label(self)
        self.place(x=0,y=0,relwidth=0.4,relheight=0.2)
        self.calendario_time=dt.datetime.strptime(f"{fecha}","%Y-%m-%d")
        self.data_Manager=parent.data_Manager
        self.arrows=parent.arrows
        self.anio_cambio= StringVar()
        self.mes_cambio= StringVar()
        self.imagenes=parent.imagenes
        self.user=parent.user
        self.color=parent.color
        self.panelcontrolisopen=False
        self.style()
        self.content()
        self.grid()
    def style(self):
        self.styles=ttk.Label(self,font='1', text=f"",background=self.color.get("background"),foreground="#FFFFFF")
    def content(self):
        months=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
        self.fecha1= ttk.Label(self,font=("arial", 14) , text=f"{self.calendario_time.strftime("%d")} de {months[int(self.calendario_time.strftime("%m"))-1]} de {self.calendario_time.strftime("%Y")}",background=self.color.get("background"),foreground="#FFFFFF")
        
        self.config = ttk.Button(self,command=self.controlpanel,image=self.imagenes["settings"])

        self.logo= ttk.Label(self,font='1',background=self.color.get("background"),image=self.imagenes["LogoG"])
    def grid(self):
        self.rowconfigure((0,1,2,3,4), weight=3,uniform='a')
        self.columnconfigure((0,1,2,3),weight=1,uniform='a')

        self.logo.place(x=50,y=0)
        self.config.place(x=10,y=10)
        self.fecha1.place(x=0,y=100,relwidth=1,relx=0.19,relheight=0.3)
        self.styles.place(x=0,y=0,relwidth=1,relx=0,relheight=1)
    # pantalla login
    def controlpanel(self):
        if not self.panelcontrolisopen:
            self.panelcontrolisopen=True
            self.top = Toplevel(self.master)
            self.top.iconphoto(False,ImageTk.PhotoImage(file="img/ico.png"))
            self.top.title("Control de Usuario")
            self.top.geometry("500x300") if self.user=="N" else self.top.geometry("300x200")
            self.top.minsize(500,300) if self.user=="N" else  self.top.minsize(300,200)
            self.top.maxsize(500,300) if self.user=="N" else self.top.maxsize(300,200)
            self.top.config(background=self.color.get("background"))
            if self.user=="N":
                self.lines3=ttk.Label(self.top,font='1', text=f"",background="#E5A769")
                # login
                self.txtLogin = ttk.Label(self.top,font='1',text="INGRESO",background=self.color.get("background"),foreground="#FFFFFF",)
                self.textname= ttk.Label(self.top,font=('Arial',8),text="Usuario",background=self.color.get("background"),foreground="#FFFFFF",)
                self.name=ttk.Entry(self.top,font=('calibre',10,'normal'))
                self.textpassword= ttk.Label(self.top,font=('Arial',8),text="Contraseña",background=self.color.get("background"),foreground="#FFFFFF",)
                self.password=ttk.Entry(self.top,font=('calibre',10,'normal'))
                self.LogIn = ttk.Button(self.top,command=(lambda:self.validateLogin(self.name.get(),self.password.get())),image=self.imagenes["entrar"])
                self.txtOlvido= ttk.Label(self.top,font=('Arial',8),text="Olvido su contraseña?",background=self.color.get("background"),foreground="#74ADEA",)
                # register
                self.txtRegister = ttk.Label(self.top,font='1',text="REGISTRO",background=self.color.get("background"),foreground="#FFFFFF",)
                self.textRname= ttk.Label(self.top,font=('Arial',8),text="Usuario",background=self.color.get("background"),foreground="#FFFFFF",)
                self.Rname=ttk.Entry(self.top,font=('calibre',10,'normal'))
                self.textRpassword= ttk.Label(self.top,font=('Arial',8),text="Contraseña",background=self.color.get("background"),foreground="#FFFFFF",)
                self.Rpassword=ttk.Entry(self.top,font=('calibre',10,'normal'))
                self.textRDpassword= ttk.Label(self.top,font=('Arial',8),text="Otra vez",background=self.color.get("background"),foreground="#FFFFFF",)
                self.RDpassword=ttk.Entry(self.top,font=('calibre',10,'normal'))
                self.Register = ttk.Button(self.top,command=(lambda:self.validateRegister(self.Rname.get(),self.Rpassword.get(),self.RDpassword.get())),image=self.imagenes["registro"])
                
                # ERROR
                self.error=ttk.Label(self.top,font=('Arial',10),text="",background=self.color.get("background"),foreground="#CD3D49")
                # grid 
                self.top.rowconfigure((0,1,2,3,4), weight=3,uniform='a')
                self.top.columnconfigure((0,1,2,3,4,5,6,7),weight=1,uniform='a')
                # linea
                self.lines3.place(x=250,y=20,relwidth=0.0019,relheight=0.8)
                # login grid
                self.txtLogin.place(x=85,y=40,relwidth=0.2,relheight=0.1)   
                self.textname.place(x=70,y=70,relwidth=0.2,relheight=0.06)   
                self.name.place(x=70,y=90,relwidth=0.25,relheight=0.1) 
                self.textpassword.place(x=70,y=120,relwidth=0.2,relheight=0.06)  
                self.password.place(x=70,y=140,relwidth=0.25,relheight=0.1)    
                self.LogIn.place(x=80,y=180,relwidth=0.2,relx=0,relheight=0.1)
                self.txtOlvido.place(x=75,y=210,relwidth=0.3,relheight=0.06)  
                self.txtOlvido.bind("<Button-1>", lambda event, txtOlvido=self.txtOlvido:self.restablece())

                # register grid
                self.txtRegister.place(x=325,y=40,relwidth=0.3,relheight=0.1) 
                self.textRname.place(x=315,y=70,relwidth=0.2,relheight=0.06)   
                self.Rname.place(x=315,y=90,relwidth=0.25,relheight=0.1) 

                self.textRpassword.place(x=295,y=120,relwidth=0.2,relheight=0.06)  
                self.Rpassword.place(x=280,y=140,relwidth=0.18,relheight=0.1)    
                self.textRDpassword.place(x=400,y=120,relwidth=0.2,relheight=0.06)  
                self.RDpassword.place(x=380,y=140,relwidth=0.18,relheight=0.1)    

                self.Register.place(x=325,y=180,relwidth=0.2,relx=0,relheight=0.1)

                # error grid
                self.error.place(x=200,y=260,relwidth=0.3,relheight=0.1)
            else:
                
                # panel de usuario
                self.txtuser = ttk.Label(self.top,font='1',text=f"Usuario: {self.data_Manager.data.get("users")[int(self.user)].get("name")}",background=self.color.get("background"),foreground="#FFFFFF",)
                self.txtcolor = ttk.Label(self.top,font='1',text="Cambiar el Color:",background=self.color.get("background"),foreground="#FFFFFF",)
                self.salir = ttk.Button(self.top,command=(lambda:self.logOut()),image=self.imagenes["salir"])
                self.CDefault = ttk.Button(self.top,command=(lambda:self.CamioColor("Default")),image=self.imagenes["c-default"])
                self.CAzulVs = ttk.Button(self.top,command=(lambda:self.CamioColor("Azul-Vs")),image=self.imagenes["c-azul-vs"])
                self.CPurpura = ttk.Button(self.top,command=(lambda:self.CamioColor("Purpura")),image=self.imagenes["c-purpura"])
                self.CRojo = ttk.Button(self.top,command=(lambda:self.CamioColor("Rojo")),image=self.imagenes["c-rojo"])
                self.CVerdde = ttk.Button(self.top,command=(lambda:self.CamioColor("Verde")),image=self.imagenes["c-verde"])
                # grid 
                self.top.rowconfigure((0,1,2,3,4), weight=3,uniform='a')
                self.top.columnconfigure((0,1,2,3,4,5,6,7),weight=1,uniform='a')
                self.txtuser.place(x=10,y=-10,relwidth=1,relheight=0.4)   
                self.txtcolor.place(x=30,y=50,relwidth=1,relheight=0.1)   
                self.salir.place(x=80,y=160,relwidth=0.4,relx=0,relheight=0.2)
                self.CDefault.place(x=30,y=80)
                self.CAzulVs.place(x=80,y=80)
                self.CPurpura.place(x=130,y=80)
                self.CRojo.place(x=180,y=80)
                self.CVerdde.place(x=230,y=80)
            def on_closing():
                self.panelcontrolisopen=False
                self.top.destroy()

            self.top.protocol("WM_DELETE_WINDOW", on_closing)
            self.top.mainloop()
    def admin(self,user,password,rpassword):
        self.topadmin = Toplevel(self.master)
        self.topadmin.iconphoto(False,ImageTk.PhotoImage(file="img/ico.png"))
        self.topadmin.title("Control de admin")
        self.topadmin.geometry("300x100")
        self.topadmin.minsize(300,100)
        self.topadmin.maxsize(300,100)
        self.topadmin.config(background=self.color.get("background"))

        self.topadmin.rowconfigure((0,1,2,3,4), weight=3,uniform='a')
        self.topadmin.columnconfigure((0,1,2,3,4,5,6,7),weight=1,uniform='a')

        self.textRDpassword= ttk.Label(self.topadmin,font=('Arial',8),text="Contraseña Admin",background=self.color.get("background"),foreground="#FFFFFF",)
        self.passwordAdmin=ttk.Entry(self.topadmin,font=('calibre',10,'normal'))
        self.restablecer = ttk.Button(self.topadmin,command=(lambda:self.validateadmin(self.passwordAdmin.get(),user,password,rpassword)),image=self.imagenes["restablecer"])
        
        self.textRDpassword.place(x=50,y=15,relwidth=0.7,relheight=0.2)  
        self.passwordAdmin.place(x=50,y=35,relwidth=0.7,relheight=0.2)    
        self.restablecer.place(x=100,y=60,relwidth=0.34,relx=0,relheight=0.28)

    def validateadmin(self,adminpassword,user,password,rpassword):
        if adminpassword==self.data_Manager.data.get("admin").get("contrasena"):
            self.validaterestablecer(user,password,rpassword)
            self.topadmin.destroy()
    def validateLogin(self,user,password):
        s=0
        for i in range(0,len(self.data_Manager.data.get("users"))):
            if user==self.data_Manager.data.get("users")[i].get("name"):
                s=1
                if password==self.data_Manager.data.get("users")[i].get("contrasena"):
                    self.data_Manager.logIn(i)
                else:
                    self.error.configure(text="Contraseña incorrecta")
            i+=1
            
        self.error.configure(text="No existe usuario") if s==0 else None
    
    def validateRegister(self,user,password,rpassword):
        s=0
        for i in range(0,len(self.data_Manager.data.get("users"))):
            if user==self.data_Manager.data.get("users")[i].get("name"):
                s=1
        if user=="" or password=="" or rpassword=="":
            self.error.configure(text="Un campo esta vacio")
        elif not user.isalpha() :
            self.error.configure(text="Usuario inválido")
        elif s==1:
            self.error.configure(text="Usuario ya existe")
        elif password==rpassword:
            self.data_Manager.register(user,password)
            self.error.configure(text="Cuenta creada, Ingrese",foreground="#A1B658")
        else:
            self.error.configure(text="Contraseñas desiguales")
    def restablece(self):
        self.txtRegister.configure(text="RESTABLECER")
        self.textRpassword.configure(text="Nueva Contraseña")
        self.Register.configure(command=(lambda:self.admin(self.Rname.get(),self.Rpassword.get(),self.RDpassword.get())),image=self.imagenes["restablecer"])
    def validaterestablecer(self,user,password,rpassword):
        s=0
        for i in range(0,len(self.data_Manager.data.get("users"))):
            if user==self.data_Manager.data.get("users")[i].get("name"):
                s=1
                if password==rpassword:
                    self.data_Manager.restablecer(i,password)

                    self.error.configure(text="Contraseña creada",foreground="#A1B658")
                else:
                    self.error.configure(text="Contraseñas desiguales")
        self.error.configure(text="No existe usuario") if s ==0 else None
    def logOut(self):
        self.salir.configure(command=(lambda:self.data_Manager.logOut()),image=self.imagenes["seguro"])
    def CamioColor(self,color):
        self.salir.configure(command=(lambda:self.data_Manager.cambiarColor(self.user,color)),image=self.imagenes["seguro"])


class seccion_clima(ttk.Frame):
    def __init__(self,parent,fecha):
        super().__init__(parent)
        ttk.Label(self)
        self.place(x=300,y=0,relwidth=0.6,relheight=0.2)
        self.data_clima=getWhether()
        self.data_clima.loadData()
        self.clima_time=dt.datetime.strptime(f"{fecha}","%Y-%m-%d")
        self.arrows=parent.arrows
        self.imagenes=parent.imagenes
        self.tipo_clima=parent.tipo_clima
        self.color=parent.color
        self.index=0
        # inicio de los estilos
        self.style()
        self.line1()
        self.line2()
        self.line3()
        # primera seccion
        self.descripcion()
        self.controles()
        # segunda seccion
        self.horaYminutomasGrados()
        self.texto()
        # grid
        self.grid()
    # estilos
    def style(self):
        self.styles=ttk.Label(self,font='1', text=f"",background=self.color.get("background"),foreground="#FFFFFF")
    def line1(self):
        self.lines1=ttk.Label(self,font='1', text=f"",background="#E5A769")
    def line2(self):
        self.lines2=ttk.Label(self,font='1', text=f"",background="#74ADEA")
    def line3(self):   
        self.lines3=ttk.Label(self,font='1', text=f"",background="#5662F6")

    # primera seccion
    # texto de "lluviendo" o "sol"
    def descripcion(self):
        self.descripcion1= ttk.Label(self,font='1', text=self.tipo_clima[self.data_clima.data.get("timelines").get("daily")[0].get("values").get("weatherCodeMin")],background=self.color.get("background"),foreground="#FFFFFF")
        self.descripcionDetalle1= ttk.Label(self,font=('Arial',10), text=f"Datos",background=self.color.get("background"),foreground="#FFFFFF")
        self.descripcionDetalle2= ttk.Label(self,font=('Arial',10), text=f"Temp. Max: {self.data_clima.data.get("timelines").get("daily")[0].get("values").get("temperatureMax")}°ᶜ",background=self.color.get("background"),foreground="#FFFFFF")
        self.descripcionDetalle3= ttk.Label(self,font=('Arial',10), text=f"Temp. Min: {self.data_clima.data.get("timelines").get("daily")[0].get("values").get("temperatureMin")}°ᶜ",background=self.color.get("background"),foreground="#FFFFFF")
        self.descripcionDetalle4= ttk.Label(self,font=('Arial',10), text=f"Viento: {self.data_clima.data.get("timelines").get("daily")[0].get("values").get("windSpeedAvg")}km/h",background=self.color.get("background"),foreground="#FFFFFF")
        self.descripcionDetalle5= ttk.Label(self,font=('Arial',10), text=f"Humedad: {self.data_clima.data.get("timelines").get("daily")[0].get("values").get("humidityAvg")}%",background=self.color.get("background"),foreground="#FFFFFF")
        self.fecha1= ttk.Label(self,font=("Arial",10), text=dt.datetime.today().strftime("%d/%m/%Y"),background=self.color.get("background"),foreground="#FFFFFF")
        self.imagen1=ttk.Label(self,font='1',background=self.color.get("background"),image=self.imagenes[self.data_clima.data.get("timelines").get("daily")[0].get("values").get("weatherCodeMin")])
        self.dia= ttk.Label(self, text=self.clima_time.strftime("%d"),background=self.color.get("background"),foreground="#FFFFFF")
    def controles(self):
        self.btn_nextdia = ttk.Button(self,command=self.next_dia,image=self.arrows[1])
        self.btn_prevdia = ttk.Button(self,command=self.prev_dia,image=self.arrows[22])
    def next_dia(self):
        self.configure(-1,1)
    def prev_dia(self):
        self.configure(0,-1)
    def configure(self,i,op):
        if f'{self.data_clima.data.get("timelines").get("daily")[i].get("time").split("-")[2][0:2]}-{self.data_clima.data.get("timelines").get("daily")[i].get("time").split("-")[1]}'!=self.clima_time.strftime("%d-%m"):
            try:
                self.clima_time = self.clima_time.replace(day=self.clima_time.day + op)
            except:
                self.clima_time = self.clima_time.replace(month=self.clima_time.month + op,day=(self.clima_time-(timedelta(days=1) if i==0 else -timedelta(days=1))).day)
            self.btn_nextdia.configure(image=self.arrows[1]) if i==0 else self.btn_prevdia.configure(image=self.arrows[2])
            self.index=self.index+op
            self.imagen1.configure(image=self.imagenes[self.data_clima.data.get("timelines").get("daily")[self.index].get("values").get("weatherCodeMin")])
            self.fecha1.configure(text=self.clima_time.strftime("%d/%m/%Y"))
            self.descripcion1.configure(text=self.tipo_clima[self.data_clima.data.get("timelines").get("daily")[self.index].get("values").get("weatherCodeMin")])
            self.descripcionDetalle2.configure(text=f"Temp. Avg: {self.data_clima.data.get("timelines").get("daily")[self.index].get("values").get("temperatureAvg")}°ᶜ")
            self.descripcionDetalle3.configure(text=f"Amanecer: {(dt.datetime.strptime((self.data_clima.data.get("timelines").get("daily")[self.index].get("values").get("sunriseTime").split("T")[1][0:5]),"%H:%M")-timedelta(hours=4)).strftime("%H:%M")}hrs")
            self.descripcionDetalle4.configure(text=f"Atardecer: {(dt.datetime.strptime((self.data_clima.data.get("timelines").get("daily")[self.index].get("values").get("sunsetTime").split("T")[1][0:5]),"%H:%M")-timedelta(hours=4)).strftime("%H:%M")}hrs")
            self.descripcionDetalle5.configure(text=f"Humedad: {self.data_clima.data.get("timelines").get("daily")[self.index].get("values").get("humidityAvg")}%")
            self.dia.configure(text=self.clima_time.strftime("%d"))
            if f'{self.data_clima.data.get("timelines").get("daily")[i].get("time").split("-")[2][0:2]}-{self.data_clima.data.get("timelines").get("daily")[i].get("time").split("-")[1]}'==self.clima_time.strftime("%d-%m"):
                self.btn_prevdia.configure(image=self.arrows[22]) if i==0 else self.btn_nextdia.configure(image=self.arrows[11])
                if self.index==0:
                    self.descripcionDetalle2.configure(text=f"Temp. Max: {self.data_clima.data.get("timelines").get("daily")[0].get("values").get("temperatureMax")}°ᶜ")
                    self.descripcionDetalle3.configure(text=f"Temp. Min: {self.data_clima.data.get("timelines").get("daily")[0].get("values").get("temperatureMin")}°ᶜ")
                    self.descripcionDetalle4.configure(text=f"Viento: {self.data_clima.data.get("timelines").get("daily")[0].get("values").get("windSpeedAvg")}km/h")
                    self.descripcionDetalle5.configure(text=f"Humedad: {self.data_clima.data.get("timelines").get("daily")[0].get("values").get("humidityAvg")}%")
    # segunda seccion
    def texto(self):
        self.texto1= ttk.Label(self,font=('Times New Roman',15), text=f"Hoy",background=self.color.get("background"),foreground="#FFFFFF")
        self.texto2= ttk.Label(self,font=('Times New Roman',8), text=f"Al minuto",background=self.color.get("background"),foreground="#FFFFFF")
    def change_horaYminutomasGrados(self):
        delta=dt.datetime.now()+timedelta(hours=4)
        try:
            for i in range(len(self.data_clima.data.get("timelines").get("minutely"))):
                if self.data_clima.data.get("timelines").get("minutely")[i].get("time") ==f"{delta.strftime("%Y-%m-%d")}T{delta.strftime("%H")}:{delta.strftime("%M")}:00Z":
                    gradoMinute = self.data_clima.data.get("timelines").get("minutely")[i].get("values")
                    break
            self.hora1.configure(text=time.strftime("%H:%M:%S"))
            self.gradosXminuto1.configure(text=f"{gradoMinute.get("temperature")}°ᶜ")
            self.gradosSec1.configure(text=f"{gradoMinute.get("humidity")}% de Humedad")
            self.gradosSec2.configure(text=f"Viento de {gradoMinute.get("windSpeed")} km/h")
        except:
            self.data_clima.apiCall()
        self.after(1000,self.change_horaYminutomasGrados)
    def horaYminutomasGrados(self):
        self.hora1= ttk.Label(self,font=('Times New Roman',15), text="",background=self.color.get("background"),foreground="#FFFFFF")
        self.gradosXminuto1= ttk.Label(self,font=('Arial',20), text=f"{"00"}°ᶜ",background=self.color.get("background"),foreground="#FFFFFF")
        self.gradosSec1= ttk.Label(self,font=('Arial',10), text=f"{"0"}% de Humedad",background=self.color.get("background"),foreground="#FFFFFF")
        self.gradosSec2= ttk.Label(self,font=('Arial',10), text=f"Viento de {"0"}km/h",background=self.color.get("background"),foreground="#FFFFFF")
        self.change_horaYminutomasGrados()
    # grid seccion
    def grid(self):
        self.rowconfigure((0,1,2,3,4), weight=3,uniform='a')
        self.columnconfigure((0,1,2,3,4,5,6,7),weight=1,uniform='a')
        # lineas separadoras 
        self.lines1.place(x=0,y=0,relwidth=0.012,relheight=1)
        self.lines2.place(x=138,y=30,relwidth=0.0009,relheight=1)
        self.lines3.place(x=265,y=0,relwidth=0.012,relheight=1)
        # primera seccion
        self.imagen1.place(x=47,y=56,relwidth=0.2,relx=0,rely=0,relheight=0.65)
        self.descripcionDetalle1.place(x=180,y=18,relwidth=0.1,relx=0,relheight=0.2)
        self.descripcionDetalle2.place(x=140,y=43,relwidth=0.29,relx=0,relheight=0.2)
        self.descripcionDetalle3.place(x=140,y=68,relwidth=0.29,relx=0,relheight=0.2)
        self.descripcionDetalle4.place(x=140,y=93,relwidth=0.297,relx=0,relheight=0.2)
        self.descripcionDetalle5.place(x=140,y=118,relwidth=0.29,relx=0,relheight=0.2)
        self.descripcion1.place(x=5,y=12,relwidth=0.3,relx=0,relheight=0.3)
        self.fecha1.place(x=110,y=4,relwidth=0.3,relx=0,relheight=0.15)
        self.styles.place(x=5,y=0,relwidth=1,relx=0,relheight=1)
        self.dia.grid(row=3,column=0, sticky='')
        self.btn_prevdia.grid(row=4, column=0, sticky='',rowspan=2)
        self.btn_nextdia.grid(row=2, column=0, sticky='',columnspan=1)
        # tercera seccion
        self.texto1.place(x=315,y=0,relwidth=0.3,relx=0,relheight=0.2)
        self.texto2.place(x=305,y=80,relwidth=0.3,relx=0,relheight=0.1)
        self.hora1.place(x=296,y=14,relwidth=0.3,relx=0,relheight=0.3)
        self.gradosXminuto1.place(x=290,y=50,relwidth=0.3,relx=0,relheight=0.2)
        self.gradosSec1.place(x=272,y=93,relwidth=0.3,relx=0,relheight=0.2)
        self.gradosSec2.place(x=274,y=118,relwidth=0.3,relx=0,relheight=0.2)


class seccion_calendario(ttk.Frame):
    def __init__(self,parent,fecha):
        super().__init__(parent)
        ttk.Label(self)
        self.user=parent.user
        self.data_Manager=parent.data_Manager
        self.color=parent.color
        self.data_clima=getWhether()
        self.data_clima.loadData()
        self.place(x=0,y=150,relwidth=1,relheight=1)
        self.imagen=parent.imagenes
        self.calendario=Calendar(self)
        self.isopen=[]
        self.selected_date = StringVar()
        self.calendario.place(x=0,y=0,relwidth=1,relx=0,relheight=0.785)
        self.calendario.bind("<<CalendarSelected>>", self.on_date_click) if self.user!="N" else self.calendario.bind("<<CalendarSelected>>", bienvenida(parent,fecha).controlpanel())

    def on_date_click(self, event):
        try:
            self.isopen.remove(self.calendario.get_date())
            self.isopen.append(self.calendario.get_date())
            print(self.isopen)
        except:
            self.isopen.append(self.calendario.get_date())
            
            self.selected_date.set(self.calendario.get_date())
            self.top = Toplevel(self.master)
            self.top.iconphoto(False,ImageTk.PhotoImage(file="img/ico.png"))
            self.top.title(f"Block de notas : {self.calendario.get_date()}")
            self.top.geometry("400x600")
            self.top.minsize(400,600)
            self.top.maxsize(400,600)
            self.top.config(background=self.color.get("background"))
        
            def on_closing():
                self.isopen.remove(self.calendario.get_date())
                self.top.destroy()

            # entry de texto
            day_data = self.data_Manager.data.get("users")[int(self.user)].get("data").get(self.calendario.get_date(), "")
            self.event_entry = Text(self.top,wrap=tk.WORD, height=3, width=30,background="#E6DFCE")
            self.event_entry.insert(tk.END, day_data)
            # bortones
            self.boton1= ttk.Button(self.top,text="CANCELAR",image=self.imagen["cancelar"],command=lambda:on_closing())
            self.boton2= ttk.Button(self.top, command=(lambda:self.save_data(self.calendario.get_date(),self.event_entry.get("1.0",tk.END))) ,image=self.imagen["guardar"])


            #grid general
            self.top.rowconfigure((0,1,2,3,4), weight=3,uniform='a')
            self.top.columnconfigure((0,1,2,3,4,5,6,7),weight=1,uniform='a')
            
            self.event_entry.place(x=31,y=10,relwidth=0.82,relx=0,relheight=0.9)
            self.boton1.place(x=30,y=560,relwidth=0.3,relx=0,relheight=0.05)
            self.boton2.place(x=240,y=560,relwidth=0.3,relx=0,relheight=0.05)

            print(self.isopen)
            self.top.protocol("WM_DELETE_WINDOW", on_closing)
            self.top.mainloop()
    def save_data(self,date, data):
        self.data_Manager.save_data(int(self.user),date, data)
        self.top.destroy()


CalendarioApp(dt.datetime.today().strftime('%Y-%m-%d'))


