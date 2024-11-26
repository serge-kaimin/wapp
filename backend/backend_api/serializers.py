# api/serializers.py
from rest_framework import serializers
from .models import YourModel


class YourModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = YourModel
        fields = "__all__"

class RequestSerializer(serializers.Serializer):
    id_instance = serializers.CharField(max_length=100, required=True)
    api_token_instance = serializers.CharField(max_length=100, required=True)

def validate_yes_no(value):
    choices = ['yes', 'no']
    if value not in choices:
        raise serializers.ValidationError(f"Value must be one of {choices}.")
    return value

class SettingsResponseSerializer(serializers.Serializer):
    # string: WhatsApp instance ID
    wid = serializers.CharField(max_length=100)
    # string: not used
    countryInstance = serializers.CharField(max_length=100, allow_blank=True, required=False)
    # string: not used
    typeAccount = serializers.CharField(max_length=100, allow_blank=True, required=False)
    # string: URL для получения входящих уведомлений. 
    # При получении уведомлений технологией HTTP API, 
    # поле должно быть пустым. https://green-api.com/docs/api/receiving/technology-webhook-endpoint/
    webhookUrl = serializers.CharField(max_length=100, allow_blank=True, required=False)
    # string
    # Токен для доступа к вашему серверу уведомлений. Описание работы поля.
    webhookUrlToken = serializers.CharField(max_length=100, allow_blank=True, required=False)
    # Интервал отправки сообщений в миллисекундах
    delaySendMessagesMilliseconds = serializers.IntegerField()
    # string
    # Отмечать входящие сообщения прочитанными или нет, возможные значения: yes, no. 
    # Игнорируется, если markIncomingMessagesReadedOnReply в значении 'yes'.
    markIncomingMessagesReaded = serializers.CharField(max_length=10, validators=[validate_yes_no])
    # string: Отмечать входящие сообщения прочитанными при отправке сообщения 
    # в чат через API, возможные значения: yes, no. Если в значении 'yes', 
    # то настройка markIncomingMessagesReaded игнорируется.
    markIncomingMessagesReadedOnReply = serializers.CharField(max_length=10, validators=[validate_yes_no])
    # string: Не используется
    sharedSession = serializers.CharField(max_length=100, required=False)
    # string
    # Получать уведомления о статусах отправки/доставки/прочтении исходящих сообщений,
    # возможные значения: yes, no.
    outgoingWebhook = serializers.CharField(max_length=10, validators=[validate_yes_no])
    # string
    # Получать уведомления о сообщениях, отправленных с телефона, возможные значения: yes, no
    outgoingMessageWebhook = serializers.CharField(max_length=10, validators=[validate_yes_no])
    # string
    # Получать уведомления о сообщениях, отправленных через API, 
    # возможные значения: yes, no. При отправке сообщения на несуществующий аккаунт WhatsApp,
    # уведомление не придет.
    outgoingAPIMessageWebhook = serializers.CharField(max_length=10, validators=[validate_yes_no])    
    # string	Получать уведомления о входящих сообщениях и файлах, возможные значения: yes, no
    incomingWebhook = serializers.CharField(max_length=10)
    # string	Временно не работает. Получать уведомления об устройстве (телефоне) и уровне заряда батареи, возможные значения: yes, no
    deviceWebhook = serializers.CharField(max_length=10)
    # string	Не используется
    statusInstanceWebhook = serializers.CharField(max_length=100, required=False)
    # string	Получать уведомления об изменении состояния авторизации инстанса, возможные значения: yes, no
    stateWebhook = serializers.CharField(max_length=10)
    # string	Не используется
    enableMessagesHistory = serializers.CharField(max_length=10)
    # string	Выставляет статус 'В сети' для вашего аккаунта
    keepOnlineStatus = serializers.CharField(max_length=10)
    # string	Получать уведомления о создании опроса и голосовании в опросе, возможные значения: yes, no
    pollMessageWebhook = serializers.CharField(max_length=10)
    # string	Временно не работает. Получать уведомления о добавлении чата в список заблокированных контактов, возможные значения: yes, no
    incomingBlockWebhook = serializers.CharField(max_length=10)
    # string	Получать уведомления о статусах входящего звонка, возможные значения: yes, no
    incomingCallWebhook = serializers.CharField(max_length=10)

    # missing fields on https://green-api.com/docs/api/account/GetSettings/

    # string: Прокси инстанса
    proxyInstance = serializers.CharField(max_length=100, allow_blank=True, required=False)
    # string: Получать уведомления о редактировании сообщений, возможные значения: yes, no
    editedMessageWebhook = serializers.CharField(max_length=10)
    # string: Получать уведомления об удалении сообщений, возможные значения: yes, no
    deletedMessageWebhook = serializers.CharField(max_length=10)

# Example:
# {
#    "stateInstance": "authorized"
#}
# reference: https://green-api.com/docs/api/account/GetStateInstance/
class StateInstanceResponseSerializer(serializers.Serializer):
    # Состояние инстанса. Принимает значения:
    # notAuthorized - Инстанс не авторизован.
    # authorized - Инстанс авторизован
    # blocked - Инстанс забанен
    # sleepMode - Статус устарел. Инстанс ушел в спящий режим. Состояние возможно, когда выключен телефон. После включения телефона может потребоваться до 5 минут для перехода состояния инстанса в значение authorized
    # starting - Инстанс в процессе запуска (сервисный режим). Происходит перезагрузка инстанса, сервера или инстанс в режиме обслуживания. Может потребоваться до 5 минут для перехода состояния инстанса в значение authorized
    # yellowCard - На инстансе частично или полностью приостановлена отправка сообщений из-за спамерской активности. Сообщения отправленные после получения статуса хранятся в очереди к отправке 24 часа. Для продолжения работы инстанса требуется сделать перезагрузку инстанса
    stateInstance = serializers.CharField(max_length=100)

# Example:
# {
#    "chatId": "11001234567@с.us",
#    "message": "I use Green-API to send this message to you!",
#    "quotedMessageId": "361B0E63F2FDF95903B6A9C9A102F34B"
#}
class SendMessageRequestSerializer(serializers.Serializer):
    chatId = serializers.CharField(max_length=100, required=True)
    message = serializers.CharField(max_length=1000, required=True)
    quotedMessageId = serializers.CharField(max_length=100, allow_blank=True, required=False)
    linkPreview = serializers.CharField(max_length=10, allow_blank=True, required=False)

# Example:
# {
#    "idMessage": "3EB0C767D097B7C7C030"
# }
class SendMessageResponseSerializer(serializers.Serializer):
    idMessage = serializers.CharField(max_length=100)


class SendFileByUrlRequestSerializer(serializers.Serializer):
    chatId = serializers.CharField(max_length=100, required=True)
    url = serializers.URLField(max_length=200, required=True)

# - chatId
# - urlFile
# - fileName
# - caption (optional)
# - quotedMessageId (optional)
class SendFileByUrlRequestSerializer(serializers.Serializer):
    chatId = serializers.CharField(max_length=100, required=True)
    urlFile = serializers.URLField(max_length=200, required=True)
    fileName = serializers.CharField(max_length=100, required=True)
    caption = serializers.CharField(max_length=1000, allow_blank=True, required=False)
    quotedMessageId = serializers.CharField(max_length=100, allow_blank=True, required=False)
