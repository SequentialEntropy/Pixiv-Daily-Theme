import requests
from datetime import datetime, timedelta
import pytz

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

    print(f'お題：{data["body"]["idea_anniversary_tag"]}')
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
    print('[5] Quit')
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

if __name__ == "__main__":
    main()