from mycalendar import MyCalendar
from datetime import datetime  # これもあとで使う

def formatday(self, day, weekday, theyear, themonth):
    """
    オーバーライド (引数を変えるのはPythonでは多分非推奨)
    引数で year と month を渡すようにした。
    """
    if day == 0:
        return '<td style="background-color: #eeeeee">&nbsp;</td>'  # 空白
    else:
        html = '<td class="text-center {highlight}"><a href="{url}" style="color:{text}">{day}</a></td>'
        text = 'blue'
        highlight = ''
        # もし予定があるなら強調
        date = datetime(year=theyear, month=themonth, day=day)
        date_str = date.strftime('%Y%m%d')
        if date_str in self.linked_date:
            if self.linked_date[date_str]:  # 終了した予定
                highlight = 'bg-success'
                text = 'white'
            elif date < datetime.now():  # 過去の予定
                highlight = 'bg-secondary'
                text = 'white'
            else:  # これからの予定
                highlight = 'bg-warning'
        return html.format(  # url を /todo/{username}/year/month/day に
                           url='/todo/{}/{}/{}/{}'.format(self.username, theyear, themonth, day),
                           text=text,
                           day=day,
                           highlight=highlight)