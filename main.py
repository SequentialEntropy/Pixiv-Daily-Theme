import requests
from datetime import datetime, timedelta
import pytz
from tag import fetch_tag

red = "\033[91m"
green = "\033[94m"
reset = "\033[0m"

jp = pytz.timezone("Japan")

def int_input():
    value = input()
    try:
        return int(value)
    except ValueError:
        print(f'{value} is not a number.')
        print(f'{value} は数ではありません。')
    return False
    
def date_clean(date):
    date_formatted = datetime.strftime(date, "%Y-%m-%d")
    date_full = datetime.strftime(date, "%A %-d %B %Y")
    return date_formatted, date_full

def error_message(reason, reason_jp):
    print(f'The theme could not be found for this date.')
    print(f'Reason: {reason}')
    print(f'お題を検索することができませんでした。')
    print(f'理由：{reason_jp}')

def fetch_theme(date):
    date_formatted, date_full = date_clean(date)

    response = requests.get(f'https://www.pixiv.net/ajax/idea/anniversary/{date_formatted}')

    print(f'\n{date_full}')

    if response.status_code != 200:
        error_message(f'The API returned the status code { response.status_code }.', f'API からステータス・コード「{ response.status_code }」が返されました。')
        return

    data = response.json()

    if data.get('error', True):
        error_message(f'The API returned the error message "{ data.get("message", "(No message given)") }".', f'API からエラー「{ data.get("message", "（エラーメッセージ無し）") }」が返されました。')
        return

    tag_name = data["body"]["idea_anniversary_tag"]

    tag_data = fetch_tag(data["body"]["idea_anniversary_tag"])

    if tag_data:
        print(f'ID: { tag_data["body"]["pixpedia"]["id"] }')
        print(f'Theme: {green}{ tag_data["body"]["tagTranslation"][tag_name]["en"] }{reset}')

    print(f'お題：{red}{ tag_name }{reset}')

    if tag_data:
        print(f'読み仮名：{ tag_data["body"]["pixpedia"].get("yomigana", "") }')

    print(data['body']['idea_anniversary_description'])

def menu():
    print('Choose an option:')
    print('オプションを選択してください：')
    print('[1] Query today\'s theme')
    print('    今日のお題を検索')
    print('[2] Query themes for the next x days')
    print('    〇日後までのお題を検索')
    print('[3] Query themes for the previous x days')
    print('    〇日前までのお題を検索')
    print('[4] Query theme on a specific date')
    print('    〇月〇日のお題を検索')
    print('[5] Query all themes between two dates')
    print('    〇月〇日から〇月〇日までのお題を検索')
    print('[6] Quit')
    print('    閉じる')

def main():
    menu()

    option = input()

    if option in ['1', '１']:
        now = datetime.now(jp)
        fetch_theme(now)

    elif option in ['2', '２']:
        print('Enter the number of days to query:')
        print('検索するお題の日にちの数を入力してください：')
        days = int_input()
        if not days:
            return
        
        now = datetime.now(jp)
        for i in range(days):
            fetch_theme(now + timedelta(days=i + 1))

    elif option in ['3', '３']:
        print('Enter the number of days to query:')
        print('検索するお題の日にちの数を入力してください：')
        days = int_input()
        if not days:
            return

        now = datetime.now(jp)
        for i in range(days):
            fetch_theme(now - timedelta(days=i + 1))

    elif option in ['4', '４']:
        print('Enter the year:')
        print('年を入力してください：')
        year = int_input()
        if not year:
            return

        print('Enter the month:')
        print('月を入力してください：')
        month = int_input()
        if not month:
            return
        
        print('Enter the day:')
        print('日にちを入力してください：')
        day = int_input()
        if not day:
            return

        try:
            date = datetime(year, month, day)
        except ValueError:
            error_message('An invalid date was entered', '無効な日付が入力されました')
            return

        fetch_theme(date)

    elif option in ['5', '５']:
        print('Enter the year for the starting date:')
        print('最初の日にちの年を入力してください：')
        year1 = int_input()
        if not year1:
            return

        print('Enter the month for the starting date:')
        print('最初の日にちの月を入力してください：')
        month1 = int_input()
        if not month1:
            return
        
        print('Enter the day for the starting date:')
        print('最初の日にちの日にちを入力してください：')
        day1 = int_input()
        if not day1:
            return
        
        try:
            date1 = datetime(year1, month1, day1)
        except ValueError:
            error_message('An invalid date was entered', '無効な日付が入力されました')
            return

        print('Enter the year for the ending date:')
        print('最後の日にちの年を入力してください：')
        year2 = int_input()
        if not year2:
            return

        print('Enter the month for the ending date:')
        print('最後の日にちの月を入力してください：')
        month2 = int_input()
        if not month2:
            return
        
        print('Enter the day for the ending date:')
        print('最後の日にちの日にちを入力してください：')
        day2 = int_input()
        if not day2:
            return

        try:
            date2 = datetime(year2, month2, day2)
        except ValueError:
            error_message('An invalid date was entered', '無効な日付が入力されました')
            return

        if (date2 - date1).days < 0:
            error_message('An invalid range was entered. The starting date must be earlier than the ending date.', '無効な期間が入力されました。最初と最後の日にちの順番を確認してください。')

        for i in range((date2 - date1).days + 1):
            fetch_theme(date1 + timedelta(days=i))

if __name__ == "__main__":
    main()