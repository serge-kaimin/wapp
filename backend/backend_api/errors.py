# errors.py

error_messages = {
    204: 'No Content: Использован метод запроса OPTIONS, измените метод запроса на GET',
    400: {
        'instance in starting process try later': 'Инстанс находится в процессе запуска/перезапуска. Попробуйте повторить попытку спустя несколько секунд',
        'instance is starting or not authorized': 'Инстанс не авторизован. Для авторизации инстанса перейдите в личный кабинет и считайте QR-код из приложения WhatsApp Business на телефоне',
        'Instance account is expired. Renew your instance from personal area': 'Срок действия инстанса истек. Продлите свой инстанс из личного кабинета',
        'bad request data': 'Данные запроса не валидны. Исправьте ошибку в параметрах запроса и повторите попытку',
        'Instance is deleted': 'Инстанс был удалён',
        'Bad Request\nValidation failed': 'Ошибка валидации, подробнее в таблице',
        'Unexpected token _ in JSON at position ХХ': 'Ошибка в структуре JSON'
    },
    401: 'Unauthorized: Проблема с авторизацией, проверьте корректность указания apiTokenInstance, partnerToken',
    403: 'Forbidden: Проблема с аутентификацией, проверьте корректность указания idInstance и адрес запроса',
    404: 'Not Found: Некорректный метод запроса',
    429: 'Too Many Requests: Пользователь отправил слишком много запросов за заданный промежуток времени. Уменьшите частоту запросов. Рекомендации по частоте запросов',
    466: 'correspondentsStatus: Исчерпан лимит, подробнее в теле ошибки. Пример тела ошибки',
    499: 'Client Closed Request: Пользователь закрыл соединение, пока сервер обрабатывал запрос. Требуется увеличить время ожидания ответа от сервера и повторить запрос с задержкой. Если ошибка повторится, то информировать оператора и дать возможность повторить отправку',
    500: {
        'File from url exceeded max upload size. Size: XXXXmb Limit: 100mb Url:': 'Попытка отправки файла размером более 100 МБайт',
        'request entity too large': 'Превышение допустимой длины json (>100кб)'
    },
    502: 'Bad Gateway: Сервер не способен получить ответ от целевого сервера. Требуется 3 раза повторить запрос с задержкой. Если ошибка повторится, то информировать оператора и дать возможность повторить отправку'
}

def process_error(status_code, error_message=None):
    error_response = error_messages.get(status_code, 'An error occurred')
    if isinstance(error_response, dict):
        error_response = error_response.get(error_message, 'An error occurred')
    return error_response